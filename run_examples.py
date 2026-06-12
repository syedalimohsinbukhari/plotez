"""Auto-runner script for all example files.

Discovers all .py files under the examples/ directory and runs them in-process (with each file's directory as the
working directory) so that any relative-path `plt.savefig(...)` calls land in the correct folder.

Usage
-----
    python run_examples.py [options]

Options
-------
    --dir DIR
        Root directory to search for example files (default: examples/)
    --pattern PAT
        Glob pattern for example files (default: **/*.py)
    --dry-run
        Print the files that would be run without executing them
    --stop-on-error
        Stop execution after the first failure (default: continue)
    -v, --verbose
        Show per-file stdout / stderr output
"""

from __future__ import annotations

import argparse
import importlib.util
import os
import sys
import time
import traceback
from pathlib import Path

# ---------------------------------------------------------------------------
# ANSI colours (disabled automatically when stdout is not a tty)
# ---------------------------------------------------------------------------
_USE_COLOUR = sys.stdout.isatty()

_GREEN = "\033[32m" if _USE_COLOUR else ""
_RED = "\033[31m" if _USE_COLOUR else ""
_YELLOW = "\033[33m" if _USE_COLOUR else ""
_CYAN = "\033[36m" if _USE_COLOUR else ""
_BOLD = "\033[1m" if _USE_COLOUR else ""
_RESET = "\033[0m" if _USE_COLOUR else ""


def _fmt(colour: str, text: str) -> str:
    return f"{colour}{text}{_RESET}"


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def collect_examples(root: Path, pattern: str) -> list[Path]:
    """Return all files matching *pattern* under *root*, sorted."""
    files = sorted(root.glob(pattern))
    # Exclude __init__.py and similar non-example files
    return [f for f in files if f.name not in {"__init__.py", "conftest.py"}]


def run_file(path: Path, verbose: bool) -> tuple[bool, float, str | None]:
    """Execute `path` as a Python script inside its own directory.

    Returns
    -------
    (success, elapsed_seconds, error_message_or_None)
    """
    original_dir = os.getcwd()
    original_argv = sys.argv[:]

    try:
        os.chdir(path.parent)
        sys.argv = [str(path)]

        spec = importlib.util.spec_from_file_location(name="__example__", location=path)
        module = importlib.util.module_from_spec(spec)  # type: ignore[arg-type]
        module.__file__ = str(path)

        t0 = time.perf_counter()
        spec.loader.exec_module(module)  # type: ignore[union-attr]
        elapsed = time.perf_counter() - t0

        return True, elapsed, None

    except Exception:
        elapsed = time.perf_counter() - t0  # noqa: F821 – defined above
        return False, elapsed, traceback.format_exc()

    finally:
        os.chdir(original_dir)
        sys.argv = original_argv


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Run all example .py files found under a directory.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "--dir",
        default="examples",
        metavar="DIR",
        help="Root directory to search (default: examples/)",
    )
    parser.add_argument(
        "--pattern",
        default="**/*.py",
        metavar="PAT",
        help="Glob pattern relative to --dir (default: **/*.py)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print files that would be run without executing them.",
    )
    parser.add_argument(
        "--stop-on-error",
        action="store_true",
        help="Abort after the first failure.",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Show per-file output / tracebacks inline.",
    )
    args = parser.parse_args()

    # Resolve root relative to *this* script's location so the runner works regardless of the calling working directory.
    script_dir = Path(__file__).parent
    root = (script_dir / args.dir).resolve()

    if not root.exists():
        print(_fmt(colour=_RED, text=f"[ERROR] directory not found: {root}"), file=sys.stderr)
        return 1

    examples = collect_examples(root=root, pattern=args.pattern)

    if not examples:
        print(_fmt(colour=_YELLOW, text=f"[WARN] No files matched '{args.pattern}' under {root}"))
        return 0

    print(_fmt(colour=_BOLD, text=f"\nFound {len(examples)} example file(s) under {root}\n") + "-" * 60)

    if args.dry_run:
        for f in examples:
            print(f"  {f.relative_to(script_dir)}")
        return 0

    passed: list[Path] = []
    failed: list[tuple[Path, str]] = []

    for i, path in enumerate(examples, start=1):
        rel = path.relative_to(script_dir)
        label = f"[{i}/{len(examples)}] {rel}"
        print(_fmt(colour=_CYAN, text=f"  → {label}"), end=" ", flush=True)

        ok, elapsed, err = run_file(path=path, verbose=args.verbose)

        if ok:
            print(_fmt(colour=_GREEN, text=f"✓  ({elapsed:.2f}s)"))
            passed.append(path)
        else:
            print(_fmt(colour=_RED, text=f"✗  ({elapsed:.2f}s)"))
            failed.append((path, err or ""))
            if args.verbose or args.stop_on_error:
                print(_fmt(colour=_RED, text=err or ""))
            if args.stop_on_error:
                break

    # Summary
    print("-" * 60)
    total = len(passed) + len(failed)
    print(
        _fmt(_BOLD, "\nResults: ")
        + _fmt(_GREEN, f"{len(passed)} passed")
        + ", "
        + (_fmt(_RED, f"{len(failed)} failed") if failed else _fmt(_GREEN, "0 failed"))
        + f"  (total: {total})\n"
    )

    if failed and not args.verbose:
        print(_fmt(_RED, "Failed files:"))
        for path, err in failed:
            rel = path.relative_to(script_dir)
            print(f"\n  {_fmt(_BOLD, str(rel))}")
            # Print only the last few lines of the traceback for brevity
            short = "\n".join(err.strip().splitlines()[-6:])
            print(f"    {short.replace(chr(10), chr(10) + '    ')}")
        print()

    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
