#!/usr/bin/env python3
import search


if __name__ == '__main__':
	search._search('/lib/libGL.so', 'glUniform1d')
	assert search._is_object_file('/lib/libGL.so') == True
	assert search._is_object_file('foo.a') == True
	assert search._is_object_file('bar.as') == False
	assert search._is_object_file('foobar.so.11') == True
