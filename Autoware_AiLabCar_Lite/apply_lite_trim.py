#!/usr/bin/env python3
"""Apply Autoware 1.7.1 Lite COLCON_IGNORE + strip depends.

Usage (from Autoware workspace root):
  python3 apply_lite_trim.py --src src --list lite_trim_ignore_packages.txt

Does NOT apply C++ / launch patches. See autoware_lite_trim_playbook.html.
"""
import argparse
import os
import re
import xml.etree.ElementTree as ET
from pathlib import Path

HARD_KEEP = {
    "autoware_tensorrt_yolox",
    "autoware_bytetrack",
    "autoware_ndt_scan_matcher",
    "autoware_osqp_interface",
    "autoware_pure_pursuit",
    "autoware_planning_validator_test_utils",
    "autoware_test_utils",
    "autoware_planning_test_manager",
}


def load_names(path):
    names = []
    for line in Path(path).read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        names.append(line)
    return names


def find_packages(src):
    found = {}
    for dirpath, _, files in os.walk(src):
        if "package.xml" not in files:
            continue
        px = Path(dirpath) / "package.xml"
        try:
            name = ET.parse(px).getroot().find("name").text.strip()
        except Exception:
            continue
        found[name] = Path(dirpath)
    return found


DEP_RE = re.compile(
    r"^[ \t]*<(depend|exec_depend|test_depend|build_depend|build_export_depend)>([^<]+)</\1>[ \t]*\n",
    re.M,
)


def strip_deps(package_xml: Path, ignore: set, dry: bool):
    text = package_xml.read_text()
    removed = []

    def repl(m):
        pkg = m.group(2).strip()
        if pkg in ignore:
            removed.append(pkg)
            return ""
        return m.group(0)

    new = DEP_RE.sub(repl, text)
    if removed and not dry:
        package_xml.write_text(new)
    return removed


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", default="src")
    ap.add_argument("--list", required=True, help="one package name per line")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()
    src = Path(args.src)
    names = load_names(args.list)
    found = find_packages(src)
    ignore = set()
    missing = []
    skipped_keep = []
    for n in names:
        if n in HARD_KEEP:
            skipped_keep.append(n)
            continue
        if n not in found:
            missing.append(n)
            continue
        ignore.add(n)
        ig = found[n] / "COLCON_IGNORE"
        print(f"IGNORE {n}  ({found[n]})")
        if not args.dry_run:
            ig.write_text("")
    print(f"\n# touched {len(ignore)} COLCON_IGNORE")
    if skipped_keep:
        print("# refused HARD_KEEP:", ", ".join(skipped_keep))
    if missing:
        print("# not found on this tree (ok if unused):")
        for n in missing:
            print("  -", n)

    n_xml = 0
    for name, d in found.items():
        if name in ignore:
            continue
        if (d / "COLCON_IGNORE").exists():
            continue
        removed = strip_deps(d / "package.xml", ignore, args.dry_run)
        if removed:
            n_xml += 1
            print(f"STRIP {name}: {', '.join(sorted(set(removed)))}")
    print(f"\n# stripped {n_xml} package.xml files")
    print("# NEXT: apply C++/launch patches from autoware_lite_trim_playbook.html then colcon build")


if __name__ == "__main__":
    main()
