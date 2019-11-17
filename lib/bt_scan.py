import subprocess
class bt_scan(object):
    
    def __init__(self, adapter, name, address):
        self.adapter = adapter
        self.name = name
        self.address = address
        # should there be a timeout value here?
    def scan(self):
        print ("Starting Scan")
        # do a bluetooth scan here, update last_scan and return results
        hci_results = subprocess.run(["hcitool", "-i", self.adapter, "name", self.address], capture_output=True, text = True)
        print("The length of self.name is " + str(len(self.name)))
        print (str(hci_results.returncode))
        print (hci_results.stdout)
        print("The length of stdout is " + str(len(hci_results.stdout)))
        print (hci_results.stderr)
        if hci_results.returncode == 0 and hci_results.stdout[0:len(hci_results.stdout)-1] == self.name:
            # update results here
            print ("Scan for " + self.name + " was sucessful")
        else:
            print ("Scan for " + self.name + " failed")
   # last_scan is a read only property that contains the results from the last scan
    @property
    def last_scan(self):
        # Store the results here in a dictionary or as a json string
        pass



