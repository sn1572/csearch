#!/usr/bin/env python3
import os, re
import subprocess as sub
import argparse


# Python utility for finding symbols in C/C++ shared object files

# Bash colors
RED = '\033[0;31m'
NC  = '\033[0m'


def _search(fname, token):
	try:
		out = sub.check_output('nm -D -C {} | grep -n {}'.format(fname, token),
			shell=1)
		out = out.decode('utf-8')
		out = out.split()
		for line in out:
			if token in line:
				print("{}{}{}: {}".format(RED, fname, NC, line))
	except sub.CalledProcessError:
		pass



def _is_object_file(fname):
	r = re.compile(r'\.(?P<extension>((so)|(a)|(o)))(\.|$)')
	m = r.search(fname)
	if m:
		return(True)
	return(False)


def _search_directory(dname, token):
	contents = os.listdir(dname)
	for thing in contents:
		thing = os.path.join(dname, thing)
		if _is_object_file(thing):
			_search(thing, token)


def main(name, token):
	if os.path.isfile(name):
		if _is_object_file(name):
			_search(name, token)
		else:
			raise TypeError("Must be an object file.")
	elif os.path.isdir(name):
		_search_directory(name, token)
	else:
		raise TypeError("Must be a directory or file.")


if __name__ == '__main__':
	descr = '''
	Utility for locating symbols in C/C++ object files (on Linux).
	'''

	parser = argparse.ArgumentParser(
		allow_abbrev=True,
		description=descr)
	parser.add_argument('--directory', '-d',
		action='store',
		type=str,
		default='.',
		help='Directory of object files to search')
	parser.add_argument('symbol',
		metavar='symbol',
		type=str,
		nargs='+',
		help='symbol to find')
	args = parser.parse_args()
	directory = os.path.abspath(args.directory)

	main(directory, args.symbol[0])
