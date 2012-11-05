#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ts=4 et sw=4 sts=4 ai fenc=utf-8:

# dnw.py - python port of dnw client, smdk-usbdl
#
# Copyright (C) 2012 Jeff Kent <jakent@gmail.com>
# - Development mode automatically transmits
# - Adjusted the default address for the S5PV210
# - Code now follows standard coding conventions
#
# Original author:
# Copyright (C) 2011 Homin Lee <suapapa@insignal.co.kr>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.

# need python-usb
import usb
import sys
import os
import struct
import time

def LOG(msg):
    print msg
    sys.stdout.flush()

def LOGE(msg):
    print >> sys.stderr, msg
    sys.stderr.flush()

def find_device(idVendor, idProduct):
    for bus in usb.busses():
        for device in bus.devices:
            if len(device.configurations) == 1 and \
                    device.idVendor == idVendor and \
                    device.idProduct == idProduct:
                return device
    return None

def send_data(device, epNum, data):
    handle = device.open()
    handle.claimInterface(0)
    LOG("Sending %d bytes..."%len(data))
    wroteLen = handle.bulkWrite(epNum, data, 5*1000)
    assert(wroteLen == len(data))

def checksum(data):
    sum = 0
    for byte in data:
        sum += ord(byte)
    sum &= 0xffff
    LOG("Checksum 0x%04x" % sum)
    return struct.pack('<H', sum)

def make_packet(filename, addr = 0xd0020000):
    data = open(filename, 'rb').read()
    LOG("Loaded %d bytes from \"%s\"" % (len(data), filename))
    header = struct.pack('<II', addr, len(data) + 10)
    return header + data + checksum(data)

if __name__ == '__main__':
    from optparse import OptionParser
    optPsr = OptionParser("Usage: %prog [-iXXXX:XXXX] your_binary.hex")
    optPsr.add_option('-d', '--id', type='string',
                    help="USB ID of target. in form of VID:PID")
    optPsr.add_option('-a', '--addr', type='string',
                    help="Destination address in memory in hex")
    optPsr.add_option('-l', '--loop', action='store_true',
                    help="Loop and wait for device presence")
    (opts, args) = optPsr.parse_args()

    if (not len(args) == 1) or (not os.path.exists(args[0])):
        LOGE("No file specified, or file does not exist");
        sys.exit(1)

    # SMDK's default vid and pid
    vid, pid = 0x04e8, 0x1234
    if opts.id:
        vid_pid = opts.id.split(':')
        vid, pid = map(lambda x: int(x, 16), vid_pid)

    addr = 0xd0020000
    if opts.addr:
        addr = int(opts.addr, 16)

    if opts.loop:
        done = False
        while not done:
            LOG("Waiting for USB device with ID %04x:%04x" % (vid, pid))

            while True:
                device = find_device(vid, pid)
                if device:
                    break
                time.sleep(0.25)

            LOG("Device found")

            time.sleep(0.25)
            
            packet = make_packet(args[0], addr)
            send_data(device, 2, packet)
            
            LOG("Finished")
            
            while find_device(vid, pid):
                time.sleep(0.25)

            LOG("Device disappeared")

    else:
        device = find_device(vid, pid)
        if not device:
            LOGE("Can't find device with ID %04x:%04x" % (vid, pid))
            sys.exit(1)

        LOG("Found device with ID %04X:%04X" % (vid, pid))
            
        packet = make_packet(args[0], addr)
        send_data(device, 2, packet)
            
        LOG("Finished")
        sys.exit()
