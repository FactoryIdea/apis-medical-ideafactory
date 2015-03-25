#sample test file to test various apis

from medicine_api_messages import *
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
qry = MedicineStore.query(MedicineStore.medicine.composition.name == "gudia").fetch()


class MainPage(webapp2.RequestHandler):
    def get(self):
        self.response.write(str(qry[0].medicine.description))
        self.response.write(str(med1.mrp[0].value)+" "+str(med1.composition[1].name)+" ")
        self.response.write(str(med1.name)+" "+str(med1.dossage.units) +" ")
        self.response.write(str(composition1.name)+" "+str(composition1.dossage.units) +" ")
        self.response.write(str(cost2.value)+" "+str(cost2.currency) +" ")
        self.response.write(str(dossage.units)+" "+str(dossage.quant))

    

yo = webapp2.WSGIApplication([
    ('/',MainPage)],debug=True)

    
    
