from libnmap.process import NmapProcess
from libnmap.parser import NmapParser
import sys
import json
import os

vault_name = "WRCCDC"
output_filename = "nmap.xml"
mode = "run"
options = "-p 80,22,443,445 -Pn -sV -T4"
# mode = parse

#Check the system we are running on
if sys.platform == "win32":
    obsidian_path = os.path.expandvars("%APPDATA%/obsidian/obsidian.json")
elif sys.platform == "linux":
    obsidian_path = "~/.config/obsidian/obsidian.json"
elif sys.platform == "darwin":
    obsidian_path = "~/Library/Application Support/obsidian/obsidian.json"
else: raise("Unknown OS")

# Find the vault directory from the obsidian.json file
with open(obsidian_path) as f:
    obsidian_json = json.load(f)
    for vault in obsidian_json.get("vaults"):
        if obsidian_json["vaults"][vault]["path"].endswith(vault_name):
            vault_path = obsidian_json["vaults"][vault]["path"]

def invoke(vault_path, mode, options):
    if mode == "run":
        print("Running nmap with options: " + options)
        nm = NmapProcess("127.0.0.1, scanme.nmap.org", options=options)
        nm.run()
        print("Finished running nmap")
        nmap_report = NmapParser.parse(nm.stdout)
    if mode == "parse":
        nmap_report = NmapParser.parse_fromfile(output_filename)
    print("Finished parsing nmap")

    nmap_path = os.path.join(vault_path, "Scan Results", "nmap")
    if not os.path.exists(nmap_path):
        os.makedirs(nmap_path)
    for scanned_hosts in nmap_report.hosts:
        print(scanned_hosts.address)
        # Make a directory for each host
        # Make a file for each port
        # Write the port information to the file
        host_path = os.path.join(nmap_path, scanned_hosts.address)
        if not os.path.exists(host_path):
            os.makedirs(host_path)
        # make a file for each host linked to each service
        host_file_path = host_path +".md"
        with open(host_file_path, "w") as f:
            f.write('\n')
            f.write('\n')
            f.close()
        for scanned_services in scanned_hosts.services:
            service_path = os.path.join(host_path, str(scanned_services.port) + ".md")
            with open(service_path, "w") as f:
                f.write(str(scanned_services))
                f.close()
            local_obsidian_path = "Scan Results/nmap/" + scanned_hosts.address + '/' + str(scanned_services.port)
            with open(host_file_path, "a+") as f:
                f.write(f'![[{local_obsidian_path + "|" + str(scanned_services.port)}]]')
                f.close()

invoke (vault_path, mode, options)