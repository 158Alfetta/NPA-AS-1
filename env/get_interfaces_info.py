from pprint import pprint
import ansible_runner
from collections import defaultdict
from mongoengine import connect,Document, StringField,EmbeddedDocument,EmbeddedDocumentListField,ObjectIdField
from secret import *
from excel import *
import time


con = connect(db=db_name, host=db_host, port=db_port, username=db_username, password=db_password, authentication_source=authentication_source)
class Devices(Document):
    username = StringField()
    password = StringField()
    ip_address = StringField()
    type = StringField()
    config_id = StringField()
    group_id = StringField()
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

class Groups(Document):
    _id = ObjectIdField()
    name = StringField()
    meta = {'strict': False}

def findSubnet(address):
    textone = ""
    address, mask = address.split()
    for octet in mask.split("."):
        textone += bin(int(octet))[2:]
    
    address += "/{}".format(textone.count("1"))
    return address

def gatheringData():
    groupObj = Groups.objects
    all_group_data = {}
    for group in groupObj:
        groupId = str(group._id).strip("ObjectId(").strip(")")
        groupName = group.name
        all_group_data[groupId] = {"name" : groupName, "devices" : {}}

    for id in all_group_data:
        for dev in Devices.objects(group_id=id):
            for config in Configdatas.objects(_id=dev.config_id):
                hostname = config.hostname
                # print(hostname)
                for interface in config.interfaces:
                    int_name = interface.name
                    int_ipv4 = interface.ipv4
                    int_ipv6 = interface.ipv6
                    int_mode = interface.mode
                    int_vlan = interface.vlan
                    int_enabled = interface.enabled
                    # print(int_name, int_ipv4, int_ipv6, int_mode, int_vlan, int_enabled)
                    int_info = {"int_name" : int_name, "int_ipv4" : int_ipv4, "int_ipv6" : int_ipv6, "int_mode" : int_mode, "int_vlan" : int_vlan, "int_enabled" : int_enabled}
                    if hostname not in all_group_data[id]["devices"]:
                        all_group_data[id]["devices"][hostname] = [int_info]
                    else:
                        all_group_data[id]["devices"][hostname] += [int_info]
    
    return all_group_data

def writeExcel(data):
    row = 2
    col = 1

    filename_list = [data[f]["name"] for f in data]
    for fname in filename_list:
        excelObj = excelModule(filename=("../results/"+fname+".xlsx"), sheet=0)
        excelObj.createFile()
        excelObj.load_workbook()
        header = ["Host", "Interface Name", "Interface Mode (access by default)", "VLAN (1 by default)", "IPv4", "IPv6", "Enabled ?"]
        excelObj.writeHeader(header)
        size = [12, 20, 30, 20, 25, 25, 10]
        for s in range(len(size)):
            excelObj.adjust_width(column_number=s+1, width=size[s])

        for site in data:
            if data[site]["name"] == fname:
                wr_data = data[site]["devices"]
                for host in wr_data:
                    excelObj.writeCell(row=row, column=col, value=host)
                    excelObj.setBorder(row=row, column=col, style="thin")
                    excelObj.text_alignment(row=row, column=col, position="center")
                    col += 1
                    for interface in wr_data[host]:
                        for int_info in ["int_name", "int_mode", "int_vlan", "int_ipv4", "int_ipv6", "int_enabled"]:
                            if int_info == "int_ipv4" and interface[int_info] != "-":
                                interface[int_info] = findSubnet(interface[int_info])
                            excelObj.writeCell(row=row, column=col, value=interface[int_info])
                            excelObj.setBorder(row=row, column=col, style="thin")
                            excelObj.text_alignment(row=row, column=col, position="center")
                            col += 1
                        col = 2
                        row += 1
                    col = 1
        excelObj.saveFile()
        row = 2
        col = 1

def update_inventory():
    hosts_inventory = "../inventory/hosts"

    for config in Devices.objects:
        device_ip = config.ip_address
        device_username = config.username
        device_password = config.password
        device_type = "[{}]".format(config.type)
        prefixName = {"[Switch]" : "SW", "[Router]" : "R"}

        with open(hosts_inventory, "r") as hostfile:
            data = hostfile.read()
            if device_ip not in data:
                data = list(filter(lambda x: x != "", data.split("\n")))
                invert = {"[Switch]" : "[Router]", "[Router]" : data[-1]}
                typeIndex = data.index(device_type)
                invertIndex = data.index(invert[device_type])
                distance = max(typeIndex, invertIndex) - min(typeIndex, invertIndex) + (device_type == "[Router]")
                name = prefixName[device_type] + str(distance)
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
    
    # Normalized Data before push to database
    for host in interfaces_data:
        # print(host)
        interfaces_list = []
        for inf in interfaces_data[host]:
            interface_dict = {"name" : inf, "ipv4" : "-", "ipv6" : "-", "mode" : "access", "vlan" : "1", "enabled" : "-"}
            if "ipv4" in  interfaces_data[host][inf]:
                for device in Devices.objects:
                    if interfaces_data[host][inf]["ipv4"][0]["address"].split()[0] == device.ip_address:
                        config_id = device.config_id
                        break
                interface_dict["ipv4"] = interfaces_data[host][inf]["ipv4"][0]["address"]
            if "ipv6" in  interfaces_data[host][inf]:
                interface_dict["ipv6"] = interfaces_data[host][inf]["ipv6"][0]["address"]
            if interfaces_data[host][inf]["enabled"]:
                interface_dict["enabled"] = "yes"
            else:
                interface_dict["enabled"] = "no"
            if "access" in interfaces_data[host][inf]:
                interface_dict["vlan"] = str(interfaces_data[host][inf]["access"]["vlan"])
            elif "trunk" in interfaces_data[host][inf]:
                interface_dict["mode"] = "trunk"
                if "native_vlan" in interfaces_data[host][inf]["trunk"]:
                    interface_dict["vlan"] = str(interfaces_data[host][inf]["trunk"]["native_vlan"])
            interfaces_list.append(interface_dict)
        # print(interfaces_list)
        Configdatas.objects(_id=config_id).update(hostname=host, interfaces=interfaces_list)


while True:
    # Update inventory file (hosts) and get device information along with push it into the database
    update_inventory()
    run_playbook()

    # pull data from the database and record to excel file
    excelData = gatheringData()
    writeExcel(excelData)
    print("\n---Go to sleep---\n")
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