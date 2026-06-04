try {
    $fontDir = [System.Environment]::GetFolderPath('LocalApplicationData') + '\Microsoft\Windows\Fonts\'
    if (Test-Path ($fontDir + 'Yozai-Regular.ttf')) {
        Write-Host 'Yozai-Regular.ttf file exists'
    }

    Add-Type -AssemblyName PresentationCore
    $font = [System.Windows.Media.Fonts]::GetFontFamilies($fontDir) | Where-Object { $_.Source -like '*Yozai*' }
    if ($font) {
        Write-Host 'Font found!'
        Write-Host 'Family names:'
        foreach ($key in $font.FamilyNames.Keys) {
            Write-Host "  $key = $($font.FamilyNames[$key])"
        }
    } else {
        Write-Host 'Font NOT found by Windows font system'
        Write-Host 'Listing all fonts in user directory:'
        Get-ChildItem $fontDir | Select-Object Name, Length
    }
} catch {
    Write-Host "Error: $_"
}
