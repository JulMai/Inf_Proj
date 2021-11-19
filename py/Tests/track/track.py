import trackPieceFactory 


class Track :
    trackPieces = []

    def __init__(self, ids):
        self.trackPieces = []

        for i in ids:
            trackPiece = trackPieceFactory.get_TrackPiece(i)

            if trackPiece != None:
                self.trackPieces.append(trackPiece)


    def get_TrackPieces(self):
        return self.trackPieces



