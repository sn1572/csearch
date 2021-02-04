#!/usr/bin/env python3
import csearch as c


if __name__ == '__main__':
	c._search('/lib/libGL.so', 'glUniform1d')
	assert c._is_object_file('/lib/libGL.so') == True
	assert c._is_object_file('foo.a') == True
	assert c._is_object_file('bar.as') == False
	assert c._is_object_file('foobar.so.11') == True
