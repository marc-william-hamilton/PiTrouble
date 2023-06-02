#!/usr/bin/python3

import subprocess
import re
import os
from datetime import datetime


subprocess_options = {"capture_output": True, "text": True}
logging_file = open("log.txt", "a")


def check_package():

    result = subprocess.run(["dpkg", "-s", "net-tools"], **subprocess_options)

    result = re.search("Status.*", result.stdout)
    if result and result.group(0) != "Status: install ok installed":
        log("run <sudo apt install net-tools>")
        quit()


def get_interface():

    result = subprocess.run(["iwconfig"], **subprocess_options)

    result = result.stdout
    result = result[0:result.find(" ")]

    return result


def ping():

    response = os.system(f"ping -qc 1 google.com 2>&1 >/dev/null")

    if response == 0:
        return "Pinged Google"
    else:
        return "Ping to Google failed"


def wifi_connected(interface):

    # Run the command to check the Wi-Fi connection status
    result = subprocess.run(["iwconfig", interface], **subprocess_options)
    result = re.search("ESSID:\".*\"", result.stdout)
    if result:
        return not "off" in result.group(0)
    else:
        return False


def reconnect_wifi(interface):
    subprocess.run(["sudo", "ifconfig", interface, "down"])
    subprocess.run(["sudo", "ifconfig", interface, "up"])


def log(message):

    time = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

    logging_file.write(f"{time} {message}\n")
    logging_file.flush()


def main():
    check_package()
    interface = get_interface()

    if not wifi_connected(interface):
        log("Wi-Fi is disconnected. Reconnecting...")
        reconnect_wifi(interface)
    else:
        log("Wi-Fi is connected")

    log(ping())


if __name__ == "__main__":
    main()
