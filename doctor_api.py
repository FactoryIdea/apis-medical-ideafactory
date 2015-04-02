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
                 request.designation[i].disease_name[j].name =r.name.lower()
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

      @endpoints.method(DoctorNameMessage,DoctorListMessage,
                      path='doctorgetbyname',http_method='GET',
                      name='doctorInfo.get_by_name',
                      
                        )
      def get_doctor_by_name(self,request):
            limit=request.limit
            offset=request.offset

            query =DoctorStore.query()
            if request.name:
                  name=request.name.lower()
                  query=query.filter(DoctorStore.doctor.name==name)
            if request.last_name:
                  last_name=request.last_name.lower()
                  query=query.filter(DoctorStore.doctor.last_name==last_name)
            if request.designation_name:
                  designation_name=request.designation_name.lower()
                  query=query.filter(DoctorStore.doctor.designation.name==designation_name)
            if request.city_name:
                  city_name=request.city_name.lower()
                  query=query.filter(DoctorStore.doctor.home_address.city_name==city_name)
            if request.country_name:
                  country_name=request.country_name.lower()
                  query=query.filter(DoctorStore.doctor.home_address.country_name==country_name)

            doctorList=[]
            qryArray=[]
            if query is not None:
                 qryArray=query.fetch(limit=limit,offset=offset)
            for q in qryArray:
                 doctorList.append(q.doctor)
         
            return DoctorListMessage(doctor_list=doctorList)

      @endpoints.method(DoctorDiseaseMessage,SpecilizationListMessage,
                      path='specilizationbydisease',http_method='GET',
                      name='SpecilizationInfo.get_by_disease_name',
                      
                        )
      def get_specilization_by_disease_name(self,request):
            limit=request.limit
            offset=request.offset
            i=0
            for q in request.name:
                  request.name[i]=q.lower()
                  i=i+1
            if not request.name:
                  return SpecilizationListMessage(specilization_list=[])
            query=SpecilizationStore.query(SpecilizationStore.specilization.disease_name.name.IN(request.name))
            specializationList=[]
            qryArray=[]
            if query is not None:
                  qryArray=query.fetch(limit=limit,offset=offset)
            for q in qryArray:
                  specializationList.append(q.specilization)

            return SpecilizationListMessage(specilization_list=specializationList)
    
      @endpoints.method(DoctorDiseaseMessage,DoctorListMessage,
                      path='doctorbydisease',http_method='GET',
                      name='DoctorInfo.get_by_disease_name',
                      
                        )
      def get_doctor_by_disease_name(self,request):
            limit=request.limit
            offset=request.offset
            i=0
            for q in request.name:
                  request.name[i]=q.lower()
                  i=i+1
            if not request.name:
                  return DoctorListMessage(doctor_list=[])
            query=SpecilizationStore.query(SpecilizationStore.specilization.disease_name.name.IN(request.name))
            specializationList=[]
            qryArray=[]
            if query is not None:
                  qryArray=query.fetch(limit=limit,offset=offset)
            for q in qryArray:
                  specializationList.append(q.specilization.name)

            if not specializationList:
                  return DoctorListMessage(doctor_list=[])

            doctorList=[]
            qryArray=[]
            docQuery=DoctorStore.query(DoctorStore.doctor.designation.name.IN(specializationList))

            if docQuery is not None:
                  qryArray=docQuery.fetch(limit=limit,offset=offset)
            for q in qryArray:
                  doctorList.append(q.doctor)
            return DoctorListMessage(doctor_list=doctorList)

            
            


























            
        
