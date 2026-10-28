#!/usr/bin/env python3
"""Apply the tested in-place MonoMod.Core 1.3.2 PS5 workaround.

Requires only Python 3. No game binaries, .NET runtime or original MonoMod binary
are included here. This is version- and path-specific.
"""
import argparse
import hashlib
from pathlib import Path

EXPECTED_INPUT_SHA256 = "32d22e9aa161059518ddb5bd4c1403630a0a9cd882ed44ec2512e6576c8d33e8"
EXPECTED_OUTPUT_SHA256 = "a8ae931bb7bec075fb9a1405ed8d903eb2a7d7289f3d7c9cca538e91c0b38677"
# Patched IL makes CoreBaseRuntime.GetClrJitPath return a constant user string.
# The user string points at:
# Z:\data\playden-games\1281930\LaunchUtils\shared\Microsoft.NETCore.App\8.0.0\clrjit.dll
# One existing diagnostic metadata string is reused to avoid growing metadata.
PATCHES = (
    (0x62f0, bytes.fromhex(
        "060000005a000011729d2900702a"
    )),
    (0x2c7da, bytes.fromhex(
        "af5a003a005c0064006100740061005c0070006c0061007900640065006e002d00670061006d00650073005c0031003200380031003900330030005c004c00610075006e00630068005500740069006c0073005c007300680061007200650064005c004d006900630072006f0073006f00660074002e004e004500540043006f00720065002e004100700070005c0038002e0030002e0030005c0063006c0072006a00690074002e0064006c006c0000"
    )),
)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("original_dll", type=Path, help="Original MonoMod.Core.dll")
    parser.add_argument("--output", type=Path, help="Where to write patched DLL")
    args = parser.parse_args()
    data = args.original_dll.read_bytes()
    digest = hashlib.sha256(data).hexdigest()
    if digest != EXPECTED_INPUT_SHA256:
        parser.error("Unsupported original DLL SHA-256: " + digest +
                     ". Expected exactly MonoMod.Core v1.3.2 from the tested setup. "
                     "Do NOT force this patch onto another build.")
    buf = bytearray(data)
    for offset, replacement in PATCHES:
        buf[offset:offset + len(replacement)] = replacement
    outbytes = bytes(buf)
    assert len(outbytes) == len(data), "Patch must preserve file length"
    got = hashlib.sha256(outbytes).hexdigest()
    assert got == EXPECTED_OUTPUT_SHA256, "Unexpected patched DLL digest: " + got
    out = args.output or args.original_dll.with_name("MonoMod.Core.patched.dll")
    if out.resolve() == args.original_dll.resolve():
        parser.error("Refusing to overwrite original. Choose a separate --output path.")
    out.write_bytes(outbytes)
    print("Patched DLL written:", out)
    print("SHA-256:", got)
    print("Copy it onto your PS5 as MonoMod.Core.dll AFTER backing up the original.")


if __name__ == "__main__":
    main()
