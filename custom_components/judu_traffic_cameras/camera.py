"""Camera platform for JUDU traffic cameras."""

from __future__ import annotations

from datetime import timedelta
import logging
import time

from homeassistant.components.camera import Camera
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.update_coordinator import CoordinatorEntity, DataUpdateCoordinator
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .catalog import async_get_catalog
from .const import (
    CONF_CAMERAS,
    CONF_REFRESH_MINUTES,
    DEFAULT_REFRESH_MINUTES,
    DOMAIN,
    IMAGE_URL,
    PAGE_URL,
)

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Create entities for the cameras selected by the user."""
    catalog = await async_get_catalog(hass)
    refresh_minutes = entry.options.get(
        CONF_REFRESH_MINUTES,
        entry.data.get(CONF_REFRESH_MINUTES, DEFAULT_REFRESH_MINUTES),
    )
    coordinator = DataUpdateCoordinator(
        hass,
        _LOGGER,
        name="JUDU traffic camera refresh",
        update_method=lambda: _async_refresh_timestamp(),
        update_interval=timedelta(minutes=refresh_minutes),
    )
    await coordinator.async_config_entry_first_refresh()
    entities = [
        JUDUTrafficCamera(coordinator, image, catalog[image])
        for image in entry.options.get(CONF_CAMERAS, entry.data[CONF_CAMERAS])
        if image in catalog
    ]
    async_add_entities(entities)


async def _async_refresh_timestamp() -> int:
    """Run a lightweight coordinator tick for the configured interval."""
    return int(time.time())


class JUDUTrafficCamera(CoordinatorEntity, Camera):
    """A periodically refreshed JUDU JPEG camera."""

    _attr_has_entity_name = True

    def __init__(self, coordinator: DataUpdateCoordinator, image: str, name: str) -> None:
        CoordinatorEntity.__init__(self, coordinator)
        Camera.__init__(self)
        self._image = image
        self._attr_unique_id = f"{DOMAIN}_{image.removesuffix('.jpg').lower()}"
        self._attr_name = name
        self._attr_content_type = "image/jpeg"

    @property
    def still_image_url(self) -> str:
        """Return the current JUDU image URL."""
        return f"{IMAGE_URL.format(image=self._image)}?v={self.coordinator.data}"

    async def async_camera_image(
        self, width: int | None = None, height: int | None = None
    ) -> bytes | None:
        """Fetch the current JPEG for Home Assistant's camera proxy."""
        session = async_get_clientsession(self.hass)
        try:
            async with session.get(self.still_image_url) as response:
                if response.status != 200:
                    _LOGGER.warning(
                        "JUDU camera %s returned HTTP %s", self._image, response.status
                    )
                    return None
                return await response.read()
        except Exception as err:  # Keep the entity available if a source is down.
            _LOGGER.warning("Unable to fetch JUDU camera %s: %s", self._image, err)
            return None

    @property
    def extra_state_attributes(self) -> dict[str, str]:
        """Expose the source page and camera filename."""
        return {"source_page": PAGE_URL, "camera_image": self._image}
