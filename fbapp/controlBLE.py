#! /usr/bin/env python3
# coding: utf-8

import asyncio
from datetime import datetime

from bleak import BleakScanner
# from bleson import UUID16
# from bleson.core.types import UUID128

# https://macaddresschanger.com/bluetooth-mac-lookup/A4%3AC1%3A38
# OUI Prefix	Company
# A4:C1:38	Telink Semiconductor (Taipei) Co. Ltd.
GOVEE_BT_mac_OUI_PREFIX = "A4:C1:38"

# H5075_UPDATE_UUID16 = UUID128(0xEC88)
MODEL_NBR_UUID = "00002a24-0000-1000-8000-00805f9b34fb"


# ###########################################################################
FORMAT_PRECISION = ".2f"

# Decode Temperature into degrees Celcius
def decode_temp_in_c(encoded_data):
    if(encoded_data & 0x800000):
        return format( float((encoded_data ^0x800000) / -10000), FORMAT_PRECISION)
    return format(float (encoded_data / 10000), FORMAT_PRECISION)

# Decode percent humidity
def decode_humidity(encoded_data):
    return format(float((encoded_data % 1000) / 10), FORMAT_PRECISION)

devices = {}

# callback du scan
def detection_callback(device, advertisement_data):
    mac = device.address
  
    if device.address.startswith(GOVEE_BT_mac_OUI_PREFIX):
        if '0000ec88-0000-1000-8000-00805f9b34fb' in advertisement_data.service_uuids:
            devices[mac] = {}
            encoded_data = int(advertisement_data.manufacturer_data[60552].hex()[2:8], 16)
            
            devices[mac]["name"] = advertisement_data.local_name
            print(advertisement_data.local_name)

            devices[mac]["temperature"] = decode_temp_in_c(encoded_data)
            devices[mac]["hygrometrie"] = decode_humidity(encoded_data)

            devices[mac]["batterie"] = int(advertisement_data.manufacturer_data[60552].hex()[8:10], 16)

            devices[mac]["timeStamp"] = datetime.today()

async def scanner_loop():
        scanner = BleakScanner()
        scanner.register_detection_callback(detection_callback)
        await scanner.start()
        await asyncio.sleep(10.0)
        await scanner.stop()

        return devices