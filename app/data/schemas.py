from pydantic import BaseModel, Field
from typing import Optional, Dict
from datetime import timedelta, datetime   # for Interval type




# ======= Response =======
# API response template
class API_Response(BaseModel):
   class MetaData(BaseModel):
      total: int = 0
      metadata: str = 'metadata here'
   
   # actual data from Data base:
   data: list[object] = []
   # metadata about data (for pagination)
   meta: Optional[MetaData] = {} #= Optional[Dict]
   # some request info:
   status: str = 'not implemented' # code-word to identify response from API | why? - 400 code may be caused by several reasons - so status-code-word clarifies the reason of 400-code
   details: Optional[str] = ''         # details about status | see response_details.py  | for ex explain why client gets 400-code and how to fix it 
   error_values: Optional[object] = []       # exact values that caused an exception


# ==== Tables

# separate inherit from BaseModel, due there`s different PK (category) - not id and excluding pole is too tricky ( Field(exclude=True) doesn`t work and stackoverflow suggest post-proceessing xD`) 
class WasteCategory(BaseModel):
   category: str
   time_to_recycle: timedelta
   # auto generated poles - so make `em optional (by None)
   created_at: Optional[datetime] =  None
   updated_at: Optional[datetime] =  None

# common poles for each table
class CommonTable(BaseModel):
   # auto generated poles - so make `em optional (by None)
   id: Optional[str] = None
   created_at: Optional[datetime] =  None
   updated_at: Optional[datetime] =  None

   # add support for orm`s objects - by poles (in pydentic - by keys):
   #   in orm:      id = data.id
   #   in pydentic: id = data['id']  
   class Config:
     from_attributes = True

class Polluter_OO(CommonTable):
   name: str  
   x_geo: float
   y_geo: float

class PolluterWaste(CommonTable):
   amount: int 
   category: str
   polluter_id: str = Field(..., length=36)
   

'''
#TODO-Microsevice
   !!! mb will be usefull for HTTP request to Recycler Microservice 
   - or mb not (some poles aren`t needed for Recycler to define if it has free slots for Wastes)
   
   - Was used in IPC to feed data to Demon 
   - much alike to HTTP request where raw sqlalchemy model is invalid to pass
    
'''
def convert_to_pydentic(model_obj, pydentic_cls):
   '''   
   sql_alchemy_model -> pydentic object

      - also converts UUID poles to str (id pole: pole "id" or pole that ends with "_id")
   '''
   params = model_obj.__dict__
   for k, v in params.items():
      # cast ids to str - to make pydentic and postgres CALM about UUID4 and str for id in different places - everywhere`ll be str
      if k == 'id' or k.endswith('_id'):
         params[k] = str(v)         

   return pydentic_cls(**params)

