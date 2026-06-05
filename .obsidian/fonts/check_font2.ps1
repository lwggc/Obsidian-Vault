try {
    $fonts = New-Object -ComObject Shell.Application
    $fontsPath = [Environment]::GetFolderPath('LocalApplicationData') + '\Microsoft\Windows\Fonts'
    $file = Join-Path $fontsPath 'Yozai-Regular.ttf'
    if (Test-Path $file) {
        Write-Host "FONT_FILE_EXISTS"
    } else {
        Write-Host "FONT_FILE_MISSING"
        exit
    }
    # Check registry
    $regPath = 'HKCU:\Software\Microsoft\Windows NT\CurrentVersion\Fonts'
    $val = Get-ItemProperty -Path $regPath -Name 'Yozai (TrueType)' -ErrorAction SilentlyContinue
    if ($val) {
        Write-Host "FONT_REGISTERED"
    } else {
        Write-Host "FONT_NOT_REGISTERED"
    }
} catch {
    Write-Host "ERROR: $_"
}
