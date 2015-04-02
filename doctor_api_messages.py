from protorpc import messages
from google.appengine.ext import ndb
from google.appengine.ext.ndb import msgprop #alpha feature dangerous

class Name(messages.Message):
    name=messages.StringField(1)
    
class Specilization(messages.Message):
    name=messages.StringField(1,required=True)
    disease_name=messages.MessageField(Name,2,repeated=True)

class Address(messages.Message):
    pincode=messages.StringField(1)
    lattitude=messages.FloatField(2)
    longitude=messages.FloatField(3)
    city_name=messages.StringField(4,required=True)
    state_name=messages.StringField(5)
    country_name=messages.StringField(6,required=True)
    address_line=messages.StringField(7)


class Doctor(messages.Message):
    name=messages.StringField(1,required=True)
    last_name=messages.StringField(2)
    designation=messages.MessageField(Specilization,3,repeated=True)
    home_address=messages.MessageField(Address,4,required=True)
    work_addresses=messages.MessageField(Address,5,repeated=True)

#class for message presentation:

class DoctorNameMessage(messages.Message):
    limit= messages.IntegerField(1,default=10,required=False)
    offset=messages.IntegerField(2,default=0,required=False)
    name=messages.StringField(3)
    last_name=messages.StringField(4)
    city_name=messages.StringField(5)
    country_name=messages.StringField(6)
    designation_name=messages.StringField(7)

class DoctorDiseaseMessage(messages.Message):
    limit= messages.IntegerField(1,default=10,required=False)
    offset=messages.IntegerField(2,default=0,required=False)
    name=messages.StringField(3,repeated=True)
    
class SpecilizationListMessage(messages.Message):
    specilization_list=messages.MessageField(Specilization,1,repeated=True)

class DoctorListMessage(messages.Message):
    doctor_list=messages.MessageField(Doctor,1,repeated=True)
    
#classes for handling Database interaction

class DoctorStore(ndb.Model):
    doctor=msgprop.MessageProperty(Doctor,indexed_fields=['name',
                            'designation.name','home_address.city_name',
                            'work_addresses.city_name',
                            'home_address.country_name',
                            'work_addresses.country_name',
                            'last_name'
                            ])
    
    #warning this feature is in alpha
#Symptom class to fetch the specilization names from disease names
class SpecilizationStore(ndb.Model):
    specilization=msgprop.MessageProperty(Specilization,indexed_fields=['name',
                            'disease_name.name',
                            ])
    
    #warning this feature is in alpha
