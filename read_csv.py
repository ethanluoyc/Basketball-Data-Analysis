import csv,arff
import pandas as pd
 
from EmptyArff import EmptyArff

#with open('data/example.csv', 'rb') as csvfile:
#	reader = csv.reader(csvfile)
#	for row in reader:
#		print row


#the obj here is actually a dictionary type in python
"""
obj = { 
    'description': u'',
    'relation': 'weather',
    'attributes': [
        ('outlook', ['sunny', 'overcast', 'rainy']),
        ('temperature', 'REAL'),
        ('humidity', 'REAL'),
        ('windy', ['TRUE', 'FALSE']),
        ('play', ['yes', 'no'])
    ],
    'data': [
        ['sunny', 85.0, 85.0, 'FALSE', 'no'], # 'data' used a list that has dict inside
        ['sunny', 80.0, 90.0, 'TRUE', 'no'],
        ['overcast', 83.0, 86.0, 'FALSE', 'yes'],
        ['rainy', 70.0, 96.0, 'FALSE', 'yes'],
        ['rainy', 68.0, 80.0, 'FALSE', 'yes'],
        ['rainy', 65.0, 70.0, 'TRUE', 'no'],
        ['overcast', 64.0, 65.0, 'TRUE', 'yes'],
        ['sunny', 72.0, 95.0, 'FALSE', 'no'],
        ['sunny', 69.0, 70.0, 'FALSE', 'yes'],
        ['rainy', 75.0, 80.0, 'FALSE', 'yes'],
        ['sunny', 75.0, 70.0, 'TRUE', 'yes'],
        ['overcast', 72.0, 90.0, 'TRUE', 'yes'],
        ['overcast', 81.0, 75.0, 'FALSE', 'yes'],
        ['rainy', 71.0, 91.0, 'TRUE', 'no']
    ],
 }

with open('output.arff', 'wb') as f:
	arff.dump(obj,f)
"""
df = pd.read_csv('data/Rankings.csv')
print df








#this is to a code snippet to try a instance of the empty arff file

new2 = EmptyArff()

new2.set_attributes([
	('outlook', ['sunny', 'overcast', 'rainy']),
	('temperature', 'REAL'),
	('humidity', 'REAL'),
	('windy', ['TRUE', 'FALSE']),
	('play', ['yes', 'no'])
	])
print new2.properties['attributes']
