import platform
import subprocess

def iperf3(host, port = 5201):
    """Send a ping packet to the specified host, using the system "ping" command."""
    args = [
        'C:\\Users\\Engah\\Desktop\\iperf-3.1.3-win64\\iperf3.exe'
    ]

    platform_os = platform.system().lower()

    if platform_os  in ('linux', 'darwin', 'windows'):
        args.extend(['-c', host])
    else:
        raise NotImplemented('Unsupported OS: {}'.format(platform_os))

    args.append(host)

    try:
        myoutput = open('old_results/inlog/windowsIperf.txt', 'w')
        if platform_os == 'windows':
            output = subprocess.run(args, check=True, universal_newlines=True,stdout=myoutput).stdout
            print(output)

            # print(output)
            # if output and 'TTL' not in output:
            #     return False
        else:
            subprocess.run(args, check=True,stdout=myoutput)

        return True
    except (subprocess.CalledProcessError, subprocess.TimeoutExpired):
        return False

iperf3('10.79.134.193', port = 5201)