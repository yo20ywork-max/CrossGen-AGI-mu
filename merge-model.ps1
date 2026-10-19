param([string]$Directory = $PSScriptRoot)
$ErrorActionPreference = 'Stop'
$parts = @(
    @{ Name = 'CrossGen-core-Q4_K_M.gguf.part01'; Bytes = 1600000000; Hash = 'ab4267e6badda719ce4795737e8678024abd48dfc9b6aa5808607cf7afefbbbd' },
    @{ Name = 'CrossGen-core-Q4_K_M.gguf.part02'; Bytes = 1600000000; Hash = '89deae3e50880809596be6c53890a3ccfcf03309c44653d80df27752840ebda5' },
    @{ Name = 'CrossGen-core-Q4_K_M.gguf.part03'; Bytes = 1483074048; Hash = '6c234b53f429ca4503614d143b4d184d568a3c75d245e838d575dc59819d8722' }
)
$expectedHash = '60e05f2100071479f596b964f89f510f057ce397ea22f2833a0cfe029bfc2463'
$output = Join-Path $Directory 'CrossGen-core-Q4_K_M.gguf'
$partial = $output + '.partial'
if (Test-Path -LiteralPath $output) {
    if ((Get-FileHash -LiteralPath $output -Algorithm SHA256).Hash.ToLowerInvariant() -eq $expectedHash) {
        Write-Host 'Model already verified.'
        exit 0
    }
    throw 'An existing model has a different checksum; move it before retrying.'
}
foreach ($part in $parts) {
    $path = Join-Path $Directory $part.Name
    if ((Get-Item -LiteralPath $path).Length -ne $part.Bytes) { throw ('Wrong size: ' + $part.Name) }
    if ((Get-FileHash -LiteralPath $path -Algorithm SHA256).Hash.ToLowerInvariant() -ne $part.Hash) {
        throw ('Checksum mismatch: ' + $part.Name)
    }
}
$stream = [System.IO.File]::Open($partial, [System.IO.FileMode]::CreateNew, [System.IO.FileAccess]::Write)
try {
    foreach ($part in $parts) {
        $source = [System.IO.File]::OpenRead((Join-Path $Directory $part.Name))
        try { $source.CopyTo($stream, 8388608) } finally { $source.Dispose() }
    }
} finally { $stream.Dispose() }
if ((Get-FileHash -LiteralPath $partial -Algorithm SHA256).Hash.ToLowerInvariant() -ne $expectedHash) {
    throw 'Combined model checksum mismatch; partial file retained for inspection.'
}
Move-Item -LiteralPath $partial -Destination $output
Write-Host ('Verified: ' + $output)
