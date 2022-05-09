from lxml import etree
from .log1 import l

def getdata(text):

    l.info('正则匹配已经填过的项目....')
    data = {}
    rules = []
    html = etree.HTML(text)
    rules.append(html.xpath('//input[@type="text"]'))

    rules.append(html.xpath('//input[@type="radio" and @checked="checked"]'))

    rules.append(html.xpath('//input[@type="number"]'))

    for rule in rules:
        for i in rule:
            key = i.xpath('./@name')[0]
            value = i.xpath('./@value')[0]

            data[key] = value

    selects = html.xpath('//select[@class="select_type"]')
    for select in selects:
        try:
            option = select.xpath('./option[@selected="true"]')
            option = select.xpath('./option[@selected="true"]')[len(option) - 1]

            key = option.xpath('../@name')[0]
            value = option.xpath('./@value')[0]

            data[key] = value
        except Exception as msg:
            print(msg)

    for key, value in data.items():
        print(f'{key}:{value}')

    data["qtyc"] = "无"
    return data
