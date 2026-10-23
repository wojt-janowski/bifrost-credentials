"""Behavioral checks for the release-package guard."""

import importlib.util
import tempfile
import unittest
from pathlib import Path

SPEC = importlib.util.spec_from_file_location(
    "skill_validator", Path(__file__).resolve().parents[1] / "scripts" / "validate.py"
)
validator = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(validator)


class PackageValidationTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        (self.root / "SKILL.md").write_text(
            "---\nname: bifrost-credentials\ndescription: Set up mobile signing.\n---\n"
            "# Skill\n[Reference](references/ios.md)\n",
            encoding="utf-8",
        )
        (self.root / "references").mkdir()
        (self.root / "references" / "ios.md").write_text(
            "[Entry](../SKILL.md#skill)\n[Vendor](https://example.com/docs)\n",
            encoding="utf-8",
        )

    def test_valid_relative_and_external_links(self):
        self.assertEqual([], validator.validate(self.root))

    def test_broken_reference_is_rejected(self):
        (self.root / "references" / "ios.md").unlink()
        self.assertTrue(any("Broken local link" in e for e in validator.validate(self.root)))

    def test_encoded_escape_is_rejected_even_when_target_exists(self):
        outside = self.root.parent / (self.root.name + "-outside.md")
        outside.write_text("Outside", encoding="utf-8")
        self.addCleanup(outside.unlink)
        with (self.root / "SKILL.md").open("a", encoding="utf-8") as handle:
            handle.write(f"[Outside](%2e%2e/{outside.name})\n")
        self.assertTrue(any("escapes" in e for e in validator.validate(self.root)))

    def test_credential_artifacts_are_rejected_without_reading_contents(self):
        for filename in (".env", ".env.backup", "store.P12", "upload.jks", "credentials/key.json"):
            with self.subTest(filename=filename):
                path = self.root / filename
                path.parent.mkdir(exist_ok=True)
                path.write_bytes(b"synthetic fixture")
                self.assertTrue(any("Credential artifact" in e for e in validator.validate(self.root)))
                path.unlink()

    def test_external_symlink_is_rejected(self):
        (self.root / "linked.md").symlink_to(self.root.parent)
        self.assertTrue(any("Symlink" in e for e in validator.validate(self.root)))

    def test_missing_description_is_rejected(self):
        path = self.root / "SKILL.md"
        path.write_text("---\nname: bifrost-credentials\n---\n", encoding="utf-8")
        self.assertTrue(any("description" in e for e in validator.validate(self.root)))


if __name__ == "__main__":
    unittest.main()
