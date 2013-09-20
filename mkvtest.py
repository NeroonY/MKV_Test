# -*- coding: UTF-8 -*-
#include some encoding vodoo for windows cyrillic work

import os, sys, fnmatch
import subprocess 
import itertools
from config import * 

# TODO:
# vorbis audio(Codec ID: A_VORBIS) - нет строки DUR_STR, 
# Продолжительность по умолчанию: 33.000ms (30.303 кадров/полей в секунду для видеодорожки) - для видеодорожки плохо
# аргументы командной строки


SHOW_FULL_INFO = False
SHOW_FULL_INFO = True

CONSOLE_ENCODING = "cp1251" #win console

MKV_MASK = "*.mkv"

# MISC_ATTRIBS= ' -r temp.txt --output-charset UTF-8 --ui-language "EN"'
MISC_ATTRIBS= ' --output-charset UTF-8 --ui-language "EN"'

cmd_pattern = MKVINFO_PATH + MISC_ATTRIBS + ' "%s"'

#mkvinfo output patterns
APP_STR = "| + Writing application: "
TRACK_STR = "| + A track"
AUDIO_TRACK_STR = "|  + Track type: audio"
DUR_STR = "|  + Default duration: "
FISRT_LEVEL_STR = "|+"
SECOND_LEVEL_STR = "| +"

#Checking values
BAD_VERSION = "mkvmerge v4.1.0"
GOOD_TIMING = "32.000ms"
COMPRESSION_SIGN = "+ Content compression"



class mkv_short_info:
	def __init__(self, fname):
		self.ver = ""
		self.audio_tracks = []
		self.filename = fname
		self.is_compression_titles = False

	def Fill_by_mkvinfo_out(self, output):
		ilines = iter(output.readlines())
		
		for l in ilines:
			# print l,
			if l.startswith(APP_STR):
				#%APP_STR% mkvmerge %ver% (%nickname ver%) %other stuff%
				self.ver = l[len(APP_STR):].split("(")[0]
				# print l, self.ver
				break
		
		#tracks
		for l in ilines:
			# zprint (l)
			
			if l.startswith(AUDIO_TRACK_STR):
				#audio track
				for ll in ilines:
					if ll.startswith(DUR_STR):
						self.audio_tracks.append(ll[len(DUR_STR):].split("(")[0])
						# break
					if ll.startswith(FISRT_LEVEL_STR) or ll.startswith(SECOND_LEVEL_STR):
						break
					if COMPRESSION_SIGN in ll:
						self.is_compression_titles  = True	

			# print l,
		# for track in mkv_info.audio_tracks:
		# 	print track

	def Print(self):
		zprint(self.filename)
		print self.ver
		if self.is_compression_titles:
			print "compression titles"
		else:
			print "no compression"

		for track in self.audio_tracks:
			zprint(track)


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

def Read_mkv_info(full_fname):
	with open(full_fname) as f:
		mkv_info = mkv_short_info(os.path.basename(full_fname))
		mkv_info.Fill_by_mkvinfo_out(f)

	return mkv_info

def Check_for_WDTV(file_info):
	ver_ok = not (BAD_VERSION in file_info.ver)
	tracks_ok = file_info.audio_tracks and all(map(lambda t: GOOD_TIMING in t, file_info.audio_tracks))
	compression_ok = not file_info.is_compression_titles
	is_ok = ver_ok and tracks_ok and compression_ok

	full_info = {}
	full_info["ver_ok"] = ver_ok
	full_info["tracks_ok"] = tracks_ok
	full_info["compression_ok"] = compression_ok

	return is_ok, full_info

def Print_error_descr(info, res_descr):

		if not res_descr.get("ver_ok",True):
			print "   ver: "+ info.ver
		if not res_descr.get("tracks_ok",True) :
			if not info.audio_tracks:
				print "   no tracks"
			else:
				for track in info.audio_tracks:
					print "   track: " + track
		if not res_descr.get("compression_ok",True) :
			print "   compression titles"


def Check_files(files_info):
	for info in files_info:
		is_ok, res_descr = Check_for_WDTV(info)

		if is_ok:	
			zprint("OK " + info.filename)
		else:
			zprint("BAD " + info.filename)

		Print_error_descr(info,res_descr)


def Full_Print(files_info):
	print "\n==================================================="
	for inf in files_info:
		inf.Print()
		print "------------------"


if __name__ == "__main__":

	files_info = []

	# for f in itertools.islice(os.listdir(VIDEO_FOLDER), 3):
	for f in os.listdir(unicode(VIDEO_FOLDER)):
		if fnmatch.fnmatch(f, MKV_MASK):
			files_info.append(Get_mkv_info(os.path.join(VIDEO_FOLDER,f)))

	for f in os.listdir(unicode(VIDEO_FOLDER)):	
		if fnmatch.fnmatch(f, "*.log"):
			print f
			files_info.append(Read_mkv_info(os.path.join(VIDEO_FOLDER,f)))
	
	# files_info=[]
	# files_info.append(Get_mkv_info(ur"D:\video\cinema\Живая сталь.2011.mkv"))

	Check_files(files_info)

	if SHOW_FULL_INFO:
		Full_Print(files_info)



