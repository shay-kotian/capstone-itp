import threading
import csv
from netmiko import ConnectHandler
import time


class intiate_ovs:

    def __init__(self, filename = "nsot.csv"):
        try:
            with open(filename, 'r') as csv_file:
                csv_reader = csv.DictReader(csv_file)

                for line in csv_reader:
                    switch_name = line['switch_name']
                    switch_ip = line['switch_ip']
                    controllerip = line['controllerip']
                    controllerport = line['controllerport']
                    protocol = line['protocol']
                    username = line['username']
                    password = line['password']

                    all_thread = threading.Thread(target=self.start_ovs, args=(switch_name, switch_ip, controllerip, controllerport, protocol,
                                                                               username,password))

                    all_thread.start()
                    all_thread.join()

        except Exception as ex:
            print("ERROR: " + str(ex))


    def start_ovs(self, name, ip, controller_ip, controller_port, protocol, username, password):
        try:
            print("Configuring switch: " + str(name))
            routers = {'device_type': 'linux', 'ip': ip, 'username': username, 'password': password}
            net_connect = ConnectHandler(**routers)
            command = "sudo ovs-vsctl set-controller team7 {}:{}:{}".format(protocol, controller_ip, controller_port)
            output = net_connect.send_command_timing('{}'.format(command))
            if '[sudo] password' in output:
                output += net_connect.send_command_timing(password)
                time.sleep(5)
                output = net_connect.send_command_timing("sudo ovs-vsctl show")
                time.sleep(5)
                if 'is_connected: true' in output:
                    return True
                else:
                    return False

        except Exception as ex:
            print("ERROR start_ovs: " + str(ex))

