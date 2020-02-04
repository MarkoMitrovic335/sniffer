import sys
sys.path.append('/home/marko/PROJECTS/ast-proxy/demo1/model/')

from aiohttp import web

from base import Session
from reqres import ReqRes

async def handler(request):
    path = request.match_info.get('path', '')
    path = f'/{path}'
    # print(f'DEBUG: path: {path!r}')

    # query database
    session = Session()
    q = session.query(ReqRes)
    
    q = q.filter(
        ReqRes.req_method=='GET', # query filter
        ReqRes.req_path==path,
    ) 

    reqres = q.first()
    
    if reqres:
        # pprint(reqres)
        # pprint(dir(reqres))
        res_status = reqres.res_status
        res_content_type = reqres.res_content_type
        res_payload = reqres.res_payload
        # print(res_status)
        # print(res_content_type)
        # print(res_payload)
    else:
        res_status = 500
        res_content_type = None
        res_payload = None

    session.close()
    session = None
    
    if not res_payload:
        
        return web.Response(
            status=res_status,
            body=b'',
            content_type='text/html'
        )
    
    # query against database for `path`
    res_content_type = res_content_type.split(';')[0]

    res = web.Response(
        body=res_payload if isinstance(res_payload, bytes) else res_payload.encode(),
        status=res_status,
        headers=None,
        content_type=res_content_type,
    )

    return res

app = web.Application()

app.add_routes([
    web.get('/{path:.*}', handler)
])

if __name__ == '__main__':
    web.run_app(app, host="printer.com")