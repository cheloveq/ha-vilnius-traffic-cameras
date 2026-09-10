"""Tests for JUDU catalog parsing and integration metadata."""

from __future__ import annotations

import json
from pathlib import Path
import unittest


ROOT = Path(__file__).parents[1]
COMPONENT = ROOT / "custom_components" / "judu_traffic_cameras"


class CatalogTestCase(unittest.TestCase):
    """Keep the integration selectable and HACS-compatible."""

    def test_manifest(self) -> None:
        manifest = json.loads((COMPONENT / "manifest.json").read_text())
        self.assertEqual(manifest["domain"], "judu_traffic_cameras")
        self.assertTrue(manifest["config_flow"])
        self.assertEqual(manifest["version"], "0.1.0")

    def test_catalog_parser_and_selectable_entities(self) -> None:
        source = (COMPONENT / "catalog.py").read_text()
        flow = (COMPONENT / "config_flow.py").read_text()
        self.assertIn("var config =", source)
        self.assertIn("async_get_catalog", flow)
        self.assertIn("CONF_CAMERAS", flow)
        self.assertIn("CONF_REFRESH_MINUTES", flow)
        self.assertIn("DEFAULT_REFRESH_MINUTES", flow)

    def test_image_endpoint_and_refresh(self) -> None:
        camera = (COMPONENT / "camera.py").read_text()
        self.assertIn("/camera/api/camera/{image}", (COMPONENT / "const.py").read_text())
        self.assertIn("coordinator.data", camera)
        self.assertIn("update_interval=timedelta(minutes=refresh_minutes)", camera)


if __name__ == "__main__":
    unittest.main()
