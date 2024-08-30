import argparse
import csv
import datetime
import io
import os
import re


# Decide if game is part of a collection
def isCollection(dict):
    if dict['Status'] == 'None' and dict['Format'] == "0" and dict['Ownership'] == "0":
        return True
    else:
        return False


# Decide if game has been beaten
def isBeaten(dict):
    if dict['Status'] == "Beaten" or dict['Status'] == "Completed":
        return True
    else:
        return False


# Get parent game (DLC & Copllection)
def getParent(dict, list):
    return next((item for item in list if item["Unique Game ID"] == row['Child Of']), None)


parser = argparse.ArgumentParser("convert")
parser.add_argument("file", help="The backloggery exported Game Library file to convert.", type=argparse.FileType('r', encoding='UTF-8'))
args = parser.parse_args()

print(f"# Converting '{os.path.basename(args.file.name)}'")

# Read header
header = args.file.readline()
args.file.readline() # Expect empty line
print(f"## Input file header '{header.strip()}'")

# Read content
reader = csv.DictReader(args.file)
games = list(reader)

# Fix DLC nameing
for row in games:
    parent = getParent(row, games)
    if parent and not isCollection(parent):
        row['Title'] = f"{parent['Title']}: {row['Title']}"

# Lexicographical sort & format the output
games.sort(key=lambda tup: re.sub(r'^(a |the |an )', '', tup['Title'].casefold()))

# Write output
outfile = io.open("README.md", mode="w", encoding="utf-8")
outfile.write("## Completed games\n\n")
for row in games:
    print(f"### Processing '{row['Title']}'")
    if not isBeaten(row):
        continue
    else:
        parent = getParent(row, games)
        if parent and isCollection(parent):
            outfile.write(f"- {row['Title']} ({parent['Title']}) [{row['Platform']}]\n")
        else:
            outfile.write(f"- {row['Title']} [{row['Platform']}]\n")

outfile.write(f"\nmaq777 - {datetime.datetime.now().strftime('%Y-%m-%d')}")
outfile.close()
