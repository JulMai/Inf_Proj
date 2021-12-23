
class TrackPiece:

    id = 0
    type = 0
    coordinates = []

    def __init__(self, id, type, coordinates):
        self.id = id
        self.type = type
        self.coordinates = coordinates

    def get_TrackPieceType(id):
        return {
            10: 'intersection',     
            17: 'curve',
            18: 'curve',
            20: 'curve',
            23: 'curve',
            33: 'start',
            34: 'finish',
            36: 'straight',
            39: 'straight',
            40: 'straight',
            48: 'straight'            
        }.get(id, '')
    
    def get_id(self):
        return self.id

    def get_type(self):
        return self.type

    def get_coordinates(self):
        return self.coordinates
