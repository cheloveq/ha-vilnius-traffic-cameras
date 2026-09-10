"""Constants for JUDU traffic cameras."""

from homeassistant.const import Platform

DOMAIN = "judu_traffic_cameras"
PLATFORMS = [Platform.CAMERA]
CONF_CAMERAS = "cameras"
CONF_REFRESH_MINUTES = "refresh_minutes"
DEFAULT_REFRESH_MINUTES = 5
CATALOG_URL = "https://map.sviesoforai.lt/camera/js/config.js"
IMAGE_URL = "https://map.sviesoforai.lt/camera/api/camera/{image}"
PAGE_URL = "https://judu.lt/vairuotojams/eismo-zemelapiai/eismo-stebejimo-kameros/"
