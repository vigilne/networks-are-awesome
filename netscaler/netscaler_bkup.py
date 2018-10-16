#  Import functions used in script
from netmiko import ConnectHandler, SCPConn
import time, os, sys

#  Create device dictionary
netscaler_device = {
       'device_type': 'netscaler',
       'ip': '192.168.1.1',
       'username': 'username',
       'password': 'password',
}

#  open file containing commands
with open('commands.txt') as f:
     commands_list = f.read().splitlines()

#  Establish ssh session to device and send commands
net_connect = ConnectHandler(**netscaler_device)
net_connect.send_config_set(commands_list, delay_factor=4)

#  open secure copy protocol to transfer backup file to server
ssh_conn = ConnectHandler(**netscaler_device)
scp_conn = SCPConn(ssh_conn)

s_file = '/var/ns_sys_backup/backupfile.tgz'
d_file = '/usr/backups/backupfile.tgz'

scp_conn.scp_get_file(s_file, d_file)

#  Close secure copy protocol session
scp_conn.close()

#  Close ssh session
net_connect.disconnect()

timestr = time.strftime("%Y%m%d-%H%M%S")

#  Rename backup file to contain time and date stamp
os.rename("/usr/backups/backupfile.tgz","/usr/backups/backupfile.tgz" + timestr)
