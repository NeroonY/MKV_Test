# -*- coding: UTF-8 -*-

import mkvtest
import unittest


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
		is_ok,_,_ = mkvtest.Check_for_WDTV(self.get_good_info())
		self.assertTrue(is_ok)

		is_ok,_,_ = mkvtest.Check_for_WDTV(self.get_bad_audio_info())
		self.assertFalse(is_ok)



if __name__ == "__main__":
	unittest.main()
