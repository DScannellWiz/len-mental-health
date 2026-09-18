param(
    [Parameter(Mandatory = $true)]
    [string]$Version,
    [string]$ArtifactRevision = "",
    [string]$Python = ""
)

$ErrorActionPreference = "Stop"
if ($Version -eq "0.3.0-alpha.1") {
    throw "Version 0.3.0-alpha.1 is frozen. Build Len with a newer version."
}
$Root = Split-Path -Parent $PSScriptRoot
$Dist = Join-Path $Root "dist"
$Build = Join-Path $Root "build"
$PortableOut = Join-Path $Root "release"
$ArtifactLabel = if ([string]::IsNullOrWhiteSpace($ArtifactRevision)) {
    $Version
} else {
    "$Version-$ArtifactRevision"
}
if ([string]::IsNullOrWhiteSpace($Python)) {
    $RepositoryPython = Join-Path $Root ".venv\Scripts\python.exe"
    $Python = if (Test-Path -LiteralPath $RepositoryPython) { $RepositoryPython } else { "python" }
}

$PythonBase = & $Python -c "import sys; print(sys.base_prefix)"
if ($LASTEXITCODE -ne 0) {
    throw "Unable to inspect the selected Python runtime: $Python"
}
$TkinterLib = Join-Path $PythonBase "Lib\tkinter"
$TclLib = Join-Path $PythonBase "tcl\tcl8.6"
$TkLib = Join-Path $PythonBase "tcl\tk8.6"
$TclPackages = Join-Path $PythonBase "tcl\tcl8"
$TkinterExtension = Join-Path $PythonBase "DLLs\_tkinter.pyd"
$TclDll = Join-Path $PythonBase "DLLs\tcl86t.dll"
$TkDll = Join-Path $PythonBase "DLLs\tk86t.dll"
$TkRuntimeHook = Join-Path $Root "packaging\pyi_rth_tkinter_portable.py"
$PortableEntry = Join-Path $Root "packaging\portable_entry.py"

& $Python -c "import openpyxl, pandas, PIL, reportlab, pypdf"
if ($LASTEXITCODE -ne 0) {
    throw "Release dependencies are incomplete. Install requirements.txt and PyInstaller in the build environment."
}

& $Python (Join-Path $PSScriptRoot "verify_release_licenses.py")
if ($LASTEXITCODE -ne 0) {
    throw "Release licensing verification failed."
}

$RequiredTkPaths = @(
    $TkinterLib,
    $TclLib,
    $TkLib,
    $TclPackages,
    $TkinterExtension,
    $TclDll,
    $TkDll,
    $TkRuntimeHook,
    $PortableEntry
)
foreach ($RequiredPath in $RequiredTkPaths) {
    if (-not (Test-Path -LiteralPath $RequiredPath)) {
        throw "Tk runtime dependency is missing: $RequiredPath"
    }
}

New-Item -ItemType Directory -Force -Path $Dist, $Build, $PortableOut | Out-Null

& $Python -m PyInstaller `
  --noconfirm `
  --clean `
  --onedir `
  --name "PHQ9Tracker" `
  --distpath $Dist `
  --workpath $Build `
  --paths "$Root\src" `
  --icon "$Root\packaging\assets\PHQ9_Tracker.ico" `
  --add-data "$Root\README.md;." `
  --add-data "$TkinterLib;tkinter" `
  --add-data "$TclLib;_tcl_data" `
  --add-data "$TkLib;_tk_data" `
  --add-data "$TclPackages;tcl8" `
  --add-binary "$TkinterExtension;." `
  --add-binary "$TclDll;." `
  --add-binary "$TkDll;." `
  --runtime-hook $TkRuntimeHook `
  --exclude-module pytest `
  --exclude-module unittest `
  --exclude-module IPython `
  --exclude-module notebook `
  $PortableEntry

if ($LASTEXITCODE -ne 0) {
    throw "PyInstaller release build failed."
}

$DistApp = Join-Path $Dist "PHQ9Tracker"
$RequiredBundlePaths = @(
    (Join-Path $DistApp "PHQ9Tracker.exe"),
    (Join-Path $DistApp "_internal\_tcl_data\init.tcl"),
    (Join-Path $DistApp "_internal\_tk_data\tk.tcl"),
    (Join-Path $DistApp "_internal\_tkinter.pyd"),
    (Join-Path $DistApp "_internal\tcl86t.dll"),
    (Join-Path $DistApp "_internal\tk86t.dll")
)
foreach ($RequiredBundlePath in $RequiredBundlePaths) {
    if (-not (Test-Path -LiteralPath $RequiredBundlePath -PathType Leaf)) {
        throw "Built bundle is missing required Tcl/Tk content: $RequiredBundlePath"
    }
}

# The controlled runtime may contain redundant Tkinter bytecode caches whose
# compiled filenames disclose the local runtime path. Remove only that copied
# cache from the built bundle; do not mutate the controlled Python installation.
$BundledTkinterCache = Join-Path $DistApp "_internal\tkinter\__pycache__"
if (Test-Path -LiteralPath $BundledTkinterCache -PathType Container) {
    Remove-Item -Recurse -Force -LiteralPath $BundledTkinterCache
}

& $Python (Join-Path $PSScriptRoot "verify_release_hygiene.py") `
  $DistApp `
  --forbid-root $Root `
  --forbid-root $PythonBase
if ($LASTEXITCODE -ne 0) {
    throw "Release bundle hygiene verification failed."
}

Copy-Item -LiteralPath (Join-Path $Root "LICENSE") -Destination (Join-Path $DistApp "LICENSE")
Copy-Item -Recurse -LiteralPath (Join-Path $Root "THIRD_PARTY_NOTICES") -Destination (Join-Path $DistApp "THIRD_PARTY_NOTICES")

$PortableDir = Join-Path $PortableOut "Len-Portable-$ArtifactLabel"
if (Test-Path $PortableDir) {
    $ExpectedPortableRoot = [IO.Path]::GetFullPath($PortableOut).TrimEnd('\') + '\'
    $ResolvedPortableDir = [IO.Path]::GetFullPath($PortableDir)
    if (-not $ResolvedPortableDir.StartsWith($ExpectedPortableRoot, [StringComparison]::OrdinalIgnoreCase)) {
        throw "Refusing to remove unexpected portable output path: $ResolvedPortableDir"
    }
    Remove-Item -Recurse -Force $PortableDir
}
Copy-Item -Recurse $DistApp $PortableDir
Set-Content -Path (Join-Path $PortableDir "Launch Portable Len.bat") -Value @"
@echo off
setlocal
set PHQ9_TRACKER_PORTABLE=1
cd /d "%~dp0"
"%~dp0PHQ9Tracker.exe"
"@

$ZipPath = Join-Path $PortableOut "Len-Portable-$ArtifactLabel.zip"
if (Test-Path $ZipPath) {
    Remove-Item -Force $ZipPath
}
Compress-Archive -Path "$PortableDir\*" -DestinationPath $ZipPath -CompressionLevel Optimal

Write-Host "Built folder-based app: $Dist\PHQ9Tracker"
Write-Host "Built portable folder: $PortableDir"
Write-Host "Built portable zip: $ZipPath"
Write-Host "Included project license: $PortableDir\LICENSE"
Write-Host "Included third-party notices: $PortableDir\THIRD_PARTY_NOTICES"
Write-Host "Next: compile packaging\PHQ9Tracker.iss with Inno Setup."
