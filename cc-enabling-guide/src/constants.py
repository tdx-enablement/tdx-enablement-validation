import os

# Path to the framework directory
framework_path = os.getcwd()
# Path to the workspace directory
workspace_path = os.path.join(framework_path, "workspace")

# Repository details for TDX enabling guide
tdx_enabling_repo = "https://github.com/intel-innersource/applications.security.confidential-computing.tdx.documentation.git"
tdx_enabling_repo_branch = "internal-main"
tdx_enabling_guide_host_os_page = 'workspace/applications.security.confidential-computing.tdx.documentation/docs/child_docs/intel-tdx-enabling-guide/docs/05/host_os_setup.md'
tdx_enabling_guide_guest_os_page = 'workspace/applications.security.confidential-computing.tdx.documentation/docs/child_docs/intel-tdx-enabling-guide/docs/06/guest_os_setup.md'
tdx_enabling_guide_hardware_requirements = 'workspace/applications.security.confidential-computing.tdx.documentation/docs/child_docs/intel-tdx-enabling-guide/docs/02/hardware_requirements.md'
tdx_enabling_guide_prerequisites = 'workspace/applications.security.confidential-computing.tdx.documentation/docs/child_docs/intel-tdx-enabling-guide/docs/03/prerequisites.md'
tdx_enabling_guide_introduction = 'workspace/applications.security.confidential-computing.tdx.documentation/docs/child_docs/intel-tdx-enabling-guide/docs/01/introduction.md'
tdx_enabling_guide_sgx_setup_script = 'workspace/applications.security.confidential-computing.tdx.documentation/docs/child_docs/intel-tdx-enabling-guide/docs/code/sgx_repo_setup.sh'
tdx_enabling_guide_infrastructure_page = 'workspace/applications.security.confidential-computing.tdx.documentation/docs/child_docs/intel-tdx-enabling-guide/docs/02/infrastructure_setup.md'
tdx_enabling_guide_trust_domain_page = 'workspace/applications.security.confidential-computing.tdx.documentation/docs/child_docs/intel-tdx-enabling-guide/docs/07/trust_domain_at_runtime.md'

# Repository details for Canonical TDX
canonical_repo = "https://github.com/canonical/tdx.git"
canonical_readme_path = "workspace/tdx/README.md"

# Repository details for SIG CentOS TDX
sig_centos_repo = "https://gitlab.com/adarshan-intel/docs.git"
sig_centos_branch = "adarsh/sigcentos-fixes"
sig_centos_host_os_path = 'workspace/docs/docs/tdx/host.md'
sig_centos_guest_os_path = 'workspace/docs/docs/tdx/guest.md'

# TDX Enabling Guide Host OS page commands
# Format:- search_string:verifier_string 
#   Verifier string is the expected output string when the command is executed.
#   If there is no clear expected output, provide an empty string and the 
#   framework will look for popular keywords like error.
# Exception:- If the command is a link, provide just the string.
tdx_guide_ubuntu24_04_setup_host = "Setup Host OS"
tdx_guide_centos_stream9_setup_host = "Configure a host"
tdx_guide_module_initialized = "Intel TDX Module is initialized:module initialized"
tdx_guide_install_msr_tools = "install the MSR Tools package:"
tdx_guide_intel_tme_enabled = "Intel TME is enabled:1"
tdx_guide_intel_tme_keys = "Intel TME keys:7f"
tdx_guide_sgx_mcheck_status = "Intel SGX and MCHECK status:0"
tdx_guide_tdx_status = "Intel TDX status:1"
tdx_guide_intel_tdx_keys = "Intel TDX keys:40"
tdx_guide_intel_sgx_package = "Intel SGX package repository:"
tdx_guide_install_qgs = "Install the QGS:"

