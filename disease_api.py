#sample test file to test various apis
import endpoints
from disease_api_messages import *
from protorpc import messages
from protorpc import remote

WEB_CLIENT_ID='yo yo sample id'
ANDROID_CLIENT_ID='yo yo ULHA sample id'
IOS_CLIENT_ID='yo yo ULLUsample id'
ANDROID_AUDIENCE= WEB_CLIENT_ID
WEB_CLIENT_ADMIN_ID="adminstuff@adminstuff"
@endpoints.api(name='diseaseinfo',version='v1',
               allowed_client_ids=[WEB_CLIENT_ID,
                                   ANDROID_CLIENT_ID,
                                   IOS_CLIENT_ID,
                                   endpoints.API_EXPLORER_CLIENT_ID],
               audiences=[],
               scopes=[endpoints.EMAIL_SCOPE],
               description="API To ACCESS WEB SERVICES For disease data")
class DiseaseInfoApi(remote.Service):
      #TODO ADD AUTHORIZATION
      @endpoints.method(DiseaseMessage,DiseaseMessage,
                      path='diseaseInsert',http_method='POST',
                      name='diseaseInfo.insert',
                      allowed_client_ids=[WEB_CLIENT_ADMIN_ID]
                        )
      def insert_disease(self,request):
          #Normalizing the fields
          disease=request.disease
          disease.primary_name= disease.primary_name.lower()
          if(not disease.secondry_names):
                disease.secondry_names =[Name(name=disease.primary_name.lower())]
          else:
              disease.secondry_names[0].name=disease.primary_name.lower()  

          i=0
          for q in disease.secondry_names:
                disease.secondry_names[i].name = q.name.lower()
                i=i+1
          i=0
          for q in disease.symptoms:
               disease.symptoms[i].primary_name = q.primary_name.lower()
               if(not disease.symptoms[i].secondry_names):
                 disease.symptoms[i].secondry_names =[Name(name=q.primary_name.lower())]
               else:
                 disease.symptoms[i].secondry_names[0].name=q.primary_name.lower()
               j=0
               for r in disease.symptoms[i].secondry_names:
                      disease.symptoms[i].secondry_names[j].name= r.name.lower()
                      j=j+1
               i=i+1
    
          response=DiseaseStore(disease=request.disease).put()
          for q in request.disease.symptoms:
                SymptomsStore(symptoms=q).put()
          ##TODO return the response instead of request
          ##TODO make complex arrangements so that the complexity of primary names and
          ##Secondry names can be removed
          return request

      @endpoints.method(DiseaseAndSymptomsNameMessage,DiseaseListMessage,
                      path='diseaseget_byName',http_method='GET',
                      name='diseaseInfo.getdisease'
                       )
      def get_disease_byname(self,request):
           offset=request.offset
           limit=request.limit
           query=DiseaseStore.query()
           i=0
           for q in request.ds_name:
                request.ds_name[i]=q.lower()
                i=i+1

           if request.ds_name :
            query=query.filter(DiseaseStore.disease.secondry_names.name.IN(request.ds_name))

           diseaseList=[]
           qryArray=[]
           if query is not None:
                 qryArray=query.fetch(limit=limit,offset=offset)
           for q in qryArray:
                 diseaseList.append(q.disease)
         
           return DiseaseListMessage(disease_list=diseaseList)

      @endpoints.method(DiseaseAndSymptomsNameMessage,DiseaseListMessage,
                      path='diseaseget_by_Symptoms_Name',http_method='GET',
                      name='diseaseInfo.getdisease_bySymptoms'
                       )
      def get_disease_by_symptoms_name(self,request):
           offset=request.offset
           limit=request.limit
           query=SymptomsStore.query(projection=[SymptomsStore.symptoms.primary_name], group_by=[SymptomsStore.symptoms.primary_name])
           
           i=0
           for q in request.ds_name:
                 request.ds_name[i]=q.lower()
                 i=i+1

           if request.ds_name :
            query=query.filter(SymptomsStore.symptoms.secondry_names.name.IN(request.ds_name))

           symptomsNameList=[]
           qryArray=[]
           if query is not None:
                 qryArray=query.fetch(limit=limit,offset=offset)
           for q in qryArray:
                 symptomsNameList.append(q.symptoms.primary_name)

           diseaseQuery=DiseaseStore.query(DiseaseStore.disease.symptoms.primary_name
                                           .IN(symptomsNameList))
          

           diseaseList=[]
           qryArray=[]
           if diseaseQuery is not None:
                 qryArray=diseaseQuery.fetch(limit=limit,offset=offset)
           for q in qryArray:
                 diseaseList.append(q.disease)
         
           return DiseaseListMessage(disease_list=diseaseList)
