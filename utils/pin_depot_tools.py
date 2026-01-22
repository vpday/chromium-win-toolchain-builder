#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import base64
import re
import sys
import urllib.request

def get_depot_tools_commit(chromium_version):
    deps_url = f"https://chromium.googlesource.com/chromium/src/+/refs/tags/{chromium_version}/DEPS?format=TEXT"

    try:
        with urllib.request.urlopen(deps_url) as response:
            base64_content = response.read()
            deps_content = base64.b64decode(base64_content).decode('utf-8')
    except Exception:
        sys.exit(1)

    match = re.search(r"depot_tools\.git'\s*\+\s*'@'\s*\+\s*'([^']+)',", deps_content)

    if not match:
        sys.exit(1)

    return match.group(1)

def main():
    if len(sys.argv) > 1:
        chromium_version = sys.argv[1]
    else:
        chromium_version = "144.0.7559.96"

    target_hash = get_depot_tools_commit(chromium_version)
    print(target_hash)

if __name__ == '__main__':
    main()