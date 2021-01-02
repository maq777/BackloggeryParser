from lxml import html

tree = html.parse("backloggery.html")
for gamebox in tree.xpath('//section[@class="gamebox" and child::div[@class="gamerow"]]'):

    name = next(iter(gamebox.xpath('./h2/b/text()')), '')
    dlc = next(iter(gamebox.xpath('../../h2/b/text()')), '')
    compilation = next(iter(gamebox.xpath('../../h2/b/text()[2]')), '')
    platform = next(iter(gamebox.xpath('.//div[@class="gamerow"]/b/text()')), '')
    #progress = next(iter(gamebox.xpath('(.//div[@class="gamerow"]/text())[2]')), '')

    dlc = dlc.strip()
    compilation = compilation.strip()
    platform = platform.strip()
    #progress = progress.strip()

    if dlc:
        name = f'{dlc}: {name}'

    if compilation:
        name = f'{name} ({compilation})'

    print(f'{name} [{platform}]')
