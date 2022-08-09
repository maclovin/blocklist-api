import re
import glob
from db import connection, cursor
from os import path

def generate_query(ip_list):
    query = "DELETE * FROM firehol;"
    query = "INSERT INTO firehol (ip) VALUES"
    for ip in ip_list:
        query += "('" + ip + "'),"
    
    query = query[:-1] + ";"
    return query

def parse_ips(path_to_file=""):
    try:
        ipset_file = open(path_to_file, "r")
        ipset_text = ipset_file.read()
        ipset_file.close()
        pattern = re.compile(r"(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})")
        ipset_ips = pattern.findall(ipset_text)
    except:
        return []
    
    return ipset_ips

def main():
    ips = []

    for ipset_file in glob.glob("./blocklist-ipsets/*.ipset"):
        print("Parsing IPs from %s..." %(ipset_file))
        parsed_ipset = parse_ips(ipset_file)
        ips = ips + parsed_ipset
    
    print("Inserting IPs in local database...")
    ips_to_insert_query = generate_query(ips)
    cursor.execute(ips_to_insert_query)
    connection.commit()
    connection.close()

    print("%d IPs was added secessfully!" %(len(ips)))

if __name__ == "__main__":
    main()

ips = parse_ips()
#ips_to_insert_query = generate_query(ips)
#cursor = cursor.execute(ips_to_insert_query)
#connection.commit()
#connection.close()

#print("%d IPs was added." %(len(ips)))
