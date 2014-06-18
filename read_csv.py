import csv,arff
import pandas as pd
 
from EmptyArff import EmptyArff

#with open('data/example.csv', 'rb') as csvfile:
#	reader = csv.reader(csvfile)
#	for row in reader:
#		print row


#the obj here is actually a dictionary type in python

df = pd.read_csv('data_test/20081028.CLEBOS.csv',index_col="time")

dfs = df[df['team']=='BOS']

print dfs.to_csv



#chunker = pd.read_csv('data/New York.csv',index_col="Season",chunksize=10)
#print chunker

#with open('data/New York.csv','rb') as f2read:
#    f_read = csv.reader(f2read)
#    for rows in f_read:
#        print rows


#def convert_csv_to_arff(file_path):

#this is to a code snippet to try a instance of the empty arff file

# new2 = EmptyArff()

# new2.set_attributes([
# 	('outlook', ['sunny', 'overcast', 'rainy']),
# 	('temperature', 'REAL'),
# 	('humidity', 'REAL'),
# 	('windy', ['TRUE', 'FALSE']),
# 	('play', ['yes', 'no'])
# 	])


# obj = { 
#     'description': u'',
#     'relation': 'weather',
#     'attributes': [
#         ('outlook', ['sunny', 'overcast', 'rainy']),
#         ('temperature', 'REAL'),
#         ('humidity', 'REAL'),
#         ('windy', ['TRUE', 'FALSE']),
#         ('play', ['yes', 'no'])
#     ],
#     'data': [
#         ['sunny', 85.0, 85.0, 'FALSE', 'no'], # 'data' used a list that has dict inside
#         ['sunny', 80.0, 90.0, 'TRUE', 'no'],
#         ['overcast', 83.0, 86.0, 'FALSE', 'yes'],
#         ['rainy', 70.0, 96.0, 'FALSE', 'yes'],
#         ['rainy', 68.0, 80.0, 'FALSE', 'yes'],
#         ['rainy', 65.0, 70.0, 'TRUE', 'no'],
#         ['overcast', 64.0, 65.0, 'TRUE', 'yes'],
#         ['sunny', 72.0, 95.0, 'FALSE', 'no'],
#         ['sunny', 69.0, 70.0, 'FALSE', 'yes'],
#         ['rainy', 75.0, 80.0, 'FALSE', 'yes'],
#         ['sunny', 75.0, 70.0, 'TRUE', 'yes'],
#         ['overcast', 72.0, 90.0, 'TRUE', 'yes'],
#         ['overcast', 81.0, 75.0, 'FALSE', 'yes'],
#         ['rainy', 71.0, 91.0, 'TRUE', 'no']
#     ],
#  }

# with open('output.arff', 'wb') as f:
#     arff.dump(obj,f)
