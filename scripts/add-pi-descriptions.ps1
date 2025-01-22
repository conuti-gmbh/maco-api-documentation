# Read the processinfo.json file
$processInfo = Get-Content -Path "$PSScriptRoot/../pythons/processinfo.json" -Raw | ConvertFrom-Json

# Create a hashtable to store PI descriptions
$piDescriptions = @{}

# Process each entry in processinfo.json
foreach ($process in $processInfo) {
    $description = "$($process.pruefidentifikator) - $($process.absender) an $($process.empfaenger) - $($process.aktion)"
    $piNumber = $process.pruefidentifikator
    
    # Add to hashtable if not exists, or if exists and is from GPKE (preferred over GeLi Gas)
    if (-not $piDescriptions.ContainsKey($piNumber) -or 
        ($process.prozessbeschreibung -eq "GPKE" -and $piDescriptions.ContainsKey($piNumber))) {
        $piDescriptions[$piNumber] = $description
    }
}

# Get all PI yaml files
$piFiles = Get-ChildItem -Path "$PSScriptRoot/../macoapp-schreiben/components/requestBodies/PIs/" -Filter "PI_*.yml"

foreach ($file in $piFiles) {
    $content = Get-Content $file.FullName -Raw
    $piNumber = $file.BaseName -replace "PI_", ""
    
    if ($piDescriptions.ContainsKey($piNumber)) {
        $description = $piDescriptions[$piNumber]
        
        if ($content -match 'description:\s*"[^"]*"') {
            # Replace existing description
            $content = $content -replace 'description:\s*"[^"]*"', "description: `"$description`""
        } else {
            # Add description if it doesn't exist
            $content = "`ndescription: `"$description`"`n" + $content
        }
        
        Set-Content -Path $file.FullName -Value $content
    }
}

Write-Host "Finished adding descriptions to PI files"
