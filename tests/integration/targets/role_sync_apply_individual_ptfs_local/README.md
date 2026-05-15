# Integration Tests for role_sync_apply_individual_ptfs_local

This directory contains integration tests for the `sync_apply_individual_ptfs_local` role.

## Overview

The tests are organized into two main categories:
- **Positive Tests** (`positive_tests.yml`): Verify successful operations
- **Negative Tests** (`negative_tests.yml`): Verify proper error handling

## Prerequisites

Before running these tests, you need to:

1. **IBM i Target System**: A running IBM i system configured in your Ansible inventory
   - The system must be accessible via SSH
   - Python 3 must be installed on the IBM i system
   - Proper user permissions for PTF operations

2. **Update Test Variables**: Replace placeholder values with actual test data:
   - `test_ptf_id`: PTF `SJ08667` is a small PTF for 7.6 release (replace if needed)
   - `test_credentials`: Update with valid machine credentials for PTF download
   - PTF product and release are automatically extracted from download results

3. **Network Access**: Control node needs internet access to download PTFs from IBM's cloud

4. **Dependencies**: The following roles must be available:
   - `check_ptf`: Used to verify PTF status
   - `load_ptf`: Used to load PTFs
   - `load_apply_ptfs`: Used by the role under test

## Test Coverage

### Positive Tests

1. **TC01 - Single PTF with Delete False**: Downloads and applies PTF with delete option false
2. **TC02 - Already Loaded PTF**: Loads PTF first, then applies it using the role
3. **TC03 - Single PTF with Delete True**: Downloads and applies PTF with delete option true
4. **TC04 - Permanent Apply with Delayed Option**: Currently skipped for now
5. **TC05 - Immediate Temp Apply**: Tests immediate temporary application

### Negative Tests

1. **TC01 - Missing PTF Files**: Tests with non-existent PTF files
2. **TC02 - Empty Lists**: Tests with empty not_loaded_list and already_loaded_list

## Running the Tests

### Run All Tests
```bash
ansible-test integration role_sync_apply_individual_ptfs_local
```

### Run Against Specific Host
```bash
ansible-playbook -i inventory tests/integration/targets/role_sync_apply_individual_ptfs_local/tasks/main.yml
```

### Run Specific Test File
```bash
ansible-playbook -i inventory tests/integration/targets/role_sync_apply_individual_ptfs_local/tasks/positive_tests.yml
ansible-playbook -i inventory tests/integration/targets/role_sync_apply_individual_ptfs_local/tasks/negative_tests.yml
```

## Expected Results

### Positive Tests
All tests should pass when:
- Valid machine credentials are provided for PTF download
- The IBM i target system is accessible
- Proper permissions are configured
- Dependencies (check_ptf, load_ptf, load_apply_ptfs roles) are available

### Negative Tests
All tests should properly handle errors and:
- Return appropriate error messages
- Define all expected return variables
- Not cause the playbook to crash unexpectedly

## Role Return Variables

The role returns the following variables (all should be defined after execution):

- `sync_apply_individual_ptfs_local_load_success_list`: List of successfully loaded PTFs
- `sync_apply_individual_ptfs_local_load_fail_list`: List of PTFs that failed to load
- `sync_apply_individual_ptfs_local_load_fail_dict`: Dictionary of load failures with details
- `sync_apply_individual_ptfs_local_apply_fail_with_requisite_list`: List of PTFs that failed due to requisites
- `sync_apply_individual_ptfs_local_apply_fail_dict`: Dictionary of apply failures with details
- `sync_apply_individual_ptfs_local_requisite_list`: List of requisite PTFs identified
- `sync_apply_individual_ptfs_local_apply_success_list`: List of successfully applied PTFs
- `sync_apply_individual_ptfs_local_apply_fail_list`: List of PTFs that failed to apply

## Key Features

- **Real PTF Download**: Uses `ibmi_download_fix_from_cloud` module to download actual PTF files
- **Automatic PTF Details**: Product and release information extracted from download results
- **Proper Cleanup**: Each test case removes the PTF after testing for reusability
- **Test Ordering**: TC01 uses delete=false to preserve files for TC02's already-loaded test

## Notes

- PTF files are downloaded once at the beginning and reused across test cases
- Each test case removes the PTF after completion to allow the same PTF to be used again
- The `aliases` file marks these tests as `unsupported` for automated CI/CD runs
- Tests run against an actual IBM i system (not localhost)

## Integration with ibmi_download_fix_from_cloud

This role is typically used in conjunction with the `ibmi_download_fix_from_cloud` module:

1. Use `ibmi_download_fix_from_cloud` to download PTFs to the control node
2. Use `check_ptf` role to determine which PTFs need to be loaded/applied
3. Use `sync_apply_individual_ptfs_local` role to transfer and apply the PTFs

See the example playbook at `usecases/fix_management/download_cloud_apply_individual_ptfs_local.yml` for the complete workflow.

## Troubleshooting

If tests fail:

1. **Connection Issues**:
   - Verify SSH connectivity to the IBM i system
   - Check that Python 3 is installed and accessible
   - Verify user permissions

2. **PTF Download Issues**:
   - Ensure control node has internet access
   - Verify machine credentials are valid
   - Check entitlement for the PTF

3. **PTF Issues**:
   - Verify PTF ID is valid for your system
   - Check that products are installed on the target system
   - Ensure PTF is compatible with system release

4. **Role Dependencies**:
   - Verify `check_ptf` role is available
   - Verify `load_ptf` role is available
   - Verify `load_apply_ptfs` role is available
   - Check role paths in ansible.cfg

5. **Permission Issues**:
   - Ensure user has authority to load/apply PTFs
   - Check library permissions (default is QGPL)
   - Verify file system permissions on target

## TODO Items

The following placeholders need to be replaced before running tests:
- [ ] `test_ptf_id`: PTF `SJ08667` is a small PTF for 7.6 release (replace if needed)
- [ ] `test_credentials`: Update with valid machine credentials
- [ ] Configure IBM i target system in inventory
- [ ] Ensure dependent roles (check_ptf, load_ptf, load_apply_ptfs) are available

## Example Test Execution

```bash
# Set up inventory
cat > test_inventory.ini << EOF
[ibmi]
test_system ansible_host=your.ibmi.system ansible_user=youruser
EOF

# Run positive tests only
ansible-playbook -i test_inventory.ini \
  tests/integration/targets/role_sync_apply_individual_ptfs_local/tasks/positive_tests.yml \
  -e "test_ptf_id=SJ08500"