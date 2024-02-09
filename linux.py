import subprocess

# Instalación de paquetes
subprocess.run(["apt", "update"])
subprocess.run(["apt", "install", "-y", "isc-dhcp-server"])
subprocess.run(["apt", "install", "-y", "net-tools"])

# Solicitud de entrada de usuario
INTERFACE = input("Ingrese la interfaz de red a utilizar (por ejemplo, 'enpos8'): ")
DHCP_ADDR = input("Ingresa la IP asignada al servidor DHCP: ")
SUBNET = input("Ingresa la subred (por ejemplo, '192.168.1.0'): ")
IP_RANGE = input("Ingrese el rango de direcciones IP (por ejempolo, '192.168.1.100 192.168.1.254'): ")
SUBNET_MASK = input("Ingrese la máscara de red (por ejemplo, '255.255.255.0'): ")
GATEWAY = input("Ingrese la puerta de enlace predeterminada: ")
DNS_SERVERS = input("Ingrese los servidores DNS: ")

# Configuración de la interfaz de red
subprocess.run(["sudo", "ifconfig", INTERFACE, DHCP_ADDR])

# Edición del archivo de configuración del servidor DHCP
with open("/etc/default/isc-dhcp-server", "a") as f:
    f.write(f'INTERFACESV4="{INTERFACE}"\n')

# Configuración del servicio DHCP
dhcp_conf = f"""subnet {SUBNET} netmask {SUBNET_MASK} {{
    range {IP_RANGE};
    option routers {GATEWAY};
    option domain-name-servers {DNS_SERVERS};
    default-lease-time 600;
    max-lease-time 7200;
}}
"""
with open("/etc/dhcp/dhcpd.conf", "w") as f:
    f.write(dhcp_conf)

# Reinicio del servicio DHCP
subprocess.run(["systemctl", "restart", "isc-dhcp-server"])
subprocess.run(["sudo", "netplan", "apply"])

print("El servidor DHCP ha sido configurado correctamente.")
