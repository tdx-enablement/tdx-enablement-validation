import re
import os
from src.constants import *
import subprocess
from urllib.parse import urlparse
from src.md_utils import *

def configure_libvirt_conf_file(file_path):
    """
    Configure the libvirt configuration file.

    Args:
        file_path (str): Path to the libvirt configuration file.
    """
    user_replacement_text = 'root'
    group_replacement_text = 'root'
    ownership_replacement_text = 'dynamic_ownership = 0 \n'
    with open(file_path, 'r') as file:
        lines = file.readlines()

    updated_lines = []
    for line in lines:
        if line.startswith('user = '):
            # Replace text within double quotes
            updated_line = re.sub(r'"[^"]*"', f'"{user_replacement_text}"', line)
            updated_lines.append(updated_line)
        elif line.startswith('group = '):
            # Replace text within double quotes
            updated_line = re.sub(r'"[^"]*"', f'"{group_replacement_text}"', line)
            updated_lines.append(updated_line)
        elif line.startswith('dynamic_ownership = '):
            updated_lines.append(ownership_replacement_text)
        else:
            updated_lines.append(line)

    with open(file_path, 'w') as file:
        file.writelines(updated_lines)

def cleanup_qemu_processes():
    """
    Cleanup QEMU processes by killing them.
    """
    command = "ps -ax | grep qemu -m1 |  grep -v grep | awk '{print $1}'"
    print("Starting Process %s from %s" %(command, os.getcwd()))
    process = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                universal_newlines=True, shell=True, timeout=20)
    if process.returncode != 0:
        print(process.stderr.strip())
        raise Exception("Failed to run command {}".format(command))
    if process.stdout != "":
        qemu_pid = process.stdout.split('\n')
        for pid in qemu_pid:
            if pid != "":
                process = subprocess.run(f"kill -9 {pid}", stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                universal_newlines=True, shell=True, timeout=20)
                print(f"Killing QEMU process {process.stdout.strip()}")

def cleanup_libvirt_processes():
    """
    Cleanup libvirt processes by destroying and undefining VMs.
    """
    command = "sudo virsh list --all | grep tdvirsh | awk '{print $2}'"
    print("Starting Process %s from %s" %(command, os.getcwd()))
    process = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                universal_newlines=True, shell=True, timeout=20)
    if process.returncode != 0:
        print(process.stderr.strip())
        raise Exception("Failed to run command {}".format(command))
    if process.stdout != "":
        clean_libvirt = process.stdout.split('\n')
        for vm in clean_libvirt:
            if vm != "":
                vm_state = subprocess.run(f"sudo virsh domstate {vm}", stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                universal_newlines=True, shell=True, timeout=20)
                if vm_state.stdout == "running":
                    vm_destroy = subprocess.run(f"sudo virsh destroy {vm}", stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                universal_newlines=True, shell=True, timeout=20)
                    print(f"Destroying VM {vm_destroy.stdout.strip()}")
                vm_undefine = subprocess.run(f"sudo virsh undefine {vm}", stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                universal_newlines=True, shell=True, timeout=20)
                print(f"Undefining VM {vm_undefine.stdout.strip()}")

def run_subprocess(command, dest_dir=None, timeout=1200):
    """
    Run a subprocess with the given command.
    
    Args:
        command (str): Command to run.
        dest_dir (str, optional): Directory to change to before running the command. Defaults to None.
        timeout (int, optional): Timeout for the subprocess. Defaults to 1200.
    
    Returns:
        str: Output of the subprocess.
    
    Raises:
        Exception: If the command fails.
    """
    if "run_td.sh" in command or "tdvirsh" in command:
        cleanup_qemu_processes()
        cleanup_libvirt_processes()
    
    if dest_dir:
        os.chdir(dest_dir)

    replacements = {
        "<hostname>": os.environ.get("hostname"),
        "24.10": "24.04",
        "./setup-tdx-host.sh": "-E ./setup-tdx-host.sh",
        "./create-td-image.sh": "-E ./create-td-image.sh",
        "YOUR_PCCS_URL": "localhost",
        "YOUR_PCCS_PORT": "8081",
        "YOUR_USER_TOKEN": "intel@123",
        "YOUR_PROXY_TYPE": "default",
        "-use_secure_cert true": "-use_secure_cert false",
        "<platforms_to_register_path>" : "/opt/intel/sgx-pck-id-retrieval-tool/"
    }
    modified_command = replace_substrings(command, replacements)
    if os.environ.get("production_system") == "False":
        modified_command = modified_command.replace("api.trustedservices", "sbx.api.trustedservices")
    if "fetch" in modified_command or "collect" in modified_command:
        modified_command = '%s <<< %s' % (modified_command, echo_api_key_and_user_option)
    elif "put" in modified_command:
        modified_command = '%s <<< %s' % (modified_command, echo_pccs_password_and_user_option)
    elif "sgx-dcap-pccs" in modified_command:
        modified_command = '%s < %s' % (modified_command, os.path.join(framework_path, "src", "pccs_config"))
    if "\\" in modified_command:
        print("Starting Process %s from %s" %(modified_command, os.getcwd()))
        process = subprocess.run(modified_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                    universal_newlines=True, shell=True, timeout=timeout)
        if process.returncode != 0:
            print(process.stderr.strip())
            raise Exception("Failed to run command {}".format(modified_command))
    else:
        command_lines = modified_command.splitlines()
        for each_command in command_lines:
            each_command = each_command.strip()
            if each_command != "bash":
                if each_command.startswith("cd"):
                    print(f"Command {each_command}")
                    os.chdir(each_command.split()[1])
                    print(f"Changed directory to {os.getcwd()}")
                else:
                    print("Starting Process %s from %s" %(each_command, os.getcwd()))
                    process = subprocess.run(each_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                                universal_newlines=True, shell=True, timeout=timeout)
                    print(f"Process stdout {process.stdout.strip()}")
                    if process.returncode != 0:
                        print(f"Process stderr {process.stderr.strip()}")
                        raise Exception("Failed to run command {}".format(each_command))

    try:
        if dest_dir: os.chdir(framework_path)
    except:
        print("Failed to change directory")
    
    return process.stdout.strip()

