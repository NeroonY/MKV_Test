# -*- coding: UTF-8 -*-
#include some encoding vodoo for windows cyrillic work

import os, sys, fnmatch
import subprocess 
import itertools

# TODO:
# vorbis audio(Codec ID: A_VORBIS) - нет строки DUR_STR, 
# Продолжительность по умолчанию: 33.000ms (30.303 кадров/полей в секунду для видеодорожки) - для видеодорожки плохо
# аргументы командной строки


SHOW_FULL_INFO = False
# SHOW_FULL_INFO = True

CONSOLE_ENCODING = "cp1251" #win console

MKV_MASK = "*.mkv"

VIDEO_FOLDER = r"."
VIDEO_FOLDER = r"D:\video\cinema"
# VIDEO_FOLDER = ur"G:\Video\Cinema\Bad Source"

MKVINFO_PATH = r"D:\Programs\mkvtoolnix\mkvinfo.exe"

# MISC_ATTRIBS= ' -r temp.txt --output-charset UTF-8 --ui-language "EN"'
MISC_ATTRIBS= ' --output-charset UTF-8 --ui-language "EN"'

cmd_pattern = MKVINFO_PATH + MISC_ATTRIBS + ' "%s"'

#
APP_STR = "| + Writing application: "
TRACK_STR = "|  + Track type: "
AUDIO_TRACK_STR = "|  + Track type: audio"
DUR_STR = "|  + Default duration: "

BAD_VERSION = "mkvmerge v4.1.0"

GOOD_TIMING = "32.000ms"



class mkv_short_info:
	def __init__(self, fname):
		self.ver = ""
		self.audio_tracks = []
		self.filename = fname

	def Fill_by_mkvinfo_out(self, output):
		ilines = iter(output.readlines())
		
		for l in ilines:
			# print l,
			if l.startswith(APP_STR):
				#%APP_STR% mkvmerge %ver% (%nickname ver%) %other stuff%
				self.ver = l[len(APP_STR):].split("(")[0]
				# print l, self.ver
				break
		
		#audio tracks
		for l in ilines:
			# zprint (l)
			if l.startswith(AUDIO_TRACK_STR):
				for ll in ilines:
					if ll.startswith(DUR_STR):
						self.audio_tracks.append(ll[len(DUR_STR):].split("(")[0])
						break
			# print l,
		# for track in mkv_info.audio_tracks:
		# 	print track

#support for work in sublime and win-console
def zprint(arg):
	try:
		print arg
	except:
		print arg.encode('utf8') 

def Get_mkv_info(full_fname):
	mkv_info = mkv_short_info(os.path.basename(full_fname))

	cmd = cmd_pattern % full_fname
	# print type(cmd)
	# zprint(cmd)

	PIPE = subprocess.PIPE
	proc = subprocess.Popen(cmd.encode(CONSOLE_ENCODING) , shell=True, stdin=PIPE, stdout=PIPE,
    						stderr=subprocess.STDOUT)
	
	mkv_info.Fill_by_mkvinfo_out(proc.stdout)

	return mkv_info

def Check_files(files_info):
	for info in files_info:
		ver_ok = not (BAD_VERSION in info.ver)
		tracks_ok = info.audio_tracks and all(map(lambda t: GOOD_TIMING in t, info.audio_tracks))

		if ver_ok and tracks_ok:
			zprint("OK " + info.filename)
		else:
			zprint("BAD " + info.filename)

			if not ver_ok:
				print "   ver: "+ info.ver
			if not tracks_ok:
				if not info.audio_tracks:
					print "   no tracks"
				else:
					for track in info.audio_tracks:
						print "   track: " + track

def Full_Print(files_info):
	for inf in files_info:
		zprint(inf.filename)
		print inf.ver
		for track in inf.audio_tracks:
			zprint(track)
		print "------------------"


if __name__ == "__main__":

	files_info = []

	# for f in itertools.islice(os.listdir(VIDEO_FOLDER), 3):
	for f in os.listdir(unicode(VIDEO_FOLDER)):
		if fnmatch.fnmatch(f, MKV_MASK):
			files_info.append(Get_mkv_info(os.path.join(VIDEO_FOLDER,f)))
	
	# files_info=[]
	# files_info.append(Get_mkv_info(ur"D:\video\cinema\Живая сталь.2011.mkv"))

	Check_files(files_info)

	if SHOW_FULL_INFO:
		Full_Print(files_info)



