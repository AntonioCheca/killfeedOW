### This program is used as "python killfeedOW video start end"
### video is an overwatch video that must be on the same folder as this file
### start and end are optional arguments, they are integers and the program will search on the killfeed from the second "start" to the second "end"
### I have tested it with python 2.7.6
### The code is uploaded on github.com/AntonioCheca/killfeedOW


import numpy as np
import cv2
import math
import sys

if len(sys.argv) < 2 or len(sys.argv) > 4 or len(sys.argv) == 3 or ((len(sys.argv) == 4) and int(sys.argv[2]) >= int(sys.argv[3])):
	print "### This program is used as 'python killfeedOW video start end'"
	print "### video is an overwatch video that must be on the same folder as this file"
	print "### start and end are optional arguments, they are integers and the program will search on the killfeed from the second 'start' to the second 'end', therefore, start < end"
	sys.exit("Wrong arguments")




#absPathString is the name of the folder with the template faces
absPathString = "feedcharacters"
def absPath(x):
	return absPathString + "/" + x 

def enemy(x):
	return x + "EN.png"

def friendly(x):
	return x + "FR.png"

def undoMaps(x):
	y = x.split('/')[1]
	return y.split('.')[0]

	

characters = ["turret", "mecha", "ana", "bastion", "dva", "genji", "hanzo", "junkrat", "lucio", "mccree", "mei", "mercy", "orisa", "pharah", "reaper", "reinhardt", "roadhog",
"soldier", "sombra", "symmetra", "torbjorn", "tracer", "widowmaker", "winston", "zarya", "zenyatta"]

characters = map(absPath, characters)
charNames = list(set().union(map(enemy, characters),map(friendly,characters)))

cap = cv2.VideoCapture(sys.argv[1])
	
#The templates were saved on a screenshot of 1680x945 px, so we need to scale them if the video hasn't this resolution
width_or = 1680
height_or = 945
scale_w = cap.get(3)*1.0/width_or
scale_h = cap.get(4)*1.0/height_or

#The time to wait for a feed to automatically disappear is 8 seconds
frames_to_wait = cap.get(5)*8
frames_per_sec = cap.get(5)

#If the video has 0 width, it means the name of the video was wrong
last_frame = -1
first_frame = 1
if cap.get(3) == 0.0:
	sys.exit("The argument " + sys.argv[1] + " isn't the name of a video on the folder.\nPlease, check again, remember it has to contain the file extension ( .flv, .mp4, etc.)")
if len(sys.argv) == 4:
	first_frame = int(sys.argv[2]) * frames_per_sec
	cap.set(1,first_frame)
	end = int(sys.argv[3])
	last_frame = frames_per_sec * end + 1

#Returns False when l1 and l2 are a feed found earlier, or are characters of the same team (unless one of them is mercy, in that case it's allowed because of the rez)
def isNotADouble(global_log, frame_count, l1, l2):
	boolean = True
	rez1 = "mercyFR"
	rez2 = "mercyEN"
	if l1[len(l1)-2:len(l1)-1] == l2[len(l2)-2:len(l2)-1] and l1 != rez1 and l2 != rez1 and l1 != rez2 and l2 != rez2:
		return False
	for g in global_log:
		if (abs(frame_count - g[2]) < frames_to_wait) and ((l1 == g[0] and l2 == g[1]) or (l1 == g[1] and l2 == g[0])):
			boolean = False
		if not boolean:
			break
	return boolean	

def readImage(x):
	temp = cv2.imread(x,1)
	return (x,cv2.resize(temp,None,fx=scale_w, fy=scale_h, interpolation = cv2.INTER_AREA))

#We read the template images of the faces and save them on a vector
template_v = map(readImage, charNames)

ret, frame = cap.read()

#frame is the actual frame being read, and frame_count the number
#global_log is where the actual killfeed is saved
#threshold is the similarity between the template faces (the ones on feedcharacters) and the image on the screen being showed to be detected as the same

c,w,h = frame.shape[::-1]
beg_frame = (2*w/3-1,1)
end_frame = (w-1,h/2-1)
global_log = []
frame_count = first_frame
threshold = 0.85
teamfight = False


while(cap.isOpened() and ((last_frame == -1) or frame_count <= last_frame)):

	#If the program detects faces (there is a teamfight going on), it reads a frame per 1/2 sec. If doesn't detect anything on screen, reads a frame per 2 sec
	if not teamfight:
		r = int(frames_per_sec*2)
	else:
		r = int(math.ceil(frames_per_sec/2))

	for i in range(r):
		if cap.isOpened():
			frame_count = frame_count + 1
			ret, frame = cap.read()

	#We only need the top right corner of the screen
	frame = frame[beg_frame[1]:end_frame[1], beg_frame[0]:end_frame[0]]
	log = set()
	for name_temp in template_v:

		name = name_temp[0]
		template = name_temp[1]
		c, w, h = template.shape[::-1]

		res = cv2.matchTemplate(frame,template,cv2.TM_SQDIFF_NORMED)
		
		loc = np.where( res <= 1-threshold)
		found = len(zip(*loc[::-1])) > 0
		#For each face detected, we make a log of the name, the y axis and the x axis
		for pt in zip(*loc[::-1]):
			log.add((undoMaps(name), pt[1], pt[0]))
	
	#Uncomment the next line if you want to see the speed of the program		
	cv2.imshow('frame', frame[1:frame.shape[0],1:frame.shape[1]])
	print frame_count
	teamfight = len(log) > 0
	for l in log:
		for l2 in log:
			if abs(l2[1]-l[1]) <= w/2 and l[0] != l2[0] and isNotADouble(global_log, frame_count, l[0], l2[0]):
				#For each face detected before, we make a global log (the actual killfeed) only under some conditions, explained on the 'isNotADouble' function
				#We use the x axis of the point where we found the faces to see which one is the killer, and which one is the killed
				if l[2] < l2[2]:
					global_log.append((l[0],l2[0], frame_count))
				else:
					global_log.append((l2[0],l[0], frame_count))

	if cv2.waitKey(1) & 0xFF == ord('q'):
		break
for l in global_log:
	print l
cap.release()
cv2.destroyAllWindows()
