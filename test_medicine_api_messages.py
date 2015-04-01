#sample test file to test various apis
from doctor_api_messages import *
from medicine_api_messages import *
from disease_api_messages import *
import webapp2

dossage= Dossage(units=Dossage.Units.GRAM,quant=100)
cost1= Cost(value=100,currency="Ruppes")
cost2= Cost(value=77,currency="Eurro")
composition1 =Composition(name="Paracetamol",dossage=dossage)
composition2 =Composition(name="YOParacetamol",dossage=dossage,description="HI")
med1=Medicine()
med1.name="yeh hei"
med1.mrp=[Cost(value=88,currency="Ruppes")]
med1.composition=[composition1,composition2]
med1.medicine_type=Medicine.MedicineType.NULLL
med1.dossage=dossage
med1.description="YO"
qry = SymptomsStore.query().fetch()

speciliaztion = Specilization(name="Child Specilist",disease_name=['nimonia','heart disease'])
address = Address(city_name="bikaner" , country_name="India")
doctor = Doctor(name="Dr Sanjay Kochar",designation=[speciliaztion],
                home_address=address)
class MainPage(webapp2.RequestHandler):
    def get(self):
        self.response.write(doctor.name +" "+doctor.home_address.country_name+"<br/>")
        self.response.write(address.city_name +" "+address.country_name+"<br/>")
        self.response.write(speciliaztion.name +" "+speciliaztion.disease_name[1]+"<br/>")
        self.response.write(str(qry[0].symptoms.description))
        self.response.write(str(med1.mrp[0].value)+" "+str(med1.composition[1].name)+" ")
        self.response.write(str(med1.name)+" "+str(med1.dossage.units) +" ")
        self.response.write(str(composition1.name)+" "+str(composition1.dossage.units) +" ")
        self.response.write(str(cost2.value)+" "+str(cost2.currency) +" ")
        self.response.write(str(dossage.units)+" "+str(dossage.quant))

    

yo = webapp2.WSGIApplication([
    ('/',MainPage)],debug=True)

    
    
