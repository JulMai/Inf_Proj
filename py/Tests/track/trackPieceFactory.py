from trackPiece import TrackPiece

def get_TrackPiece(id):
    return {
        'straight'  : get_StraightPiece(id),
        'curve'     : get_CurvePiece(id),
        'start'     : get_StartPiece(id),
        'finish'    : get_FinishPiece(id)
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
    coordinates[0] = lane00
    coordinates[1] = lane01
    coordinates[2] = lane02
    coordinates[3] = lane03
    coordinates[4] = lane04
    coordinates[5] = lane05
    coordinates[6] = lane06
    coordinates[7] = lane07
    coordinates[8] = lane08
    coordinates[9] = lane09
    coordinates[10] = lane10
    coordinates[11] = lane11
    coordinates[12] = lane12
    coordinates[13] = lane13
    coordinates[14] = lane14
    coordinates[15] = lane15

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
    coordinates[0] = lane00
    coordinates[1] = lane01
    coordinates[2] = lane02
    coordinates[3] = lane03
    coordinates[4] = lane04
    coordinates[5] = lane05
    coordinates[6] = lane06
    coordinates[7] = lane07
    coordinates[8] = lane08
    coordinates[9] = lane09
    coordinates[10] = lane10
    coordinates[11] = lane11
    coordinates[12] = lane12
    coordinates[13] = lane13
    coordinates[14] = lane14
    coordinates[15] = lane15

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
    coordinates[0] = lane00
    coordinates[1] = lane01
    coordinates[2] = lane02
    coordinates[3] = lane03
    coordinates[4] = lane04
    coordinates[5] = lane05
    coordinates[6] = lane06
    coordinates[7] = lane07
    coordinates[8] = lane08
    coordinates[9] = lane09
    coordinates[10] = lane10
    coordinates[11] = lane11
    coordinates[12] = lane12
    coordinates[13] = lane13
    coordinates[14] = lane14
    coordinates[15] = lane15

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
    coordinates[0] = lane00
    coordinates[1] = lane01
    coordinates[2] = lane02
    coordinates[3] = lane03
    coordinates[4] = lane04
    coordinates[5] = lane05
    coordinates[6] = lane06
    coordinates[7] = lane07
    coordinates[8] = lane08
    coordinates[9] = lane09
    coordinates[10] = lane10
    coordinates[11] = lane11
    coordinates[12] = lane12
    coordinates[13] = lane13
    coordinates[14] = lane14
    coordinates[15] = lane15