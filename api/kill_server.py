import time

import psutil as psutil
import pyuac

while True:
    for proc in psutil.process_iter():
        if proc.name() == "python.exe":
            if not pyuac.isUserAdmin():
                print("Re-launching as admin!")
                pyuac.runAsAdmin()
                proc.kill()
                break
    time.sleep(10) # Time needed for restart
