# PNG size corruption checker

Simple python program which checks PNG file's size in IHDR is correct.

Inspired from CTF problem.

## Usage

    python checker.py <image file name>

## Description

These two images below are actually same images.

![](sample/sunmoon_wrong_size.png)

![](sample/sunmoon.png)

The difference between two image is the height value in IHDR (and the CRC of IHDR).

This can be used for a steganography method.

Therefore, this program checks whether the height value in IHDR is correct, by directly calculating size from image data(IDAT) section.

### Requirements

- Python3

### References

> https://www.w3.org/TR/PNG/

> http://halicery.com/Image/png/pngdecoding.html

> http://www.libpng.org/pub/png/spec/1.2/PNG-Chunks.html
