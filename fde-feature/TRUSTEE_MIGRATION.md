# Migration from ITA KBS to Trustee KBS - Summary

## Overview
This document summarizes the changes made to migrate the FDE automation framework from Intel Trust Authority (ITA) Key Broker Service to Confidential Containers (CoCo) Trustee Key Broker Service.

## Key Changes Made

### 1. Configuration Updates (`configuration/configuration.py`)
- **Repository URL**: Changed from `intel/trustauthority-kbs` to `confidential-containers/trustee`
- **Version**: Updated from `v1.3.0` to `v0.14.0`
- **Directory Name**: Changed from `ita-kbs` to `trustee`
- **Canonical TDX**: Updated from branch `3.1` to `3.2`

### 2. New Trustee KBS Setup (`libs/trustee_kbs.py`)
Created a new module to handle Trustee KBS setup:
- **Dependencies**: Rust installation, build tools
- **Components Built**:
  - CoCo Attestation Service (grpc-as)
  - Trustee Key Broker Service (kbs)
- **Certificate Generation**: Self-signed certificates for HTTPS
- **Configuration Files**: 
  - AS config (`config.json`)
  - KBS config (`kbs-config.toml`)

### 3. Updated FDE Library (`libs/fde.py`)
- **Key Generation**: Updated `retrieve_encryption_key()` function
  - Removed: `--kbs-env-file-path`, `--pk-kr-path`, `--sk-kr-path`
  - Added: `--auth-private-key-path`, `--kbs-resource-path`
- **Environment Variables**: 
  - Removed: `KBS_ENV`, `PK_KR_PATH`, `SK_KR_PATH`, `ID_k_RFS`
  - Added: `KBS_K_PATH`

### 4. Test Framework Updates (`conftest.py`, `tests/test_e2e_fde_workflow.py`)
- **Imports**: Changed from `kbs` module to `trustee_kbs` module
- **Function Calls**: `run_kbs()` → `run_trustee_kbs_stack()`
- **Port Changes**: KBS port changed from `9443` to `8080`
- **Cleanup**: Removed Docker log checking (not applicable to Trustee)
- **Process Management**: Added process cleanup for Trustee services

## Architecture Changes

### Before (ITA KBS)
```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   TD Guest      │────│   ITA KBS       │────│ HashiCorp Vault │
│                 │    │  (Docker)       │    │                 │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                              │
                       ┌─────────────────┐
                       │ Intel Trust     │
                       │ Authority       │
                       └─────────────────┘
```

### After (Trustee KBS)
```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   TD Guest      │────│  Trustee KBS    │────│ HashiCorp Vault │
│                 │    │  (Native)       │    │                 │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                              │
                       ┌─────────────────┐
                       │ CoCo AS         │
                       │ (grpc-as)       │
                       └─────────────────┘
```

## Key Differences

| Aspect | ITA KBS | Trustee KBS |
|--------|---------|-------------|
| **Deployment** | Docker container | Native binaries |
| **Attestation Service** | Intel Trust Authority | CoCo Attestation Service |
| **Port** | 9443 | 8080 |
| **Authentication** | Username/Password + API Key | Private key authentication |
| **Key ID Format** | UUID-based key ID | Resource path |
| **Configuration** | Environment file (.env) | TOML configuration |

## Environment Variables Changes

### Removed Variables
- `KBS_ENV` - No longer needed (no env file)
- `PK_KR_PATH` - Public key path (generated dynamically)
- `SK_KR_PATH` - Private key path (generated dynamically)  
- `ID_k_RFS` - Key ID (replaced with resource path)
- `TRUSTAUTHORITY_API_KEY` - ITA API key
- `ADMIN_USERNAME` - KBS admin username
- `ADMIN_PASSWORD` - KBS admin password

### New Variables
- `KBS_K_PATH` - Resource path for key storage (`keybroker/secret/k_rfs`)

### Updated Variables
- `KBS_URL` - Port changed from 9443 to 8080
- `KBS_CERT_PATH` - Now points to `/etc/cert.pem`

## Migration Steps

1. **Update Configuration**: Modify repository URLs and versions
2. **Install Dependencies**: Ensure Rust and build tools are available
3. **Build Components**: Build Attestation Service and KBS from source
4. **Generate Certificates**: Create self-signed certificates for KBS
5. **Update Tests**: Modify test functions and expected behaviors
6. **Process Management**: Replace Docker container management with process management

## Testing Considerations

- Tests now manage native processes instead of Docker containers
- Error checking is simplified (no Docker logs)
- Certificate handling is standardized (`/etc/cert.pem`)
- Port configuration is centralized

## Benefits of Migration

1. **Simplified Deployment**: No Docker dependency
2. **Better Integration**: Native process management
3. **Open Source**: Fully open-source attestation stack
4. **Standardized**: Industry-standard attestation protocols
5. **Flexibility**: More configuration options via TOML

## Potential Issues and Mitigations

1. **Permission Requirements**: Some operations require sudo access
   - Mitigation: Ensure proper permissions for certificate generation

2. **Process Management**: Background processes need proper cleanup
   - Mitigation: Added cleanup functions in test teardown

3. **Port Conflicts**: Default port 8080 might conflict
   - Mitigation: Configurable port in TOML config

4. **Certificate Management**: Self-signed certificates need proper handling
   - Mitigation: Automated certificate generation in setup

## Validation

The migration maintains the same FDE workflow:
1. Generate base image with dummy encryption
2. Boot TD to get quote/measurements  
3. Register TD with Trustee KBS
4. Retrieve actual encryption key
5. Re-encrypt image with real key
6. Boot final encrypted TD

All test cases should pass with the same security guarantees.