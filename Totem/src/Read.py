#!/usr/bin/env python
# -*- coding: utf8 -*-

import RPi.GPIO as GPIO
import MFRC522.MFRC522 as MFRC522
import signal
from RESTapi import Api


class ReadTag:
    def __init__(self):
        # Hook the SIGINT
        # Create an object of the class MFRC522
        self.RESULT = {}
        self.continue_reading = True
        self.rest = True
        self.MIFAREReader = MFRC522.MFRC522()
        signal.signal(signal.SIGINT, self.end_read)
        # Welcome message
        print ("Welcome to the MFRC522 data read example")
        print ("Press Ctrl-C to stop.")

    # Capture SIGINT for cleanup when the script is aborted
    def end_read(self, signal, frame):
        global continue_reading
        print ("Ctrl+C captured, ending read.")
        self.continue_reading = False
        GPIO.cleanup()
        raise SystemExit

    def read_loop(self):
        # This loop keeps checking for chips. If one is near it will get the UID and authenticate
        while self.continue_reading:

            # Scan for cards
            (status,TagType) = self.MIFAREReader.MFRC522_Request(self.MIFAREReader.PICC_REQIDL)

            # If a card is found
            if status == self.MIFAREReader.MI_OK:
                print ("Card detected")

            # Get the UID of the card
            (status,uid) = self.MIFAREReader.MFRC522_Anticoll()

            # If we have the UID, continue
            if status == self.MIFAREReader.MI_OK:

                # Print UID
                tag = "{0}:{1}:{2}:{3}".format(uid[0], uid[1], uid[2], uid[3])
                if self.get_request:
                    api = Api()
                    post_tag = {"tag": tag}
                    resp = api.post("tag/validate/", post_tag)
                    self.RESULT.update({'ok': resp.ok, 'data': resp.json()})
                    print("Response:\n{}".format(self.RESULT))
                    break
                    # return res_json

                # This is the default key for authentication
                # key = [0xFF,0xFF,0xFF,0xFF,0xFF,0xFF]
                #
                # # Select the scanned tag
                # self.MIFAREReader.MFRC522_SelectTag(uid)
                #
                # # Authenticate
                # status = self.MIFAREReader.MFRC522_Auth(self.MIFAREReader.PICC_AUTHENT1A, 8, key, uid)
                #
                # # Check if authenticated
                # if status == self.MIFAREReader.MI_OK:
                #     self.MIFAREReader.MFRC522_Read(8)
                #     self.MIFAREReader.MFRC522_StopCrypto1()
                # else:
                #     print ("Authentication error")
