# Raspberry Pi Wifi Troubleshooting
Requires python3.
Execution to be scheduled with ```crontab```.

## Behaviour
 - Checks for successful ping to google.com.
 - Uses grep to check if some wifi ESSID is present.
 - If no ESSID found, turn network interface off and on again.