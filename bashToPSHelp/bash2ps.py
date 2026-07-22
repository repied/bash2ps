#!/usr/bin/env python3
"""Deterministic bash-to-PowerShell translation helper for learning PowerShell."""

from __future__ import annotations

import argparse
import os
import re
import shutil
import subprocess
import sys
from typing import List


COMMAND_MAPPINGS = {
    "ls": ["Get-ChildItem"],
    "ll": ["Get-ChildItem"],
    "la": ["Get-ChildItem"],
    "pwd": ["Get-Location"],
    "cd": ["Set-Location"],
    "mkdir": ["New-Item -ItemType Directory -Force"],
    "rmdir": ["Remove-Item -Recurse -Force"],
    "cp": ["Copy-Item"],
    "mv": ["Move-Item"],
    "rm": ["Remove-Item -Recurse -Force"],
    "rename": ["Rename-Item"],
    "ln": ["New-Item -ItemType SymbolicLink"],
    "lns": ["New-Item -ItemType SymbolicLink"],
    "cat": ["Get-Content"],
    "less": ["Get-Content"],
    "more": ["Get-Content"],
    "head": ["Select-Object -First"],
    "tail": ["Select-Object -Last"],
    "tee": ["Tee-Object"],
    "echo": ["Write-Output"],
    "printf": ["Write-Output"],
    "grep": ["Select-String"],
    "egrep": ["Select-String"],
    "fgrep": ["Select-String"],
    "find": ["Get-ChildItem -Recurse"],
    "which": ["Get-Command"],
    "where": ["Get-Command"],
    "touch": ["New-Item -ItemType File -Force"],
    "chmod": ["Set-ItemProperty -Name Mode"],
    "chown": ["Set-ItemProperty -Name Owner"],
    "clear": ["Clear-Host"],
    "uname": ["$PSVersionTable.PSVersion.ToString()"],
    "whoami": ["[System.Security.Principal.WindowsPrincipal] [System.Security.Principal.WindowsIdentity]::GetCurrent()"],
    "id": ["[System.Security.Principal.WindowsIdentity]::GetCurrent().Name"],
    "groups": ["(Get-LocalUser).Name"],
    "date": ["Get-Date"],
    "history": ["Get-History"],
    "man": ["Get-Help"],
    "help": ["Get-Help"],
    "ps": ["Get-Process"],
    "top": ["Get-Process | Sort-Object CPU -Descending"],
    "htop": ["Get-Process | Sort-Object CPU -Descending"],
    "kill": ["Stop-Process"],
    "pkill": ["Stop-Process"],
    "pgrep": ["Get-Process"],
    "jobs": ["Get-Job"],
    "bg": ["Start-Job"],
    "fg": ["Receive-Job"],
    "sleep": ["Start-Sleep"],
    "nohup": ["Start-Process"],
    "nice": ["Start-Process"],
    "curl": ["Invoke-WebRequest"],
    "wget": ["Invoke-WebRequest"],
    "nc": ["Test-NetConnection"],
    "telnet": ["Test-NetConnection"],
    "ping": ["Test-Connection"],
    "ip": ["Get-NetIPConfiguration"],
    "ifconfig": ["Get-NetIPConfiguration"],
    "ipconfig": ["Get-NetIPConfiguration"],
    "netstat": ["Get-NetTCPConnection"],
    "ss": ["Get-NetTCPConnection"],
    "route": ["Get-NetRoute"],
    "nslookup": ["Resolve-DnsName"],
    "ssh": ["Enter-PSSession"],
    "scp": ["Copy-Item"],
    "tar": ["Compress-Archive"],
    "untar": ["Expand-Archive"],
    "zip": ["Compress-Archive"],
    "unzip": ["Expand-Archive"],
    "diff": ["Compare-Object"],
    "cmp": ["Compare-Object"],
    "sort": ["Sort-Object"],
    "uniq": ["Select-Object -Unique"],
    "cut": ["Select-Object -Skip"],
    "paste": ["Out-String"],
    "wc": ["Measure-Object"],
    "sed": ["Get-Content"],
    "awk": ["ForEach-Object"],
    "tr": ["ForEach-Object"],
    "rev": ["ForEach-Object"],
    "basename": ["Split-Path -Leaf"],
    "dirname": ["Split-Path -Parent"],
    "realpath": ["Resolve-Path"],
    "env": ["Get-ChildItem Env:"],
    "export": ["$env:"],
    "source": ["."],
    "hostname": ["$env:COMPUTERNAME"],
    "alias": ["Get-Alias"],
    "type": ["Get-Content"],
    "tree": ["Get-ChildItem -Recurse"],
    "du": ["Get-ChildItem -Recurse | Measure-Object Length -Sum"],
    "df": ["Get-PSDrive | Select-Object Name, Used, Free"],
    "mount": ["Get-PSDrive"],
    "umount": ["Remove-PSDrive"],
    "passwd": ["Set-LocalUser"],
    "sudo": ["Start-Process"],
    "su": ["Start-Process"],
    "apt": ["Install-Module"],
    "apt-get": ["Install-Module"],
    "yum": ["Install-Module"],
    "dnf": ["Install-Module"],
    "brew": ["Install-Module"],
    "choco": ["Install-Module"],
    "git": ["git"],
    "svn": ["svn"],
    "hg": ["hg"],
    "pip": ["python -m pip"],
    "python": ["python"],
    "pip3": ["python -m pip"],
    "node": ["node"],
    "npm": ["npm"],
    "yarn": ["yarn"],
    "make": ["make"],
    "cargo": ["cargo"],
    "go": ["go"],
    "docker": ["docker"],
    "kubectl": ["kubectl"],
    "systemctl": ["Get-Service"],
    "service": ["Get-Service"],
    "start": ["Start-Service"],
    "stop": ["Stop-Service"],
    "restart": ["Restart-Service"],
    "status": ["Get-Service"],
    "lsblk": ["Get-Disk"],
    "df": ["Get-PSDrive | Select-Object Name, Used, Free"],
    "du": ["Get-ChildItem -Recurse | Measure-Object Length -Sum"],
    "free": ["Get-Counter '\\Memory\\Available MBytes'"],
    "top": ["Get-Process | Sort-Object CPU -Descending"],
    "uptime": ["(Get-Date) - (Get-CimInstance Win32_OperatingSystem).LastBootUpTime"],
    "uname": ["$PSVersionTable.PSVersion.ToString()"],
    "hostname": ["$env:COMPUTERNAME"],
    "who": ["Get-LocalUser"],
    "w": ["Get-Process"],
    "last": ["Get-History"],
    "finger": ["Get-LocalUser"],
    "passwd": ["Set-LocalUser"],
    "sudo": ["Start-Process"],
    "su": ["Start-Process"],
    "mount": ["Get-PSDrive"],
    "umount": ["Remove-PSDrive"],
    "open": ["Invoke-Item"],
    "explorer": ["Invoke-Item"],
    "pwd": ["Get-Location"],
    "pushd": ["Push-Location"],
    "popd": ["Pop-Location"],
    "test": ["Test-Path"],
    "touch": ["New-Item -ItemType File -Force"],
    "mkdir": ["New-Item -ItemType Directory -Force"],
    "rmdir": ["Remove-Item -Recurse -Force"],
    "basename": ["Split-Path -Leaf"],
    "dirname": ["Split-Path -Parent"],
    "realpath": ["Resolve-Path"],
    "grep -r": ["Select-String -Path"],
}


