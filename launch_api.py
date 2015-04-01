from disease_api import *
from medicine_api import *
from doctor_api import *
import endpoints

APPLICATION = endpoints.api_server([DoctorInfoApi,DiseaseInfoApi,MedicineInfoApi],
                                   restricted=False)

