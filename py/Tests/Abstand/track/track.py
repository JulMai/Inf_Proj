from track.trackPieceFactory import get_TrackPiece


class Track :
    trackPieces = []

    def __init__(self, ids):
        self.trackPieces = []

        for i in ids:
            trackPiece = get_TrackPiece(i)

            if trackPiece != None:
                self.trackPieces.append(trackPiece)


    def get_TrackPieces(self):
        return self.trackPieces



