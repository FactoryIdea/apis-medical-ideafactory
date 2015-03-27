from disease_api import *
from medicine_api import *
import endpoints

APPLICATION = endpoints.api_server([DiseaseInfoApi,MedicineInfoApi],
                                   restricted=False)

