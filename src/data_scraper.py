from lxml.html import parse
from urllib2 import urlopen
from pandas.io.parsers import TextParser

parsed = parse(urlopen(
    'http://stats.nba.com/teamLineups.html?TeamID=1610612739&pageNo=1&rowsPerPage=25&SeasonType=Regular%20Season'))
doc = parsed.getroot()
# print doc
table = doc.xpath('.//table')
print table


def _unpack(row, kind='td'):
    elts = row.findall('.//%s' % kind)
    return [val.text_content() for val in elts]


def parse_options_data(table):
    rows = table.findall('.//tr')
    print rows
    header = _unpack(rows[0], kind='th')
    data = [_unpack(r) for r in rows[1:]]
    return TextParser(data, names=header).get_chunk()


call_data = table

data = parse_options_data(call_data)
print data
