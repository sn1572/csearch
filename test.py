#!/usr/bin/env python3
import csearch as c
import unittest


class Test_Type_Check_Funs(unittest.TestCase):

	def test_is_object_file(self):
		self.assertEqual(c._is_object_file('/lib/libGL.so'), True)
		self.assertEqual(c._is_object_file('foo.a'), True)
		self.assertEqual(c._is_object_file('bar.as'), False)
		self.assertEqual(c._is_object_file('foobar.so,'), False)
		self.assertEqual(c._is_object_file('no_extension'), False)
		self.assertEqual(c._is_object_file('shared_object.so'), True)
		# dll's are not currently supported
		self.assertEqual(c._is_object_file('windows\\object.dll'), False)
		self.assertEqual(c._is_object_file('windows\\path\\to\\some.a'), True)

	def test_is_c_header(self):
		self.assertEqual(c._is_c_header('test.h'), True)
		self.assertEqual(c._is_c_header('test.hpp'), True)
		self.assertEqual(c._is_c_header('something.h.1'), False)
		self.assertEqual(c._is_c_header('definitely_wrong.asdf'), False)
		self.assertEqual(c._is_c_header('no_file_extension'), False)
		self.assertEqual(c._is_c_header('path/to/header.h'), True)
		self.assertEqual(c._is_c_header('unholy\\windows\\path\\to\\header.hpp'), True)

	def test_is_c_source(self):
		self.assertEqual(c._is_c_source('definitely_c_source.c'), True)
		self.assertEqual(c._is_c_source('linux/path/to/source.cu'), True)
		self.assertEqual(c._is_c_source('windows\\path\\to\\source.cpp'), True)
		self.assertEqual(c._is_c_source('negative_example.py'), False)
		self.assertEqual(c._is_c_source('no_file_extension'), False)
		self.assertEqual(c._is_c_source('invalid/path/'), False)
		self.assertEqual(c._is_c_source('trailing_characters.c.deb'), False)


if __name__ == '__main__':
	unittest.main()
