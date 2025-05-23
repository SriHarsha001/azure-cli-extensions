
Release History
===============

2.1.2
++++++
Added images available for --distro flag to include current distributions, will remove EoL versions in future releases
Fixing a logic bug to allow V2 linux detection to work properly, and with Arm64
Disabled trusted launch for Arm64

2.1.1
++++++
Updated README file for `vm repair` extension. 

2.1.0
++++++
Added new parameter `--os-disk-type` to `vm repair create` to let users specify the repair vm's os disk storage account type. 

2.0.3
++++++
Added new long parameter functionality in `vm repair run` cmd `parameters` parameter. When using the prefix `++`, the entire key=value string will be sent to the running script, not just the value.


2.0.2
++++++
Updated parameter descriptions and examples for `az vm repair create`.

2.0.1
++++++
Fixed 2 Unbound variable bugs in `vm repair create` and improved the code documentation.  

2.0.0
++++++
Changed default VM image to 2022-datacenter-smalldisk for better default security. 

1.1.1
++++++
Migrated VM Repair off of the `msrestazure` API to `azure.core` and `azure.mgmt` APIs.
Fixed a bug with `--associate-public-ip` where it was always creating a public IP. Now a private IP will be used if `--associate-public-ip` is not specified.

1.1.0
++++++
Added script for GT fixit button.
Added support for `--disable-trusted-launch` flag parameter to set security type to `Standard` on the repair VM no matter what the source VM has.

1.0.10
++++++
Added breaking change warning for the default image for Windows source VMs if the source VM image is not found in `az vm repair create`. It will change from a 2016 image to 2022 in November 2024.

1.0.9
++++++
Fixed and updated several vm-repair tests for better coverage. 
Removed and updated broken image aliases pointing at images that no longer existed. 
Add `--encrypt-recovery-key` string parameter to `vm repair create` to use recovery key provided by the user to unlock the disk for a confidential VM. 

1.0.8
++++++
SELFHELP telemetry added as initiator. Extra parameters is introduced at the backend to capture the telemetry data.

1.0.7
++++++
az command adjustment

1.0.6
++++++
Add CLI update wait for ASG to wait for the operation done as the async 2rd operation will cancel the 1st call.

1.0.5
++++++
Bug fix ASG is not added properly when reset the nic
Add ASG if exist when nic is reset 

1.0.4
++++++
Logging improvements and script fixing

1.0.3
++++++
Bug fix the win-nest specific SKU issue

1.0.2
++++++
Bug fix for repo null string check so its set to main correctly
Add more logging to capture issues

1.0.1
++++++
Fix bug in win-run-driver.ps1 for 1.0.0b1.

1.0.0b1
++++++
Fix bug in win-run-driver.ps1 default values for invoking run command through az vm repair run.

0.5.9
++++++
Adding default values in win-run-driver.ps1 script for repo_fork and branch_name.

0.5.8
++++++
Fix az vm repair run --preview parameter to take in fork and branch name of User's repository.

0.5.7
++++++
Remove VM-repair SUSE image check

0.5.6
++++++
Renaming the Public IP resource.
Fix the name of the resource, previously the name was always "yes". Now it follows the format repair-<VM>_PublicIP

0.5.5
++++++
Adding ARM64 support.
Fix for telemetry for repair-and-restore command.
Repair VM fix for gen1 VM attaching disk on SCSI controller, preventing nested VM from booting (by Ryan McCallum)

0.5.4
++++++
Adding repair-and-restore command to create a one command flow for vm-repair with fstab scripts.

0.5.3
++++++
Removing check for EncryptionSettingsCollection.enabled is string 'false'.

0.5.2
++++++
Fix bug in _fetch_encryption_settings, add check for EncryptionSettingsCollection.enabled is false.

0.5.1
++++++
Updated exsiting privateIpAddress field to privateIPAddress and privateIpAllocationMethod to privateIPAllocationMethod.

0.5.0
++++++
Support for hosting repair vm in existing resource group and fixing existing resource group logic 

0.5.0
++++++
Support for hosting repair vm in existing resource group and fixing existing resource group logic 

0.4.10
++++++
Support for hosting repair vm in existing resource group and fixing existing resource group logic 

0.4.9
++++++
Fix for encrypted vm's auto unlock feature 

0.4.8
++++++
Fix for encrypted vm's and fixing test cases

0.4.7
++++++
Setting subscription account for reset-nic

0.4.6
++++++
Updating the fetch_repair_vm to use the small letters in the query instead of capital letters

0.4.5
++++++
Improve az vm repair reset-nic command to use subnet list available ips command

0.4.4
++++++
Add az vm repair reset-nic command

0.4.3
++++++
Adding a new distro option for creating the recovery VM, adding the detect for gen2 Linux machine and create a gen2 recovery VM

0.4.2
++++++
Linux only: Fixing duplicated UUID issue. Data disk gets attached only after VM got created.

0.4.1
++++++
Fixing bug in preview parameter

0.4.0
++++++
Fixing issue in disk copy, removing floating point in disk name.

0.3.9
++++++
Add support for preview flag and fix Gen2 bug

0.3.8
++++++
Add support for optional public IP 

0.3.6
++++++
Add support for ALAR2 which requires cloud-init script to prepare the recovery VM with a
build environment for Rust.

0.3.5
++++++

Add support for nested VMs
