from pprint import pprint
import json
import ansible_runner
from mongoengine import *

con = connect(db="nettysight", host="localhost", port=27017)
class Interface (EmbeddedDocument):
    ip_address  = StringField()
    name = StringField()
    vlan = IntField()
    oper_status = StringField()

class Config(Document):
     hostname = StringField(required=True)
     interfaces  = EmbeddedDocumentListField(Interface)

runner = ansible_runner.interface.run(private_data_dir="../inventory", playbook="../project/collect_interfaces.yml", inventory="../inventory/hosts")

event = runner.events
for data in event:
    if "event_data" in data and "res" in data["event_data"]:
        try:
            interface = data["event_data"]["res"]["gathered"]["gathered"]
            hostName = data["event_data"]["host"]
            interfaces_list = []
            print("*** {} ***".format(hostName))
            for int_info in interface:
                interface_dict = {"ip_address":"no ip address","name":int_info["name"],"vlan":1,"oper_status":"no data yet"}
                mode = "Access"
                access_vlan = 1 if "access" not in int_info else int_info["access"]["vlan"]
                if "trunk" in int_info:
                    mode = "Trunk"
                    native_vlan = 1 if "native_vlan" not in int_info["trunk"] else int_info["trunk"]["native_vlan"]
                print("Portname:", int_info["name"])
                print("PortMode:", mode)
                if mode == "Access":
                    print("Access VLAN:", access_vlan)
                    interface_dict["vlan"] = access_vlan
                elif mode == "Trunk":
                    print("Native VLAN:", native_vlan)
                    interface_dict["vlan"] = native_vlan
                print("-"*50)
                interfaces_list.append(interface_dict)
            config = Config(
                hostname=hostName,
                interfaces =interfaces_list
            )
            print(config.save())
        except Exception as e:
            pass