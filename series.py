import argparse
import csv
import datetime
import io
import os
import re

# Based on GiantBomb guid's
series = {
    "3025-11":   {"header": "## 194X", "games": []},
    "3025-2074": {"header": "## Alan Wake", "games": []},
    "3025-28":   {"header": "## Alone in the Dark", "games": []},	
    "3025-38":   {"header": "## Assassin's Creed", "games": []},
    "3025-44":   {"header": "## Baldur's Gate", "games": []},
    "3025-70":   {"header": "## Broken Sword", "games": []},
    "3025-82":   {"header": "## Call of Duty", "games": []},
    "3025-1258": {"header": "### Modern Warfare", "games": []},
    "3025-2275": {"header": "### Black Ops", "games": []},
    "3025-182":  {"header": "## Fable", "games": []},
    "3025-2":    {"header": "## Halo", "games": []},
    "3025-523":  {"header": "## Mega Man", "games": []},
    "3025-626":  {"header": "### Mega Man Classic", "games": []},
    "3025-524":  {"header": "### Mega Man X", "games": []},
    "3025-548":  {"header": "## Monkey Island", "games": []},
    "3025-616":  {"header": "## S.T.A.L.K.E.R.", "games": []},
    "3025-331":  {"header": "## Street Fighter", "games": []},
    "3025-1795": {"header": "### Street Fighter II", "games": []},
    "3025-960":  {"header": "### Street Fighter Alpha", "games": []},
    "3025-1662": {"header": "### Street Fighter III", "games": []},
    "3025-2693": {"header": "### Street Fighter IV", "games": []},
    "3025-210":  {"header": "## Wolfenstein", "games": []},
}

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

# Find games in series
for game in games:
    for match in re.finditer(r"\(franchise,(.+?),(\d+)\)", game["Notes"]):
        game_tuple = (game["Title"], match.group(2))  # tuple of game name and year
        series[match.group(1)]["games"].append(game_tuple)
        series[match.group(1)]["games"].sort(
            key=lambda tup: int(tup[1])
        )  # sort by year

# Write output
with io.open("SERIES.md", mode="w", encoding="utf-8") as outfile:
    outfile.write("## Game Series Completion Status\n")
    for serie in series:
        print(f"### Processing '{series[serie]}'")
        outfile.write(f"\n{series[serie]['header']}\n\n")

        for game in series[serie]["games"]:  # if the game already have a year at the end
            if game[0].endswith("(" + game[1] + ")"):
                outfile.write(f"- {game[0]}\n")
            else:
                outfile.write(f"- {game[0]} ({game[1]})\n")

    outfile.write(f"\nmaq777 - {datetime.datetime.now().strftime('%Y-%m-%d')}")
    outfile.close()
