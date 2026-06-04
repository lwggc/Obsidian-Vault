$fontPath = "$env:LOCALAPPDATA\Microsoft\Windows\Fonts\Yozai-Regular.ttf"
if (Test-Path $fontPath) {
    Write-Host "Font file exists at: $fontPath"
    $shell = New-Object -ComObject Shell.Application
    $folder = $shell.Namespace((Get-Item $fontPath).DirectoryName)
    $item = $folder.ParseName((Get-Item $fontPath).Name)
    $item.InvokeVerb("Install")
    Write-Host "Installation attempted for: $($item.Name)"
} else {
    Write-Host "Font file not found!"
}
