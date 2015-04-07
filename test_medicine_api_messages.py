#sample test file to test various apis
from doctor_api_messages import *
from medicine_api_messages import *
from disease_api_messages import *
import webapp2



class MainPage(webapp2.RequestHandler):
    def get(self):
        self.response.write("Hello Kamal")

    

yo = webapp2.WSGIApplication([
    ('/',MainPage)],debug=True)

    
    
