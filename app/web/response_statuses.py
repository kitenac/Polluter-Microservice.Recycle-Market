'''
Setting up info for HTTP codes:
    Status - code-word 
    Detailes - clarification of Staus
'''
common_statuses = {
    200: {
        'OK': {
            'status': 'OK',
            'details': 'all right'
        }
    },
    201: {
        'CREATED':
        {
            'status': 'OK',
            'details': 'entity created'
        }
    },
    404: {
        'NO_SUCH_RESOURCE': {
            'status': 'NO_SUCH_RESOURCE',
            'details': 'Chosen resource doesn`t excists!'
        }
    },
    409: {
        'CONFLICT_DATA': {
            'status': 'CONFLICT_DATA',
            'details': 'Chosen type of data doesn`t excists!'
        }
    },
    422:{
        'ERR_BAD_DATA': {
            'status': 'ERR_BAD_DATA',
            'details': 'paramter doesn`t meet limits'
        },
        'ERR_NEGATIVE_ENTITIES':{
            'status': 'ERR_NEGATIVE_ENTITIES',
            'details': 'Number of entitis must be > 0. -You can try DELETE method for this resource instead :)'
        },
    },
    500: {
        'UNHANDLED_EXCEPTION': {
            'status': 'UNHANDLED_EXCEPTION',
            'details': 'Something unpredicted happend. Check "error values" for more info'
        }
    },
}


recycler_statuses = {
    400: {
        'NOT_ENOUGH_SPACE': {
            'status': 'NOT_ENOUGH_SPACE',
            'details': 'Required wastes configuration can`t be accepted by chosen Recycler. Check avaliable storage space for each type of waste in chosen Recycler'
        },
    },
    409: {
        'CONFLICT_PK': {
            'status': 'CONFLICT_PK',
            'details': 'Chosen combination of PK-s: waste_category, recycler_id - already excists!'
        },
    }
}

