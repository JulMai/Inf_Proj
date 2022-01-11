import os
import sys

currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(os.path.dirname(currentdir))
sys.path.append(parentdir)

from Track.trackPiece import TrackPiece

d = {'003300': None,
	 '011837': None, 
	 '021836': None, 
	 '031835': None, 
	 '041837': None, 
	 '051836': None, 
	 '061835': None, 
	 '075147': None, 
	 '085146': None, 
	 '095145': None, 
	 '101004': None, 
	 '111800': None, 
	 '121801': None, 
	 '132000': None, 
	 '142001': None, 
	 '151700': None, 
	 '161701': None, 
	 '171000': None, 
	 '181737': None, 
	 '191736': None, 
	 '201735': None, 
	 '213400': None}

def dictostr(dic):
	track = []
	if len(dic) == 0:
		dic = d
	c = 0
	for key in dic:
		t = int(key[2:4])
		trackpart = TrackPiece.get_TrackPieceType(t)
		
		if trackpart == 'curve':
			if int(key[4:]) > 15:
				trackpart = 'right'
			else:
				trackpart = 'left'
		elif trackpart == 'finish':
			break

		if len(track) > 0:
			if trackpart == track[len(track)-1]:
				c += 1
			else:
				c = 0
		if trackpart == "left":
			mod = 2
		else:
			mod = 3
		#print(str(c) + " " + str(mod))
		if c%mod == 0:
			track.append(trackpart)

	#print(track)
	return track