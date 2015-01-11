# -*- coding: utf-8 -*-

# configure.py
#
# Author: Vincent Vande Vyvre <vincent.vandevyvre@oqapy.eu>
#

import sys
import os
import site
from distutils.sysconfig import get_python_inc, get_python_lib
import subprocess

if sys.version_info[0] < 3:
    sys.exit('ERROR: py3exiv2 requires Python ≥ 3.3')

def show_help():
    help = """
    configure.py\n
    Script to configure the compilation and the installation of py3exiv2.\n
    This script require Python >= 3.3\n
    Usage:  python3 configure.py [OPTION]\n
    Options:
    -h               Show this info and exit.
    --libboost=FILE  Define the path of libboost_python-3\n
"""
    print(help)
    sys.exit()

def get_libboost_name():
    """Returns the name of the lib libboost_python 3

    """
    # libboost libs are provided without .pc files, so we can't use pkg-config
    rep = subprocess.Popen(['find', '/usr/lib/', '-name', 
                            'libboost_python*'], 
                            stdout=subprocess.PIPE).communicate()[0]
    if not rep:
        return

    # rep is type bytes
    libs = rep.decode(sys.getfilesystemencoding()).split('\n')
    for l in libs:
        _, l = os.path.split(l)
        if l.endswith('.so'):
            l = l[:-3]
            if '-py3' in l:
                return l.replace('libboost', 'lboost')

def write_build_file(dct):
    dct['wrp'] = 'exiv2wrapper'
    dct['wrpy'] = 'exiv2wrapper_python'
    dct['flags'] = '-c -fPIC'
    txt = """#!/bin/sh

if [ "$1" = "-i" ]; then
    echo "install libexiv2python.so to %(dist)s"
    cp build/libexiv2python.so %(dist)s/libexiv2python.so
    test -d %(pyexiv)s || mkdir -p %(pyexiv)s
    sudo cp src/pyexiv2/__init__.py %(pyexiv)s/__init__.py
    sudo cp src/pyexiv2/exif.py %(pyexiv)s/exif.py
    sudo cp src/pyexiv2/iptc.py %(pyexiv)s/iptc.py
    sudo cp src/pyexiv2/metadata.py %(pyexiv)s/metadata.py
    sudo cp src/pyexiv2/preview.py %(pyexiv)s/preview.py
    sudo cp src/pyexiv2/utils.py %(pyexiv)s/utils.py
    sudo cp src/pyexiv2/xmp.py %(pyexiv)s/xmp.py

else
    test -d build || mkdir -p build
    g++ -o build/%(wrp)s.os %(flags)s -I/usr/include/python3.4m src/%(wrp)s.cpp
    g++ -o build/%(wrpy)s.os %(flags)s -I/usr/include/python3.4m src/%(wrpy)s.cpp
    g++ -o build/libexiv2python.so -shared build/%(wrp)s.os build/%(wrpy)s.os -%(boost)s -lexiv2
    echo "build/libexiv2python.so compiled, use ./build.sh -i to install"

fi""" % dct

    with open('build.sh', 'w') as outf:
        outf.write(txt)

    os.system("chmod +x build.sh")

if __name__ == '__main__':
    dct = {}
    for arg in sys.argv[1:]:
        if arg == '-h':
            show_help()

        elif arg.startswith('--libboost='):
            path = arg.split('=')[1].strip()
            if not os.path.isfile(path):
                print('No such file: %s' % path)
                sys.exit()

            else:
                dct['boost'] = path

    if not dct:
        dct['boost'] = get_libboost_name()
        if dct['boost'] is None:
            print("Can't find libboost_python-3, use the option --libboost=FILE")
            sys.exit()

    dct['py'] = get_python_inc()
    dct['dist'] = get_python_lib()
    dct['pyexiv'] = dct['dist'] + '/pyexiv2'
    write_build_file(dct)



