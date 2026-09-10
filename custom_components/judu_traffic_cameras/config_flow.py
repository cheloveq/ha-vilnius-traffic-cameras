"""Config flow for JUDU traffic cameras."""

from __future__ import annotations

from typing import Any

import voluptuous as vol
from homeassistant import config_entries
from homeassistant.core import callback
from homeassistant.helpers import selector

from .catalog import CatalogError, async_get_catalog
from .const import CONF_CAMERAS, CONF_REFRESH_MINUTES, DEFAULT_REFRESH_MINUTES, DOMAIN


class JUDUTrafficCamerasConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Configure selected JUDU traffic camera entities."""

    VERSION = 1

    async def async_step_user(self, user_input: dict[str, Any] | None = None):
        """Select cameras during initial setup."""
        return await self._async_step_select("user", user_input)

    async def _async_step_select(self, step_id: str, user_input: dict[str, Any] | None):
        errors: dict[str, str] = {}
        try:
            catalog = await async_get_catalog(self.hass)
        except CatalogError:
            catalog = {}
            errors["base"] = "cannot_connect"

        if user_input and catalog:
            selected = user_input[CONF_CAMERAS]
            if selected:
                if step_id == "user":
                    return self.async_create_entry(
                        title="JUDU Traffic Cameras",
                        data={
                            CONF_CAMERAS: selected,
                            CONF_REFRESH_MINUTES: user_input[CONF_REFRESH_MINUTES],
                        },
                    )
                return self.async_create_entry(title="JUDU Traffic Cameras", data=user_input)
            errors[CONF_CAMERAS] = "no_cameras"

        schema = vol.Schema(
            {
                vol.Required(CONF_CAMERAS): _camera_selector(catalog),
                vol.Required(CONF_REFRESH_MINUTES, default=DEFAULT_REFRESH_MINUTES): vol.All(
                    vol.Coerce(int), vol.Range(min=1, max=60)
                ),
            }
        )
        return self.async_show_form(
            step_id=step_id,
            data_schema=schema,
            errors=errors,
            description_placeholders={"camera_count": str(len(catalog))},
        )

    @staticmethod
    @callback
    def async_get_options_flow(config_entry: config_entries.ConfigEntry):
        """Return the options flow."""
        return JUDUTrafficCamerasOptionsFlow()


class JUDUTrafficCamerasOptionsFlow(config_entries.OptionsFlow):
    """Change the selected camera entities."""

    async def async_step_init(self, user_input: dict[str, Any] | None = None):
        """Select cameras to keep enabled."""
        try:
            catalog = await async_get_catalog(self.hass)
        except CatalogError:
            return self.async_abort(reason="cannot_connect")
        if user_input:
            return self.async_create_entry(title="", data=user_input)
        return self.async_show_form(
            step_id="init",
            data_schema=vol.Schema(
                {
                    vol.Required(
                        CONF_CAMERAS,
                        default=self.config_entry.options.get(
                            CONF_CAMERAS, self.config_entry.data.get(CONF_CAMERAS, [])
                        ),
                    ): _camera_selector(catalog),
                    vol.Required(
                        CONF_REFRESH_MINUTES,
                        default=self.config_entry.options.get(
                            CONF_REFRESH_MINUTES,
                            self.config_entry.data.get(
                                CONF_REFRESH_MINUTES, DEFAULT_REFRESH_MINUTES
                            ),
                        ),
                    ): vol.All(vol.Coerce(int), vol.Range(min=1, max=60)),
                }
            ),
        )


def _camera_selector(catalog: dict[str, str]) -> selector.SelectSelector:
    """Build a labeled multi-select from the current JUDU catalog."""
    return selector.SelectSelector(
        selector.SelectSelectorConfig(
            options=[{"value": image, "label": name} for image, name in catalog.items()],
            multiple=True,
            mode=selector.SelectSelectorMode.DROPDOWN,
        )
    )
