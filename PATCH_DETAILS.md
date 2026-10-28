# Patch details

This patch reproduces the exact byte changes made in the confirmed-working v2 workaround. The original `MonoMod.Core.dll` is **not** bundled. Obtain it from your own tModLoader installation.

- Original SHA-256: `32d22e9aa161059518ddb5bd4c1403630a0a9cd882ed44ec2512e6576c8d33e8`
- Patched SHA-256: `a8ae931bb7bec075fb9a1405ed8d903eb2a7d7289f3d7c9cca538e91c0b38677`
- Original and patched size: `431104` bytes
- Patch byte spans: `0x62f0..0x62fd`, `0x2c7da..0x2c889`
- No PE sections are added and file size is unchanged.
- The IL method `CoreBaseRuntime.GetClrJitPath()` returns the exact hard-coded runtime JIT DLL path: `Z:\data\playden-games\1281930\LaunchUtils\shared\Microsoft.NETCore.App\8.0.0\clrjit.dll`.
- A pre-existing user-string metadata entry is reused. This changes a diagnostic message, so avoid this patch on other builds.

**WARNING:** This is a targeted workaround; there is no guarantee of compatibility outside the exact tested versions/layout.
