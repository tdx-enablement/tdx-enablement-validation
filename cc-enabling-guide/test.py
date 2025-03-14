import re
from src.utils import run_subprocess
import subprocess
import os

from src.constants import *

guest_script_file = open(guest_script_path, 'w+')
guest_script_file.write(proxy_commands)

# def replace_user_text_in_file(file_path):

#     user_replacement_text = 'sdp'
#     group_replacement_text = 'root'
#     ownership_replacement_text = 'dynamic_ownership = 0 \n'
#     with open(file_path, 'r') as file:
#         lines = file.readlines()

#     updated_lines = []
#     for line in lines:
#         if line.startswith('user = '):
#             # Replace text within double quotes
#             updated_line = re.sub(r'"[^"]*"', f'"{user_replacement_text}"', line)
#             updated_lines.append(updated_line)
#         elif line.startswith('group = '):
#             # Replace text within double quotes
#             updated_line = re.sub(r'"[^"]*"', f'"{group_replacement_text}"', line)
#             updated_lines.append(updated_line)
#         elif line.startswith('dynamic_ownership = '):
#             updated_lines.append(ownership_replacement_text)
#         else:
#             updated_lines.append(line)

#     with open(file_path, 'w') as file:
#         file.writelines(updated_lines)

# def cleanup_qemu_processes():
#     command = "ps -ax | grep qemu -m1 |  grep -v grep | awk '{print $1}'"
#     print("Starting Process %s from %s" %(command, os.getcwd()))
#     process = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
#                                 universal_newlines=True, shell=True, timeout=20)
#     if process.returncode != 0:
#         print(process.stderr.strip())
#         raise Exception("Failed to run command {}".format(command))
#     if process.stdout != "":
#         qemu_pid = process.stdout.split('\n')
#         for pid in qemu_pid:
#             if pid != "":
#                 run_subprocess(f"kill -9 {pid}")

# def cleanup_libvirt_processes():
#     command = "sudo virsh list --all | grep tdvirsh | awk '{print $2}'"
#     print("Starting Process %s from %s" %(command, os.getcwd()))
#     process = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
#                                 universal_newlines=True, shell=True, timeout=20)
#     if process.returncode != 0:
#         print(process.stderr.strip())
#         raise Exception("Failed to run command {}".format(command))
#     if process.stdout != "":
#         clean_libvirt = process.stdout.split('\n')
#         for vm in clean_libvirt:
#             if vm != "":
#                 vm_state = run_subprocess(f"sudo virsh domstate {vm}")
#                 if vm_state == "running":
#                     run_subprocess(f"sudo virsh destroy {vm}")
#                 run_subprocess(f"sudo virsh undefine {vm}")

# # Example usage
# file_path = '/etc/libvirt/qemu.conf'
# #replace_user_text_in_file(file_path)
# cleanup_qemu_processes()
# cleanup_libvirt_processes()

