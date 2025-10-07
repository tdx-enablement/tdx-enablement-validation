import subprocess
import os
import sys
import time
from utils import get_ip_address, clone_repo, set_environment_variables, run_command
sys.path.insert(1, os.path.join(os.getcwd(), 'configuration'))
import configuration

trustee_dir = "trustee"

class TrusteeKBSConfig:
    def __init__(self, **kwargs):
        self.external_ip = get_ip_address()
        self.config = {
            "KBS_CERT_PATH": "/etc/cert.pem",
            "KBS_EXTERNAL_IP": self.external_ip,
            "KBS_URL": f"https://{self.external_ip}:8080",
            "KBS_K_PATH": "keybroker/secret/k_rfs"
        }
        self.config.update(kwargs)

    def create_config_files(self):
        """Create necessary configuration files for Trustee KBS and AS"""
        # Create AS config
        as_config = {
            "policy_engine": "opa",
            "rvps_config": {
                "type": "BuiltIn",
                "storage": {
                    "type": "LocalFs"
                }
            },
            "attestation_token_broker": {
                "type": "Simple",
                "duration_min": 5
            }
        }
        
        as_config_path = os.path.join(trustee_dir, "attestation-service", "config.json")
        os.makedirs(os.path.dirname(as_config_path), exist_ok=True)
        
        import json
        with open(as_config_path, 'w') as f:
            json.dump(as_config, f, indent=4)
        
        # Create KBS config
        kbs_config = f"""[http_server]
sockets = ["0.0.0.0:8080"]
private_key = "/etc/key.pem"
certificate = "/etc/cert.pem"
insecure_http = false

[attestation_token]
insecure_key = true

[attestation_service]
type = "coco_as_grpc"
as_addr = "http://0.0.0.0:50004"
policy_engine = "opa"

[attestation_service.attestation_token_broker]
type = "Ear"
duration_min = 5

[attestation_service.rvps_config]
type = "BuiltIn"

[admin]
auth_public_key = "/etc/public.pub"

[[plugins]]
name = "resource"
type = "Vault"
vault_url = "{os.environ.get('VAULT_ADDR', 'http://127.0.0.1:8200')}"
token = "{os.environ.get('VAULT_ROOT_TOKEN', '')}"
mount_path = "keybroker"
kv_version = 1
"""
        
        kbs_config_path = os.path.join(trustee_dir, "config", "kbs-config.toml")
        os.makedirs(os.path.dirname(kbs_config_path), exist_ok=True)
        
        with open(kbs_config_path, 'w') as f:
            f.write(kbs_config)
        
        return as_config_path, kbs_config_path

