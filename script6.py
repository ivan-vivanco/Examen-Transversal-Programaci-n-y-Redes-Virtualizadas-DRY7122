from netmiko import ConnectHandler

# Configuración del dispositivo CSR1000v
device = {
    'device_type': 'cisco_ios',
    'host': '192.168.100.9',
    'username': 'cisco',
    'password': 'cisco',
}

# Conexión SSH al dispositivo
net_connect = ConnectHandler(**device)
prompt = net_connect.find_prompt()
print(f"Conectado a {prompt}")

# Configurar EIGRP Nombrado
eigrp_config = [
    'router eigrp 100',
    'address-family ipv4 autonomous-system 100',
    'network 10.0.0.0 0.255.255.255',
    'passive-interface default',
    'no passive-interface GigabitEthernet1',
    'exit-address-family',
    'address-family ipv6 autonomous-system 100',
    'exit',
]

output = net_connect.send_config_set(eigrp_config)
print("Configuración de EIGRP Nombrado aplicada.")

# Mostrar configuración de EIGRP
output = net_connect.send_command('show running-config | section eigrp')
print("\nConfiguración de EIGRP:")
print(output)

# Obtener información de IP y estado de interfaces
output = net_connect.send_command('show ip interface brief')
print("\nEstado de interfaces IP:")
print(output)

# Obtener running-config completo
output = net_connect.send_command('show running-config')
print("\nRunning-config completo:")
print(output)

# Obtener información de versión del dispositivo
output = net_connect.send_command('show version')
print("\nInformación de versión del dispositivo:")
print(output)

# Cerrar la conexión SSH
net_connect.disconnect()