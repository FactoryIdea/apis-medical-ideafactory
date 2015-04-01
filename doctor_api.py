#api for feteching doctor's information
import endpoints
from doctor_api_messages import *
from protorpc import messages
from protorpc import remote

WEB_CLIENT_ID='yo yo sample id'
ANDROID_CLIENT_ID='yo yo ULHA sample id'
IOS_CLIENT_ID='yo yo ULLUsample id'
ANDROID_AUDIENCE= WEB_CLIENT_ID
WEB_CLIENT_ADMIN_ID="adminstuff@adminstuff"
@endpoints.api(name='doctorinfo',version='v1',
               allowed_client_ids=[WEB_CLIENT_ID,
                                   ANDROID_CLIENT_ID,
                                   IOS_CLIENT_ID,
                                   endpoints.API_EXPLORER_CLIENT_ID],
               audiences=[],
               scopes=[endpoints.EMAIL_SCOPE],
               description="API To ACCESS WEB SERVICES For doctor's data")
class DoctorInfoApi(remote.Service):
      #TODO ADD AUTHORIZATION
      #RULE of thumb : no need to put doctor in doctor's name
      @endpoints.method(Doctor,Doctor,
                      path='doctorInsert',http_method='POST',
                      name='doctorInfo.insert',
                      allowed_client_ids=[WEB_CLIENT_ADMIN_ID]
                        )
      def insert_doctor(self,request):
          #Normalizing the fields
          request.name=request.name.lower()
          if request.last_name:
             request.last_name=request.last_name.lower()
          i=0 
          for q in request.designation:
             request.designation[i].name =q.name.lower()
             j=0
             for r in request.designation[i].disease_name:
                 request.designation[i].disease_name[j] =r.lower()
                 j=j+1
             i=i+1

          request.home_address.city_name =request.home_address.city_name.lower()
          request.home_address.country_name =request.home_address.country_name.lower()

          i=0
          for q in request.work_addresses:
              request.work_addresses[i].city_name =q.city_name.lower()
              request.work_addresses[i].country_name =q.country_name.lower()
              i=i+1

          #let the inserting begin
          DoctorStore(doctor=request).put()
          for q in request.designation:
              SpecilizationStore(specilization=q).put()
          return request

        