def install_rust():
    """Install Rust if not already installed"""
    try:
        result = subprocess.run(['cargo', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            print("Rust is already installed")
            return
    except FileNotFoundError:
        pass
    
    print("Installing Rust...")
    curl_cmd = ["curl", "--proto", "=https", "--tlsv1.2", "-sSf", "https://sh.rustup.rs"]
    install_cmd = ["sh", "-s", "--", "-y"]
    
    curl_process = subprocess.Popen(curl_cmd, stdout=subprocess.PIPE)
    subprocess.run(install_cmd, stdin=curl_process.stdout)
    curl_process.wait()
    
    # Source cargo env
    cargo_env = os.path.expanduser("~/.cargo/env")
    if os.path.exists(cargo_env):
        subprocess.run(["bash", "-c", f"source {cargo_env}"])

def build_attestation_service():
    """Build CoCo Attestation Service"""
    print("Building CoCo Attestation Service...")
    as_dir = os.path.join(trustee_dir, "attestation-service")
    
    env = os.environ.copy()
    env["WORKDIR"] = os.path.abspath(as_dir)
    
    build_cmd = ["make", "VERIFIER=tdx-verifier", "RVPS_GRPC=false", "grpc-as"]
    subprocess.run(build_cmd, cwd=as_dir, env=env, check=True)
    
    # Install the binary
    binary_path = os.path.join(trustee_dir, "target", "release", "grpc-as")
    subprocess.run(["sudo", "install", "-D", "-m0755", binary_path, "/usr/local/bin"], check=True)

def build_kbs():
    """Build Trustee KBS"""
    print("Building Trustee KBS...")
    kbs_dir = os.path.join(trustee_dir, "kbs")
    
    build_cmd = ["make", "background-check-kbs", "AS_TYPES=coco-as", "COCO_AS_INTEGRATION_TYPE=grpc", "VAULT=true"]
    subprocess.run(build_cmd, cwd=kbs_dir, check=True)
    
    # Install KBS
    subprocess.run(["sudo", "make", "install-kbs"], cwd=kbs_dir, check=True)

def generate_certificates():
    """Generate self-signed certificates for KBS"""
    print("Generating certificates...")
    
    cert_config = """[req]
default_bits       = 2048
default_keyfile    = localhost.key
distinguished_name = req_distinguished_name
req_extensions     = req_ext
x509_extensions    = v3_ca

[req_distinguished_name]
countryName                 = Country Name (2 letter code)
countryName_default         = CN
stateOrProvinceName         = State or Province Name (full name)
stateOrProvinceName_default = Zhejiang
localityName                = Locality Name (eg, city)
localityName_default        = Hangzhou
organizationName            = Organization Name (eg, company)
organizationName_default    = localhost
organizationalUnitName      = organizationalunit
organizationalUnitName_default = Development
commonName                  = Common Name (e.g. server FQDN or YOUR name)
commonName_default          = localhost
commonName_max              = 64

[req_ext]
subjectAltName = @alt_names

[v3_ca]
subjectAltName = @alt_names

[alt_names]
DNS.1   = localhost
DNS.2   = 127.0.0.1
"""
    
    with open("localhost.conf", "w") as f:
        f.write(cert_config)
    
    # Generate certificate and key
    cert_cmd = [
        "openssl", "req", "-x509", "-nodes", "-days", "365",
        "-newkey", "rsa:2048",
        "-keyout", "/etc/key.pem",
        "-out", "/etc/cert.pem",
        "-config", "localhost.conf",
        "-passin", "pass:",
        "-batch"
    ]
    subprocess.run(["sudo"] + cert_cmd, check=True)
    
    # Generate resource retrieval key pair
    subprocess.run(["sudo", "openssl", "genpkey", "-algorithm", "ed25519", "-out", "/etc/private.key"], check=True)
    subprocess.run(["sudo", "openssl", "pkey", "-in", "/etc/private.key", "-pubout", "-out", "/etc/public.pub"], check=True)
    
    # Clean up
    os.remove("localhost.conf")

def run_attestation_service():
    """Run CoCo Attestation Service"""
    print("Starting CoCo Attestation Service...")
    as_config_path = os.path.join(trustee_dir, "attestation-service", "config.json")
    
    cmd = [
        "sudo", "RUST_LOG=debug", "grpc-as",
        "--config-file", as_config_path,
        "--socket", "127.0.0.1:50004"
    ]
    
    # Run in background using nohup
    with open(os.devnull, 'w') as devnull:
        subprocess.Popen(cmd, stdout=devnull, stderr=devnull)
    
    time.sleep(5)  # Give it time to start

def run_trustee_kbs():
    """Run Trustee KBS"""
    print("Starting Trustee KBS...")
    kbs_config_path = os.path.join(trustee_dir, "config", "kbs-config.toml")
    
    cmd = [
        "sudo", "RUST_LOG=debug", "kbs",
        "--config-file", kbs_config_path
    ]
    
    # Run in background using nohup  
    with open(os.devnull, 'w') as devnull:
        subprocess.Popen(cmd, stdout=devnull, stderr=devnull)
    
    time.sleep(10)  # Give it time to start

def setup_trustee_environment():
    """Setup complete Trustee environment"""
    print("Setting up Trustee environment...")
    
    # Install dependencies
    run_command(["sudo", "apt", "install", "-y", "make"])
    install_rust()
    
    # Clone Trustee repository
    clone_repo(configuration.kbs_url, trustee_dir, configuration.kbs_branch)
    
    # Generate certificates
    generate_certificates()
    
    # Create config files
    config = TrusteeKBSConfig()
    config.create_config_files()
    
    # Build components
    build_attestation_service()
    build_kbs()

def run_trustee_kbs_stack():
    """Run the complete Trustee KBS stack"""
    print("Starting Trustee KBS stack...")
    
    # Start Attestation Service
    run_attestation_service()
    
    # Start KBS
    run_trustee_kbs()
    
    # Set environment variables
    external_ip = get_ip_address()
    set_environment_variables(key="KBS_URL", data=f"https://{external_ip}:8080")
    set_environment_variables(key="KBS_CERT_PATH", data="/etc/cert.pem")
    set_environment_variables(key="KBS_K_PATH", data="keybroker/secret/k_rfs")
    
    return True

def check_trustee_services():
    """Check if Trustee services are running"""
    try:
        # Check if AS is running
        as_check = subprocess.run(["pgrep", "-f", "grpc-as"], capture_output=True)
        
        # Check if KBS is running  
        kbs_check = subprocess.run(["pgrep", "-f", "kbs"], capture_output=True)
        
        return as_check.returncode == 0 and kbs_check.returncode == 0
    except:
        return False