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

$tempFile = [System.IO.Path]::GetTempFileName()
try {
    & $pythonCommand @pythonArgs $scriptPath @Arguments 2>&1 | Tee-Object -FilePath $tempFile | Out-Host
    if ($LASTEXITCODE -eq 0) {
        $content = Get-Content -Path $tempFile -Raw
        if ($content -match '(^|\n)(Get-|Set-|New-|Remove-|Copy-|Move-|Invoke-|Select-|Write-|Test-|Start-|Stop-|Restart-|Measure-|Compare-|Sort-|Push-|Pop-).+') {
            $match = [regex]::Match($content, '(?m)^(Get-|Set-|New-|Remove-|Copy-|Move-|Invoke-|Select-|Write-|Test-|Start-|Stop-|Restart-|Measure-|Compare-|Sort-|Push-|Pop-).+$')
            if ($match.Success) {
                $command = $match.Value.Trim()
                Write-Host "" 
                Write-Host "PS> $command" -ForegroundColor Cyan
                Write-Host "Press Enter to run it, or Ctrl+C to cancel." -ForegroundColor Yellow
            }
        }
    }
}
finally {
    Remove-Item $tempFile -ErrorAction SilentlyContinue
}
exit $LASTEXITCODE