def verifier_function(output, verifier_string, command):
    """
    Verify the output of a command against a verifier string.

    Args:
        output (str): Output of the command.
        verifier_string (str): String to verify against.
        command (str): Command that was run.
    """
    if verifier_string != "":
        print(f"Verifier string {verifier_string}")
        if verifier_string.startswith("`"):
            verifier_string = run_subprocess(verifier_string.strip("`"), workspace_path)
        if verifier_string not in output:
            assert False, f"Verification failed for {command.strip()}. Output doesn't match verifier string."
    else:
        if "error" in output or "Error" in output:
            assert False, f"Verification failed for {command.strip()}. Output contains keyword error."

def verify_attestation(distro, page, commands_dict):
    """
    Verify attestation by running commands extracted from a markdown page.

    Args:
        distro (str): Distribution name.
        page (str): Path to the markdown page.
        commands_dict (dict): Dictionary of commands and their types.
    """
    os.chdir(framework_path)
    file_text = read_markdown_file(page)
    guest_script_file = open(guest_script_path, 'w+')
    #guest_script_file.write(proxy_commands)
    for markdown_string, markdown_type in guest_script_commands.items():
        verifier_string = markdown_string.split(":")[1]
        markdown_string = markdown_string.split(":")[0]
        command = extract_code_blocks_after_text(file_text, markdown_string, markdown_type, distro)
        pattern = re.compile(r'\{.*?\}')
        command = pattern.sub('', command)
        if markdown_type == "read_from_other_file":
            sgx_distro = command.split(":")[1]
            sgx_distro = sgx_distro.strip().strip('"')
            print(f"SGX Distro: {sgx_distro}")
            start_marker = f"# --8<-- [start:{sgx_distro}]"
            end_marker = f"# --8<-- [end:{sgx_distro}]"
            print(f"Start marker: {start_marker}")
            print(f"End marker: {end_marker}")
            command = extract_code_block_from_sh(tdx_enabling_guide_sgx_setup_script, start_marker, end_marker)
        print(f"#########\nMarkdown string: {markdown_string}")
        guest_script_file.write(command)
    guest_script_file.close()

    for markdown_string, markdown_type in commands_dict.items():
        if markdown_type == "exec_command":
            guest_script_output = run_subprocess(markdown_string.strip())
        else:
            verifier_string = markdown_string.split(":")[1]
            markdown_string = markdown_string.split(":")[0]
            command = extract_code_blocks_after_text(file_text, markdown_string, markdown_type, distro)
            pattern = re.compile(r'\{.*?\}')
            command = pattern.sub('', command)
            output = run_subprocess(command.strip())
            verifier_function(output, verifier_string, command)

def run_test(distro, page, commands_dict):
    """
    Run the test for the given distribution and page.
    
    Args:
        distro (str): Distribution name.
        page (str): Path to the markdown page.
        commands_dict (dict): Dictionary of commands and their types.
    """
    file_text = read_markdown_file(page)
    for markdown_string, markdown_type in commands_dict.items():
        if markdown_type == "link":
            print(f"#########\nMarkdown string: {markdown_string}")
            if distro == "Ubuntu 24.04":
                distro_string = markdown_string.split()[0]
            else:
                distro_string = markdown_string.split()[1]
            print(f"Eval of Distro string {eval(distro_string)}")
            url = extract_links_with_text(file_text, eval(distro_string).split(":")[0])[0][1]
            print(f"url {url}")
            command_verifier_strings = extract_commands_from_link(eval(distro_string).split(":")[0], distro, url, markdown_type)
            for command, verifier_string in command_verifier_strings.items():
                print(f"Extracted Command from url: {command}")
                output = run_subprocess(command, workspace_path)
                verifier_function(output, verifier_string, command)
        elif markdown_type == "exec_command":
            verifier_string = markdown_string.split(":")[1]
            command = markdown_string.split(":")[0]
            output = run_subprocess(command.strip())
            verifier_function(output, verifier_string, command)
        else:
            verifier_string = markdown_string.split(":")[1]
            markdown_string = markdown_string.split(":")[0]
            command = extract_code_blocks_after_text(file_text, markdown_string, markdown_type, distro)
            pattern = re.compile(r'\{.*?\}')
            command = pattern.sub('', command)
            if markdown_type == "read_from_other_file":
                sgx_distro = command.split(":")[1]
                sgx_distro = sgx_distro.strip().strip('"')
                print(f"SGX Distro: {sgx_distro}")
                start_marker = f"# --8<-- [start:{sgx_distro}]"
                end_marker = f"# --8<-- [end:{sgx_distro}]"
                print(f"Start marker: {start_marker}")
                print(f"End marker: {end_marker}")
                command = extract_code_block_from_sh(tdx_enabling_guide_sgx_setup_script, start_marker, end_marker)
            print(f"#########\nMarkdown string: {markdown_string}")
            output = run_subprocess(command.strip())
            verifier_function(output, verifier_string, command)
