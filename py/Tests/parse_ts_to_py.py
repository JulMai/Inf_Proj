import os

print(os.getcwd())


with open("Tests/ts/trackPieceFactory.ts") as file:
    for line in file:
        if line.find("let ")>-1 and line.find("coordinates")==-1:
            str = line
            row = str.replace("let ", "").strip()
            row = row.replace(":", "=", 1)
            row = row.replace("Array<number> = ", "")
            row = row.replace(";", "")
            print(row)

    