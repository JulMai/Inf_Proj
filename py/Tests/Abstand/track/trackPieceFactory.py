from track.trackPiece import TrackPiece

def get_TrackPiece(id):
    return {
        'straight'      : get_StraightPiece(id),
        'curve'         : get_CurvePiece(id),
        'start'         : get_StartPiece(id),
        'finish'        : get_FinishPiece(id)
        'intersection'  : get_IntersectionPiece(id),
    }.get(TrackPiece.get_TrackPieceType(id), None)

def get_CurvePiece(id):
    lane00= [ 0, 1 ]
    lane01= [ 2, 3 ]
    lane02= [ 4, 5 ]
    lane03= [ 6, 7 ]
    lane04= [ 8, 9 ]
    lane05= [ 10, 11 ]
    lane06= [ 12, 13 ]
    lane07= [ 14, 15 ]
    lane08= [ 16, 17 ]
    lane09= [ 18, 19 ]
    lane10= [ 20, 21, 22 ]
    lane11= [ 23, 24, 25 ]
    lane12= [ 26, 27, 28 ]
    lane13= [ 29, 30, 31 ]
    lane14= [ 32, 33, 34 ]
    lane15= [ 35, 36, 37 ]
    coordinates = []
    coordinates.append(lane00)
    coordinates.append(lane01)
    coordinates.append(lane02)
    coordinates.append(lane03)
    coordinates.append(lane04)
    coordinates.append(lane05)
    coordinates.append(lane06)
    coordinates.append(lane07)
    coordinates.append(lane08)
    coordinates.append(lane09)
    coordinates.append(lane10)
    coordinates.append(lane11)
    coordinates.append(lane12)
    coordinates.append(lane13)
    coordinates.append(lane14)
    coordinates.append(lane15)
    return TrackPiece(id, 'curve', coordinates)

def get_StraightPiece(id):
    lane00= [ 0, 1, 2 ]
    lane01= [ 3, 4, 5 ]
    lane02= [ 6, 7, 8 ]
    lane03= [ 9, 10, 11 ]
    lane04= [ 12, 13, 14 ]
    lane05= [ 15, 16, 17 ]
    lane06= [ 18, 19, 20 ]
    lane07= [ 21, 22, 23 ]
    lane08= [ 24, 25, 26 ]
    lane09= [ 27, 28, 29 ]
    lane10= [ 30, 31, 32 ]
    lane11= [ 33, 34, 35 ]
    lane12= [ 36, 37, 38 ]
    lane13= [ 39, 40, 41 ]
    lane14= [ 42, 43, 44 ]
    lane15= [ 45, 46, 47 ]
    coordinates = []
    coordinates.append(lane00)
    coordinates.append(lane01)
    coordinates.append(lane02)
    coordinates.append(lane03)
    coordinates.append(lane04)
    coordinates.append(lane05)
    coordinates.append(lane06)
    coordinates.append(lane07)
    coordinates.append(lane08)
    coordinates.append(lane09)
    coordinates.append(lane10)
    coordinates.append(lane11)
    coordinates.append(lane12)
    coordinates.append(lane13)
    coordinates.append(lane14)
    coordinates.append(lane15)
    return TrackPiece(id, 'straight', coordinates)

def get_FinishPiece(id):
    lane00= [ 0, 1 ]
    lane01= [ 2, 3 ]
    lane02= [ 4, 5 ]
    lane03= [ 6, 7 ]
    lane04= [ 8, 9 ]
    lane05= [ 10, 11 ]
    lane06= [ 12, 13 ]
    lane07= [ 14, 15 ]
    lane08= [ 16, 17 ]
    lane09= [ 18, 19 ]
    lane10= [ 20, 21 ]
    lane11= [ 22, 23 ]
    lane12= [ 24, 25 ]
    lane13= [ 26, 27 ]
    lane14= [ 28, 29 ]
    lane15= [ 30, 31 ]
    coordinates = []
    coordinates.append(lane00)
    coordinates.append(lane01)
    coordinates.append(lane02)
    coordinates.append(lane03)
    coordinates.append(lane04)
    coordinates.append(lane05)
    coordinates.append(lane06)
    coordinates.append(lane07)
    coordinates.append(lane08)
    coordinates.append(lane09)
    coordinates.append(lane10)
    coordinates.append(lane11)
    coordinates.append(lane12)
    coordinates.append(lane13)
    coordinates.append(lane14)
    coordinates.append(lane15)
    return TrackPiece(id, 'finish', coordinates)

def get_StartPiece(id):
    lane00= [ 0 ]
    lane01= [ 1 ]
    lane02= [ 2 ]
    lane03= [ 3 ]
    lane04= [ 4 ]
    lane05= [ 5 ]
    lane06= [ 6 ]
    lane07= [ 7 ]
    lane08= [ 8 ]
    lane09= [ 9 ]
    lane10= [ 10 ]
    lane11= [ 11 ]
    lane12= [ 12 ]
    lane13= [ 13 ]
    lane14= [ 14 ]
    lane15= [ 15 ]
    coordinates = []
    coordinates.append(lane00)
    coordinates.append(lane01)
    coordinates.append(lane02)
    coordinates.append(lane03)
    coordinates.append(lane04)
    coordinates.append(lane05)
    coordinates.append(lane06)
    coordinates.append(lane07)
    coordinates.append(lane08)
    coordinates.append(lane09)
    coordinates.append(lane10)
    coordinates.append(lane11)
    coordinates.append(lane12)
    coordinates.append(lane13)
    coordinates.append(lane14)
    coordinates.append(lane15)
    return TrackPiece(id, 'start', coordinates)

def get_CrossPiece(id):
    lane00 = [0, 4, 8, 12]
    lane01 = [0, 4, 8, 12]
    lane02 = [0, 4, 8, 12]
    lane03 = [0, 4, 8, 12]
    lane04 = [1, 5, 9, 13]
    lane05 = [1, 5, 9, 13]
    lane06 = [1, 5, 9, 13]
    lane07 = [1, 5, 9, 13]
    lane08 = [2, 6, 10, 14]
    lane09 = [2, 6, 10, 14]
    lane10 = [2, 6, 10, 14]
    lane11 = [2, 6, 10, 14]
    lane12 = [3, 7, 11, 15]
    lane13 = [3, 7, 11, 15]
    lane14 = [3, 7, 11, 15]
    lane15 = [3, 7, 11, 15]
    coordinates = []
    coordinates.append(lane00)
    coordinates.append(lane01)
    coordinates.append(lane02)
    coordinates.append(lane03)
    coordinates.append(lane04)
    coordinates.append(lane05)
    coordinates.append(lane06)
    coordinates.append(lane07)
    coordinates.append(lane08)
    coordinates.append(lane09)
    coordinates.append(lane10)
    coordinates.append(lane11)
    coordinates.append(lane12)
    coordinates.append(lane13)
    coordinates.append(lane14)
    coordinates.append(lane15)
    return TrackPiece(id, 'cross', coordinates)
