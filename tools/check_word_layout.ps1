<#
.SYNOPSIS
Verify the APA Word document's actual pagination using desktop Microsoft Word.
.DESCRIPTION
Uses a new invisible Word instance and closes only that instance. Does not
change the document. PDF generation is handled by export_report.py.
#>
param()

$ErrorActionPreference = 'Stop'
$projectRoot = Split-Path -Parent $PSScriptRoot
$documentPath = Join-Path $projectRoot 'docs\final_report.docx'
$evidenceDirectory = Join-Path $projectRoot 'docs\validation'
$wordApplication = $null
$reportDocument = $null
try {
    Write-Output 'Opening report in an isolated Word instance.'
    $wordApplication = New-Object -ComObject Word.Application
    $wordApplication.Visible = $false
    $wordApplication.DisplayAlerts = 0
    $reportDocument = $wordApplication.Documents.Open($documentPath, $false, $true)
    $reportDocument.Repaginate()
    $firstHashPage = $reportDocument.Bookmarks.Item('HashExplanationStart').Range.Information(3)
    $collisionPage = $reportDocument.Bookmarks.Item('CollisionExplanationStart').Range.Information(3)
    $lastHashPage = $reportDocument.Bookmarks.Item('HashExplanationEnd').Range.Information(3)
    if ($collisionPage -ne ($firstHashPage + 1) -or $lastHashPage -ne $collisionPage) {
        throw "Hashing explanation must occupy two consecutive pages: $firstHashPage, $collisionPage, $lastHashPage"
    }
    $layout = [ordered]@{
        renderer = 'Microsoft Word'
        renderer_version = $wordApplication.Version
        total_pages = $reportDocument.ComputeStatistics(2)
        hash_function_page = $firstHashPage
        collision_resolution_page = $collisionPage
        hash_explanation_last_page = $lastHashPage
        docx_sha256 = (Get-FileHash -LiteralPath $documentPath -Algorithm SHA256).Hash.ToLowerInvariant()
    }
    $layout | ConvertTo-Json | Set-Content -LiteralPath (Join-Path $evidenceDirectory 'word_layout.json') -Encoding utf8
    $layout | ConvertTo-Json
}
finally {
    if ($null -ne $reportDocument) {
        $reportDocument.Close(0)
        [void][System.Runtime.InteropServices.Marshal]::ReleaseComObject($reportDocument)
    }
    if ($null -ne $wordApplication) {
        $wordApplication.Quit()
        [void][System.Runtime.InteropServices.Marshal]::ReleaseComObject($wordApplication)
    }
}
