# -*- coding: UTF-8 -*-

import mkvtest
import unittest
import os,sys, fnmatch

TEST_FOLDER_GOOD  = ur".\tests\good"
TEST_FOLDER_BAD  = ur".\tests\bad"

TEST_FILE = ur".\tests\good\good1.log"
LOG_MASK = "*.log"

class mkv_short_info_TestCase(unittest.TestCase):
	def test_init(self):
		TEST_FILE = "test.mkv"
		info = mkvtest.mkv_short_info(TEST_FILE)

		self.assertTrue(len(info.audio_tracks)==0)
		self.assertEqual(info.filename, TEST_FILE)

	def get_good_info(self):
		info = mkvtest.mkv_short_info("TEST_FILE")
		info.audio_tracks.append("32.000ms ")
		info.audio_tracks.append("32.000ms ")
		info.ver = "mkvmerge v5.8.0 "
		return info

	def get_bad_audio_info(self):
		info = mkvtest.mkv_short_info("TEST_FILE")
		info.audio_tracks.append("28.000ms ")
		info.ver = "mkvmerge v5.8.0 "
		return info

	def test_Check_for_WDTV(self):
		is_ok,_ = mkvtest.Check_for_WDTV(self.get_good_info())
		self.assertTrue(is_ok)

		is_ok,_ = mkvtest.Check_for_WDTV(self.get_bad_audio_info())
		self.assertFalse(is_ok)

	def test_check_from_good_log(self):
		for fname in os.listdir((TEST_FOLDER_GOOD)):
				if fnmatch.fnmatch(fname, LOG_MASK):
					# print fname	
					info = mkvtest.Read_mkv_info(os.path.join(TEST_FOLDER_GOOD,fname))
					is_ok,_ = mkvtest.Check_for_WDTV(info)
					self.assertTrue(is_ok, fname)

						

	def test_check_from_bad_log(self):
		for fname in os.listdir((TEST_FOLDER_BAD)):
				if fnmatch.fnmatch(fname, LOG_MASK):
					# print fname
					info = mkvtest.Read_mkv_info(os.path.join(TEST_FOLDER_BAD,fname))
					is_ok,_ = mkvtest.Check_for_WDTV(info)
					# mkvtest.Print_error_descr(info, descr)
					self.assertFalse(is_ok,fname)						

		


if __name__ == "__main__":
	unittest.main()
