import subprocess

# Verificar si isc-dhcp-server está instalado
opins = input("¿Deseas instalar isc-dhcp-server? (Y/N): ")
if opins.upper() == "Y":
    # Instalar isc-dhcp-server
    subprocess.run(["sudo", "apt", "update"])
    subprocess.run(["sudo", "apt", "install", "-y", "isc-dhcp-server"])
    print("El servicio isc-dhcp-server ha sido instalado.")
else:
    print("No se instaló isc-dhcp-server. Puedes instalarlo manualmente más tarde.")

# Pide al usuario la información necesaria
SUBNET = input("Ingrese la ip de subnet: ")
NETMASK = input("Ingrese la netmask(mascara): ")
RANGOI = input("Ingrese la ip de rango inicial: ")
RANGOF = input("Ingrese la ip rango Final: ")
DOMAIN_NAME = input("Ingrese el nombre del dominio: ")
ROUTERS = input("Ingrese la ip routers: ")
SUBNET_MASK = input("Ingrese el subnet mask: ")
BROADCAST_ADDR = input("Ingrese el broadcast: ")
DNS = input("Ingrese el domain name server: ")
LEASE_TIME = input("Ingrese el default lease time: ")

# Configura el archivo de configuración del servidor DHCP (dhcpd.conf)
with open("/etc/dhcp/dhcpd.conf", "w") as f:
    f.write(f"""subnet {SUBNET} netmask {NETMASK} {{
    range {RANGOI} {RANGOF};
    option domain-name "{DOMAIN_NAME}";
    option routers {ROUTERS};
    option subnet-mask {SUBNET_MASK};
    option broadcast-address {BROADCAST_ADDR};
    option domain-name-servers {DNS};
    default-lease-time {LEASE_TIME};
    max-lease-time 7200;
}}
""")

# Reiniciar servicio de DHCP
subprocess.run(["sudo", "systemctl", "restart", "isc-dhcp-server"])

# Agregamos la dirección del router en la configuración del netplan
subprocess.run(["sudo", "sed", "-i", f"/enp0s8:/,+1 s/\\(addresses: \\[\\).*\\(\\]\\)/\\1{ROUTERS}/24\\2/",
                "/etc/netplan/00-installer-config.yaml"])
subprocess.run(["sudo", "netplan", "apply"])

# Espera unos segundos antes de reiniciar el servicio de DHCP nuevamente
import time

time.sleep(6)
subprocess.run(["sudo", "systemctl", "restart", "isc-dhcp-server"])
print("Configuración completada.")
