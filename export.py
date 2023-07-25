from lxml import html
import io
import re

tree = html.parse("maq's Backloggery.html")
list = []
for gamebox in tree.xpath('//section[@class="gamebox" and child::div[@class="gamerow"]]'):

    name = next(iter(gamebox.xpath('./h2/b/text()')), '').strip()
    dlc = next(iter(gamebox.xpath('../../h2/b/text()')), '').strip()
    compilation = next(iter(gamebox.xpath('../../h2/b/text()[2]')), '').strip()
    platform = next(iter(gamebox.xpath('.//div[@class="gamerow"]/b/text()')), '').strip()

    # Swap name/dlc
    if dlc:
        name, dlc = dlc, name

    list.append((name, dlc, compilation, platform))

# Lexicographical sort & format the output
list.sort(key=lambda tup: re.sub(r'^(a |the |an )', '', tup[0].casefold()))
outfile = io.open("games.txt", mode="w", encoding="utf-8")

for game in list:
    name = game[0]
    dlc = f': {game[1]}' if game[1] else ""
    compilation = f' ({game[2]})' if game[2] else ""
    platform = game[3]
    outfile.write(f'{name}{dlc}{compilation} [{platform}]\n')

outfile.close()
print(f'Number of beaten games: {len(list)}')
