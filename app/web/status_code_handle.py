from fastapi import HTTPException, Response
from app.web.response_statuses import common_statuses

from functools import wraps # to correctly wrap (in my custom wrapper) endpoint`s functions - so that fastapi and OpenAPI can be pretty
#from psycopg.errors import ForeignKeyViolation
from sqlalchemy.exc import IntegrityError

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

def try_except_commonHandler(endpoint_func: callable):
    ''' 
    *Mostly suitable for /endpoints that has id (FK) parametr (Body, PATH, ...) that must excist in Table
    
    This decorator:
        1. Wraps endpoint`s function into try/except construction
        - so, u dont need to manually write try/except blocks in each API method with such wrapper 
        
        2. Handels common errors like PK/FK violations from sqlalchemy 
        - also it pops up already handled in endpoint_func() Exceptions - tested 
    '''
    @wraps(endpoint_func)   # technical wrapping - so that fastapi and OpenAPI can be prettified
    async def wrapper(*args, **kwargs):
        # Normal execution scenario
        try:
            return await endpoint_func(*args, **kwargs)
        
        # ------ Handle common exceptions for endpoints ------
        except IntegrityError as e:
            invalid_FK_handler(e)

        except Exception as e:
            # here we bypass (raise upper) already handled Exceptions that poped up from endpoint`s function 
            if e.detail:
                raise HTTPException(e.status_code, e.detail)
            # ones that realy wasnt handled
            unknown_err_handler(e) 
    return wrapper


def unknown_err_handler(e: Exception):
    raise HTTPException(500, detail={
        'body_params_dict': common_statuses[500]['UNHANDLED_EXCEPTION'],
        'error_values': f'{e} \nDetailed: {e.__doc__}'
    })

def invalid_FK_handler(e: Exception):    
    '''handles id (FK) violations. That means that requested resource (id) is unavaliable'''
    raise HTTPException(404, detail={
            'body_params_dict': common_statuses[404]['NO_SUCH_RESOURCE'],
            'error_values': f'some FK value is invalid - check "id"-like parametrs or Investigate Exception: {e}'
    })       


# (UPD) Teeeeechincaly invalid_FK_handler() is capable to replace this method but in this case info`d be kinda mmessier - so mb later workaround to provide prettier output for mentioned method 
def category_handler(category: str):
    '''Throws HTTP exception when chosen category doesn`t excists'''
    avaliable_categories = ['биоотходы', 'стекло', 'пластик']
    if category not in avaliable_categories:
        raise HTTPException(409, detail={
            'body_params_dict': common_statuses[409]['CONFLICT_DATA'],
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
