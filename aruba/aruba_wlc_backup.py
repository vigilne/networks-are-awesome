from netmiko import ConnectHandler

# Create device dictionaries
wlc01 = {
    'device_type': 'aruba_os',
    'ip': '192.168.1.10',
    'username': 'admin',
    'password':'password',
}

# Establish secure session to device
net_connect = ConnectHandler(**wlc01)

# Send command to create backup file and wait 2 seconds for backup to complete
net_connect.send_command('backup flash', delay_factor=2)

# Send command to copy backup file to backup server via ftp
cmd1 = 'copy flash: flashbackup.tar.gz ftp: 172.16.1.100 ftpusername /backups flashbackup.tar.gz'
output = net_connect.send_command_timing(cmd1)
if 'Password:' in output:
    output += net_connect.send_command_timing('ftpuserpassword')

#  Disconnect secure session from device
net_connect.disconnect()
