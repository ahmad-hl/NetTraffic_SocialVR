import os

# Unify units into Mb/s
def getBWs_as_Mbits(field):
    components = field.split()
    print(components)
    if field.find("Kbits/sec") > 0:
        return float(components[0]) / 1024
    elif field.find("Gbits/sec") > 0:
        return float(components[0]) * 1024
    elif field.find("Mbits/sec") > 0:
        return float(components[0])
    elif field.find("bits/sec") > 0:
        return float(components[0])

rootDir = os.path.dirname(os.path.realpath(__file__))
currDir = os.path.join(rootDir, 'old_results/inlog')
os.chdir(rootDir)
print(os.getcwd())

in_files = ['inlog/LinuxIperf.txt']
out_log = 'outlog/wifi-eduroam-bw-1.log'

with open(out_log, "w", newline='\n') as bwcsv:
    for infile in in_files:
        # Read vehicles bandwidth --write---> bw.csv
        file = open(infile, "r")
        lines = file.readlines()[6:]

        for line in lines:
            fields = line.split("  ")
            fields_no = len(fields)
            bw_string = fields[fields_no-1].replace('\n', '')
            bw  = getBWs_as_Mbits(bw_string)
            if bw>0:
                bwcsv.write("{}\n".format(bw))
bwcsv.close()





