#sample test file to test various apis
import endpoints
from medicine_api_messages import *
from protorpc import messages
from protorpc import remote


WEB_CLIENT_ID='yo yo sample id'
ANDROID_CLIENT_ID='yo yo ULHA sample id'
IOS_CLIENT_ID='yo yo ULLUsample id'
ANDROID_AUDIENCE= WEB_CLIENT_ID
WEB_CLIENT_ADMIN_ID="adminstuff@adminstuff"
@endpoints.api(name='medicineinfo',version='v1',
               allowed_client_ids=[WEB_CLIENT_ID,
                                   ANDROID_CLIENT_ID,
                                   IOS_CLIENT_ID,
                                   endpoints.API_EXPLORER_CLIENT_ID],
               audiences=[],
               scopes=[endpoints.EMAIL_SCOPE],
               description="API To ACCESS WEB SERVICES")
class MedicineInfoApi(remote.Service):
      #TODO ADD AUTHORIZATION
      @endpoints.method(MedicineMessage,MedicineMessage,
                      path='medicineInsert',http_method='POST',
                      name='medicineInfo.insert',
                      allowed_client_ids=[WEB_CLIENT_ADMIN_ID]
                        )
      def insert_medicine(self,request):
          response=MedicineStore(medicine=request.medicine).put()
          ##TODO return the response instead of request
          return request




APPLICATION = endpoints.api_server([MedicineInfoApi],
                                   restricted=False)
    
    
