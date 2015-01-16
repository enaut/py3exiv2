# -*- coding: utf-8 -*-

# ******************************************************************************
#
# Copyright (C) 2008-2010 Olivier Tilloy <olivier@tilloy.net>
#
# This file is part of the pyexiv2 distribution.
#
# pyexiv2 is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# pyexiv2 is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with pyexiv2; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, 5th Floor, Boston, MA 02110-1301 USA.
#
# Authors: Olivier Tilloy <olivier@tilloy.net>
#          Mark Lee <pyexiv2@lazymalevolence.com>
#
# ******************************************************************************

import pyexiv2
from pyexiv2.utils import is_fraction, make_fraction

import unittest
import os.path
import datetime

import testutils


FRACTION = 'fraction'


class ReadMetadataTestCase(unittest.TestCase):

    """
    Test case on reading the metadata contained in a file.
    """

    def check_type_and_value(self, tag, etype, evalue):
        if etype == FRACTION:
            self.assert_(is_fraction(tag.value))
        else:
            self.assert_(isinstance(tag.value, etype))
        self.assertEqual(tag.value, evalue)

    def check_type_and_values(self, tag, etype, evalues):
        for value in tag.value:
            self.assert_(isinstance(value, etype))
        self.assertEqual(tag.value, evalues)

    def assertCorrectFile(self, filename, md5sum):
        """
        Ensure that the filename and the MD5 checksum match up.
        """
        self.assert_(testutils.CheckFileSum(filename, md5sum))

    def testReadMetadata(self):
        """
        Perform various tests on reading the metadata contained in a file.
        """
        # Check that the reference file is not corrupted
        filename = os.path.join('data', 'exiv2-bug540.jpg')
        filepath = testutils.get_absolute_file_path(filename)
        md5sum = 'c066958457c685853293058f9bf129c1'
        self.assertCorrectFile(filepath, md5sum)

        # Read the image metadata
        image = pyexiv2.ImageMetadata(filepath)
        image.read()

        # Exhaustive tests on the values of EXIF metadata
        exifTags = [('Exif.Image.ImageDescription', str, 'Well it is a smiley that happens to be green'),
                    ('Exif.Image.XResolution', FRACTION, make_fraction(72, 1)),
                    ('Exif.Image.YResolution', FRACTION, make_fraction(72, 1)),
                    ('Exif.Image.ResolutionUnit', int, 2),
                    ('Exif.Image.Software', str, 'ImageReady'),
                    ('Exif.Image.DateTime', datetime.datetime, datetime.datetime(2004, 7, 13, 21, 23, 44)),
                    ('Exif.Image.Artist', str, 'No one'),
                    ('Exif.Image.Copyright', str, ''),
                    ('Exif.Image.ExifTag', int, 226),
                    ('Exif.Photo.Flash', int, 80),
                    ('Exif.Photo.PixelXDimension', int, 167),
                    ('Exif.Photo.PixelYDimension', int, 140)]
        self.assertEqual(image.exif_keys, [tag[0] for tag in exifTags])
        for key, ktype, value in exifTags:
            self.check_type_and_value(image[key], ktype, value)

        # Exhaustive tests on the values of IPTC metadata
        iptcTags = [('Iptc.Application2.Caption', str, ['yelimS green faced dude (iptc caption)']),
                    ('Iptc.Application2.Writer', str, ['Nobody']),
                    ('Iptc.Application2.Byline', str, ['Its me']),
                    ('Iptc.Application2.ObjectName', str, ['GreeenDude']),
                    ('Iptc.Application2.DateCreated', datetime.date, [datetime.date(2004, 7, 13)]),
                    ('Iptc.Application2.City', str, ['Seattle']),
                    ('Iptc.Application2.ProvinceState', str, ['WA']),
                    ('Iptc.Application2.CountryName', str, ['USA']),
                    ('Iptc.Application2.Category', str, ['Things']),
                    ('Iptc.Application2.Keywords', str, ['Green', 'Smiley', 'Dude'])]
                    #('Iptc.Application2.Copyright', str, ['© 2004 Nobody'])]
                    #('Iptc.Application2.Copyright', bytes, [b'\xa9 2004 Nobody'])]
        self.assertEqual(image.iptc_keys, [tag[0] for tag in iptcTags])
        for key, ktype, values in iptcTags:
            self.check_type_and_values(image[key], ktype, values)

    def testReadMetadataXMP(self):
        filename = os.path.join('data', 'exiv2-bug540.jpg')
        filepath = testutils.get_absolute_file_path(filename)
        md5sum = '64d4b7eab1e78f1f6bfb3c966e99eef2'
        self.assertCorrectFile(filepath, md5sum)

        # Read the image metadata
        image = pyexiv2.ImageMetadata(filepath)
        image.read()

        xmpTags = [('Xmp.dc.Creator', list, ['Vincent Vande Vyvre']),
                   ('Xmp.dc.Description', dict, {'x-default': 'Communications'}),
                   ('Xmp.dc.Rights', dict, {'x-default': 'Vincent Vande Vyvre - www.oqapy.eu'}),
                   ('Xmp.dc.Source', str, 'www.oqapy.eu'),
                   ('Xmp.dc.Subject', list, ['Communications']),
                   ('Xmp.dc.Title', dict, {'x-default': 'Communications'}),
                   ('Xmp.exif.BrightnessValue', FRACTION, make_fraction(333, 1280)),
                   ('Xmp.exif.ColorSpace', int, 1),
                   ('Xmp.exif.DateTimeOriginal',
                    datetime.datetime,
                    datetime.datetime(2013, 8, 21, 15, 58, 28, tzinfo=pyexiv2.utils.FixedOffset())),
                   ('Xmp.exif.ExifVersion', str, '0203'),
                   ('Xmp.exif.ExposureBiasValue', FRACTION, make_fraction(-13, 20)),
                   ('Xmp.exif.ExposureProgram', int, 4),
                   ('Xmp.exif.FNumber', FRACTION, make_fraction(3, 5)),
                   ('Xmp.exif.FileSource', int, 0),
                   ('Xmp.exif.FlashpixVersion', str, '0100'),
                   ('Xmp.exif.FocalLength', FRACTION, make_fraction(53, 4)),
                   ('Xmp.exif.FocalPlaneResolutionUnit', int, 2),
                   ('Xmp.exif.FocalPlaneXResolution', FRACTION, make_fraction(3085, 256)),
                   ('Xmp.exif.FocalPlaneYResolution', FRACTION, make_fraction(3085, 256)),
                   ('Xmp.exif.ISOSpeedRatings', list, ['64']),
                   ('Xmp.exif.MeteringMode', int, 5),
                   ('Xmp.exif.PixelXDimension', int, 4608),
                   ('Xmp.exif.PixelYDimension', int, 2595),
                   ('Xmp.exif.SceneType', int, 0),
                   ('Xmp.exif.SensingMethod', int, 2),
                   ('Xmp.exif.ShutterSpeedValue', FRACTION, make_fraction(30827, 3245)),
                   ('Xmp.pdf.Keywords', str, 'Communications'),
                   ('Xmp.photoshop.AuthorsPosition', str, 'Photographer'),
                   ('Xmp.photoshop.CaptionWriter', str, 'Vincent Vande Vyvre'),
                   ('Xmp.photoshop.Category', str, 'BUS'),
                   ('Xmp.photoshop.City', str, 'Brussel'),
                   ('Xmp.photoshop.Country', str, 'Belgium'),
                   ('Xmp.photoshop.Credit', str, 'Vincent Vande Vyvre'),
                   ('Xmp.photoshop.DateCreated', datetime.date, datetime.date(2013, 8, 21)),
                   ('Xmp.photoshop.Headline', str, 'Communications'),
                   ('Xmp.photoshop.State', str, ' '),
                   ('Xmp.photoshop.SupplementalCategories', list, [u'Communications']),
                   ('Xmp.photoshop.Urgency', int, 5),
                   ('Xmp.tiff.Artist', str, 'Vincent Vande Vyvre'),
                   ('Xmp.tiff.BitsPerSample', list, [8]),
                   ('Xmp.tiff.Compression', int, 6),
                   ('Xmp.tiff.ImageLength', int, 400),
                   ('Xmp.tiff.ImageWidth', int, 600),
                   ('Xmp.tiff.Make', str, 'FUJIFILM'),
                   ('Xmp.tiff.Model', str, 'FinePix S4800'),
                   ('Xmp.tiff.Orientation', int, 1),
                   ('Xmp.tiff.ResolutionUnit', int, 2),
                   ('Xmp.tiff.Software', str, 'Oqapy 2.0')]
        #self.assertEqual(image.xmp_keys, [tag[0] for tag in xmpTags])
        for key, ktype, value in xmpTags:
            self.check_type_and_value(image[key], ktype, value)

