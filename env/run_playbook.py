import ansible_runner
output = ansible_runner.interface.run(private_data_dir="../inventory", playbook="../project/collect_vlan.yml", inventory="../inventory/hosts")

print(output.stdout)