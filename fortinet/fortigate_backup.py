from netmiko import ConnectHandler
from netmiko.ssh_exception import NetMikoTimeoutException
from paramiko.ssh_exception import SSHException
from netmiko.ssh_exception import AuthenticationException
import time

with open('device_ip_list.txt') as f:
    device_list = f.read().splitlines()

for devices in device_list:

    ip_address = devices
    firewall = {
        'device_type': 'fortinet',
        'ip': ip_address,
        'username': 'admin',
        'password': 'admin_password',
    }

    timestr = time.strftime("%Y%m%d")

    try:
        net_connect = ConnectHandler(**firewall)
    except (AuthenticationException):
        continue
    except (NetMikoTimeoutException):
        continue
    except (EOFError):
        continue
    except (SSHException):
        continue
    except Exception as unknown_error:
        continue

    output = net_connect.send_command("show full-configuration", delay_factor=2)

    backup_path = '/usr/backups/fortinet/%s' % (firewall['ip'])

    filename = backup_path + str("_backupfile_"+ timestr)
    f = open(filename, 'w+')
    f.write(output)
    f.close()

    net_connect.disconnect()
