#!/usr/bin/env python

"""
Generate QR codes for mote IDs
"""

import os
import sys

try:
	import qrcode
	import qrcode.image.svg
except ImportError:
	print('Could not import qrcode.')
	sys.exit(1)

def validate (rawid):
	rawid = rawid.strip()
	# see if it just nicely formated
	bytes = rawid.split(':')
	if len(bytes) == 8:
		for b in bytes:
			try:
				int(b, 16)
			except:
				print('Chunk {} in {} not hex!'.format(b, rawid))
				return None
		return rawid.upper()
	elif len(bytes) == 1:
		try:
			int(rawid, 16)
		except:
			print('ID not hex: {}'.format(rawid))
			return None
		return (':'.join([rawid[i:i+2] for i in range(0, 16, 2)])).upper()

	else:
		print('Invalid ID: {}'.format(rawid))
		return None


# List of ids to make QR codes of
ids = []

if len(sys.argv) != 2:
	print('Usage: {} <64 bid id|file of ids>'.format(__file__))
	sys.exit(1)

if os.path.exists(sys.argv[1]):
	with open(sys.argv[1]) as f:
		for l in f:
			nodeid = validate(l)
			if nodeid:
				ids.append(nodeid)
else:
	nodeid = validate(sys.argv[1])
	if nodeid:
		ids.append(nodeid)

if len(ids) == 0:
	print('No IDs to make QR codes of!')
	sys.exit(1)

for nodeid in ids:
	img = qrcode.make(nodeid, image_factory=qrcode.image.svg.SvgPathImage, border=0)
	img.save('{}.svg'.format(nodeid.replace(':', '')))


