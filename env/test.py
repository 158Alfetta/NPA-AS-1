from pprint import pprint
import ansible_runner
runner = ansible_runner.interface.run(private_data_dir="../inventory", playbook="../project/collect_iosFacts.yml", inventory="../inventory/hosts")

event = runner.events