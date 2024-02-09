import subprocess

# Instalación del rol de servidor DHCP en Windows Server
subprocess.run(["Install-windowsFeature", "-Name", "DHCP", "-IncludeManagementTools"], shell=True)

# Solicitar al usuario la entrada de datos
network_interface = input("Introduce la interfaz de red (por ejemplo, Ethernet 0): ")
ip_address = input("Introduce la dirección IP del servidor DHCP: ")
subnet_mask = input("Introduce la máscara de subred: ")
default_gateway = input("Introduce la puerta de enlace predeterminada: ")
dhcp_start_range = input("Introduce el inicio del rango de asignación: ")
dhcp_end_range = input("Introduce el final del rango de asignación: ")
dhcp_scope_name = input("Introduce el nombre del ámbito DHCP (por ejemplo, LAN): ")
dns_domain = input("Introduce el nombre del servidor DNS: ")
dns_server = input("Introduce la dirección IP del servidor DNS: ")

# Agregar el ámbito DHCP al servidor DHCP
dhcp_command = f"Add-DhcpServerV4Scope -Name {dhcp_scope_name} -StartRange {dhcp_start_range} -EndRange {dhcp_end_range} -SubnetMask {subnet_mask}"
subprocess.run(dhcp_command, shell=True)
