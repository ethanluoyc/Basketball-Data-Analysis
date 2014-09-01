from lxml.html import parse
from urllib2 import urlopen
from pandas.io.parsers import TextParser

parsed =parse(urlopen('http://www.basketball-reference.com/teams/LAL/stats_totals.html'))
doc = parsed.getroot()
links = doc.findall('.//table')
print links

def _unpack(row, kind='td'):
	elts = row.findall('.//%s' % kind)
	return [val.text_content() for val in elts]

def parse_options_data(table):
	rows = table.findall('.//tr')     
	header = _unpack(rows[0],kind='th')
	data =[_unpack(r) for r in rows[1:]]
	return TextParser(data,names=header).get_chunk()
