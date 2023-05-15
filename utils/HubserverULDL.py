import time, math, os, logging
from datetime import datetime
#https://www.kernel.org/doc/Documentation/ABI/testing/sysfs-class-net-statistics

currDir = os.path.dirname(os.path.realpath(__file__))
Logs_Dir = os.path.join(currDir, 'old_results/outlog')
dlul_log_url = os.path.join(Logs_Dir, "ULDL.sr.log")
with open(dlul_log_url, 'w'):
    pass

dlul_logger = logging.getLogger('Traffic_Logger')
hdlr_1 = logging.FileHandler(dlul_log_url)
dlul_logger.setLevel(logging.INFO)
dlul_logger.addHandler(hdlr_1)
dlul_logger.info("second,ul,dl,tx_bytes,rx_bytes,rx_packets,rx_dropped,tx_packets,tx_dropped")

#/sys/class/<iface>/statistics/tx_packets
def get_bytes(interface, type):
    with open('/sys/class/net/' + interface + '/statistics/' + type + '_bytes', 'r') as f:
        data = f.read()
        return int(data)

#/sys/class/<iface>/statistics/tx_dropped
def get_dropped_packets(interface, type):
    with open('/sys/class/net/' + interface + '/statistics/' + type + '_dropped', 'r') as f:
        data = f.read()
        return int(data)

#/sys/class/<iface>/statistics/rx_packets
def get_packets(interface, type):
    with open('/sys/class/net/' + interface + '/statistics/' + type + '_packets', 'r') as f:
        data = f.read()
        return int(data)

iface = 'eno1'
# Interface Throughput statistics
rx1 = get_bytes(iface, 'rx')
tx1 = get_bytes(iface, 'tx')

rx_dropped1 = get_dropped_packets(iface, 'rx')
tx_dropped1 = get_dropped_packets(iface, 'tx')

rx_packets1 = get_packets(iface, 'rx')
tx_packets1 = get_packets(iface, 'tx')

timer_start = time.time()

while True:
    #Measure every dowload/upload second
    if time.time() - timer_start > 1:
        timer_start = time.time()
        # Download
        rx2 = get_bytes(iface, 'rx')
        rx_bytes_sec = rx2 - rx1
        download_in_mbit = round((rx_bytes_sec) * 8 / 1024.0/ 1024.0, 4)
        # Upload
        tx2 = get_bytes(iface, 'tx')
        tx_bytes_sec = tx2 - tx1
        upload_in_mbit = round((tx_bytes_sec) * 8 / 1024.0/ 1024.0, 4)
        seconds = math.ceil(time.mktime(datetime.today().timetuple()))
        rx1 = rx2
        tx1 = tx2
        print("Upload: {} Bytes, {} Mbit/s, Download: {} Bytes, {} Mbit/s".format(tx_bytes_sec, upload_in_mbit, rx_bytes_sec, download_in_mbit))

        rx_dropped2 = get_dropped_packets(iface, 'rx')
        rx_dropped = rx_dropped2 - rx_dropped1
        rx_packets2 = get_packets(iface, 'rx')
        rx_packets = rx_packets2 - rx_packets2
        print("RX Packets: {} packets/s, Dropped: {} packets/s".format(rx_packets, rx_dropped))
        rx_packets1 = rx_packets2
        rx_dropped1 = rx_dropped2

        tx_dropped2 = get_dropped_packets(iface, 'tx')
        tx_dropped = tx_dropped2 - tx_dropped1
        tx_packets2 = get_packets(iface, 'tx')
        tx_packets = tx_packets2 - tx_packets2
        print("TX Packets: {} packets/s, Dropped: {} packets/s".format(tx_packets, tx_dropped))
        tx_packets1 = tx_packets2
        tx_dropped1 = tx_dropped2
        #log the info
        dlul_logger.info("{},{},{},{},{},{},{}".format(seconds, upload_in_mbit, download_in_mbit,tx_bytes_sec, rx_bytes_sec,rx_packets,rx_dropped,tx_packets,tx_dropped ))
        


