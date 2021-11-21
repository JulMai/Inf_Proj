import os
import re

print(os.getcwd())

def parse_lanes():
    with open("Tests/ts/trackPieceFactory.ts") as file:
        for line in file:
            if line.find("let ")>-1 and line.find("coordinates")==-1:
                str = line
                row = str.replace("let ", "").strip()
                row = row.replace(":", "=", 1)
                row = row.replace("Array<number> = ", "")
                row = row.replace(";", "")
                print(row)

def parse_coordinates():
    doc = ""
    with open("Tests/track/trackPieceFactory.py") as file:
        for line in file:
            if line.find("coordinates") > -1 and line.find("coordinates = []") == -1:
                str = line
                str = re.sub('\D+\[\d+\]\ \=\ ', "coordinates.append(", str)
                str = str.replace("\n", ")\n")
                line = str
            doc = doc + line
    print(doc)            


if __name__ == '__main__':
    parse_coordinates()

            
    