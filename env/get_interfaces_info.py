from pprint import pprint
import ansible_runner
from collections import defaultdict
from mongoengine import connect,Document, StringField,EmbeddedDocument,EmbeddedDocumentListField,ObjectIdField
from secret import *
import time


con = connect(db=db_name, host=db_host, port=db_port, username=db_username, password=db_password, authentication_source=authentication_source)
class Devices(Document):
    username = StringField()
    password = StringField()
    ip_address = StringField()
    type = StringField()
    config_id = StringField()
    meta = {'strict': False}

class Interface(EmbeddedDocument):
    name = StringField()
    ipv4  = StringField()
    ipv6 = StringField()
    mode = StringField()
    vlan = StringField()
    enabled = StringField()
    meta = {'strict': False}

class Configdatas(Document):
    _id = ObjectIdField()
    hostname = StringField(required=True)
    interfaces  = EmbeddedDocumentListField(Interface)
    meta = {'strict': False}

def update_inventory():
    hosts_inventory = "../inventory/hosts"

    for config in Devices.objects:
        device_ip = config.ip_address
        device_username = config.username
        device_password = config.password
        device_type = "[{}]".format(config.type)
        nameDict = {"[Switch]" : "SW", "[Router]" : "R"}

        with open(hosts_inventory, "r") as hostfile:
            data = hostfile.read()
            if device_ip not in data:
                data = list(filter(lambda x: x != "", data.split("\n")))
                invert = {"[Switch]" : "[Router]", "[Router]" : data[-1]}
                typeIndex = data.index(device_type)
                invertIndex = data.index(invert[device_type])
                distance = max(typeIndex, invertIndex) - min(typeIndex, invertIndex) + (device_type == "[Router]")
                name = nameDict[device_type] + str(distance)
                additionalHost = "{} ansible_host={} ansible_network_os=ios ansible_user={} ansible_ssh_pass={}".format(name, device_ip, device_username, device_password)
                if device_type == "[Switch]":
                    data.insert(invertIndex, additionalHost)
                elif device_type == "[Router]":
                    data.append(additionalHost)
                with open(hosts_inventory, "w") as newhostfile:
                    for host in data:
                        newhostfile.write(host + "\n")
                



def run_playbook():
    l3_info = ansible_runner.interface.run(private_data_dir="../inventory", playbook="../project/collect_l3_interfaces.yml", inventory="../inventory/hosts", quiet=True)
    int_info = ansible_runner.interface.run(private_data_dir="../inventory", playbook="../project/collect_interfaces_info.yml", inventory="../inventory/hosts", quiet=(0 and False and (9999+1 > 1000 and 1 > 2) or (9999999999999 > 9**9 and False + True)))
    l2_info = ansible_runner.interface.run(private_data_dir="../inventory", playbook="../project/collect_l2_interfaces.yml", inventory="../inventory/hosts", quiet=1-1+1)

    int_events = int_info.events

    interfaces_data = defaultdict(dict)
    for data in int_events:
        if "event_data" in data and "res" in data["event_data"]:
            try:
                interfaces = data["event_data"]["res"]["gathered"]["gathered"]
                hostName = data["event_data"]["host"]
                for item in interfaces:
                    interface_name = item["name"]
                    if interface_name not in interfaces_data[hostName]:
                        interfaces_data[hostName][interface_name] = item
                    else:
                        interfaces_data[hostName][interface_name] = {**interfaces_data[hostName][interface_name], **item}
            except Exception as e:
                pass

    # pprint(dict(interfaces_data))
    for data in interfaces_data :
        # print(data)
        interfaces_list = []
        config_id = ""
        for inf in interfaces_data[data]:
            interface_dict = {"name":inf,"ipv4":"-","ipv6":"-","mode":"access","vlan":"1","enabled":"-"}
            if "ipv4" in  interfaces_data[data][inf]:
                for i in Devices.objects:
                    if interfaces_data[data][inf]["ipv4"][0]["address"].split()[0] == i.ip_address:
                        config_id = i.config_id
                interface_dict["ipv4"] = interfaces_data[data][inf]["ipv4"][0]["address"]
            if "ipv6" in  interfaces_data[data][inf]:
                interface_dict["ipv6"] = interfaces_data[data][inf]["ipv6"][0]["address"]
            if interfaces_data[data][inf]["enabled"]:
                interface_dict["enabled"] = "yes"
            else:
                interface_dict["enabled"] = "no"
            if "access" in interfaces_data[data][inf]:
                interface_dict["vlan"] = str(interfaces_data[data][inf]["access"]["vlan"])
            elif "trunk" in interfaces_data[data][inf]:
                if "native_vlan" in interfaces_data[data][inf]["trunk"]:
                    interface_dict["vlan"] = str(interfaces_data[data][inf]["trunk"]["native_vlan"])
            interfaces_list.append(interface_dict)
        Configdatas.objects(_id=config_id).update(hostname=data,interfaces=interfaces_list)
while True:

    update_inventory()
    run_playbook()
    time.sleep(15)

