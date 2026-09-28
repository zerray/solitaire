from pathlib import Path
import json
import unittest


class HomeScreenMetadataTest(unittest.TestCase):
    def test_ios_home_screen_web_app_metadata_is_present(self):
        html = (Path(__file__).parents[1] / "index.html").read_text()

        self.assertIn(
            '<meta name="apple-mobile-web-app-capable" content="yes">',
            html,
        )
        self.assertIn(
            '<meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">',
            html,
        )
        self.assertIn(
            '<link rel="manifest" href="manifest.webmanifest">',
            html,
        )

        manifest = json.loads(
            (Path(__file__).parents[1] / "manifest.webmanifest").read_text()
        )
        self.assertEqual(manifest["display"], "standalone")
        self.assertEqual(manifest["start_url"], "./index.html")


if __name__ == "__main__":
    unittest.main()
