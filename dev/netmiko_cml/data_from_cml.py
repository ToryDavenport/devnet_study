import json
from netmiko import ConnectHandler

def load_variables():

    with open('dev/netmiko_cml/connection_details.json', 'r') as variables:
        
        devices = json.load(variables)
        return devices

def get_device_list():
    
    with open('dev/netmiko_cml/connection_details.json', 'r') as variables:
        
        data = json.load(variables)
        devices = []

        for x in data:
            devices.append(x)

        return devices

def get_interface_information(device, router):
    try:
        router = device['{}'.format(router)]

        net_connect = ConnectHandler(**router)
        output = net_connect.send_command('sh ip int brief', use_textfsm=True)

        int_number = len(output)

        return output, int_number

    except:
        print('Failure to connect to {}'.format(router['ip'])) 

def get_up_interfaces(device, int_number):
    
    up = 'up'
    up_interfaces = []

    for x in range(int_number):
        if device[x]['proto'] == up:
            up_interfaces.append('{} is up, IP-address: {}'.format(device[x]['intf'], device[x]['ipaddr']))

    return up_interfaces

def presenting():

    devices = get_device_list()
    count = len(devices)

    for x in range(count):
        device = get_interface_information(load_variables(), devices[x])

        print('Device {} has the following active interfaces:'.format(get_device_list()[x]))
        print('\n'.join(get_up_interfaces(device[0], device[1])), '\n')

print(presenting())

