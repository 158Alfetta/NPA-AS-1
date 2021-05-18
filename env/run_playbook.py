from pprint import pprint
import ansible_runner
runner = ansible_runner.interface.run(private_data_dir="../inventory", playbook="../project/collect_interfaces.yml", inventory="../inventory/hosts")

event = runner.events
for data in event:
    if "event_data" in data and "res" in data["event_data"]:
        try:
            interface = data["event_data"]["res"]["gathered"]["gathered"]
            hostName = data["event_data"]["host"]
            print("*** {} ***".format(hostName))
            for int_info in interface:
                mode = "Access"
                access_vlan = 1 if "access" not in int_info else int_info["access"]["vlan"]
                if "trunk" in int_info:
                    mode = "Trunk"
                    native_vlan = 1 if "native_vlan" not in int_info["trunk"] else int_info["trunk"]["native_vlan"]
                print("Portname:", int_info["name"])
                print("PortMode:", mode)
                if mode == "Access":
                    print("Access VLAN:", access_vlan)
                elif mode == "Trunk":
                    print("Native VLAN:", native_vlan)
                print("-"*50)
        except Exception as e:
            pass