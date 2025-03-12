import pytest
from src.constants import *
from src.dmr_main import *

distro = "Ubuntu 24.04"

def test_tdx_enabling_guide_host_setup_ubuntu24_04():
    """
    Test the TDX enabling guide for host setup on Ubuntu 24.04.
    """
    run_test(distro, tdx_enabling_guide_host_os_page, host_setup_commands)

def test_tdx_enabling_guide_guest_setup_ubuntu24_04():
    """
    Test the TDX enabling guide for guest setup on Ubuntu 24.04.
    """
    run_test(distro, tdx_enabling_guide_guest_os_page, guest_setup_commands)

def test_tdx_enabling_infrastructure_setup_direct_registration_online_automatic_ubuntu24_04():
    """
    Test the TDX enabling guide for infrastructure setup Direct Registration online automatic on Ubuntu 24.04.
    """
    run_test(distro, tdx_enabling_guide_infrastructure_page, infrastructure_setup_direct_registration_mpa_commands)
    verify_attestation(distro, tdx_enabling_guide_trust_domain_page, trust_domain_setup_commands)

def test_tdx_enabling_infrastructure_setup_direct_registration_on_offline_manual_ubuntu24_04():
    """
    Test the TDX enabling guide for infrastructure setup Direct Registration On-/Offline manual on Ubuntu 24.04.
    """
    run_test(distro, tdx_enabling_guide_infrastructure_page, infrastructure_setup_direct_registration_offline_manual_commands)
    verify_attestation(distro, tdx_enabling_guide_trust_domain_page, trust_domain_setup_commands)

def test_tdx_enabling_infrastructure_setup_indirect_registration_online_manual_ubuntu24_04():
    """
    Test the TDX enabling guide for infrastructure setup Indirect Registration Online manual on Ubuntu 24.04.
    """
    run_test(distro, tdx_enabling_guide_infrastructure_page, infrastructure_setup_indirect_registration_online_manual_commands)
    verify_attestation(distro, tdx_enabling_guide_trust_domain_page, trust_domain_setup_commands)

def test_tdx_enabling_infrastructure_setup_indirect_registration_on_offline_pccs_based_ubuntu24_04():
    """
    Test the TDX enabling guide for infrastructure setup Indirect Registration On-/Offline PCCS-based on Ubuntu 24.04.
    """
    run_test(distro, tdx_enabling_guide_infrastructure_page, infrastructure_setup_indirect_registration_on_offline_pccs_based_commands)
    verify_attestation(distro, tdx_enabling_guide_trust_domain_page, trust_domain_setup_commands)

def test_tdx_enabling_infrastructure_setup_indirect_registration_on_offline_local_cache_based_ubuntu24_04():
    """
    Test the TDX enabling guide for infrastructure setup Indirect Registration On-/Offline Local Cache-based on Ubuntu 24.04.
    """
    run_test(distro, tdx_enabling_guide_infrastructure_page, infrastructure_setup_indirect_registration_on_offline_local_cache_based_commands)
    verify_attestation(distro, tdx_enabling_guide_trust_domain_page, trust_domain_setup_commands)