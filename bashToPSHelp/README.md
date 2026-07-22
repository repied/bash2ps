# bash2ps

bash2ps is a small Python-based PowerShell learning helper that translates common bash commands into PowerShell equivalents.

## Usage

- Run the tutorial:
  - `./bash2ps.ps1 --tutorial`
- Translate a command:
  - `./bash2ps.ps1 "ls -la"`

The tool uses a deterministic mapping for common commands and offers a few likely alternatives. If `fzf` is available, it lets you select one suggestion interactively; the selected command is copied to the clipboard for pasting into your PowerShell prompt.
