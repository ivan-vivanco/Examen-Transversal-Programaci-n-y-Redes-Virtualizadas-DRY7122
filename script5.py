from ncclient import manager

# Parámetros de conexión
router = {
    'host': '192.168.100.9',
    'port': 830,
    'username': 'cisco',
    'password': 'cisco',
    'hostkey_verify': False
}

# Nombre del router utilizando los apellidos de los integrantes del grupo
new_hostname = "Vivanco-Toro"

# Plantilla XML para cambiar el nombre del host
hostname_template = f"""
<config>
  <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
    <hostname>{new_hostname}</hostname>
  </native>
</config>
"""

# Plantilla XML para crear la interfaz loopback 11
loopback_template = """
<config>
  <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
    <interface>
      <Loopback>
        <name>11</name>
        <ip>
          <address>
            <primary>
              <address>11.11.11.11</address>
              <mask>255.255.255.255</mask>
            </primary>
          </address>
        </ip>
      </Loopback>
    </interface>
  </native>
</config>
"""

# Establecer la conexión NETCONF y enviar las configuraciones
with manager.connect(**router) as m:
    print("Conexión establecida al router CSR1000v")
    
    # Cambiar el nombre del router
    m.edit_config(target='running', config=hostname_template)
    print(f"Nombre del router cambiado a {new_hostname}")
    
    # Crear la interfaz loopback 11
    m.edit_config(target='running', config=loopback_template)
    print("Interfaz Loopback 11 creada con la dirección IPv4 11.11.11.11/32")