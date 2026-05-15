# Integration Tests for ibmi_download_fix_from_cloud Module

This directory contains integration tests for the `ibmi_download_fix_from_cloud` module.

## Overview

The tests are organized into two main categories:
- **Positive Tests** (`positive_tests.yml`): Verify successful operations
- **Negative Tests** (`negative_tests.yml`): Verify proper error handling

## Prerequisites

Before running these tests, you need to:

1. **Update Test Variables**: Replace placeholder values with actual test data:
   - `test_ptf_id`: PTF `SJ08667` is a small PTF for 7.6 release (replace if needed)
   - `test_credentials`: Update with valid machine credentials:
     - `machine_model`: e.g., "HEX"
     - `machine_type`: e.g., "9080"
     - `serial_number`: Your system's serial number
     - `country`: Country code, e.g., "US"

2. **Network Access**: Ensure the control node has internet access to reach IBM's Electronic Fix Delivery (EFD) cloud API.

3. **Valid Entitlement**: The machine credentials must have valid entitlement for the PTFs being tested.

## Test Coverage

### Positive Tests

1. **Preview Operation**: Tests the preview operation without downloading
2. **Validate Operation**: Tests entitlement validation without downloading
3. **Download Without Requisites**: Downloads a single PTF without requisites
4. **Download With Requisites**: Downloads a PTF including its requisites
5. **Download to Existing Directory**: Tests downloading to a pre-existing directory
6. **Clean Directory Option**: Tests the clean_directory parameter

### Negative Tests

1. **Invalid PTF ID**: Tests with a non-existent PTF
2. **Invalid Credentials**: Tests with incorrect machine credentials
3. **Missing Required Parameters**: Tests missing ptf_id, credentials, and directory
4. **Invalid Operation Value**: Tests with an invalid operation parameter
5. **Invalid Directory Path**: Tests with restricted/inaccessible directory
6. **Incomplete Credentials**: Tests with missing credential fields
7. **Empty PTF ID**: Tests with an empty string for PTF ID
8. **Invalid Boolean Value**: Tests with invalid value for include_requisites
9. **Invalid clean_directory Value**: Tests with invalid boolean value

## Running the Tests

### Run All Tests
```bash
ansible-test integration ibmi_download_fix_from_cloud
```

### Run Specific Test File
```bash
ansible-playbook tests/integration/targets/ibmi_download_fix_from_cloud/tasks/positive_tests.yml
ansible-playbook tests/integration/targets/ibmi_download_fix_from_cloud/tasks/negative_tests.yml
```

## Expected Results

- **Positive Tests**: All tests should pass when valid credentials and PTF IDs are provided
- **Negative Tests**: All tests should properly handle errors and return appropriate error messages

## Notes

- Tests run on `localhost` (the Ansible control node) using `delegate_to: localhost`
- Downloaded files are stored in temporary directories that are cleaned up after each test
- The `aliases` file marks these tests as `unsupported` for automated CI/CD runs since they require valid IBM credentials and network access

## Troubleshooting

If tests fail:
1. Verify your machine credentials are correct and have valid entitlement
2. Check network connectivity to IBM's EFD cloud API
3. Ensure the PTF ID exists and is available for download
4. Review the test output for specific error messages
5. Check that you have sufficient disk space for PTF downloads

## TODO Items

The following placeholders need to be replaced before running tests:
- [ ] `test_ptf_id`: PTF `SJ08667` is a small PTF for 7.6 release (replace if needed)
- [ ] `machine_model`: Replace `HEX` with actual model
- [ ] `machine_type`: Replace `9080` with actual type
- [ ] `serial_number`: Replace `XXXXXXX` with actual serial number
- [ ] `country`: Replace `US` with actual country code if different