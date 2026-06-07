"""Created on Jun 07 19:54:24 2026"""

# Pre-commit hook: verify that README.md mentions the same version as version.py.

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[0]
VERSION_FILE = ROOT / "src" / "plotez" / "version.py"
README_FILE = ROOT / "README.md"


def get_version_from_version_py() -> str:
    """Extract __version__ value from version.py."""
    content = VERSION_FILE.read_text(encoding="utf-8")
    match = re.search(r'^__version__\s*=\s*["\']([^"\']+)["\']', content, re.MULTILINE)
    if not match:
        print(f"ERROR: Could not find __version__ in {VERSION_FILE}", file=sys.stderr)
        sys.exit(1)
    return match.group(1)


def check_readme_contains_version(version: str) -> bool:
    """Return True if README.md contains the version string (with or without the 'v' prefix)."""
    content = README_FILE.read_text(encoding="utf-8")
    # Accept both a bare version and v-prefixed version (e.g., 0.3.3 and v0.3.3)
    return version in content


def main() -> None:
    version = get_version_from_version_py()
    if not check_readme_contains_version(version):
        print(
            f"ERROR: Version mismatch!\n"
            f"  version.py says : {version}\n"
            f"  README.md does NOT contain '{version}' (or 'v{version}').\n"
            f"  Please update README.md before committing.",
            file=sys.stderr,
        )
        sys.exit(1)

    print(f"OK: README.md is in sync with version.py (version {version}).")


if __name__ == "__main__":
    main()
