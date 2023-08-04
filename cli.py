# Write a cli tool that will invoke nmap and parse the results
# It should be invoked like "obsidian-map run nmap -p 80,22,443,445 -Pn -sV -T4"
# Or "obsidian-map parse nmap nmap.xml"
# Or "obsidian-map run nuclei -t cves -l urls.txt"

# Path: obsidan-map\cli.py
# Compare this snippet from obsidan-map\nmap.py:
import tools.nmap
import sys
import json
import os

class cli:
    def __init__(self, vault_name, output_filename, mode, options):
        self.vault_name = vault_name
        self.output_filename = output_filename
        self.mode = mode
        self.options = options
        self.get_vault_path()

    def get_vault_path(self):
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
                if obsidian_json["vaults"][vault]["path"].endswith(self.vault_name):
                    self.vault_path = obsidian_json["vaults"][vault]["path"]

    def run(self):
        tools.nmap.invoke(self.vault_path, self.mode, self.options)

vault_path = sys.argv[1]
mode = sys.argv[2]
options = sys.argv[3]

new_cli = cli(vault_path, "test", mode, options)
new_cli.run()