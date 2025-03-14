# tdx_enabling_guide_automation

This project automates the testing of different pages of the CC enabling guide present at: [Intel TDX Enabling Guide](https://cc-enabling.trustedservices.intel.com/intel-tdx-enabling-guide/01/introduction/index.html). The automation extracts commands from the Markdown file, executes them, and compares the results against the expected output.

## Prerequisites
- A system with Intel TDX support
- `pytest` installed:
    ```bash
    sudo apt install python3-pytest
    ```
- Add root user to the KVM group:
    ```bash
    sudo usermod -aG kvm root
    ```
