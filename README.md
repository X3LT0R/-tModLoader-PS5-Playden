# tModLoader on PS5 — Playden / Prospero-Win Setup

**Unofficial community-tested guide to running Windows tModLoader on a jailbroken PlayStation 5 using Playden.**

> **Status (October 28, 2026):** tModLoader successfully launched on one PS5 using this setup. Individual mod compatibility, controller support and long-term stability have **not** been verified. This is not an official PS5 port.

## Tested configuration

| Component | Working setup |
| --- | --- |
| Console | PS5, firmware 13.60, jailbroken |
| Launcher | Playden PS5 0.8.0-beta.1 |
| Windows layer | Prospero-Win / Wine |
| Game | tModLoader 1.4.4.9 + 2026.08.3.0, Steam app ID 1281930 |
| Framework | Portable Windows x64 .NET 8.0.0 |
| MonoMod.Core | Version 1.3.2 with the specific PS5 workaround |
| Graphics | DXVK + Direct3D 11 |
| Steam features | Game's own files |
| Game directory | `/data/playden-games/1281930/` |

Versions matter. The included patcher supports **only the exact MonoMod.Core file and path used here**, not arbitrary updates.

## Requirements

- A jailbroken PS5 with working [Playden](https://github.com/leolobato/playden-ps5), configured according to its own documentation.
- Legitimate Windows Terraria and tModLoader installations. No game binaries are distributed here.
- A PS5 file manager or FTP access.
- [Windows x64 .NET 8 runtime](https://dotnet.microsoft.com/en-us/download/dotnet/8.0).
- Python 3 on a PC or Mac to generate the patched MonoMod DLL.

## Step 1 — Copy your tModLoader files

Install/import tModLoader (Steam app ID **1281930**) in Playden. The folder should be:

~~~text
/data/playden-games/1281930/
~~~

You should have `tModLoader.dll`, `Libraries/`, and the rest of the installed game files.

The tested setup also included a copy of Terraria inside:

~~~text
/data/playden-games/1281930/Terraria/
~~~

That **inner copy came from an original Terraria installation downloaded through Playden**, which was next to the `1281930` folder and renamed to `/data/playden-games/Terraria/` first. See **Step 4** for the correct rename-then-copy order.

**Do not rearrange the Libraries directory.** In particular, this file needs to be accessible:

~~~text
/data/playden-games/1281930/Libraries/ReLogic/1.0.0/ReLogic.dll
~~~

## Step 2 — Install portable .NET 8

Extract the Windows **x64** runtime into `LaunchUtils/`, so `dotnet.exe` and the `host/` and `shared/` folders live directly inside it.

Expected structure:

~~~text
/data/playden-games/1281930/
├── tModLoader.dll
├── Libraries/
│   ├── ReLogic/1.0.0/ReLogic.dll
│   └── monomod.core/1.3.2/lib/net8.0/MonoMod.Core.dll
└── LaunchUtils/
    ├── dotnet.exe
    ├── host/fxr/8.0.0/hostfxr.dll
    └── shared/Microsoft.NETCore.App/8.0.0/
        ├── coreclr.dll
        └── clrjit.dll
~~~

**Important:** The MonoMod patch hard-codes the above `clrjit.dll` path. If you use another runtime directory or move the game, the patch is not suitable without modification.

## Step 3 — Fix MonoMod.Core (Access denied)

The unmodified MonoMod.Core version 1.3.2 triggered:

~~~text
System.ComponentModel.Win32Exception (5): Access denied
System.Diagnostics.Process.get_Modules()
MonoMod.Core.Platforms.Systems.WindowsSystem.GetLoadedModuleFiles()
~~~

MonoMod tries to identify the CLR JIT by enumerating loaded process modules, which failed under the tested Playden/Wine environment.

This repository includes [patch_monomod_ps5.py](patch_monomod_ps5.py), which changes `CoreBaseRuntime.GetClrJitPath()` to return the known `clrjit.dll` path instead.

1. Find `/data/playden-games/1281930/Libraries/monomod.core/1.3.2/lib/net8.0/MonoMod.Core.dll`.
2. **Back up the original** somewhere safe outside the game folder, and copy it to your computer.
3. Put that file next to `patch_monomod_ps5.py` and run:

   ~~~bash
   python3 patch_monomod_ps5.py MonoMod.Core.dll
   ~~~

4. If the original DLL is exactly the supported build, the script creates `MonoMod.Core.patched.dll`.
5. Copy it back to the PS5's `net8.0` folder, rename it to `MonoMod.Core.dll` and replace the original file. Keep your backup.

The script verifies both SHA-256 hashes and refuses unsupported input:

~~~text
Original: 32d22e9aa161059518ddb5bd4c1403630a0a9cd882ed44ec2512e6576c8d33e8
Patched:  a8ae931bb7bec075fb9a1405ed8d903eb2a7d7289f3d7c9cca538e91c0b38677
~~~

The file should remain **431,104 bytes**. Do not substitute the earlier v1 experimental DLL, which caused an assembly-loading error. For implementation details, see [PATCH_DETAILS.md](PATCH_DETAILS.md).

## Step 4 — Set up standalone Terraria

Two early failures were linked to Steam verification:

- tModLoader attempted to open `https://terraria.org` using `explorer.exe`, which Playden couldn't launch as an additional Windows process.
- Another launch displayed: **Please ensure Steam is logged in and running.**

**Correction about the tested setup:** Terraria was **originally downloaded as its own game through Playden** and installed **next to** the tModLoader `1281930` directory. That original Terraria directory was **renamed to `Terraria`**, then **copied into** tModLoader's folder. We did **not** start with Terraria inside tModLoader and copy it outward.

### Actual working order

1. **Download/install your legitimate Windows Terraria game through Playden**, separately from tModLoader.
2. In your PS5 file manager, open `/data/playden-games/`.
3. Find the Terraria directory Playden created. It might be called `105600` (Terraria's Steam app ID).
4. **Rename this original Playden Terraria directory to `Terraria`.** It should now be here:

   ~~~text
   /data/playden-games/Terraria/
   ~~~

   Check that `Terraria.exe` and `Content/` are directly inside this directory.
5. **Copy that renamed Terraria folder** into tModLoader's `1281930` directory. You now have:

   ~~~text
   /data/playden-games/1281930/Terraria/
   ~~~

   Copy, don't move: the **original** stays alongside the `1281930` folder, and a **second copy** lives inside it.
6. **In the original sibling directory only**, `/data/playden-games/Terraria/`, rename `steam_api.dll` to `steam_api.dll.bak` if that DLL is present. This was part of the tested setup; leave the copied Terraria directory and tModLoader's `Libraries/` DLLs alone.
7. In Playden's tModLoader settings, set **Steam features → Game's own files**.

Expected final layout:

~~~text
/data/playden-games/
├── Terraria/                          # ORIGINAL Playden Terraria install (renamed)
│   ├── Terraria.exe
│   ├── Content/
│   └── steam_api.dll.bak              # renamed here if present
└── 1281930/                          # tModLoader (do not rename)
    ├── tModLoader.dll
    ├── Terraria/                      # COPY from original sibling directory
    │   ├── Terraria.exe
    │   └── Content/
    ├── LaunchUtils/
    └── Libraries/
~~~

**Optional:** Renaming a Playden-managed game directory may break its original Playden launcher entry. To keep that standalone entry working, **copy** the newly downloaded Terraria directory to `/data/playden-games/Terraria/` instead of renaming the managed directory, then copy that directory into `1281930/`. The **tested method** was rename-then-copy.

Do not modify Steam DLLs inside tModLoader's `Libraries/` folder. The behavior can vary across Terraria and Playden versions.

## Step 5 — Configure Playden

Open **Playden → tModLoader → Game settings**:

| Setting | Value |
| --- | --- |
| Program | `LaunchUtils/dotnet.exe` |
| Program folder | `.` |
| Graphics | **DXVK** |
| Steam features | **Game's own files** |

For **Extra arguments**, use:

~~~text
tModLoader.dll /gldevice:D3D11
~~~

For an easy-to-access mod and save folder, use this instead:

~~~text
tModLoader.dll /gldevice:D3D11 -tmlsavedirectory Z:\data\playden-games\1281930\TMLData
~~~

Why these settings?

- `/gldevice:D3D11` selects Direct3D 11, letting DXVK translate rendering to Vulkan. This bypassed the earlier **SDL: No matching GL pixel format available** error.
- `Program folder = .` runs the game from the tModLoader root. Pointing it at `LaunchUtils` previously broke `ReLogic.dll` resolution.
- `-tmlsavedirectory` moves mod and save data to a directory accessible to PS5 file managers, avoiding protected Wine-prefix folders.

## Step 6 — Install mods

With the recommended `-tmlsavedirectory` argument, copy `.tmod` files here:

~~~text
/data/playden-games/1281930/TMLData/Mods/
~~~

Create the `TMLData/Mods` folders if needed. Place files directly in `Mods`, for example:

~~~text
TMLData/Mods/ExampleMod.tmod
~~~

Do not leave them inside a ZIP or put them in `Libraries/`.

Start tModLoader, go to **Workshop → Manage Mods**, enable the mods, and reload when prompted. Mods may require dependencies or a particular tModLoader version; their successful execution has not been verified by this guide.

### Default save path / Permission denied

Without the override, the game reported:

~~~text
C:\users\prospero\Documents\My Games\Terraria\tModLoader
~~~

A possible PS5 Wine-prefix location is:

~~~text
/data/playden/games/steam-1281930/library/prefixes/game/drive_c/users/prospero/Documents/My Games/Terraria/tModLoader/Mods/
~~~

A file manager may show **Permission denied** while navigating Playden's prefix. The `TMLData` approach avoids needing to browse it. If mods don't appear, inspect `tModLoader-Logs/client.log` for the line:

~~~text
Saves Are Located At:
~~~

This confirms exactly which save directory tModLoader is using. Changing the save-directory argument doesn't automatically migrate existing saves and characters.

## Troubleshooting

| Error | Suggested check |
| --- | --- |
| `ReLogic.dll` missing | Program folder must be `.`; verify `Libraries/ReLogic/1.0.0/`. |
| MonoMod `Access denied` / `Process.Modules` | Verify the original DLL hash and apply the patcher. |
| `.deps.json` reports missing `MonoMod.Core` after patching | Restore original and regenerate using the exact tested patcher. |
| `explorer.exe` or `Request not supported` | Check copied standalone Terraria folder and Steam settings. |
| `No matching GL pixel format available` | Select DXVK and use `/gldevice:D3D11`. |
| `Please ensure Steam is logged in and running` | Check adjacent Terraria copy and **Game's own files**. |
| Mods not visible | Check `-tmlsavedirectory` and `TMLData/Mods/`. |
| Protected prefix / Permission denied | Use an accessible `TMLData` folder. |
| Unexplained crash | Check `/data/playden/logs/` and `tModLoader-Logs/client.log`. |

## Notes and limitations

- **Unofficial/experimental.** This is not a native PS5 build and does not imply support from game developers.
- **One confirmed launch configuration.** Performance, mod compatibility and sustained play sessions still require separate testing.
- **Patch is exact-build and absolute-path specific.** Do not apply it to another MonoMod.Core version or after moving the runtime folder.
- **Backup first.** Save a copy of your working files, Playden settings, world/character saves and original DLL before modifying or updating anything.
- **No copyrighted game binaries are included.** Obtain Terraria, tModLoader and Windows .NET through legitimate sources.

## Credits and links

- [Playden PS5](https://github.com/leolobato/playden-ps5)
- [tModLoader](https://github.com/tModLoader/tModLoader)
- [tModLoader command-line options](https://github.com/tModLoader/tModLoader/wiki/Command-Line)
- [MonoMod](https://github.com/MonoMod/MonoMod)
- [Microsoft .NET](https://dotnet.microsoft.com/en-us/download/dotnet/8.0)

*Independent troubleshooting write-up, not affiliated with Sony, Valve, Re-Logic, MonoMod, or Playden.*
