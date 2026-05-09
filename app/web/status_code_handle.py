from fastapi import HTTPException, Response
from app.web.response_statuses import common_statuses

'''
HTTP status code-handlers for typical situations

Here we work around HTTP response status codes:
    A) via throwing HTTPException - change status code
    B) via adding info about status code from response_statuses.py
    
    # ------ TODO if need in future ------------ 
        C) via modifing Request object from router`s function 
            - need when one endpoint can return multiple successfull 2XX codes (not HTTPException case)  
            - usage: add response: Response parametr to raute`s function and pass it to handler. so that response.status_code can be modified directly
    PS
     A) HTTPException must cover such situations as C), but who knows. anyway the point and algo of C) is noted above
    # ------------------------------------------
'''


# throws Exception itself (fastapi func) - no need to patch
def category_handler(category: str):
    '''Throws HTTP exception when chosen category doesn`t excists'''
    avaliable_categorirs = ['биоотходы', 'стекло', 'пластик']
    if category not in avaliable_categorirs:
        raise HTTPException(409, detail={
            'body_params_dict': common_statuses[409]['CONFLICT_WasteCategory'],
            'error_values': f'{category}'
        })   


def amount_to_create_handler(amount: int):
    ''' handles when it`s invalid amount of entities to create
        - Returns Response 204 (tricky to throw due it have to contain empty content field and fastapi violates it) or Throws HTTP exception when amount < 0'''
    if amount == 0:
        return Response(status_code=204)  # special case with no metadata on purose: 204 must have no 'content'
    
    elif amount < 0:
        raise HTTPException(422, detail={
            'body_params_dict': common_statuses[422]['ERR_NEGATIVE_ENTITIES'],
            'error_values': f'{amount}'
        })
