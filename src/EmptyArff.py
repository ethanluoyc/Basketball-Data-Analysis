"""This is the code to create an object(dictionary) in python for mapping into a Arff file using liac_arff
only the file for the object is written here
"""
class EmptyArff:
	properties = { 
	'description': u'', #in unicode 
	'relation': '',     #NOT YET SURE OF WHAT THIS REPRESENTS
	'attributes': [],   #tuples, tuple('name of the attrbute', list[] or 'string')
	'data': [],         #list type inside data to represent rows
    }    
	
	def set_attributes(self, attributes): 
		self.properties['attributes']= attributes
	def set_description(self, description):
		self.properties['description']=description
	def set_relation(self,relation):
		self.properties['relation']=relation
	def set_data(self,data):
		self.properties['data']=data #relation must be created before input of actual data

