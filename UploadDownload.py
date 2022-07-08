import time
import psutil

def on_calculate_speed(interface):
    dt = 1  # I find that dt = 1 is good enough
    t0 = time.time()

    try:
        counter = psutil.net_io_counters(pernic=True)[interface]
    except KeyError:
        return []

    tot = (counter.bytes_sent, counter.bytes_recv)
    while True:
        last_tot = tot
        time.sleep(dt)
        try:
            counter = psutil.net_io_counters(pernic=True)[interface]
        except KeyError:
            break
        t1 = time.time()
        tot = (counter.bytes_sent, counter.bytes_recv)
        ul, dl = [
            (now - last) / (t1 - t0) / 1024.0
            for now, last
            in zip(tot, last_tot)
        ]
        return [t1, ul, dl]
        t0 = time.time()

def measure_accurate_ul_dl(dir_name, tabs = 1, interface = "Wi-Fi", oculus=False ):
    print(psutil.net_io_counters(pernic=True))
    if oculus:
        out_log = '{}/ULDLoculus_{}.log'.format(dir_name, tabs)
    else:
        out_log = '{}/ULDL_{}.log'.format(dir_name, tabs)

    with open(out_log, "w", newline='\n') as rttcsv:
        rttcsv.write("ts,ul_kBps,dl_kBps\n")
        while True:
            result_speed = on_calculate_speed(interface)
            if len(result_speed) < 1:
                print("Upload: - kB/s/ Download: - kB/s")
            else:
                t1, ul, dl = result_speed[0], result_speed[1], result_speed[2]
                print("Upload: {:0.2f} kB/s / Download: {:0.2f} kB/s".format(ul, dl))
                if dl > 0.1 or ul >= 0.1:
                    rttcsv.write("{},{:0.2f}, {:0.2f}\n".format(t1, ul, dl))


if __name__ == '__main__':
    tabs = 1 #int(sys.argv[1])
    ubuntu_iface = "wlp10s0"
    dir_name = "old_results/outlog"
    # win_iface = "Wi-Fi"
    measure_accurate_ul_dl(dir_name, tabs=tabs, interface=ubuntu_iface)