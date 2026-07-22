# PowerShell tool setup notes

This file summarizes the tools and utilities that appear in your PowerShell history, along with the install commands you used or can use again. It also notes whether each one can typically be installed without administrator privileges.

## Tools and install commands

| Tool / utility | What it does | Install command | Admin privileges needed? |
|---|---|---|---|
| WSL | Run Linux tools on Windows. | `wsl --install` | Often no for the install, but enabling the feature may require admin on some systems. |
| PowerShell | Microsoft shell and scripting environment. | `winget install --id Microsoft.PowerShell --source winget` | Usually no, if installed per-user. |
| Starship | Fast, customizable shell prompt. | `winget install --id Starship.Starship --accept-source-agreements --accept-package-agreements` | Usually no. |
| PSReadLine | Better command-line editing, history, and autocomplete in PowerShell. | `Install-Module PSReadLine -Force -Scope CurrentUser` | No. |
| ripgrep | Very fast text search tool (similar to grep). | `winget install BurntSushi.ripgrep.MSVC` | Usually no. |
| fd | Fast file finder (similar to find). | `winget install sharkdp.fd` | Usually no. |
| bat | Better `cat` with syntax highlighting and paging. | `winget install sharkdp.bat` | Usually no. |
| fzf | Fuzzy finder for files, commands, and more. | `winget install junegunn.fzf` | Usually no. |
| eza | Modern replacement for `ls` with icons and better formatting. | `winget install eza-community.eza` | Usually no. |
| yazi | Terminal file manager. | `winget install sxyazi.yazi` | Usually no. |
| FFmpeg | Audio/video conversion and processing. | `winget install Gyan.FFmpeg` | Usually no. |
| 7-Zip | Archive manager for ZIP, 7z, and related formats. | `winget install 7zip.7zip` | Usually no. |
| jq | JSON formatter and processor for the command line. | `winget install jqlang.jq` | Usually no. |
| Poppler | PDF utility tools such as `pdfinfo` and `pdftotext`. | `winget install oschwartz10612.Poppler` | Usually no. |
| zoxide | Smarter directory jumping based on usage history. | `winget install ajeetdsouza.zoxide` | Usually no. |
| ImageMagick | Command-line image conversion and editing. | `winget install ImageMagick.ImageMagick` | Usually no. |
| uv | Fast Python environment and package manager. | `powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 \| iex"` | Usually no. |
| Claude CLI | Command-line client for Claude AI. | `irm https://claude.ai/install.ps1 \| iex` | Usually no. |
| pyaranet4 | Python package for the aranetserv project. | `uv pip install pyaranet4` | No. |

## Notes on admin privileges

- The easiest way to avoid admin rights is to use user-scoped installs such as:
  - `winget` packages installed for the current user
  - `Install-Module ... -Scope CurrentUser`
  - `uv pip install ...` or `pip install --user ...`
- Some Windows features, such as WSL, can still require admin access if the required OS components are not already enabled.

## Useful follow-up commands

```powershell
# Check whether a command is available
Get-Command <name>

# Show installed PowerShell modules
Get-Module -ListAvailable

# Show current PATH entries
$env:Path -split ';'
```
