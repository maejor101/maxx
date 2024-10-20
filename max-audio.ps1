# max-audio.ps1
# PowerShell script to set up and run the Flask video trimming app

# Ensure Python and pip are installed
$python = Get-Command python -ErrorAction SilentlyContinue
$pip = Get-Command pip -ErrorAction SilentlyContinue

if (-not $python) {
    Write-Host "Python is not installed. Please install Python to continue." -ForegroundColor Red
    exit
}

if (-not $pip) {
    Write-Host "pip is not installed. Installing pip..." -ForegroundColor Yellow
    python -m ensurepip --upgrade
}

# Install required Python packages
Write-Host "Installing dependencies from requirements.txt..." -ForegroundColor Green
pip install -r requirements.txt

# Create uploads and outputs directories if they don't exist
if (-not (Test-Path -Path "./uploads")) {
    New-Item -ItemType Directory -Path "./uploads"
    Write-Host "Created uploads directory."
}

if (-not (Test-Path -Path "./outputs")) {
    New-Item -ItemType Directory -Path "./outputs"
    Write-Host "Created outputs directory."
}

# Run the Flask app
Write-Host "Starting Flask server..." -ForegroundColor Green
python app.py
