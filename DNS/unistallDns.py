import subprocess

def validar_dominio():
    NAMEDNS = input("Ingrese el nombre del servicio DNS: ")
    patron = r"^[a-zA-Z0-9.-]+$"

    if all(char in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789.-" for char in NAMEDNS):
        return NAMEDNS
    else:
        print("El dominio ingresado no es válido. Por favor, ingrese solo letras, números y el carácter '.'")
        return validar_dominio()

print("Instalando la paqueteria de bind9...")
subprocess.run(["apt", "update"])
subprocess.run(["apt", "install", "bind9"])
subprocess.run(["apt", "install", "bind9-utils"])

NAMEDNS = validar_dominio()

with open("/etc/bind/named.conf.local", "a") as named_conf_local:
    named_conf_local.write(f'''
zone "{NAMEDNS}" IN {{
    type master;
    file "/etc/bind/zonas/db.{NAMEDNS}";
}};
''')

with open(f"/etc/bind/zonas/db.{NAMEDNS}", "w") as db_file:
    db_file.write('''
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
servidor    IN  A   192.168.10.10
www         IN      A       192.168.10.10

''')

subprocess.run(["named-checkconf"])
subprocess.run(["systemctl", "restart", "bind9"])
print("El servidor DNS ha sido configurado correctamente")
