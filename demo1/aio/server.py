from aiohttp import web
import asyncio
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import sys
sys.path.append('/home/marko/PROJECTS/ast-proxy/demo1/model/')
import data
import msgpack

engine = data.db_create()
session = sessionmaker(bind=engine)()

with open('/home/marko/PROJECTS/ast-proxy/demo1/auth/index.html', 'r') as f:
    html_string = f.read()

async def endpoint(request):
    if request.method == 'GET':
                              
        return web.Response(text=html_string,content_type='text/html')

        
        
    elif request.method == 'POST':
        web.Response(text="POST METHOD CALLED")

def reading_from_db():
    result = [i for i in session.query(data.Data).all()]

    for d in result:
        # print(d.time_stamp)
        # taking valuse from db
        time_db=d.time_stamp
        source_address_db=d.source_address
        destination_address_db=d.destination_address
        method_db = d.method
        destination_api_db = d.destination_api
        payload_db = d.payload

        data_dict_db = {"time_stamp":time_db,
                        "source_address":source_address_db,
                        "destination_address":destination_address_db,
                        "method":method_db,
                        "destination_api":destination_api_db,
                        "payload":payload_db}

        # formating dict to msgpack format
        # packed_dict_db = msgpack.packb(data_dict_db, use_bin_type=True)
        print(data_dict_db)
        # print("------------------------------------------------------------")
        return(data_dict_db)

        
        # with open(destination_api_db, 'r') as f:
        #         html_string = f.read()
        #         print(html_string)
       
            

async def init() -> web.Application:
    app = web.Application()
    app.router.add_get("/", endpoint)
    app.router.add_post("/", endpoint)
    return app

web.run_app(init())
    
