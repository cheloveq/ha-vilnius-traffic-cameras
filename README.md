<p align="center">
  <img src="https://raw.githubusercontent.com/cheloveq/ha-vilnius-traffic-cameras/main/brand/icon.png" alt="Vilnius Traffic Cameras" width="180">
</p>

# Vilnius Traffic Cameras

> **Unofficial community integration.** This project is not created, endorsed, or supported by JUDU, Vilnius city, or any other camera-data provider.

Home Assistant custom integration for the periodically refreshed JPEG traffic-camera images published by [JUDU](https://judu.lt/vairuotojams/eismo-zemelapiai/eismo-stebejimo-kameros/).

The integration loads JUDU's public camera catalog and lets you select which cameras become entities. It currently contains 191 camera images across 105 junction groups. Add or remove selected entities later through the integration's Options flow.

Images are requested from `map.sviesoforai.lt` with a configurable refresh interval, defaulting to five minutes, and a cache-busting query parameter. These are still images, not live video streams.

## HACS

1. Add this repository as a HACS custom **Integration**: `https://github.com/cheloveq/ha-vilnius-traffic-cameras`.
2. Install **Vilnius Traffic Cameras**.
3. Restart Home Assistant and add the integration from Settings → Devices & services.
4. Select the camera locations you want to expose.
