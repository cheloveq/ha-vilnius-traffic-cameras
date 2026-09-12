"""JUDU Vilnius traffic camera integration."""

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import ConfigEntryNotReady

from .catalog import CatalogError, async_get_catalog
from .const import PLATFORMS


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up selected JUDU traffic cameras."""
    if entry.title != "Vilnius Traffic Cameras":
        hass.config_entries.async_update_entry(entry, title="Vilnius Traffic Cameras")

    try:
        entry.runtime_data = await async_get_catalog(hass)
    except CatalogError as err:
        raise ConfigEntryNotReady("Unable to load the JUDU camera catalog") from err

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload JUDU traffic cameras."""
    return await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
