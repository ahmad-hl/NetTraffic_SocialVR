import os

rootDir = os.path.dirname(os.path.realpath(__file__))
currDir = os.path.join(rootDir, 'old_results/inlog')
os.chdir(rootDir)
print(os.getcwd())

in_files = [ r'inlog/ping6.txt']
out_log = 'outlog/mhserverRTT.log'

with open(out_log, "w", newline='\n') as rttcsv:
    for infile in in_files:
        # Read vehicles bandwidth --write---> bw.csv
        file = open(infile, "r")
        lines = file.readlines()[2:]
        try:
            for line in lines:
                fields = line.split()
                fields_no = len(fields)
                print([fields, fields_no])
                rtt_string = fields[fields_no - 2].replace('time=', '').replace('ms', '')
                rttcsv.write("{}\n".format(rtt_string))
        except:
            print("DONE...")
rttcsv.close()