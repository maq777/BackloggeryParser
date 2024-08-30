import argparse
import csv
import datetime
import io
import os
import re


def is_collection(game_dict):
    """Determine if the game/item is a collection."""
    return (
        game_dict["Status"] == "None"
        and game_dict["Format"] == "0"
        and game_dict["Ownership"] == "0"
    )


def is_beaten(game_dict):
    """Determine if the game/item has been beaten."""
    return game_dict["Status"] in ["Beaten", "Completed"]


def get_parent(row, game_list):
    """Get parent game (DLC & Collection)"""
    return next(
        (item for item in game_list if item["Unique Game ID"] == row["Child Of"]), None
    )


parser = argparse.ArgumentParser("convert")
parser.add_argument(
    "file",
    help="The backloggery exported Game Library file to convert.",
    type=argparse.FileType("r", encoding="UTF-8"),
)
args = parser.parse_args()

print(f"# Converting '{os.path.basename(args.file.name)}'")

# Read header
header = args.file.readline()
args.file.readline()  # Expect empty line
print(f"## Input file header '{header.strip()}'")

# Read content
reader = csv.DictReader(args.file)
games = list(reader)

# Fix DLC naming
for row in games:
    parent = get_parent(row, games)
    if parent and not is_collection(parent):
        row["Title"] = f"{parent['Title']}: {row['Title']}"

# Lexicographical sort & format the output
games.sort(key=lambda tup: re.sub(r"^(a |the |an )", "", tup["Title"].casefold()))

# Write output
with io.open("README.md", mode="w", encoding="utf-8") as outfile:
    outfile.write("## Completed games\n\n")
    for row in games:
        print(f"### Processing '{row['Title']}'")
        if not is_beaten(row):
            continue
        parent = get_parent(row, games)
        if parent and is_collection(parent):
            outfile.write(f"- {row['Title']} ({parent['Title']}) [{row['Platform']}]\n")
        else:
            outfile.write(f"- {row['Title']} [{row['Platform']}]\n")

    outfile.write(f"\nmaq777 - {datetime.datetime.now().strftime('%Y-%m-%d')}")
    outfile.close()
