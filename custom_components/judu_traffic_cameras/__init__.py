"""JUDU Vilnius traffic camera integration."""

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from .const import PLATFORMS


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up selected JUDU traffic cameras."""
    if entry.title != "Vilnius Traffic Cameras":
        hass.config_entries.async_update_entry(entry, title="Vilnius Traffic Cameras")
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload JUDU traffic cameras."""
    return await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
