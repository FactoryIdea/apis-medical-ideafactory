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
               description="API To ACCESS WEB SERVICES For medical data")
class MedicineInfoApi(remote.Service):
      #TODO ADD AUTHORIZATION
      @endpoints.method(MedicineMessage,MedicineMessage,
                      path='medicineInsert',http_method='POST',
                      name='medicineInfo.insert',
                      allowed_client_ids=[WEB_CLIENT_ADMIN_ID]
                        )
      def insert_medicine(self,request):
          medicine=request.medicine
          medicine.name= medicine.name.lower()
          medicine.company_name=medicine.company_name.lower()
          response=MedicineStore(medicine=request.medicine).put()
          ##TODO return the response instead of request
          
          return request

      @endpoints.method(MedicineFieldMessage,MedicineListMessage,
                      path='medicineget',http_method='GET',
                      name='medicineInfo.getmedicine'
                       )
      def get_medicine(self,request):
           #TODO make the query compound  
           offset=request.offset
           limit=request.limit
           query=MedicineStore.query()
           if(request.name is not None):
                 name=request.name.lower()
                 query=query.filter(MedicineStore.medicine.name == name)
           if(request.company_name is not None):
                 cname=request.company_name.lower()
                 query=query.filter(MedicineStore.medicine.company_name == cname)
           if(request.medicine_type is not None):
                 med_type=request.medicine_type
                 query=query.filter(MedicineStore.medicine.medicine_type == med_type)
                   
           
           mediList=[]
           qryArray=[]
           if query is not None:
                 qryArray=query.fetch(limit=limit,offset=offset)
           for q in qryArray:
                 mediList.append(q.medicine)
         
           return MedicineListMessage(medicine_list=mediList)

      @endpoints.method(MedicineCompostionMessage,MedicineListMessage,
                      path='medicinegetbycomposition',http_method='GET',
                      name='medicineInfo.getmedicinebycomposition'
                       )
      def get_medicine_bycomposition(self,request):
           #TODO make the query compound  
           offset=request.offset
           limit=request.limit
           query=MedicineStore.query()

           for q in request.compostion_name:
                 cname=q.lower()
                 query=query.filter(MedicineStore.medicine.composition.name == cname )
      
           mediList=[]
           qryArray=[]
           if query is not None:
                 qryArray=query.fetch(limit=limit,offset=offset)
           for q in qryArray:
                 mediList.append(q.medicine)
         
           return MedicineListMessage(medicine_list=mediList)



APPLICATION = endpoints.api_server([MedicineInfoApi],
                                   restricted=False)
    
    
