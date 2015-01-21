# -*- coding: utf-8 -*-

import sys
import os

import datetime

import pyexiv2

from pyexiv2.metadata import ImageMetadata
from pyexiv2.xmp import XmpTag
from pyexiv2.iptc import IptcValueError

IMAGE = 'DSCF_0273.JPG'
IMAGE2 = 'Cyrillic.jpg'
IMAGE3 = 'exiv2.jpg'
IMAGE4 = 'gri_2008_r_3_4046.jpg'

def read_metadata():
    try:
        metadata = ImageMetadata(IMAGE)
        metadata.read()
    except Exception as why:
        print("Error in read metadata, reason:\n{0}".format(why))
        sys.exit()

    return metadata

def display_exif(data):
    for key in data.exif_keys:
        try:
            tag = data[key]
            print('%-45s%-11s%-20s\t%s' % (key, tag.type, tag.value, type(tag.value)))
        except Exception as why:
            print('Error: %s\n\t%s' %(key, why))

    return
    keys = sorted(data.exif_keys)
    key = keys.pop(0)
    txt = "EXIF = {'%s': %s,\n" %(key, data[key].value)
    tab = ' ' * 8
    for key in keys:
        txt = txt + "%s'%s': %s,\n" %(tab, key, data[key].value)
    txt = txt[:-2] + '}'
    print('type: %s, len: %s' %(type(txt), len(txt)))
    with open('exif_record', 'w') as outf:
        outf.write(txt)

def display_iptc(data):
    for key in data.iptc_keys:
        try:
            tag = data[key]
            print('%-45s%-11s%-20s\t%s' % (key, tag.type, tag.value, type(tag.value)))
        except Exception as why:
            print('Error: %s\n\t%s' %(key, why))

    return
    keys = sorted(data.iptc_keys)
    key = keys.pop(0)
    txt = "IPTC = {'%s': %s,\n" %(key, data[key].value)
    tab = ' ' * 8
    for key in keys:
        txt = txt + "%s'%s': %s,\n" %(tab, key, data[key].value)
    txt = txt[:-2] + '}'
    with open('iptc_record', 'w') as outf:
        outf.write(txt)

def display_xmp(data):
    xmps = {}
    for key in data.xmp_keys:
        try:
            tag = data[key]
            print('%-45s%-11s%-20s\t%s' % (key, tag.type, tag.value, type(tag.value)))
            xmps[key] = tag.value
        except Exception as why:
            print('Error: %s\n\t%s' %(key, why))
    return

    keys = sorted(data.xmp_keys)
    key = keys.pop(0)
    txt = "XMP = {'%s': %s,\n" %(key, data[key].value)
    tab = ' ' * 7
    for key in keys:
        txt = txt + "%s'%s': %s,\n" %(tab, key, data[key].value)
    txt = txt[:-2] + '}'
    with open('xmp_record', 'w') as outf:
        outf.write(txt)

if __name__ == '__main__':
    data = read_metadata()
    print('\n ==================================  EXIF  ========================\n')
    display_exif(data)
    print('\n ==================================  IPTC  ========================\n')
    display_iptc(data)
    print('\n ==================================  XMP  ========================\n')

    key = 'Xmp.oqapy.lastEditDate'
    data[key] = datetime.datetime.today()


    print('Create new xmp ...')
    # Create a new namespace
    #pyexiv2.xmp.register_namespace('www.oqapy.eu/', 'oqapy')
    #key = 'Xmp.oqapy.lastEditDate'
    #val = 'Last edit today'
    # We can't assign directly the value, we must create the XmpTag before
    #data[key] = pyexiv2.XmpTag(key, val)

    data.write()
    display_xmp(data)
    print('=====================================================================')

    sys.exit()
    with open('exif_record', 'r') as inf:
        for l in inf.readlines():
            print(l, end='')




