# SIG CentOS Host OS page commands
# This is a page linked to the main host OS page and hence the commands are in a list.
sig_tdx_package = "Virt SIG TDX package"
sig_install_tdx = "Install the TDX host packages"
start_libvirt_service = "Start libvirtd service"
sig_running_kernel_version = "Running kernel version:`uname -r`" # Here the verifier string is actually is a command which will be executed and the output will be verified.
sig_tdx_enabled = "TDX is enabled:private KeyID range [64, 128)"
sig_reload_kvm_intel_module = "Reload kvm_intel module:"
sig_tdx_initialized = "TDX is initialized:module initialized"
sig_host = [sig_tdx_package, sig_install_tdx, start_libvirt_service, sig_running_kernel_version, 
            sig_tdx_enabled, sig_reload_kvm_intel_module, sig_tdx_initialized]

# Canonical Ubuntu 24.04 Host OS page commands
# This is a page linked to the main host OS page and hence the commands are in a list.
canonical_setup_host = "Run the `setup-tdx-host.sh` script:The host OS setup has been done successfully"
canonical_setup_host_os = [canonical_setup_host]

# Host setup commands dictionary
# Format:- search_string:command_type
#   Command type can be single_command, multi_distro, link, or read_from_other_file
#   single_command - The command is a single command
#   multi_distro - The command is different for different distros
#   link - The command is a link to another page
#   read_from_other_file - The command is read from another file
host_setup_commands = {"tdx_guide_ubuntu24_04_setup_host tdx_guide_centos_stream9_setup_host" : "link", \
                        tdx_guide_module_initialized : "single_command", \
                        tdx_guide_install_msr_tools : "multi_distro", tdx_guide_intel_tme_enabled : "single_command", \
                        tdx_guide_sgx_mcheck_status : "single_command", tdx_guide_tdx_status : "single_command", \
                        tdx_guide_intel_sgx_package: "read_from_other_file", tdx_guide_install_qgs : "multi_distro"}

# TDX Enabling Guide Guest OS page commands
# Format:- search_string
#   Guest OS page only has links to other pages and hence no verifier string is passed.
tdx_guide_ubuntu24_04_guest_setup = "Create TD Image"
tdx_guide_centos_stream9_guest_setup = "Create VM Disk Image"
tdx_guide_ubuntu24_04_launch_td = "Boot TD"
tdx_guide_centos_stream9_launch_td = "Configure and boot VM"

# Canonical Ubuntu 24.04 commands for Guest image creation.
# This is a page linked to the main guest OS page and hence the commands are in a list.
canonical_td_image = "TD image based on Ubuntu:SUCCESS"
canonical_create_td_image = [canonical_td_image]

# Canonical Ubuntu 24.04 commands for launching TD.
# This is a page linked to the main guest OS page and hence the commands are in a list.
canonical_launch_td_qemu = "Boot TD with QEMU:ssh -p 10022 root@localhost"
canonical_launch_td_virsh = "Boot TD using the following commands:"
canonical_boot_td = [canonical_launch_td_qemu, canonical_launch_td_virsh]

# SIG CentOS commands for Guest image creation.
# This is a page linked to the main guest OS page and hence the commands are in a list.
sig_centos_create_td_image = "root password and an authorized SSH key"
sig_create_vm_disk_image = [sig_centos_create_td_image]

# SIG CentOS commands for launching TD.
# This is a page linked to the main guest OS page and hence the commands are in a list.
sig_centos_launch_td_qemu = "Boot a TD guest using qemu-kvm"
sig_centos_td_guest_xml = "Create the XML template file"
sig_centos_create_vm = "Create the VM using the XML template"
sig_centos_launch_td_virsh = "Start the VM"
sig_configure_and_boot_vm = [sig_centos_launch_td_qemu, sig_centos_td_guest_xml, sig_centos_create_vm, sig_centos_launch_td_virsh]

# Guest setup commands dictionary
# Format:- search_string:command_type
#   Command type can be single_command, multi_distro, link, or read_from_other_file
#   single_command - The command is a single command
#   multi_distro - The command is different for different distros
#   link - The command is a link to another page
#   read_from_other_file - The command is read from another file
guest_setup_commands = {"tdx_guide_ubuntu24_04_guest_setup tdx_guide_centos_stream9_guest_setup" : "link", \
                        "tdx_guide_ubuntu24_04_launch_td tdx_guide_centos_stream9_launch_td" : "link"}

