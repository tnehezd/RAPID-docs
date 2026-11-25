"""Check out RAPID main for latest docs, or an exact tag for release docs."""

from pathlib import Path
import os
import re
import runpy
import subprocess


def main():
    docs = Path(__file__).resolve().parent
    latest = os.environ.get("READTHEDOCS_VERSION", "latest") == "latest"
    ref = "main" if latest else runpy.run_path(str(docs / "conf.py"))["rapid_tag"]
    if not latest and (not isinstance(ref, str) or not re.fullmatch(
        r"v[0-9]+\.[0-9]+\.[0-9]+(-[A-Za-z0-9.-]+)?", ref
    )):
        raise ValueError("Release documentation requires rapid_tag such as v2.3.0.")
    destination = str(docs.parent / "RAPID")
    print(f"Documentation RAPID source: {'branch' if latest else 'tag'} {ref}", flush=True)
    subprocess.run(
        [
            "git", "clone", "--depth", "1", "--branch", ref, "--single-branch",
            "https://github.com/tnehezd/RAPID.git", destination,
        ],
        check=True,
    )
    if not latest:
        subprocess.run(
            ["git", "-C", destination, "checkout", "--detach", f"refs/tags/{ref}"],
            check=True,
        )


if __name__ == "__main__":
    main()
