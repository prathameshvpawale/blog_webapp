<#
PowerShell helper to download PlantUML jar (if needed) and render all .puml files
Usage: pwsh -ExecutionPolicy Bypass -File .\diagram\render_puml.ps1
#>

$ErrorActionPreference = 'Stop'
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Definition
$repoRoot = Resolve-Path "$scriptDir\.."
Set-Location $repoRoot

$plantumlJar = Join-Path $repoRoot 'plantuml.jar'
$pumlDir = Join-Path $repoRoot 'diagram\collection\puml'
$outDir = Join-Path $repoRoot 'diagram\collection\pngs'

if (-not (Test-Path $pumlDir)) {
    Write-Error "PUML directory not found: $pumlDir"
    exit 1
}

if (-not (Test-Path $outDir)) {
    New-Item -ItemType Directory -Path $outDir | Out-Null
}

# Check Java
try {
    & java -version 2>$null
} catch {
    Write-Host "Java not found on PATH. Please install a JDK (e.g., AdoptOpenJDK/Temurin) before proceeding." -ForegroundColor Yellow
    Write-Host 'Chocolatey can install it: choco install temurin (requires admin).'
    exit 1
}

# Download plantuml.jar if missing
if (-not (Test-Path $plantumlJar)) {
    Write-Host "plantuml.jar not found. Downloading from GitHub releases..."
    $url = 'https://github.com/plantuml/plantuml/releases/latest/download/plantuml.jar'
    try {
        Invoke-WebRequest -Uri $url -OutFile $plantumlJar -UseBasicParsing
        Write-Host "Downloaded plantuml.jar to $plantumlJar"
    } catch {
        Write-Error "Failed to download plantuml.jar. Please download it manually from https://plantuml.com/download and place it in the project root."
        exit 1
    }
} else {
    Write-Host "Found existing plantuml.jar at $plantumlJar"
}

# Check for Graphviz 'dot' - optional but recommended
$dot = Get-Command dot -ErrorAction SilentlyContinue
if (-not $dot) {
    Write-Host "Graphviz 'dot' not found. Some diagrams (class/component) may not render fully without Graphviz." -ForegroundColor Yellow
    Write-Host 'Install Graphviz (https://graphviz.org/download/) or via Chocolatey: choco install graphviz'
}

# Render .puml files
Write-Host "Rendering .puml files from $pumlDir to $outDir"
$pumlFiles = Get-ChildItem -Path $pumlDir -Filter '*.puml' -File -Recurse
if ($pumlFiles.Count -eq 0) {
    Write-Host "No .puml files found in $pumlDir"
    exit 0
}

foreach ($file in $pumlFiles) {
    Write-Host "Rendering: $($file.Name)"
    & java -jar $plantumlJar -tpng -o $outDir $file.FullName
    if ($LASTEXITCODE -ne 0) {
        Write-Host "PlantUML failed for $($file.Name)" -ForegroundColor Red
    }
}

Write-Host "Rendering complete. PNGs are in: $outDir" -ForegroundColor Green

# End of script
