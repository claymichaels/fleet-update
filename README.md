# fleet-update
A tool to deploy a file to an entire fleet. (DEPRECATED)

Uses subprocess.popen to issue RSYNC commands to the host OS, and uses the host's /etc/hosts file to determine the devices in scope of the fleet.

Note that this script writes a tracking sheet, and will skip updated vehicles on subsequent runs.
