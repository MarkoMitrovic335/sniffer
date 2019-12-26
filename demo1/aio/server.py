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

async def endpoint(request):
    if request.method == 'GET':
              
        result = [i for i in session.query(data.Data).all()]
                
        for d in result:
            time_db=d.time_stamp
            source_address_db=d.source_address
            destination_address_db=d.destination_address
            method_db = d.method
            destination_api_db = d.destination_api
            payload_db = d.payload
            if method_db == 'GET':
                if destination_api_db == 'http://192.168.1.160/SSI/info_eventlog.htm':
                    print(d.destination_api)
                    data_dict_db = {"time_stamp":time_db,
                            "source_address":source_address_db,
                            "destination_address":destination_address_db,
                            "method":method_db,
                            "destination_api":destination_api_db,
                            "payload":payload_db}

                    packed_dict_db = msgpack.packb(data_dict_db, use_bin_type=True)
                    # print(packed_dict_db)
                    print("------------------------------------------------------------")
                    return web.json_response(data_dict_db)

        return web.Response(text="Get method called")
    elif request.method == 'POST':
        web.Response(text="POST METHOD CALLED")

async def init() -> web.Application:
    app = web.Application()
    app.router.add_get("/url", endpoint)
    app.router.add_post("/url", endpoint)
    return app

web.run_app(init())
    
