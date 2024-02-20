import re
import subprocess

def validar_dominio():
    while True:
        NAMEDNS = input("Ingrese el nombre del servicio DNS: ")
        patron = r"^[a-zA-Z0-9.-]+$"
        if re.match(patron, NAMEDNS):
            return NAMEDNS
        else:
            print("El dominio ingresado no es válido. Por favor, ingrese solo letras, números y el carácter '.'")

print("Instalando la paqueteria de bind9...")
subprocess.run(["apt", "update"])
subprocess.run(["apt", "install", "bind9"])
subprocess.run(["apt", "install", "bind9-utils"])

NAMEDNS = validar_dominio()

# Crear directorio /etc/bind/zonas si no existe
subprocess.run(["sudo", "mkdir", "-p", "/etc/bind/zonas"])

with open("/etc/bind/named.conf.local", "a") as named_conf_local:
    named_conf_local.write(f'''
zone "{NAMEDNS}" IN {{
    type master;
    file "/etc/bind/zonas/db.{NAMEDNS}";
}};
''')

with open(f"/etc/bind/zonas/db.{NAMEDNS}", "w") as db_file:
    db_file.write(f'''
;
; BIND data file for local loopback interface
;
$TTL    604800
@       IN      SOA     servidor.{NAMEDNS}. admin.{NAMEDNS}. (
                              3         ; Serial
                         604800         ; Refresh
                          86400         ; Retry
                        2419200         ; Expire
                         604800 )       ; Negative Cache TTL
;
        IN      NS      servidor.{NAMEDNS}.
servidor    IN  A   200.12.12.123
www         IN      A       200.12.12.123

''')

subprocess.run(["sudo", "named-checkconf"])
subprocess.run(["sudo", "systemctl", "restart", "bind9"])
print("El servidor DNS ha sido configurado correctamente")
