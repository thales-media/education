$ErrorActionPreference = 'Stop'
Add-Type -AssemblyName System.Drawing
$pictureRoot = Join-Path $PSScriptRoot 'assets/vocabulary'
$names = @('thanksgiving','harvest','turkey','pumpkin','cranberry','feast','thankful','grateful','gratitude','bless','happy-thanksgiving','i-m-grateful-for-your-help')
foreach ($name in $names) {
    $source = [System.Drawing.Image]::FromFile((Join-Path $pictureRoot ($name + '.png')))
    $small = New-Object System.Drawing.Bitmap 192, 192
    $graphics = [System.Drawing.Graphics]::FromImage($small)
    try {
        $graphics.Clear([System.Drawing.Color]::White)
        $graphics.InterpolationMode = [System.Drawing.Drawing2D.InterpolationMode]::HighQualityBicubic
        $graphics.DrawImage($source, 0, 0, 192, 192)
        $small.Save((Join-Path $pictureRoot ($name + '-small.png')), [System.Drawing.Imaging.ImageFormat]::Png)
    } finally {
        $graphics.Dispose()
        $small.Dispose()
        $source.Dispose()
    }
}
Write-Output ('Exported {0} small 192px assets for 64px display.' -f $names.Count)
