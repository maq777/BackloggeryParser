from lxml import html

tree = html.parse("backloggery.html")
for gamebox in tree.xpath('//section[@class="gamebox" and child::div[@class="gamerow"]]'):

    name = next(iter(gamebox.xpath('./h2/b/text()')), '')
    compilation = next(iter(gamebox.xpath('../../h2/b/text()[2]')), '')
    platform = next(iter(gamebox.xpath('.//div[@class="gamerow"]/b/text()')), '')
    progress = next(iter(gamebox.xpath('(.//div[@class="gamerow"]/text())[2]')), '')

    print(f'{name}\t{compilation.strip()}\t{platform.strip()}\t{progress.strip()}')
