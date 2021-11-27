from track import Track

test_track = [33, 10, 18, 17, 20, 10, 17, 48, 18, 18, 34]

track = Track(test_track)

track2 = {}

for piece in track.trackPieces:
    track2[piece.id] = piece.coordinates

print("")