from libnmap.process import NmapProcess
from libnmap.parser import NmapParser
import os

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
            f.write("Is Up: " + str(scanned_hosts.is_up()) + '\n')
            f.write("OS: " + ', '.join([str(x) for x in scanned_hosts.os_class_probabilities()]) + '\n')
            f.write("Hostnames: " + ', '.join([x for x in scanned_hosts.hostnames]) + '\n')
            f.write('\n')
            f.write('### Script Results\n')
            for results in scanned_hosts.scripts_results:
                f.write(scanned_hosts.scripts_results[results]['id'] + ': ' + str(scanned_hosts.scripts_results[results]['output']) + '\n')
            f.close()
            f.write('\n')
            f.write('### Ports\n')
        for scanned_services in scanned_hosts.services:
            service_path = os.path.join(host_path, str(scanned_services.port) + ".md")
            with open(service_path, "w") as f:
                f.write('State:' + str(scanned_services.state) + '\n')
                f.write('Reason:' + str(scanned_services.reason) + '\n')
                f.write('Protocol:' + str(scanned_services.protocol) + '\n')
                f.write('Service:' + str(scanned_services.service) + '\n')
                f.write('Banner:' + str(scanned_services.banner) + '\n')
                f.write(str(scanned_services) + '\n')
                f.write(scanned_services.banner + '\n')
                for results in scanned_services.scripts_results:
                    f.write(str(results) + '\n')
                
                f.close()
            local_obsidian_path = "Scan Results/nmap/" + scanned_hosts.address + '/' + str(scanned_services.port)
            with open(host_file_path, "a+") as f:
                f.write(f'![[{local_obsidian_path + "|" + str(scanned_services.port)}]]')
                f.close()