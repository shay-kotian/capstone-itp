import configure_ovs
from fabric_manager import *
from netmiko import ConnectHandler
import time
import unittest
from prettytable import PrettyTable

class initiate(unittest.TestCase):

    test_cases_passed = 0
    test_cases_failed = 0
    status = []
    @classmethod
    def setUpClass(cls):
        cls.controller_ip = "10.0.0.1"
        cls.username = "group_7"
        cls.password = "group_7"
        cls.__start_controller(cls.controller_ip, cls.username, cls.password)
        temp=configure_ovs.initiate()

    @classmethod
    def tearDownClass(cls):
        print("End of all tests")
        total = cls.test_cases_passed + cls.test_cases_failed
        table_name = PrettyTable(["Number of Test Cases", "Number of TC passed", "Number of TC Failed"])
        table_name.add_row([total, cls.test_cases_passed, cls.test_cases_failed])
        print(table_name)
        table_test = PrettyTable(["Name of Test Case", "Status"])
        table_test.add_row(["test_link_failure", cls.status[0]])
        table_test.add_row(["test_app_priority", cls.status[1]])
        table_test.add_row(["test_node_failure", cls.status[2]])
        table_test.add_row(["test_traffic_engineering", cls.status[3]])
        table_test.add_row(["test_fabric_utilization", cls.status[4]])
        table_test.add_row(["test_addition_of_new_host", cls.status[5]])
        print(table_test)

    def setUp(self):
        pass

    def tearDown(self):
        self.state = "FAILED"
        self.status.append(self.state)

    def __start_controller(self, ip, username, password):
        try:
            routers = {'device_type': 'linux', 'ip': ip, 'username': username, 'password': password}
            net_connect_hp = ConnectHandler(**routers)
            cmd1 = ["sudo ryu-manager ryu/app/simple_switch_13.py"]
            output = net_connect_hp.send_config_set(cmd1)
            time.sleep(2)

        except Exception as ex:
            print("ERROR: " + str(ex))
            exit()

    def test_link_failure(self):
        try:
            if not link_fail():
                self.test_cases_failed += 1
                self.assertRaises("FAILED")
            else:
                self.state = "PASSED"
                self.test_cases_passed += 1
        except Exception as ex:
            print("Exception occured: " + str(ex))

    def test_app_priority(self):
        try:
            if not app_http():
                self.test_cases_failed += 1
                self.assertRaises("FAILED")
            else:
                self.test_cases_passed += 1
                self.state = "PASSED"
        except Exception as ex:
            print("Exception occured: " + str(ex))

    def test_node_failure(self):
        try:
            if not fail_node():
                self.assertRaises("FAILED")
                self.test_cases_failed += 1
            else:
                self.test_cases_passed += 1
                self.state = "PASSED"
        except Exception as ex:
            print("Exception occured: " + str(ex))


    def test_traffic_engineering(self):
        try:
            if not pre_determined_path():
                self.assertRaises("FAILED")
                self.test_cases_failed += 1
            else:
                self.state = "PASSED"
                self.test_cases_passed += 1
        except Exception as ex:
            print("Exception occured: " + str(ex))


    def test_fabric_utilization(self):
        try:
            if not fabric_util():
                self.test_cases_failed += 1
                self.assertRaises("FAILED")
            else:
                self.state = "PASSED"
                self.test_cases_passed += 1

        except Exception as ex:
            print("Exception occured: " + str(ex))

    def test_addition_of_new_host(self):
        try:
            if not add_new_host():
                self.test_cases_failed += 1
                self.assertRaises("FAILED")
            else:
                self.state = "PASSED"
                self.test_cases_passed += 1

        except Exception as ex:
            print("Exception occured: " + str(ex))

if __name__ == '__main__':
    unittest.main()


