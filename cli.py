# Write a cli tool that will invoke nmap and parse the results
# It should be invoked like "obsidian-map run nmap -p 80,22,443,445 -Pn -sV -T4"
# Or "obsidian-map parse nmap nmap.xml"
# Or "obsidian-map run nuclei -t cves -l urls.txt"

# Path: obsidan-map\cli.py
# Compare this snippet from obsidan-map\nmap.py:
import nmap