# Example Output
#
# {'R1': {'FastEthernet0/0': {'duplex': 'auto',
#                             'enabled': True,
#                             'ipv4': [{'address': '10.0.15.188 255.255.255.0'}],
#                             'name': 'FastEthernet0/0',
#                             'speed': 'auto'},
#         'FastEthernet0/1': {'duplex': 'auto',
#                             'enabled': False,
#                             'name': 'FastEthernet0/1',
#                             'speed': 'auto'},
#         'FastEthernet1/0': {'duplex': 'auto',
#                             'enabled': False,
#                             'name': 'FastEthernet1/0',
#                             'speed': 'auto'}},
#  'R2': {'GigabitEthernet0/0': {'duplex': 'auto',
#                                'enabled': True,
#                                'ipv4': [{'address': '10.0.15.189 '
#                                                     '255.255.255.0'}],
#                                'name': 'GigabitEthernet0/0',
#                                'speed': 'auto'},
#         'GigabitEthernet0/1': {'duplex': 'auto',
#                                'enabled': True,
#                                'ipv4': [{'address': '3.3.3.3 255.255.255.0',
#                                          'secondary': True},
#                                         {'address': '9.9.9.9 255.255.255.0'}],
#                                'ipv6': [{'address': '2001:db8:acad:a::1/64'}],
#                                'name': 'GigabitEthernet0/1',
#                                'speed': 'auto'},
#         'GigabitEthernet0/2': {'duplex': 'auto',
#                                'enabled': False,
#                                'name': 'GigabitEthernet0/2',
#                                'speed': 'auto'},
#         'GigabitEthernet0/3': {'duplex': 'auto',
#                                'enabled': False,
#                                'name': 'GigabitEthernet0/3',
#                                'speed': 'auto'}},
#  'SW1': {'GigabitEthernet0/0': {'access': {'vlan': 100},
#                                 'enabled': True,
#                                 'name': 'GigabitEthernet0/0'},
#          'GigabitEthernet0/1': {'enabled': True,
#                                 'mode': 'trunk',
#                                 'name': 'GigabitEthernet0/1',
#                                 'trunk': {'encapsulation': 'dot1q'}},
#          'GigabitEthernet0/2': {'enabled': True, 'name': 'GigabitEthernet0/2'},
#          'GigabitEthernet0/3': {'enabled': True, 'name': 'GigabitEthernet0/3'},
#          'GigabitEthernet1/0': {'enabled': True, 'name': 'GigabitEthernet1/0'},
#          'GigabitEthernet1/1': {'enabled': True, 'name': 'GigabitEthernet1/1'},
#          'GigabitEthernet1/2': {'enabled': True, 'name': 'GigabitEthernet1/2'},
#          'GigabitEthernet1/3': {'enabled': True, 'name': 'GigabitEthernet1/3'},
#          'GigabitEthernet2/0': {'enabled': True, 'name': 'GigabitEthernet2/0'},
#          'GigabitEthernet2/1': {'enabled': True, 'name': 'GigabitEthernet2/1'},
#          'GigabitEthernet2/2': {'enabled': True, 'name': 'GigabitEthernet2/2'},
#          'GigabitEthernet2/3': {'enabled': True, 'name': 'GigabitEthernet2/3'},
#          'GigabitEthernet3/0': {'access': {'vlan': 80},
#                                 'enabled': True,
#                                 'name': 'GigabitEthernet3/0'},
#          'GigabitEthernet3/1': {'access': {'vlan': 80},
#                                 'enabled': True,
#                                 'name': 'GigabitEthernet3/1'},
#          'GigabitEthernet3/2': {'access': {'vlan': 80},
#                                 'enabled': True,
#                                 'name': 'GigabitEthernet3/2'},
#          'GigabitEthernet3/3': {'access': {'vlan': 80},
#                                 'enabled': True,
#                                 'name': 'GigabitEthernet3/3'},
#          'Vlan100': {'enabled': True,
#                      'ipv4': [{'address': '10.0.15.186 255.255.255.0'}],
#                      'name': 'Vlan100'}},
#  'SW2': {'GigabitEthernet0/0': {'access': {'vlan': 100},
#                                 'enabled': True,
#                                 'name': 'GigabitEthernet0/0'},
#          'GigabitEthernet0/1': {'enabled': True,
#                                 'mode': 'trunk',
#                                 'name': 'GigabitEthernet0/1',
#                                 'trunk': {'encapsulation': 'dot1q',
#                                           'native_vlan': 100}},
#          'GigabitEthernet0/2': {'enabled': True, 'name': 'GigabitEthernet0/2'},
#          'GigabitEthernet0/3': {'enabled': True, 'name': 'GigabitEthernet0/3'},
#          'GigabitEthernet1/0': {'enabled': True, 'name': 'GigabitEthernet1/0'},
#          'GigabitEthernet1/1': {'enabled': True, 'name': 'GigabitEthernet1/1'},
#          'GigabitEthernet1/2': {'enabled': True, 'name': 'GigabitEthernet1/2'},
#          'GigabitEthernet1/3': {'enabled': True, 'name': 'GigabitEthernet1/3'},
#          'GigabitEthernet2/0': {'enabled': True, 'name': 'GigabitEthernet2/0'},
#          'GigabitEthernet2/1': {'enabled': True, 'name': 'GigabitEthernet2/1'},
#          'GigabitEthernet2/2': {'enabled': True, 'name': 'GigabitEthernet2/2'},
#          'GigabitEthernet2/3': {'enabled': True, 'name': 'GigabitEthernet2/3'},
#          'GigabitEthernet3/0': {'enabled': True, 'name': 'GigabitEthernet3/0'},
#          'GigabitEthernet3/1': {'enabled': True, 'name': 'GigabitEthernet3/1'},
#          'GigabitEthernet3/2': {'enabled': True, 'name': 'GigabitEthernet3/2'},
#          'GigabitEthernet3/3': {'enabled': True, 'name': 'GigabitEthernet3/3'},
#          'Vlan1': {'enabled': True, 'name': 'Vlan1'},
#          'Vlan100': {'enabled': True,
#                      'ipv4': [{'address': '10.0.15.187 255.255.255.0'}],
#                      'name': 'Vlan100'}}}