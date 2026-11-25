$ErrorActionPreference = 'Stop'
Add-Type -AssemblyName System.Speech
$reader = New-Object System.Speech.Synthesis.SpeechSynthesizer
try {
    $reader.SelectVoice('Microsoft Zira Desktop')
    $reader.Rate = -2
    $reader.Volume = 100
    $manifest = Get-Content -LiteralPath (Join-Path $PSScriptRoot 'audio-manifest.json') -Raw -Encoding UTF8 | ConvertFrom-Json
    foreach ($entry in $manifest) {
        $destination = Join-Path $PSScriptRoot $entry.file
        $reader.SetOutputToWaveFile($destination)
        $reader.Speak($entry.text)
        $reader.SetOutputToNull()
    }
} finally {
    $reader.Dispose()
}
Write-Output ('Generated {0} American English speech clips.' -f $manifest.Count)
