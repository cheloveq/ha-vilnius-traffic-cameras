"""Camera platform for JUDU traffic cameras."""

from __future__ import annotations

import time

from homeassistant.components.camera import Camera
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .catalog import async_get_catalog
from .const import CONF_CAMERAS, DOMAIN, IMAGE_URL, PAGE_URL


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Create entities for the cameras selected by the user."""
    catalog = await async_get_catalog(hass)
    entities = [
        JUDUTrafficCamera(image, catalog[image])
        for image in entry.options.get(CONF_CAMERAS, entry.data[CONF_CAMERAS])
        if image in catalog
    ]
    async_add_entities(entities)


class JUDUTrafficCamera(Camera):
    """A periodically refreshed JUDU JPEG camera."""

    _attr_has_entity_name = True
    _attr_should_poll = True

    def __init__(self, image: str, name: str) -> None:
        super().__init__()
        self._image = image
        self._attr_unique_id = f"{DOMAIN}_{image.removesuffix('.jpg').lower()}"
        self._attr_name = name
        self._attr_content_type = "image/jpeg"
        self._cache_buster = int(time.time())

    async def async_update(self) -> None:
        """Change the URL so HA clients request the latest image."""
        self._cache_buster = int(time.time())

    @property
    def still_image_url(self) -> str:
        """Return the current JUDU image URL."""
        return f"{IMAGE_URL.format(image=self._image)}?v={self._cache_buster}"

    @property
    def extra_state_attributes(self) -> dict[str, str]:
        """Expose the source page and camera filename."""
        return {"source_page": PAGE_URL, "camera_image": self._image}
