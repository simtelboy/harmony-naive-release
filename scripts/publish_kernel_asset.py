#!/usr/bin/env python3
"""把内核 .so 发到滚动 Release（不依赖 gh CLI，容器里没有）。

用法: python3 scripts/publish_kernel_asset.py <tag> <asset-path> [notes]
环境: GITHUB_TOKEN（workflow 自带）、GITHUB_REPOSITORY
"""
import json
import os
import sys
import urllib.error
import urllib.request

tag = sys.argv[1]
asset_path = sys.argv[2]
notes = sys.argv[3] if len(sys.argv) > 3 else ""
repo = os.environ["GITHUB_REPOSITORY"]
token = os.environ["GITHUB_TOKEN"]
api = "https://api.github.com/repos/" + repo

HEADERS = {
    "Authorization": "Bearer " + token,
    "Accept": "application/vnd.github+json",
    "User-Agent": "atlantis-kernel-builder",
}


def request(url, data=None, method="GET", content_type="application/json"):
    req = urllib.request.Request(url, data=data, method=method, headers=dict(HEADERS))
    if data is not None:
        req.add_header("Content-Type", content_type)
    try:
        with urllib.request.urlopen(req) as resp:
            raw = resp.read()
            return json.loads(raw.decode()) if raw else {}
    except urllib.error.HTTPError as err:
        if err.code == 404:
            return None
        raise


release = request(api + "/releases/tags/" + tag)
if release is None:
    release = request(
        api + "/releases",
        json.dumps({"tag_name": tag, "name": tag, "prerelease": False}).encode(),
        method="POST",
    )
    print("created release", tag)
else:
    if notes:
        request(api + "/releases/" + str(release["id"]), json.dumps({"body": notes}).encode(),
                method="PATCH")

name = os.path.basename(asset_path)
for existing in release.get("assets", []):
    if existing.get("name") == name:
        request(api + "/releases/assets/" + str(existing["id"]), method="DELETE")
        print("replaced existing asset", name)

upload_url = release["upload_url"].split("{")[0] + "?name=" + name
with open(asset_path, "rb") as handle:
    body = handle.read()
request(upload_url, body, method="POST", content_type="application/octet-stream")
print("uploaded", name, len(body), "bytes to", tag)
