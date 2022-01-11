
from os import _exit
from PIL import Image, ImageOps
import pathlib
import math
import cv2
import numpy as np
from Draw_Track.dictostr import dictostr

_path = str(pathlib.Path().resolve()) + "/Draw_Track/images/"

_straight       = _path + "straight_v2.png"
_curve          = _path + "curve_v2.png"           
_intersection   = _path + "intersection_v2.png"
_startline      = _path + "start-end_v2.png"
_track          = _path + "track.png"

_cp = []

#default_track = ['start','left', 'left', 'straight', 'intersection', 'right', 'right', 'right', 'intersection', 'left']

def map_grid(dic):
    track = []
    track = dictostr(dic)
    rotation = 0 	#for the rotation of pieces
    
    #if len(track) > 0:
    #    print('yay ' + str(len(track)/2))
    #else:
    #    print('sucks, fall back to default...')
    #    track = default_track

    _dim = int(len(track)/2)
    w = 500
    h = 500
    grid = Image.new('RGB', size=(_dim*h, _dim*w), color='white')      #currently unknown dimensions of track -> max possible length & height
    i = 0
    y, x = round(_dim/2 - 0.5), round(_dim/2 - 0.5)
    minx, miny, maxx, maxy = x,y,0,0 
    for all in track:
        if track[i] == 'start':
            img = Image.open(_startline)
        elif track[i] == 'left':
            img = Image.open(_curve)        #-90 = clockwise; 90 = counter-clockwise
        elif track[i] == 'right':
            img = Image.open(_curve).rotate(-90)
        elif track[i] == 'straight':
            img = Image.open(_straight)
        elif track[i] == 'intersection':
            img = Image.open(_intersection)
        else:
            print("Error: Unkown piece")
        grid.paste(img.rotate(rotation), box=(y*h, x*w))
        #checkpoints(track[i], rotation, x,y)
        #if piece was curve -> rotate following pieces and direction
        if track[i] == 'left':
            rotation -= 90

        elif track[i] == 'right':
            rotation += 90
        y -= round(math.sin(math.radians(rotation)))
        x -= round(math.cos(math.radians(rotation)))
        i += 1
        
        if x < minx:
            minx = x
        elif x > maxx:
            maxx = x
        
        if y < miny:
            miny = y
        elif y > maxy:
            maxy = y

    maxx += 1
    maxy += 1
    grid = grid.crop((miny*w, minx*h, (maxy)*w, (maxx)*h))
    grid.thumbnail((800, 800))
    ImageOps.mirror(grid).save(_track)



def checkpoints():
    image = cv2.imread(_track,0)
  
    # threshold
    th, threshed = cv2.threshold(image, 100, 255, 
          cv2.THRESH_BINARY|cv2.THRESH_OTSU)
  
    # findcontours
    cnts = cv2.findContours(threshed, cv2.RETR_LIST, 
                    cv2.CHAIN_APPROX_SIMPLE)[-2]
  
    # filter by area
    s1 = 3
    s2 = 300
    xcnts = []
    for cnt in cnts:
        if s1<cv2.contourArea(cnt) <s2:
            peri = cv2.arcLength(cnt, True)
            approx = cv2.approxPolyDP(cnt, 0.04 * peri, True)
            if len(approx) > 2:
                #print(len(approx))
                if len(approx) == 3:
                    start = cnt
                xcnts.append(cnt)
                 
            
  
    # printing output
    #print("\nDots number: {}".format(len(xcnts)))
    out_images = np.array(xcnts)
    for c in xcnts:
        # compute the center of the contour
        M = cv2.moments(c)
        cX = int(M["m10"] / M["m00"])
        cY = int(M["m01"] / M["m00"])
        _cp.append((cX,cY))	

    #save start point
    
    M = cv2.moments(start)
    startX = int(M["m10"] / M["m00"])
    startY = int(M["m01"] / M["m00"])

    #sort checkpoint list from start to end of track
    cptrack = [(startX, startY)]
    (p0x, p0y) = cptrack[0]
    point = cptrack[0]


    while len(cptrack) < len(_cp) + 1:
        pd = 100000000
        cp = []
        
        if len(cptrack) == 1:                   #make dummy distance to estimated point
            px = p0x 
            py = p0y - 50
        else:                                   #calculate prediction point with the help of a vector from the last to the current point
            px = 2*p0x - cx
            py = 2*p0y - cy

        for a in _cp:                           #search closest point in the list of points 
            (p1x, p1y) = a
            dist1 = round(math.hypot(p1x - px, p1y - py))
            if pd > dist1 and a != cptrack[len(cptrack)-1]:     
                pd = dist1
                #print(pd)
                point = a
        (cx, cy) = (p0x, p0y)
        (p0x, p0y) = point
        cptrack.append(point)
    
    #visual control of the track
    #i=0
    #for all in cptrack:    
    #    cv2.putText(image, str(i), all, cv2.FONT_HERSHEY_SIMPLEX,
	#	0.5, (255, 255, 255), 2)
    #    i+=1
    #cv2.imshow("Image", image)
    #cv2.waitKey(0)

    return cptrack