# TDX Enabling Infrastructure Setup page commands
# Format:- search_string:verifier_string
#   Verifier string is the expected output string when the command is executed.
#   If there is no clear expected output, provide an empty string and the
#   framework will look for popular keywords like error.
tdx_guide_setup_pccs = "setup the PCCS:"
tdx_guide_install_pccs = "Install PCCS:"
tdx_guide_verify_pccs = "verify PCCS:" # To-Do need to figure out verification logic.
tdx_guide_install_mpa = "Install MPA:"
tdx_guide_verify_mpa_registration = "successful MPA-based registration:PLATFORM_ESTABLISHMENT or TCB_RECOVERY passed successfully"
tdx_guide_add_noble_repo = "retrieve the PCKCIDRT:"
tdx_guide_install_pckid_package = "Install PCKCIDRT:"
tdx_guide_execute_pckid_package = "retrieved from a package repository:csv has been generated successfully!"
tdx_guide_execute_pckid_standalone_package = "retrieved from a standalone package:csv has been generated successfully!"
tdx_guide_extract_pm = "commands to extract the PM:"
tdx_guide_send_pm_to_pccs = "REST API endpoint of the IRS:"
tdx_guide_indirect_registration_pckid = "trigger the Indirect Registration with the PCKCIDRT:the data has been sent to cache server successfully!"
tdx_guide_install_pccsadmin = "install prerequisites for the PCCS Admin Tool:"
tdx_guide_merge_platform_csv_to_json = "command to trigger the merge of all individual:platform_list.json  saved successfully"
tdx_guide_transmit_json_to_pccs_pccsadmin = "he input JSON file to the PCS using the PCCS Admin Tool:platform_collaterals.json  saved successfully."
tdx_guide_insert_platform_collaterals = "execute the following command to insert the data from the:Collaterals uploaded successfully"
tdx_guide_local_cache = "venv/bin/python ./pccsadmin.py cache:saved successfully"
create_dcap_qncl_in_opt_qgsd = "sudo mkdir -p /var/opt/qgsd/.dcap-qcnl"
copy_cache_file = "sudo cp -f ./cache/sdp/* /var/opt/qgsd/.dcap-qcnl/"
echo_api_key_and_user_option = "115d3d4afdbe4331afb9817d68f87b0b\nn"
echo_pccs_password_and_user_option = "intel@123\nn"

# TDX Enabling Guide Trust Domain page commands
exec_in_guest_configure_td_to_qgs = "defining the vsock port:"
exec_in_guest_generate_td_quote = "sample application generating a TD Quote:"
exec_in_guest_intel_sgx_package = "Intel SGX package repository:"
guest_script_path = os.path.join(workspace_path,'guest_script.sh')

proxy_commands = f'''echo -e "Acquire::http::proxy \\"http://proxy-iind.intel.com:911\\";\nAcquire::https::proxy \\"http://proxy-iind.intel.com:912\\";" > /etc/apt/apt.conf.d/tdx_proxy
export http_proxy="http://proxy-iind.intel.com:911"
export https_proxy="http://proxy-iind.intel.com:912"'''

repo_clone_command = f"git clone -b noble-24.04 https://github.com/canonical/tdx.git {workspace_path}/tdx"
create_td_image = f'''cd {workspace_path}/tdx/guest-tools/image/
sudo ./create-td-image.sh -v 24.04'''
run_td_qemu = f'''cd {workspace_path}/tdx/guest-tools
./run_td.sh'''
update_known_hosts = f"sudo ssh-keygen -f '/root/.ssh/known_hosts' -R '[localhost]:10022'"
copy_script_to_guest = f"sudo sshpass -p 123456 scp -o StrictHostKeyChecking=no -P 10022 {guest_script_path} root@localhost:/root/"
launch_td_qemu = f'sudo sshpass -p 123456 ssh -T -o StrictHostKeyChecking=no -p 10022 root@localhost "bash /root/guest_script.sh"'
copy_quote_to_host = f"sudo sshpass -p 123456 scp -o StrictHostKeyChecking=no -P 10022 root@localhost:/opt/intel/tdx-quote-generation-sample/quote.dat ~/quote.dat"
tdx_guide_quote_verification = "install the dependencies for the [Quote Verification Sample]:successfully returned"

