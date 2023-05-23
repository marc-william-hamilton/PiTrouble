import subprocess
from time import sleep
import re
import schedule
import os
from sty import fg

subprocess_options = {"capture_output": True, "text": True}


def check_package():

    result = subprocess.run(["dpkg", "-s", "net-tools"], **subprocess_options)

    result = re.search("Status.*", result.stdout)
    if result and result.group(0) == "Status: install ok installed":
        print(f"* {fg.blue}found net-tools{fg.rs}")
    else:
        print(
            f"net-tools {fg.li_red}not found{fg.rs}, run <sudo apt install net-tools>")
        quit()


def get_interface():

    result = subprocess.run(["iwconfig"], **subprocess_options)

    result = result.stdout
    result = result[0:result.find(" ")]

    print(f"* {fg.blue}interface is {result}{fg.rs}")
    return result


def ping():

    response = os.system(f"ping -qc 1 google.com 2>&1 >/dev/null")

    if response == 0:
        print(f"{fg.li_green}Pinged Google{fg.rs}")
    else:
        print(f"{fg.li_red}Ping to Google failed{fg.rs}")


def wifi_connected(interface):

    # Run the command to check the Wi-Fi connection status
    result = subprocess.run(["iwconfig", interface], **subprocess_options)
    result = re.search("ESSID:\".*\"", result.stdout)
    if result:
        return not "off" in result.group(0)
    else:
        return False


def reconnect_wifi(interface):
    # Run commands to reconnect to the Wi-Fi network
    subprocess.run(["sudo", "ifconfig", interface, "down"])
    subprocess.run(["sudo", "ifconfig", interface, "up"])


def main():
    check_package()
    interface = get_interface()
    print(f"{fg.li_yellow}Press CTRL+C to quit{fg.rs}")
    ping()
    schedule.every(2).minutes.do(ping)

    try:

        while True:
            if not wifi_connected(interface):
                print(f"{fg.li_red}Wi-Fi is disconnected. Reconnecting...{fg.rs}")
                reconnect_wifi(interface)
            else:
                print(f"{fg.li_green}Wi-Fi is connected{fg.rs}")

            # Delay between checks (in seconds)
            sleep(10)

    except KeyboardInterrupt:
        print("\nbyeee :)")


if __name__ == "__main__":
    main()
