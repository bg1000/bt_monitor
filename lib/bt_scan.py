import subprocess
import datetime
import json
import logging
class bt_scan(object):

    def __init__(self, adapter, name, address, scans_for_away):
        self.adapter = adapter
        self.name = name
        self.address = address
        self.ScansForAway = scans_for_away
        self.PreviousConfidence = 0.0
       # should there be a timeout value here?
    def scan(self):
        logging.info ("Starting Scan")
        # do a bluetooth scan here, update last_scan and return results
        hci_results = subprocess.run(["hcitool", "-i", self.adapter, "name", self.address], capture_output=True, text = True)
        logging.debug(str(hci_results.returncode))
        logging.debug(hci_results.stdout)
        logging.debug("The length of stdout is " + str(len(hci_results.stdout)))
        logging.debug(hci_results.stderr)
        # scan was sucessful and device was found
        if hci_results.returncode == 0 and hci_results.stdout[0:len(hci_results.stdout)-1] == self.name:
            # update results here
            self.ErrorOnScan = False
            results = {
                    "DeviceName": self.name,
                    "DeviceAddress": self.address,
                    "Confidence": "100",
                    "Timestamp": str(datetime.datetime.now())
                      }
            self.results = json.dumps(results, indent=4)
            self.PreviousConfidence = 100.0
        # scan was sucessful but deive wasn't found
        elif hci_results.returncode == 0 and hci_results.stdout[0:len(hci_results.stdout)-1] != self.name:
            self.ErrorOnScan = False
            self.PreviousConfidence = self.PreviousConfidence - 100.0/float(self.ScansForAway)
            if self.PreviousConfidence < 0.0:
                self.PreviousConfidence = 0.0
            results = {
                    "DeviceName": self.name,
                    "DeviceAddress": self.address,
                    "Confidence": str(self.PreviousConfidence),
                    "Timestamp": str(datetime.datetime.now())
                      }
            self.results = json.dumps(results, indent=4)

        # there was an error during the scan
        elif hci_results.returncode != 0:
            self.ErrorOnScan = True
   # last_scan is a read only property that contains the results from the last scan
    @property
    def last_scan(self):
        # Store the results here in a dictionary or as a json string
        pass



