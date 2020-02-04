import sys
sys.path.append('/home/marko/PROJECTS/ast-proxy/demo1/model/')
import json
from urllib import request
from urllib.parse import urlparse
from pprint import pprint
from collections import namedtuple

import msgpack
import pyshark

from base import Session
from reqres import ReqRes

# temp request
reqs = {}

# decoding payload
def parse_http_payload(payload: str) -> bytes:
    body = []

    for i in range(0, len(payload), 3):
        c = payload[i:i+2]
        c = int(c, 16)
        body.append(c)
    
    body = bytes(body)
    return body

# parsing url path
def parse_http_path_from_uri(uri):
    o = urlparse(uri)
    s = len(f'{o.scheme}://{o.netloc}')
    path = uri[s:]
    return path

# capturing packets
def capture_packets():
    global reqs

    filtered_capture = pyshark.LiveCapture(
        interface='enp3s0',
        # display_filter='http.response || http.request || http.host == 192.168.1.160',
        display_filter='http',
        only_summaries=False,
    )

    for packet in filtered_capture.sniff_continuously():
        
        if not hasattr(packet, 'http'):
            continue
        
        # ///
        tmp_url = ""
        try:
            tmp_url = packet.http.request_uri
        except:
            pass
        if tmp_url == "/login.cgi":
            print("found")
        # ///

        if packet.ip.dst == '192.168.1.1' and getattr(packet.http, 'request', None):  # http request
            key = packet.http.request_uri
            value = packet
            reqs[key] = value
        elif packet.ip.src == '192.168.1.1' and getattr(packet.http, 'response', None):   # http response
            uri = packet.http.response_for_uri
            path = parse_http_path_from_uri(uri)
            key = path
            value = reqs.get(key, None)
            
            if not value:
                continue
            
            # req/res packets
            req_packet = value
            res_packet = packet
            
            # req_payload = getattr(req_packet.http, 'file_data', namedtuple('file_data', ['binary_value'])(b'')).binary_value
            if hasattr(req_packet.http, 'file_data'):
                req_payload = req_packet.http.file_data.binary_value
            else:
                req_payload = b''
            
            try:
                res_content_type = res_packet.http.content_type
                res_payload = res_packet.http.file_data.binary_value # payload in binary
            except:
                pass

            # print(res_packet.http.content_type)

            # if res_packet.http.content_type=="image/png":
            #     print(dir(res_packet.http.content_type))
                
            if not res_payload:
                res_payload = getattr(res_packet.http, 'file_data', '') 
                        
            # session
            session = Session()
            
            reqres = ReqRes(
                req_ts=str(req_packet.sniff_time),
                req_method=req_packet.http.request_method,
                req_path=req_packet.http.request_uri,
                req_headers=None,
                req_payload=req_payload,
                res_ts=str(res_packet.sniff_time),
                res_status=int(res_packet.http.response_code),
                res_content_type=res_content_type,
                res_payload=res_payload,
            )
            
            
            # print('!', len(getattr(res_packet.http, 'file_data', '')))
            print("packet arived")
            session.add(reqres)
            session.commit()
            session.close()
            session = None

# for capturing all packets of an given ip
capture_packets()

