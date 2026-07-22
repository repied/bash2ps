function bash2ps {
    param(
        [Parameter(ValueFromRemainingArguments = $true)]
        [string[]]$Arguments
    )

    $scriptDir = Split-Path -Parent $PSCommandPath
    if (-not $scriptDir) {
        $scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
    }
    $scriptPath = Join-Path $scriptDir 'bash2ps.py'
    $pythonCommand = $null
    $pythonArgs = @()

    foreach ($candidate in @('py','python','python3')) {
        $cmd = Get-Command $candidate -ErrorAction SilentlyContinue
        if ($cmd) {
            $pythonCommand = $cmd.Source
            if ($candidate -eq 'py') { $pythonArgs = @('-3') } else { $pythonArgs = @() }
            break
        }
    }

    if (-not $pythonCommand) {
        Write-Error 'Python was not found on PATH. Install Python 3 and try again.'
        return
    }

    $pythonArgsList = @($scriptPath) + $Arguments
    $pythonOutput = & $pythonCommand @pythonArgs @pythonArgsList 2>&1
    $text = ($pythonOutput | Out-String).Trim()
    if (-not $text) { return }

    $selected = $null
    if ($text -match '(?m)^Get-|(?m)^Set-|(?m)^New-|(?m)^Remove-|(?m)^Copy-|(?m)^Move-|(?m)^Invoke-|(?m)^Select-|(?m)^Write-|(?m)^Test-|(?m)^Start-|(?m)^Stop-|(?m)^Restart-|(?m)^Measure-|(?m)^Compare-|(?m)^Sort-|(?m)^Push-|(?m)^Pop-') {
        $selected = ($text -split "`n" | Where-Object { $_ -match '^(Get-|Set-|New-|Remove-|Copy-|Move-|Invoke-|Select-|Write-|Test-|Start-|Stop-|Restart-|Measure-|Compare-|Sort-|Push-|Pop-)' } | Select-Object -First 1).Trim()
    }

    if ($selected) {
        # Write-Host ""
        # Write-Host "PS> $selected" -ForegroundColor Cyan
        try {
            if (Get-Command -Name 'Set-PSReadLineOption' -ErrorAction SilentlyContinue) {
                [Microsoft.PowerShell.PSConsoleReadLine]::DeleteLine()
                [Microsoft.PowerShell.PSConsoleReadLine]::Insert($selected)
            }
            else {
                Write-Host $selected -ForegroundColor Cyan
                Write-Host "PSReadLine is not available here, so the command was printed instead." -ForegroundColor Yellow
            }
        }
        catch {
            Write-Host $selected -ForegroundColor Cyan
            Write-Host "The command was printed instead because prompt insertion was unavailable." -ForegroundColor Yellow
        }
    }
    else {
        $text | Write-Host
    }
}
