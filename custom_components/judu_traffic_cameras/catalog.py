"""Fetch and parse the public JUDU camera catalog."""

from __future__ import annotations

import json

from aiohttp import ClientError
from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .const import CATALOG_URL


class CatalogError(RuntimeError):
    """The JUDU camera catalog could not be loaded."""


async def async_get_catalog(hass: HomeAssistant) -> dict[str, str]:
    """Return image filename to display name mappings from JUDU."""
    session = async_get_clientsession(hass)
    try:
        async with session.get(CATALOG_URL) as response:
            response.raise_for_status()
            source = (await response.text()).lstrip("\ufeff").strip()
    except (ClientError, TimeoutError) as err:
        raise CatalogError("Unable to fetch the JUDU camera catalog") from err

    if not source.startswith("var config ="):
        raise CatalogError("Unexpected JUDU camera catalog format")
    try:
        config = json.loads(source.removeprefix("var config =").strip().rstrip(";"))
    except json.JSONDecodeError as err:
        raise CatalogError("Unable to parse the JUDU camera catalog") from err

    return {
        camera["image"]: camera["name"]
        for cameras in config.values()
        for camera in cameras
        if camera.get("image") and camera.get("name")
    }
