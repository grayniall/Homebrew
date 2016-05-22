properties {
    $BuildConfiguration = if ($BuildConfiguration -eq $null ) { "debug" } else {     
        $BuildConfiguration }
    $BuildScriptsPath = Resolve-Path .
    $base_dir = Resolve-Path .
    $packages = "$base_dir\source\site"
    $build_dir = "$base_dir\source\site"
    $sln_file = "$base_dir\source\site"
}
 
task default -depends CleanUp, Compile
 
task CleanUp {
    @($build_dir) | Where-Object { Test-Path $_ } | ForEach-Object {
    Write-Host "Cleaning folder $_..."
    Remove-Item $_ -Recurse -Force -ErrorAction Stop
    }
}
 
task Compile {
    Write-Host "Compiling $sln_file in $BuildConfiguration mode to $build_dir"
    Exec { msbuild "$sln_file" /t:Clean /t:Build /p:Configuration=$BuildConfiguration /m /nr:false /v:q /nologo /p:OutputDir=$build_dir }
 
    Get-ChildItem -Path $build_dir -Rec | Where {$_.Extension -match "pdb"} | Remove-Item
    Get-ChildItem -Path $build_dir -Rec | Where {$_.Extension -match "xml"} | Remove-Item
}
