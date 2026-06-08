'''
here we connect all parts of application to make it work:
routes,
middleware,
db sessions,
etc
'''
import uvicorn # server engine
import logging
from time import perf_counter

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from admin_page.page import create_admin_page
from app.data import schemas # data schemas

# routes - like mini-apps  
from app.web.routes import router as routes_OO 
from app.app_config import APP_WORK_CFG # config tells: dev or prod mode is running


MODE = APP_WORK_CFG['WORK_MODE']


# ==== HTTP App configuration
# Настройка логирования
log_lvl = logging.DEBUG if MODE == 'DEBUG' else logging.INFO # set logging.DEBUG if app run in DEBUG mode 
logging.basicConfig(level=log_lvl)
logger = logging.getLogger(__name__)


# App settings
API_BASE = '/api/v1.0'
atom_eco_app = FastAPI(
    root_path=API_BASE, 
    title=APP_WORK_CFG['service-name'],
    
    # Swager page patch-config (~open API client)
    swagger_ui_parameters={
        'defaultModelExpandDepth': 10,   # purpose: to expand schemas bar of parametrs by degfault (FastApi`s: Body/Path/...(description='') ). work: this swager param shows structure of models without switching to "shemas" bar . 
        'displayRequestDuration': True,  # display speed of request 
        'operationsSorter': 'method'     # sort displaing of endpoints - by HTTP method 
        }
    )

# CORS - настройка разрешённых ресурсов сервера
CORS_conf = {
  'origins': ['*'],  #  разрешённые адреса клиентов 
  'allow_creds': True,   # Разрешить отправку учётных данных
  'methods': ['*'],   # GET, POST, ...
  'headers': ['*']    # Accept, Content-Type, Referer, Content-Length ...
}

# Adding FastApi`s Middleware for CORS
atom_eco_app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_conf['origins'],     
    allow_credentials=CORS_conf['allow_creds'],   
    allow_methods=CORS_conf['methods'],     
    allow_headers=CORS_conf['headers'],     
)

# Adding custom Middleware for logging HTTP communication with API (requsests and responses)
@atom_eco_app.middleware('http')
async def log_communcation_with_API(request: Request, call_next):
    ''' just one of midleware chain function. has access to Requset in app`s context'''
    start_time = perf_counter()
    logger.debug(f"   Got request {request.method} {request.url.path} from {request.client.host}")  # NOTE: to see client IP if backend works via Proxy (i.e. HTTPS Proxy that unencrypts data) - check headers: X-Forwarded-For или X-Real-IP
    response = await call_next(request) # pass execution for next midleware in queue - mandatory step if u want midlware to work :)
    duration = (perf_counter() - start_time) * 1000 # convert 0.123 s -> to 123 ms
    logger.debug(f"   Response: {response.status_code} for client {request.client.host} ({duration:.3f}ms)")
    
    return response


# URL prefixes handlers 
# - like mini-apps for each url-prefix  
atom_eco_app.include_router(routes_OO) 


# Mount the admin page app to main app - /admin
admin = create_admin_page(atom_eco_app, templates_dir='admin_page/patch_templates')
atom_eco_app.mount(app=admin, path='/admin')


# ====  HTTPException handling
# TODO: upgrade, mb
@atom_eco_app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, e: HTTPException):

    return JSONResponse(
        status_code=e.status_code,
        content=schemas.API_Response(
          error_values = e.detail['error_values'],   # exact vvalues that caused an exception
          **e.detail['body_params_dict']             # some POST body params that tells about occured exception
        ).model_dump()
    )


def start_app():
    uvicorn.run(atom_eco_app, host="0.0.0.0", port=8001)