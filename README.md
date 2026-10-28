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
- The `dotnet-runtime-8.0.0-win-x64.zip` archive in tModLoader's `LaunchUtils/` directory (see Step 2).
- Python 3 on a PC or Mac to generate the patched MonoMod DLL.

## Step 1 — Install tModLoader through Playden

Install/import tModLoader (Steam app ID **1281930**) into Playden. Its game directory should be:

~~~text
/data/playden-games/1281930/
~~~

Confirm that the folder contains `tModLoader.dll`, `Libraries/`, `LaunchUtils/`, and the other tModLoader files.

Keep the `Libraries/` folder structure intact. The ReLogic assembly, for example, should be accessible here:

~~~text
/data/playden-games/1281930/Libraries/ReLogic/1.0.0/ReLogic.dll
~~~

You'll install Terraria separately through Playden in **Step 4**, then copy its folder into tModLoader's `1281930` directory.

## Step 2 — Extract the .NET 8 runtime

tModLoader needs the Windows .NET 8 runtime to start. Playden provides the required archive, `dotnet-runtime-8.0.0-win-x64.zip`, inside the game's `LaunchUtils` folder. Extract it to set up `dotnet.exe`.

1. Open the **tModLoader** folder on your PS5:

   ~~~text
   /data/playden-games/1281930/LaunchUtils/
   ~~~

2. Locate the file `dotnet-runtime-8.0.0-win-x64.zip`.
3. Select the ZIP and choose **Extract here**. Keep the extracted files directly inside `LaunchUtils`, rather than in an additional subfolder.
4. Check that `dotnet.exe`, `host/`, and `shared/` are all in the `LaunchUtils` directory.
5. In **Step 5**, set Playden's **Program** to `LaunchUtils/dotnet.exe` and **Program folder** to `.`.

Your folder should look like this:

~~~text
/data/playden-games/1281930/
├── tModLoader.dll
├── Libraries/
│   ├── ReLogic/1.0.0/ReLogic.dll
│   └── monomod.core/1.3.2/lib/net8.0/MonoMod.Core.dll
└── LaunchUtils/
    ├── dotnet-runtime-8.0.0-win-x64.zip
    ├── dotnet.exe
    ├── host/fxr/8.0.0/hostfxr.dll
    └── shared/Microsoft.NETCore.App/8.0.0/
        ├── coreclr.dll
        └── clrjit.dll
~~~

If `dotnet.exe` is not directly inside `LaunchUtils` after extraction, move the **contents** of the extracted folder there. The original ZIP can remain in place.

**Important:** The MonoMod patch in Step 3 uses the exact `clrjit.dll` path shown above, so keep the runtime directory named `8.0.0` and the game at the documented location.

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

The patched file should remain **431,104 bytes**. The patcher verifies the exact supported original and resulting DLL before saving the output. For implementation details, see [PATCH_DETAILS.md](PATCH_DETAILS.md).

## Step 4 — Install Terraria and make it discoverable

Install your legitimate Windows copy of **Terraria** as a separate game in Playden. tModLoader needs the Terraria game files in a folder named `Terraria` both **alongside** and **inside** its own game directory.

1. **Download/install Terraria through Playden**, separately from tModLoader.
2. Open the PS5 file manager and navigate to:

   ~~~text
   /data/playden-games/
   ~~~

3. Find the Terraria installation folder. Playden may name it using Terraria's Steam app ID, `105600`.
4. **Rename the Terraria folder to `Terraria`**, so it is located at:

   ~~~text
   /data/playden-games/Terraria/
   ~~~

   Make sure `Terraria.exe` and the `Content/` folder are directly inside `Terraria/`.
5. **Copy the entire `Terraria` folder into tModLoader's `1281930` directory.** Keep the original folder in place alongside `1281930`:

   ~~~text
   /data/playden-games/1281930/Terraria/
   ~~~

6. In the **original sibling folder** at `/data/playden-games/Terraria/`, rename `steam_api.dll` to `steam_api.dll.bak` if it exists. Leave the `steam_api.dll` in the copy inside tModLoader untouched, and don't alter any DLLs in tModLoader's `Libraries/` folder.
7. In Playden's tModLoader game settings, choose **Steam features → Game's own files**.

Your completed file structure should look like this:

~~~text
/data/playden-games/
├── Terraria/                         # Terraria installation downloaded via Playden
│   ├── Terraria.exe
│   ├── Content/
│   └── steam_api.dll.bak             # renamed in this folder only, if present
└── 1281930/                         # tModLoader installation
    ├── tModLoader.dll
    ├── Terraria/                     # copy of the Terraria installation
    │   ├── Terraria.exe
    │   └── Content/
    ├── LaunchUtils/
    └── Libraries/
~~~

**If you want Terraria's own Playden launcher entry to keep working:** Instead of renaming its managed installation folder, **copy** that folder to `/data/playden-games/Terraria/` and then copy `Terraria/` into `1281930/`. Renaming a Playden-managed folder can disrupt its launcher entry.

This layout lets tModLoader find the standalone Terraria files and addresses Steam-related startup errors such as **“Please ensure Steam is logged in and running.”** Behavior can vary across Terraria and Playden versions.

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

- `/gldevice:D3D11` selects Direct3D 11, letting DXVK translate rendering to Vulkan. This avoids the **SDL: No matching GL pixel format available** error encountered with the OpenGL backend.
- `Program folder = .` runs the game from the tModLoader root. Pointing it at `LaunchUtils` can prevent the game from finding `ReLogic.dll`.
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
