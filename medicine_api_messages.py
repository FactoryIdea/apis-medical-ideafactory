# contains the entities declaration and definition of medicine information
from protorpc import messages


package = "Medicine Info"
class Dossage(messages.Message):
    class Units(messages.Enum):
        MICRO_GRAM=1
        MILLI_GRAM=2
        GRAM=3

    units=messages.EnumField('Dossage.Units',1,
                             default='MILLI_GRAM',
                             required=True)
    quant=messages.IntegerField(2,required=True)

class Cost(messages.Message):
    value=messages.IntegerField(1,required=True)
    currency=messages.StringField(2,required=True)

class Composition(messages.Message):
    name=messages.StringField(1,required=True)
    dossage=messages.MessageField(Dossage,2,required=True)
    description=messages.StringField(3)

class Medicine(messages.Message):
    class MedicineType(messages.Enum):
        TABLET=1
        INJECTION=2
        KAMAL=3 #need to be changed :D
    name=messages.StringField(1)
    mrp=messages.MessageField(Cost,2,repeated=True)
    composition=messages.MessageField(Composition,3,repeated=True)
    dossage=messages.MessageField(Dossage,4,required=True)
    medicine_type=messages.EnumField('Medicine.MedicineType',5,
                             default='KAMAL',
                             required=True)

    description=messages.StringField(6)
    
    
