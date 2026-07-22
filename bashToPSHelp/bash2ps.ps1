param(
    [Parameter(ValueFromRemainingArguments = $true)]
    [string[]]$Arguments
)

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$scriptPath = Join-Path $scriptDir 'bash2ps.py'
$pythonCommand = $null
$pythonArgs = @()

$candidates = @(
    @{ Name = 'py'; Args = @('-3') },
    @{ Name = 'python'; Args = @() },
    @{ Name = 'python3'; Args = @() },
    @{ Name = 'C:\Users\pierr\AppData\Local\Microsoft\WindowsApps\python.exe'; Args = @() },
    @{ Name = 'C:\Users\pierr\AppData\Local\Microsoft\WindowsApps\python3.exe'; Args = @() }
)

foreach ($candidate in $candidates) {
    $cmd = Get-Command $candidate.Name -ErrorAction SilentlyContinue
    if ($cmd) {
        $pythonCommand = $cmd.Source
        $pythonArgs = $candidate.Args
        break
    }
}

if (-not $pythonCommand) {
    Write-Error 'Python was not found on PATH. Install Python 3 and try again.'
    exit 1
}

& $pythonCommand @pythonArgs $scriptPath @Arguments
exit $LASTEXITCODE
