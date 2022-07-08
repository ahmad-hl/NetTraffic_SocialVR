import subprocess as sp
import platform, os
import subprocess
from multiprocessing import Process

hubs_host = '54.221.85.234'
port = 443
timeout = 5

def tcping_subproc(seconds, out_file_path):
    myoutput = open(out_file_path, 'w')
    status = sp.call(['tcping', '-p', '{}'.format(port), '-c', '{}'.format(seconds), '-t', '{}'.format(timeout), '--report', hubs_host], stdout=myoutput, stderr=sp.DEVNULL)
    if status== 0:
        print("TCP Ping was successful")
    else:
        print("TCP Ping was FAILED")

def netping(seconds, out_file_path, network_timeout=3):
    """Send a ping packet to the specified host, using the system "ping" command."""
    args = [
        'ping'
    ]

    platform_os = platform.system().lower()

    if platform_os == 'windows':
        args.extend(['-n', seconds])
        args.extend(['-w', str(network_timeout * 1000)])
    elif platform_os in ('linux', 'darwin'):
        args.extend(['-c', seconds])
        args.extend(['-W', str(network_timeout)])
    else:
        raise NotImplemented('Unsupported OS: {}'.format(platform_os))

    args.append(hubs_host)

    try:
        myoutput = open(out_file_path, 'w')
        if platform_os == 'windows':
            output = subprocess.run(args, check=True, universal_newlines=True,stdout=myoutput).stdout

            # print(output)
            # if output and 'TTL' not in output:
            #     return False
        else:
            subprocess.run(args, check=True,stdout=myoutput)

        return True
    except (subprocess.CalledProcessError, subprocess.TimeoutExpired):
        return False

def process_RTT_csv(in_log_path, out_csv_path):
    with open(out_csv_path, "w", newline='\n') as rttcsv:
        file = open(in_log_path, "r")
        lines = file.readlines()[3:]
        try:
            for line in lines:
                fields = line.split()
                fields_no = len(fields)
                print([fields, fields_no])
                rtt_string = fields[fields_no - 2].replace('time=', '').replace('ms', '')
                rttcsv.write("{}\n".format(rtt_string))
        except Exception as ex:
            print("EX: {}".format(ex))
    rttcsv.close()

def network_RTT_csv(in_log_path, out_csv_path):
    with open(out_csv_path, "w", newline='\n') as rttcsv:
        file = open(in_log_path, "r")
        lines = file.readlines()[3:]
        try:
            for line in lines:
                fields = line.split()
                fields_no = len(fields)
                print([fields, fields_no])
                rtt_string = fields[fields_no - 2].replace('time=', '').replace('ms', '')
                rttcsv.write("{}\n".format(rtt_string))
        except Exception as ex:
            print("EX: {}".format(ex))
    rttcsv.close()

if __name__ == '__main__':

    tabs = 2
    seconds = 10  # num pings
    dir_name='results/inlog'
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)

    # process Ping
    proc_log_path = '{}/procping_{}.txt'.format(dir_name,tabs)
    procRTT_process = Process(target=tcping_subproc, args=(seconds, proc_log_path,))
    procRTT_process.start()

    # Network Ping
    net_log_path  = '{}/netping_{}.txt'.format(dir_name,tabs)
    rtt_process = Process(target=netping, args=('{}'.format(seconds),  net_log_path, ))
    rtt_process.start()

    #Join Proccess
    procRTT_process.join()
    rtt_process.join()

    # Compute net and process RTT to CSV
    procRTT_csv_path = '{}/procRTT_{}.csv'.format(dir_name, tabs)
    process_RTT_csv(in_log_path=proc_log_path, out_csv_path=procRTT_csv_path)

    netRTT_csv_path = '{}/netRTT_{}.csv'.format(dir_name, tabs)
    network_RTT_csv(in_log_path=net_log_path, out_csv_path=netRTT_csv_path)