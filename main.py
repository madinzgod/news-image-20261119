#!/usr/bin/env python3
"""Entry program for news-image-20261119: "Sum up 19 November's world
news in one image".

The entry is the image itself: entry.png, a newspaper front page that
sits next to this file (it is rendered by draw.py, kept in this repo so
the build is reproducible). This program's only job is to deliver that
image, byte for byte, into the output directory.

The output directory comes from the MAKEFUN_OUTPUT_DIR environment
variable and defaults to /output. The copy is streamed in fixed-size
chunks and depends on nothing but the Python standard library, so the
delivered file is exactly the bundled one, every run.
"""

import os

IMAGE_NAME = "entry.png"
DEFAULT_OUTPUT_DIR = "/output"
CHUNK_SIZE = 64 * 1024


def source_path():
    """Absolute path of the bundled image, wherever we are run from."""
    here = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(here, IMAGE_NAME)


def output_path():
    """Where the image must land: $MAKEFUN_OUTPUT_DIR/entry.png."""
    output_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", DEFAULT_OUTPUT_DIR)
    os.makedirs(output_dir, exist_ok=True)
    return os.path.join(output_dir, IMAGE_NAME)


def copy_image(source, target):
    """Copy source to target byte-for-byte, in chunks."""
    with open(source, "rb") as fin, open(target, "wb") as fout:
        while True:
            chunk = fin.read(CHUNK_SIZE)
            if not chunk:
                break
            fout.write(chunk)


def main():
    target = output_path()
    copy_image(source_path(), target)
    print("wrote", target)


if __name__ == "__main__":
    main()
