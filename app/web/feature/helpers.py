'''
Search method = pagination + filtering + sorting

Requested params:
    Pagination - from Path:       
        limit: 10
        page: 1
        order: '-name'

    Filter - form Body:
        "filter_column":"name"
        "value": "jhon"
         
'''
from sqlalchemy import desc
from app.data.schemas import PaginationParams


def prepare_params(
        params: PaginationParams,  
        model: object
    ):
    '''
    Calculate params for /search:
     - pagination and ordering from Pagination params 
    '''
    
    def get_order(column: str):
        '''
        Getting order (column-object for sqlalchemy query.order_by()
        column:  asc: name | desc: -name
        order:   expected to be an object - column of table(model),
                    e.g. order = Polluter.name
        '''

        if column not in model.__table__.columns.keys():
            return False # no sorting required

        # Truncate leading '-' and set DESC mode if need
        ASC = True  # ascending sorting
        if column[0] == '-':
            ASC = False
            column = column[1:len(column)]

        # validate if column from request persists in table and apply sorting in ASC or DESC to statement 
        if ASC:
            return model.__dict__[column] 
        else:
            return desc(model.__dict__[column]) 
        
    # count page
    skip = (params.page - 1) * params.limit  # -1 - due index shift (frontend counts pages from 1, not from 0)
    # ordering
    ordering = get_order(params.order)

    return skip, ordering

