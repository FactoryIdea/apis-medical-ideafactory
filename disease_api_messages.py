# contains the entities declaration and definition of disease information
from protorpc import messages
from google.appengine.ext import ndb
from google.appengine.ext.ndb import msgprop#alpha feature dangerous

#contains the real entities that we are going to model in for disease api purpose
class Name(messages.Message):
    name=messages.StringField(1,required=True)
    
class Symptoms(messages.Message):
    primary_name=messages.StringField(1,required=True)
    secondry_names=messages.MessageField(Name,2,repeated=True)
    description=messages.StringField(3,required=True)
    #Todo make an api that can smartly search the sympotms from its description
    
class Disease(messages.Message):
    primary_name=messages.StringField(1,required=True)
    secondry_names=messages.MessageField(Name,2,repeated=True)
    description=messages.StringField(3,required=True)
    symptoms=messages.MessageField(Symptoms,4,repeated=True)
    
#handles the format the request will come
class DiseaseMessage(messages.Message):
    disease=messages.MessageField(Disease,1)

class DiseaseAndSymptomsNameMessage(messages.Message):
    limit=messages.IntegerField(1,default=10,required=False)
    offset=messages.IntegerField(2,default=0,required=False)
    ds_name=messages.StringField(3,repeated=True)
    
class DiseaseListMessage(messages.Message):
    disease_list=messages.MessageField(Disease,1,repeated=True)

#Do no forget to delete this one
class SListMessage(messages.Message):
    s_list=messages.MessageField(Symptoms,1,repeated=True)
#handles the storage of data in datastore
class DiseaseStore(ndb.Model):
    disease=msgprop.MessageProperty(Disease,indexed_fields=['primary_name',
                            'secondry_names.name','symptoms.primary_name'
                            ])
    
    #warning this feature is in alpha
#Symptom class to fetch the primary name from secondry names
class SymptomsStore(ndb.Model):
    symptoms=msgprop.MessageProperty(Symptoms,indexed_fields=['primary_name',
                            'secondry_names.name',
                            ])
    
    #warning this feature is in alpha

