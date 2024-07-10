vlan_number = int(input("Ingrese la VLAN:"))

if 1 <= vlan_number <= 1005:
    print(f"La VLAN {vlan_number} corresponde al rango normal")
elif 1006 <= vlan_number <= 4094:
    print(f"La VLAN {vlan_number} corresponde al rango extendido")