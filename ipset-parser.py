import re
from db import connection, cursor

def generate_query(ip_list):
    query = "DELETE * FROM firehol;"
    query = "INSERT INTO firehol (ip) VALUES"
    for ip in ip_list:
        query += "('" + ip + "'),"
    
    query = query[:-1] + ";"
    return query

def parse_ips():
    ipset_file = open("./ipsets/blocklist_de.ipset", "r")
    ipset_text = ipset_file.read()
    ipset_file.close()
    pattern = re.compile(r"(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})")
    ipset_ips = pattern.findall(ipset_text)
    return ipset_ips

ips = parse_ips()
ips_to_insert_query = generate_query(ips)
cursor = cursor.execute(ips_to_insert_query)
connection.commit()
connection.close()

print("%d IPs was added." %(len(ips)))