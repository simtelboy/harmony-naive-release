#!/usr/bin/env python3
"""Create a GitHub release and upload one asset without the gh CLI."""
import json
import os
import sys
import urllib.request

tag = sys.argv[1]
asset = sys.argv[2]
repo = os.environ["GITHUB_REPOSITORY"]
token = os.environ["GITHUB_TOKEN"]

def post(url, data, content_type, method="POST"):
    req = urllib.request.Request(url, data=data, method=method, headers={
        "Authorization": "Bearer " + token,
        "Accept": "application/vnd.github+json",
        "Content-Type": content_type,
        "User-Agent": "atlantis-release-builder",
    })
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read().decode())

release = post(
    "https://api.github.com/repos/%s/releases" % repo,
    json.dumps({"tag_name": tag, "name": tag, "prerelease": False}).encode(),
    "application/json",
)
upload = release["upload_url"].split("{")[0] + "?name=" + os.path.basename(asset)
with open(asset, "rb") as f:
    body = f.read()
post(upload, body, "application/octet-stream")
print("released", tag, os.path.basename(asset), len(body), "bytes")
