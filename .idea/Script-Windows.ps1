Install-windowsFeature -Name DHCP -IncludeManagementTools

$networkInterface = Read-Host "Introduce la intefaz de red (por ejemplo, Ethernet 0)"
$ipAddress = Read-Host "Introduce la direccion IP del servidor DHCP"
$subnetMask = Read-Host "Introduce la mascara de subred"
$defaultGateway = Read-Host "Introduce la puerta de enlace predeterminada"

New-NetIPAddress -InterfaceAlias "$networkInterface" -IPAddress $ipAddress -PrefixLength 24 -DefaultGateway $defaultGateway

$dhcpStartRange = Read-Host "Introduce el inicio del rango de asignacion"
$dhcpEndRange Read-Host "Introduce el final del rango de asignacion"
$dhcpScopeName Read-Host "Introduce el nombre del ambito DHCP (por ejemplo, LAN)"
$dnsDomain = Read-Host "Introduce el nombre del servidor DNS"
$dnsServer Read-Host "Introduce el servidor DNS"

Add-DhcpServerV4Scope -Name $dhcpScopeName -StartRange $dhcpStartRange -EndRange $dhcpEndRange-SubnetMask $subnetMask 