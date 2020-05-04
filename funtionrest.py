def get_flow(dpid,priority,cookie,in_port,dl_type,o_type,port):
    o = {
           "dpid" : dpid,
           "priority" : priority,
           "cookie" : cookie,
           "match" : {
                        "in_port" : in_port,
                        "dl_type" : dl_type
            },
            "actions" : [
               {
                    "type" : str(o_type),
                    "port" : port
               }
            ]
        }
    return(o)

def get_flows(dpid,priority,cookie,in_port,dl_type,ip_proto,o_type,port):
    o = {
           "dpid" : dpid,
           "priority" : priority,
           "cookie" : cookie,
           "match" : {
                        "in_port" : in_port,
                        "dl_type" : dl_type,
                        "ip_proto" : ip_proto
            },
            "actions" : [
               {
                    "type" : str(o_type),
                    "port" : port
               }
            ]
        }
    return(o)

if __name__ == "__main__":

    print("Function Call: Rest Funciton")