def build_tutorial_text() -> str:
    return """5-minute PowerShell tutorial
===========================
PowerShell is Microsoft's shell and scripting language for automation.
Common commands:
- Get-ChildItem  -> list files and folders (similar to ls)
- Set-Location   -> change folders (similar to cd)
- Get-Location   -> show the current folder (similar to pwd)
- New-Item       -> create files or folders
- Remove-Item    -> delete files or folders
- Copy-Item      -> copy files
- Move-Item      -> move files
- Get-Content    -> read file contents (similar to cat)
- Select-String  -> search text in files (similar to grep)
- Get-Help       -> learn about a command
Start small: try a command, inspect the output, and then add flags as you learn.
"""


def _normalize_command(input_text: str) -> str:
    text = input_text.strip()
    if not text:
        return ""
    return re.sub(r"\s+", " ", text)


def translate_command(command: str) -> List[str]:
    normalized = _normalize_command(command)
    if not normalized:
        return []

    parts = normalized.split()
    if not parts:
        return []

    base = parts[0].lower()
    suggestions: List[str] = []
    args = parts[1:]

    if base in COMMAND_MAPPINGS:
        translated = COMMAND_MAPPINGS[base]
        if base in {"ls", "ll", "la"}:
            if args:
                suggestions.append("Get-ChildItem " + " ".join(args))
            else:
                suggestions.append("Get-ChildItem")
        elif base in {"cd"}:
            suggestions.append("Set-Location " + (args[0] if args else "."))
        elif base in {"cp", "mv"}:
            src = args[0] if len(args) > 0 else "source"
            dst = args[1] if len(args) > 1 else "destination"
            suggestions.append(f"{translated[0]} -Path {src} -Destination {dst}")
        elif base in {"rm"}:
            target = args[0] if args else "target"
            suggestions.append(f"{translated[0]} {target}")
        else:
            if args:
                suggestions.append(translated[0] + " " + " ".join(args))
            else:
                suggestions.append(translated[0])
    else:
        suggestions.append(f"# No deterministic mapping for '{base}'")

    if base in {"ls", "ll", "la"}:
        suggestions.append("Get-ChildItem -Force")
        suggestions.append("Get-ChildItem -Recurse")
    elif base in {"cp", "mv", "rm"}:
        suggestions.append(f"{COMMAND_MAPPINGS[base][0]} -Path source -Destination destination")
    elif base in {"cat"}:
        suggestions.append("Get-Content -Raw")

    return suggestions


