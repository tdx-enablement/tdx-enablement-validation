import pytest
from src.constants import *
from src.dmr_main import *
import shutil

@pytest.fixture(scope="function", autouse=True)
def setup(request):
    """
    Fixture to set up the test environment.
    Deletes the existing workspace directory if it exists and creates a new one.
    Copies the required repository to the workspace.
    Purges the SGX packages from the system.
    """
    test_name = request.node.name
    if os.path.exists(workspace_path):
        shutil.rmtree(workspace_path)
    os.mkdir(workspace_path)
    check_production_system()
    check_hostname()
    os.system(f"sudo cp -rf /home/sdp/jinen/applications.security.confidential-computing.tdx.documentation {workspace_path}")
    print("Preparing a clean system for testing...")
    if "direct_registration_online_automatic_ubuntu24_04" not in test_name:
        os.system("sudo apt purge --yes sgx-ra-service sgx-pck-id-retrieval-tool tdx-qgs libsgx-dcap-ql sgx-dcap-pccs")
        os.system("sudo rm -rf /opt/intel/sgx-ra-service /opt/intel/sgx-pck-id-retrieval-tool /var/opt/qgsd/ /opt/intel/sgx-dcap-pccs")
        os.system("export no_proxy=localhost,127.0.0.1")
        if "infrastructure_setup" in test_name:
            if "ubuntu24_04" in test_name:
                distro = "Ubuntu 24.04"
            else:
                distro = "CentOS 9"
            run_test(distro, tdx_enabling_guide_host_os_page, host_setup_commands)
            os.system(f"sudo rm -rf {workspace_path}/tdx")

def check_production_system():
    """
    Checks if the system is a production system by reading a specific MSR register.
    Sets the 'production_system' environment variable based on the result.
    """
    command = "sudo rdmsr 0xCE -f 27:27"
    print("Starting Process %s from %s" %(command, os.getcwd()))
    process = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                    universal_newlines=True, shell=True, timeout=20)
    if process.returncode != 0:
        print(process.stderr.strip())
        print("Setting default value as Production system")
        production_system = True
    else:
        if str(process.stdout.strip()) == "0":
            production_system = True
            print("This is a Production system")
        else:
            production_system = False
            print("This is a Non-Production system")
    os.environ["production_system"] = str(production_system)

def check_hostname():
    """
    Retrieves the hostname of the system and sets the 'hostname' environment variable.
    """
    hostname_cmd = "hostname"
    print("Starting Process %s from %s" %(hostname_cmd, os.getcwd()))
    process = subprocess.run(hostname_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                universal_newlines=True, shell=True, timeout=20)
    hostname = process.stdout.strip()
    print(f"Hostname: {hostname}")
    os.environ["hostname"] = hostname


