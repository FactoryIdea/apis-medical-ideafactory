# contains the entities declaration and definition of medicine information
from protorpc import messages
from google.appengine.ext import ndb
from google.appengine.ext.ndb import msgprop#alpha feature dangerous

#contains the real entities that we are going to model in for medicine api purpose
class Dossage(messages.Message):
    class Units(messages.Enum):
        MICRO_GRAM=1
        MILI_GRAM=2
        GRAM=3
        MILI_LITRE=4

    units=messages.EnumField('Dossage.Units',1,
                             default='MILI_GRAM',
                             required=True)
    quant=messages.IntegerField(2,required=True)

class Cost(messages.Message):
    value=messages.IntegerField(1,required=True)
    currency=messages.StringField(2,required=True)

class Composition(messages.Message):
    name=messages.StringField(1,required=True)
    dossage=messages.MessageField(Dossage,2,required=True)
    description=messages.StringField(3,required=True)


class Medicine(messages.Message):
    class MedicineType(messages.Enum):
        TABLET=1
        INJECTION=2
        CAPSULES=3
        OINTMENT=4
        DROPS=5
        LOTION=6
        SACHET=7
        SYRUP=8
        NULLL=9 #triple L done to avoid ambiguity with NULL
        
    name=messages.StringField(1,required=True)
    mrp=messages.MessageField(Cost,2,repeated=True)
    
    composition=messages.MessageField(Composition,3,repeated=True)
    dossage=messages.MessageField(Dossage,4,required=True)
    medicine_type=messages.EnumField('Medicine.MedicineType',5,
                             default='NULLL',
                             required=True)
    

    description=messages.StringField(6)
    company_name=messages.StringField(7,required=True)

#handles the format the request will come
class MedicineMessage(messages.Message):
    medicine=messages.MessageField(Medicine,1)

class MedicineFieldMessage(messages.Message):
    limit=messages.IntegerField(1,default=10,required=False)
    offset=messages.IntegerField(2,default=0,required=False)
    name=messages.StringField(3)
    company_name=messages.StringField(4)
    medicine_type=messages.EnumField('Medicine.MedicineType',5)

class MedicineCompostionMessage(messages.Message):
       limit=messages.IntegerField(1,default=10,required=False)
       offset=messages.IntegerField(2,default=0,required=False)
       compostion_name=messages.StringField(3,repeated=True)
    
class MedicineListMessage(messages.Message):
    medicine_list=messages.MessageField(Medicine,1,repeated=True)


#handles the storage of data in datastore
class MedicineStore(ndb.Model):
    medicine=msgprop.MessageProperty(Medicine,indexed_fields=['name','medicine_type',
                            'company_name',"composition.name"])
    #warning this feature is in alpha
