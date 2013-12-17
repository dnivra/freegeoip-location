#!/usr/bin/env python2

import random
import sys
import time

import requests

MIN_REQUEST_BEFORE_SLEEP = 1
MAX_REQUEST_BEFORE_SLEEP = 10

MIN_SLEEP_DURATION = 1
MAX_SLEEP_DURATION = 10


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(''.join(["Usage: " + sys.argv[0] + " [IP_LIST_FILE]"]))
        sys.exit(1)

    print(''.join(["Reading IP list from ", sys.argv[1]]))
    ip_list = map(lambda ip: ip.strip(), open(sys.argv[1]).readlines())
    ip_list = set(ip_list)
    print("Done")

    url = "http://freegeoip.net/csv/"
    csv_header = ''.join([
                 "IP,Country Code,Country,Region Code,Region "
                 "Name,City,PIN Code,Latitude,Longitude,Metro Code,"
                 "Area Code\r\n"])

    f = open("location.csv", 'w')
    total = len(ip_list)
    f.write(csv_header)
    sleep_after_x = random.randint(MIN_REQUEST_BEFORE_SLEEP,
                                   MAX_REQUEST_BEFORE_SLEEP)
    for ip in ip_list:
        try:
            print("Remaining: " + str(total))
            r = requests.get(''.join([url, ip]))
            f.write(r.text.encode('utf-8'))
            total = total - 1
            sleep_after_x = sleep_after_x - 1
            if sleep_after_x == 0:
                time.sleep(random.randint(MIN_SLEEP_DURATION,
                                          MAX_SLEEP_DURATION))

                sleep_after_x = random.randint(MIN_REQUEST_BEFORE_SLEEP,
                                               MAX_REQUEST_BEFORE_SLEEP)
        except Exception, e:
            print(''.join(["Error when retrieving details for ", ip]))
            print(e)
            continue

    f.close()
