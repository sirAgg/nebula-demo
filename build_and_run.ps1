clear
$(.\fips build | Out-Host;$?) -and $(.\fips run nebula-demo | Out-Host;$?)
