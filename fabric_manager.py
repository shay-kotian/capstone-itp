from flask import Flask, render_template, Markup, request
import requests
import json
import subprocess
import threading
import re
import time


def pre_determined_path():
    try:

        s1_path1 = requests.post("http://10.0.0.1:8080/stats/flowentry/add",
                                 json={"dpid": 1, "table_id": 0, "priority": 22222,
                                       "match": {"in_port": 4, "tp_dst": 80, "nw_proto": 6, "dl_type": 2048,
                                                 "nw_dst": "1.1.1.0/24"}, "actions": [{"type": "OUTPUT", "port": 1}]})


        s2_path1 = requests.post("http://10.0.0.1:8080/stats/flowentry/add",
                                 json={"dpid": 2, "table_id": 0, "priority": 22222,
                                       "match": {"in_port": 1, "tp_dst": 80, "nw_proto": 6, "dl_type": 2048,
                                                 "nw_dst": "1.1.1.0/24"}, "actions": [{"type": "OUTPUT", "port": 2}]})
        s2_flow2 = requests.post("http://10.0.0.1:8080/stats/flowentry/add",
                                 json={"dpid": 2, "table_id": 0, "priority": 22222,
                                       "match": {"in_port": 2, "tp_src": 80, "nw_proto": 6, "dl_type": 2048,
                                                 "nw_dst": "2.2.2.0/24"}, "actions": [{"type": "OUTPUT", "port": 1}]})



        s3_path1 = requests.post("http://10.0.0.1:8080/stats/flowentry/add",
                                 json={"dpid": 3, "table_id": 0, "priority": 22222,
                                       "match": {"in_port": 1, "tp_dst": 80, "nw_proto": 6, "dl_type": 2048,
                                                 "nw_dst": "1.1.1.0/24"}, "actions": [{"type": "OUTPUT", "port": 2}]})
        s3_path2 = requests.post("http://10.0.0.1:8080/stats/flowentry/add",
                                 json={"dpid": 3, "table_id": 0, "priority": 22222,
                                       "match": {"in_port": 2, "tp_src": 80, "nw_proto": 6, "dl_type": 2048,
                                                 "nw_dst": "2.2.2.0/24"}, "actions": [{"type": "OUTPUT", "port": 1}]})


        s4_path1 = requests.post("http://10.0.0.1:8080/stats/flowentry/add",
                                 json={"dpid": 4, "table_id": 0, "priority": 22222,
                                       "match": {"in_port": 1, "tp_dst": 80, "nw_proto": 6, "dl_type": 2048,
                                                 "nw_dst": "1.1.1.0/24"}, "actions": [{"type": "OUTPUT", "port": 2}]})
        s4_path2 = requests.post("http://10.0.0.1:8080/stats/flowentry/add",
                                 json={"dpid": 4, "table_id": 0, "priority": 22222,
                                       "match": {"in_port": 2, "tp_src": 80, "nw_proto": 6, "dl_type": 2048,
                                                 "nw_dst": "2.2.2.0/24"}, "actions": [{"type": "OUTPUT", "port": 1}]})


        s5_path2 = requests.post("http://10.0.0.1:8080/stats/flowentry/add",
                                 json={"dpid": 5, "table_id": 0, "priority": 22222,
                                       "match": {"in_port": 4, "tp_src": 80, "nw_proto": 6, "dl_type": 2048,
                                                 "nw_dst": "2.2.2.0/24"}, "actions": [{"type": "OUTPUT", "port": 1}]})
        if s1_path1 and s2_path1 and s3_path1 and s4_path1:
            return True
        else:
            return False

    except Exception as ex:
        print(ex)


def fabric_util():
    try:
        s1_path1 = requests.post("http://10.0.0.1:8080/stats/flowentry/delete",
                                 json={"dpid": 1, "table_id": 0, "priority": 22222,
                                       "match": {"in_port": 4, "tp_dst": 80, "nw_proto": 6, "dl_type": 2048,
                                                 "nw_dst": "1.1.1.0/24"}, "actions": [{"type": "OUTPUT", "port": 1}]})


        s2_path1 = requests.post("http://10.0.0.1:8080/stats/flowentry/delete",
                                 json={"dpid": 2, "table_id": 0, "priority": 22222,
                                       "match": {"in_port": 1, "tp_dst": 80, "nw_proto": 6, "dl_type": 2048,
                                                 "nw_dst": "1.1.1.0/24"}, "actions": [{"type": "OUTPUT", "port": 2}]})
        s2_path2 = requests.post("http://10.0.0.1:8080/stats/flowentry/delete",
                                 json={"dpid": 2, "table_id": 0, "priority": 22222,
                                       "match": {"in_port": 2, "tp_src": 80, "nw_proto": 6, "dl_type": 2048,
                                                 "nw_dst": "2.2.2.0/24"}, "actions": [{"type": "OUTPUT", "port": 1}]})


        s3_path1 = requests.post("http://10.0.0.1:8080/stats/flowentry/delete",
                                 json={"dpid": 3, "table_id": 0, "priority": 22222,
                                       "match": {"in_port": 1, "tp_dst": 80, "nw_proto": 6, "dl_type": 2048,
                                                 "nw_dst": "1.1.1.0/24"}, "actions": [{"type": "OUTPUT", "port": 2}]})
        s3_path2 = requests.post("http://10.0.0.1:8080/stats/flowentry/delete",
                                 json={"dpid": 3, "table_id": 0, "priority": 22222,
                                       "match": {"in_port": 2, "tp_src": 80, "nw_proto": 6, "dl_type": 2048,
                                                 "nw_dst": "2.2.2.0/24"}, "actions": [{"type": "OUTPUT", "port": 1}]})


        s4_path1 = requests.post("http://10.0.0.1:8080/stats/flowentry/delete",
                                 json={"dpid": 4, "table_id": 0, "priority": 22222,
                                       "match": {"in_port": 1, "tp_dst": 80, "nw_proto": 6, "dl_type": 2048,
                                                 "nw_dst": "1.1.1.0/24"}, "actions": [{"type": "OUTPUT", "port": 2}]})
        s4_path2 = requests.post("http://10.0.0.1:8080/stats/flowentry/delete",
                                 json={"dpid": 4, "table_id": 0, "priority": 22222,
                                       "match": {"in_port": 2, "tp_src": 80, "nw_proto": 6, "dl_type": 2048,
                                                 "nw_dst": "2.2.2.0/24"}, "actions": [{"type": "OUTPUT", "port": 1}]})


        s5_path2 = requests.post("http://10.0.0.1:8080/stats/flowentry/delete",
                                 json={"dpid": 5, "table_id": 0, "priority": 22222,
                                       "match": {"in_port": 4, "tp_src": 80, "nw_proto": 6, "dl_type": 2048,
                                                 "nw_dst": "2.2.2.0/24"}, "actions": [{"type": "OUTPUT", "port": 1}]})

        if s5_path2 and s4_path2 and s3_path2 and s2_path2:
            return True
        else:
            return False
    except Exception as ex:
        print(ex)


def add_new_host():
    try:
        #Code to be updated to latest version
        return False
    except Exception as ex:
        print("An Exception occured:{}".format(str(ex)))


