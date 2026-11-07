from html.parser import HTMLParser
import json
from pathlib import Path
import unittest
from urllib.parse import parse_qs, urlsplit


ROOT = Path(__file__).resolve().parents[1]
FEED_URL = "https://vrc-staples.github.io/vpm-packages/index.json"


class PageLinks(HTMLParser):
    def __init__(self, html):
        super().__init__()
        self.links = []
        self.scripts = []
        self.feed(html)

    def handle_starttag(self, tag, attributes):
        attributes = dict(attributes)
        if tag == "a":
            self.links.append(attributes.get("href", ""))
        if tag == "script":
            self.scripts.append(attributes)


class CatalogTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.feed = json.loads((ROOT / "docs/index.json").read_text(encoding="utf-8"))
        cls.html = (ROOT / "docs/index.html").read_text(encoding="utf-8")

    def test_catalog_identity_and_stable_package_id_are_preserved(self):
        self.assertEqual(self.feed["name"], ".Staples. VRChat Tools")
        self.assertEqual(self.feed["id"], "com.staples.vpm")
        self.assertEqual(self.feed["url"], FEED_URL)
        self.assertIn("1.1.0", self.feed["packages"]["com.staples.asm-lite"]["versions"])

    def test_version_entries_have_matching_manifests_and_fixed_release_urls(self):
        self.assertTrue(self.feed["packages"])
        for name, package in self.feed["packages"].items():
            self.assertTrue(package["versions"])
            for version, manifest in package["versions"].items():
                with self.subTest(package=name, version=version):
                    self.assertEqual(manifest["name"], name)
                    self.assertEqual(manifest["version"], version)
                    self.assertRegex(manifest["zipSHA256"], r"\A[0-9a-f]{64}\Z")
                    url = urlsplit(manifest["url"])
                    self.assertEqual((url.scheme, url.netloc), ("https", "github.com"))
                    self.assertIn("/releases/download/", url.path)
                    self.assertTrue(url.path.endswith(".zip"))
                    self.assertNotIn("/nightly/", url.path)
                    self.assertNotIn("/latest/", url.path)

    def test_add_to_vcc_link_uses_the_exact_catalog_url_without_javascript(self):
        page = PageLinks(self.html)
        install_links = [url for url in page.links if url.startswith("vcc:")]
        self.assertEqual(len(install_links), 1)
        url = urlsplit(install_links[0])
        self.assertEqual((url.scheme, url.netloc, url.path), ("vcc", "vpm", "/addRepo"))
        self.assertEqual(parse_qs(url.query), {"url": [FEED_URL]})
        self.assertIn("index.json", page.links)
        self.assertFalse(page.scripts)

    def test_package_names_and_manual_feed_url_are_visible(self):
        self.assertIn(FEED_URL, self.html)
        for package in self.feed["packages"].values():
            for manifest in package["versions"].values():
                self.assertIn(manifest["displayName"], self.html)


if __name__ == "__main__":
    unittest.main()
