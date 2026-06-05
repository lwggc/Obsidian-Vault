$source = [Environment]::GetFolderPath('LocalApplicationData') + '\Microsoft\Windows\Fonts\Yozai-Regular.ttf'
$destination = "$env:WINDIR\Fonts\Yozai-Regular.ttf"

# Copy to system fonts folder (requires admin)
try {
    Copy-Item $source $destination -Force
    Write-Host "COPIED_TO_SYSTEM"
} catch {
    Write-Host "COPY_FAILED"
}

# Register in registry
$reg = [Microsoft.Win32.Registry]::LocalMachine.OpenSubKey('Software\Microsoft\Windows NT\CurrentVersion\Fonts', $true)
if ($reg) {
    $reg.SetValue('Yozai (TrueType)', 'Yozai-Regular.ttf')
    $reg.Close()
    Write-Host "REGISTERED_IN_REGISTRY"
} else {
    Write-Host "REGISTRY_ACCESS_DENIED"
}

# Notify system
$gdi = Add-Type -MemberDefinition '[DllImport("gdi32.dll")] public static extern int AddFontResource(string lpszFilename);' -Name 'Gdi32' -Namespace 'Win32' -PassThru
$result = $gdi::AddFontResource($source)
Write-Host "ADDFONTRESOURCE_RESULT: $result"