guest_script_commands = {exec_in_guest_configure_td_to_qgs : "single_command", exec_in_guest_intel_sgx_package: "read_from_other_file",
                          exec_in_guest_generate_td_quote: "multi_distro"}

trust_domain_setup_commands = {repo_clone_command: "exec_command", create_td_image: "exec_command", run_td_qemu: "exec_command", 
                               update_known_hosts: "exec_command", copy_script_to_guest: "exec_command", launch_td_qemu: "exec_command",
                               copy_quote_to_host: "exec_command", tdx_guide_quote_verification: "multi_distro"}



# Infrastructure setup Online Automatic dictionary
# Format:- search_string:command_type
#   Command type can be single_command, multi_distro, link, or read_from_other_file
#   single_command - The command is a single command
#   multi_distro - The command is different for different distros
#   link - The command is a link to another page
#   read_from_other_file - The command is read from another file
infrastructure_setup_direct_registration_mpa_commands = {tdx_guide_setup_pccs : "read_from_other_file", tdx_guide_install_pccs : "multi_distro", 
                                 tdx_guide_verify_pccs : "single_command", tdx_guide_install_mpa : "multi_distro", 
                                 tdx_guide_verify_mpa_registration : "single_command"}

# Infrastructure setup On-/Offline Manual dictionary
# Format:- search_string:command_type
#   Command type can be single_command, multi_distro, link, or read_from_other_file
#   single_command - The command is a single command
#   multi_distro - The command is different for different distros
#   link - The command is a link to another page
#   read_from_other_file - The command is read from another file
infrastructure_setup_direct_registration_offline_manual_commands = {tdx_guide_setup_pccs : "read_from_other_file", tdx_guide_install_pccs : "multi_distro", 
                                                                    tdx_guide_verify_pccs : "single_command", tdx_guide_add_noble_repo: "read_from_other_file",
                                                                    tdx_guide_install_pckid_package : "multi_distro", tdx_guide_execute_pckid_package : "multi_distro", 
                                                                    tdx_guide_extract_pm : "multi_distro", tdx_guide_send_pm_to_pccs : "multi_distro"}

infrastructure_setup_indirect_registration_online_manual_commands = {tdx_guide_setup_pccs : "read_from_other_file", tdx_guide_install_pccs : "multi_distro",
                                                                     tdx_guide_verify_pccs : "single_command", tdx_guide_add_noble_repo: "read_from_other_file", tdx_guide_install_pckid_package : "multi_distro",
                                                                     tdx_guide_execute_pckid_package : "multi_distro", tdx_guide_indirect_registration_pckid : "multi_distro"}

infrastructure_setup_indirect_registration_on_offline_pccs_based_commands = {tdx_guide_setup_pccs : "read_from_other_file", tdx_guide_install_pccs : "multi_distro",
                                                                     tdx_guide_verify_pccs : "single_command", tdx_guide_add_noble_repo: "read_from_other_file", tdx_guide_install_pckid_package : "multi_distro",
                                                                     tdx_guide_execute_pckid_package : "multi_distro", tdx_guide_install_pccsadmin : "multi_distro",
                                                                     tdx_guide_merge_platform_csv_to_json : "multi_distro", tdx_guide_transmit_json_to_pccs_pccsadmin : "multi_distro",
                                                                     tdx_guide_insert_platform_collaterals : "multi_distro"}

infrastructure_setup_indirect_registration_on_offline_local_cache_based_commands = {tdx_guide_setup_pccs : "read_from_other_file", tdx_guide_install_pccs : "multi_distro",
                                                                     tdx_guide_verify_pccs : "single_command", tdx_guide_add_noble_repo: "read_from_other_file", tdx_guide_install_pckid_package : "multi_distro",
                                                                     tdx_guide_execute_pckid_package : "multi_distro", tdx_guide_install_pccsadmin : "multi_distro",
                                                                     tdx_guide_merge_platform_csv_to_json : "multi_distro", tdx_guide_local_cache: "exec_command"}