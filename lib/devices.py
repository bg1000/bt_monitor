import json
from lib.bt_scan import bt_scan
class devices(object):
#
# This class manages a dictionary of bt_scan objects
# each bt_scan object represents a device to be scanned contains data from it's last scan
#

    def __init__(self):
        self.bt_scans = {}

    def update(self,message):
        # check of the device referred to in this message is in the dictionary
        # if it is update the name & ScansForAway
        # if it isn't create a bt_scan object for it and add it to the dictionary
        msg_json = json.loads(str(message.payload.decode("utf-8")))
        address = msg_json["Address"]
        if address in self.bt_scans:
            scanner = self.bt_scans[address]
            scanner.name = msg_json["DeviceName"]
            scanner.ScansForAway = msg_json["ScansForAway"]
        else:
            self.bt_scans[address] = bt_scan(msg_json["Adapter"], msg_json["DeviceName"], msg_json["Address"], msg_json["ScansForAway"])



