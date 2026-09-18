"""Fail closed when a built release bundle contains caches or build roots."""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Iterable


READ_CHUNK_SIZE = 1024 * 1024


def _path_needles(raw_path: str) -> tuple[bytes, ...]:
    variants = {
        raw_path.rstrip("\\/"),
        raw_path.rstrip("\\/").replace("/", "\\"),
        raw_path.rstrip("\\/").replace("\\", "/"),
    }
    needles: set[bytes] = set()
    for variant in variants:
        if not variant:
            continue
        needles.add(variant.casefold().encode("utf-8"))
        needles.add(variant.casefold().encode("utf-16-le"))
    return tuple(sorted(needles))


def _contains_any(path: Path, needles: tuple[bytes, ...]) -> bool:
    if not needles:
        return False
    overlap_size = max(len(needle) for needle in needles) - 1
    overlap = b""
    with path.open("rb") as handle:
        while chunk := handle.read(READ_CHUNK_SIZE):
            haystack = (overlap + chunk).lower()
            if any(needle in haystack for needle in needles):
                return True
            overlap = haystack[-overlap_size:] if overlap_size else b""
    return False


def find_hygiene_issues(bundle_root: Path, forbidden_roots: Iterable[str]) -> list[str]:
    root = bundle_root.resolve(strict=True)
    if not root.is_dir():
        raise NotADirectoryError(f"Release bundle is not a directory: {root}")

    needles = tuple(
        needle
        for forbidden_root in forbidden_roots
        for needle in _path_needles(forbidden_root)
    )
    issues: list[str] = []
    for path in sorted(root.rglob("*"), key=lambda item: str(item).casefold()):
        relative = path.relative_to(root)
        if path.is_dir():
            if path.name.casefold() == "__pycache__":
                issues.append(f"Python cache directory: {relative}")
            continue
        if path.suffix.casefold() == ".pyc":
            issues.append(f"Python bytecode cache: {relative}")
        try:
            if _contains_any(path, needles):
                issues.append(f"Embedded local build root: {relative}")
        except OSError as exc:
            issues.append(f"Unreadable bundle file: {relative} ({exc})")
    return issues


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("bundle_root", type=Path)
    parser.add_argument("--forbid-root", action="append", default=[])
    args = parser.parse_args()

    issues = find_hygiene_issues(args.bundle_root, args.forbid_root)
    if issues:
        print("Release bundle hygiene verification failed:")
        for issue in issues:
            print(f"- {issue}")
        return 1

    print("Release bundle hygiene verification passed: no caches or local build roots found.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
