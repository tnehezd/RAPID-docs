"""Check out the RAPID release used to generate the API documentation."""

from pathlib import Path
import re
import runpy
import subprocess


def main():
    docs = Path(__file__).resolve().parent
    tag = runpy.run_path(str(docs / "conf.py"))["rapid_tag"]
    if not isinstance(tag, str) or not re.fullmatch(
        r"v[0-9]+\.[0-9]+\.[0-9]+(-[A-Za-z0-9.-]+)?", tag
    ):
        raise ValueError("rapid_tag must be a RAPID release tag such as v2.3.0.")
    subprocess.run(
        [
            "git", "clone", "--depth", "1", "--branch", tag, "--single-branch",
            "https://github.com/tnehezd/RAPID.git", str(docs.parent / "RAPID"),
        ],
        check=True,
    )


if __name__ == "__main__":
    main()
