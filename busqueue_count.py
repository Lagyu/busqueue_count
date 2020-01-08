import binascii
import nfc
import requests
import sys
import subprocess

class MyCardReader(object):

    def on_startup(self, targets):
        for target in targets:
            target.sensf_req = bytearray.fromhex("00830f0000")
        return targets

    def on_connect(self, tag):
        print("touched")
        subprocess.call("aplay Fairydust.wav",shell=True)
        self.idm = binascii.hexlify(tag.idm)
        return True

    def read_id(self):
        clf = nfc.ContactlessFrontend('usb')
        try:
            clf.connect(rdwr={'targets': ['212F' , '424F'],'on-connect': self.on_connect,'on-startup': self.on_startup})
        finally:
            clf.close()

if __name__ == '__main__':
    cr = MyCardReader()
try:
    while True:
        print("touch card:")
        cr.read_id()
        response = requests.post(
        'http://iot-dojo-bus.appspot.com/api/ride_record/',
        {"member_id": cr.idm,"device": "ecf2ffc9-3d56-4f21-9bb8-bcaf98e7a2df"})
        print(cr.idm)
except KeyboardInterrupt:
    sys.exit(0)
