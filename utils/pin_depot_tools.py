#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import base64
import logging
import re
import sys
import subprocess
import urllib.request
from pathlib import Path

logging.basicConfig(level=logging.INFO, format="%(message)s")


def get_depot_tools_commit(chromium_version):
    deps_url = f"https://chromium.googlesource.com/chromium/src/+/refs/tags/{chromium_version}/DEPS?format=TEXT"
    logging.info(f"Fetching DEPS from: {deps_url}")

    try:
        with urllib.request.urlopen(deps_url) as response:
            base64_content = response.read()
            deps_content = base64.b64decode(base64_content).decode("utf-8")
    except Exception as e:
        logging.error(f"Failed to fetch or decode DEPS: {e}")
        sys.exit(1)

    match = re.search(r"depot_tools\.git'\s*\+\s*'@'\s*\+\s*'([^']+)',", deps_content)

    if not match:
        logging.error("Error: Could not find depot_tools commit hash in DEPS file.")
        sys.exit(1)

    commit_hash = match.group(1)
    logging.info(f"Found depot_tools hash: {commit_hash}")
    return commit_hash


def pin_depot_tools(target_hash, depot_tools_path):
    dt_path = Path(depot_tools_path).resolve()

    if not dt_path.exists():
        logging.error(f"Error: depot_tools directory not found at {dt_path}")
        sys.exit(1)

    logging.info(f"Pinning depot_tools at {dt_path} to {target_hash}")

    try:
        subprocess.run(["git", "fetch", "origin", target_hash], cwd=dt_path, check=True)
        subprocess.run(["git", "reset", "--hard", target_hash], cwd=dt_path, check=True)
        subprocess.run(["git", "clean", "-ffdx"], cwd=dt_path, check=True)
        logging.info("depot_tools successfully pinned.")

    except subprocess.CalledProcessError as e:
        logging.error(f"Git operation failed: {e}")
        sys.exit(1)


def main():
    if len(sys.argv) > 1:
        chromium_version = sys.argv[1]
    else:
        chromium_version = "144.0.7559.96"

    depot_tools_path = "depot_tools"

    logging.info(f"Starting Toolchain Version Locking for Chromium {chromium_version}")

    target_hash = get_depot_tools_commit(chromium_version)
    pin_depot_tools(target_hash, depot_tools_path)


if __name__ == "__main__":
    main()