def _choose_with_fzf(suggestions: List[str]) -> str | None:
    if not suggestions:
        return None

    if os.environ.get("BASH2PS_NO_FZF") == "1":
        return suggestions[0]

    try:
        process = subprocess.run(
            ["fzf"],
            input="\n".join(suggestions).encode("utf-8"),
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            check=False,
        )
    except FileNotFoundError:
        return suggestions[0]

    if process.returncode not in {0, 1}:
        return None

    if process.returncode == 0:
        selected = process.stdout.decode("utf-8").strip()
        return selected if selected else None

    return None


def _paste_to_clipboard(command: str) -> None:
    if os.name == "nt":
        subprocess.run(["clip"], input=command.encode("utf-8"), stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=False)
        return

    if shutil := os.environ.get("WAYLAND_DISPLAY"):
        subprocess.run(["wl-copy"], input=command.encode("utf-8"), stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=False)
    else:
        subprocess.run(["xclip", "-selection", "clipboard"], input=command.encode("utf-8"), stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=False)


def run_cli(argv: List[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="bash2ps")
    parser.add_argument("command", nargs="?", help="Bash command to translate")
    parser.add_argument("--tutorial", action="store_true", help="Show a short PowerShell tutorial")
    args = parser.parse_args(argv)

    if args.tutorial:
        print(build_tutorial_text())
        return 0

    if args.command is None:
        print("Usage: bash2ps \"ls -la\" or bash2ps --tutorial")
        return 0

    suggestions = translate_command(args.command)
    if not suggestions:
        print("No translation available")
        return 0

    selected = _choose_with_fzf(suggestions)
    if selected is None:
        selected = suggestions[0]

    _paste_to_clipboard(selected)
    print(selected)
    print("Copied to clipboard. Paste it into your PowerShell prompt.")
    return 0


if __name__ == "__main__":
    sys.exit(run_cli())
