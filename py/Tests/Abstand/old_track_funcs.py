def get_track_with_lanes(track_before):
    track_after = []

    for t in track_before:
        id = t[0]
        location = t[1]
        if len(t) > 2:
            clockwise = t[2]
        piece = get_TrackPiece(id)
        lane = []
        for locations in piece.coordinates:
            for c in locations:
                if c == location:
                    if clockwise:
                        for i in range(len(locations)):
                            locations[i] = [locations[i], None]
                        lane = locations
                        break
                    else:
                        k = 0
                        locations2 = []
                        for i in range(len(locations) - 1, -1, -1):
                            locations2.append([locations[i], None])
                        lane = locations2
                        break
        track_after.append([id, lane])

    return track_after

def get_track_dict(track_before):
    track_after = {}

    i = 0
    for t in track_before:
        id = t[0]
        location = t[1]
        clockwise = t[2]
        piece = get_TrackPiece(id)
        for locations in piece.coordinates:
            for c in locations:
                if c == location:
                    if clockwise:
                        for l in locations:
                            str = f"{i:02d}{id:02d}{l:02d}"
                            track_after[str] = None
                    else:
                        for l in range(len(locations), 0, -1):
                            str = f"{i:02d}{id:02d}{l:02d}"
                            track_after[str] = None
                    
        i+=1
    return track_after



    for i in range(min, max, stp):
        if lane[i] == location:
            if (i + stp) < min or (i + stp) > max:
                return 0
            else:
                return lane[i + stp]

def fix_track(track):
    # nicht fertig
    track_dict = {}
    last_piece = 0
    last_location = 0
    prev_piece = 0
    for i in range(len(track)):
        l = track[i]
        piece = l[0]
        location = l[1]
        clockwise = l[2]  # true: - ; false: +
        next_loc_prediction = predict_next_loc(piece, location, clockwise)
        
        if piece == track[i-1][0]:
            if clockwise == track[i-1][2]:
                if (location - track[i+1][1]) == -2:
                    pass
                    # i + 1 ist neues piece

        else:
            prev_piece = piece

    return track_dict

def predict_next_loc(piece, location, clockwise):
    lane = get_Lane(piece, location)

    if clockwise:
        stp = -1
        min = len(lane)
        max = 0   
    else:
        stp = 1
        min = 0
        max = len(lane)