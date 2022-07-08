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


in_files = ['inlog/windowsIperf.txt']
out_log = 'outlog/MHbw.log'

with open(out_log, "w", newline='\n') as bwcsv:
    for infile in in_files:
        # Read vehicles bandwidth --write---> bw.csv
        file = open(infile, "r")
        lines = file.readlines()[3:]
        for line in lines:
            print(line)
            fields = line.split("  ")
            fields_no = len(fields)
            for field in fields:
                if field.endswith('bits/sec'):
                    print("{}, {}, {}".format(fields, fields_no, field))
                    bw  = getBWs_as_Mbits(field)
                    print(bw)
                    if bw>0:
                        bwcsv.write("{}\n".format(bw))
bwcsv.close()

