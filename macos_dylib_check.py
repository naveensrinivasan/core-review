#!/usr/bin/env python3
# similar to contrib/devtools/symbol-check.py
# python3 macos_dylib_check.py src/qt/bitcoin-qt

import subprocess
import sys
import os
from typing import List

OTOOL_CMD = os.getenv('OTOOL', '/usr/bin/otool')

# Current for master 05c23488c2ce6f415ced607dca7e74a27e0200b5
# SystemConfiguration and CFNetwork required by wallet (payment server)
ALLOWED_LIBRARIES = {
	'AppKit', # user interface
	'ApplicationServices', # common application tasks.
	'Carbon', # deprecated c back-compat API
	'CFNetwork', # network services
	'CoreFoundation', # low level func, data types
	'CoreGraphics', # 2D rendering
	'CoreServices', # operating system services
	'CoreText', # interface for laying out text and handling fonts.
	'Foundation', # base layer functionality for apps/frameworks
	'ImageIO', # read and write image file formats.
	'IOKit', # user-space access to hardware devices and drivers.
	'libc++.1.dylib', # C++ Standard Library
	'libobjc.A.dylib', # Objective-C runtime library
	'libSystem.B.dylib', # libc, libm, libpthread, libinfo
	'SystemConfiguration', # network configuration
}

def read_libraries(filename) -> List[str]:
	p = subprocess.Popen([OTOOL_CMD, '-L', filename], stdout=subprocess.PIPE, 
		stderr=subprocess.PIPE, stdin=subprocess.PIPE, universal_newlines=True)
	(stdout, stderr) = p.communicate()
	if p.returncode:
		raise IOError('Error opening {}', filename)
	libraries = []
	for line in stdout.splitlines():
		tokens = line.split()
		# skip line with executable name
		if len(tokens) is 1: continue
		libraries.append(tokens[0].split('/')[-1])
	return libraries

if __name__ == '__main__':
	retval = 0
	for dylib in read_libraries(sys.argv[1]):
		if dylib not in ALLOWED_LIBRARIES:
			print('{} is not in ALLOWED_LIBRARIES!'.format(dylib))
			retval = 1
	sys.exit(retval)