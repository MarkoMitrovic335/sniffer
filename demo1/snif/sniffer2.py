import sys
sys.path.append('/home/marko/PROJECTS/ast-proxy/demo1/model/')
import json
from urllib import request
from urllib.parse import urlparse
from pprint import pprint

import msgpack
import pyshark

from base import Session
from reqres import ReqRes


# temp request
reqs = {}


def parse_http_payload(payload: str) -> bytes:
    body = []

    for i in range(0, len(payload), 3):
        c = payload[i:i+2]
        c = int(c, 16)
        body.append(c)
    
    body = bytes(body)
    return body


def parse_http_path_from_uri(uri):
    o = urlparse(uri)
    s = len(f'{o.scheme}://{o.netloc}')
    path = uri[s:]
    return path


def capture_packets():
    global reqs

    filtered_capture = pyshark.LiveCapture(
        interface='enp3s0',
        display_filter='http.response || http.request || http.host == 192.168.1.160',
    )

    for packet in filtered_capture.sniff_continuously():
        if not hasattr(packet, 'http'):
            continue
            
        if packet.ip.dst == '192.168.1.160' and getattr(packet.http, 'request', None):
            # request
            print(f'request: {packet.http!r}')
            # pprint(dir(packet.http))
            # pprint(dict(packet.http.__dict__))
            key = packet.http.request_uri
            value = packet
            reqs[key] = value
        elif packet.ip.src == '192.168.1.160' and getattr(packet.http, 'response', None):
            # response
            print(f'response: {packet.http!r}')
            # pprint(dir(packet.http))
            pprint(dict(packet.http.__dict__))
            uri = packet.http.response_for_uri
            path = parse_http_path_from_uri(uri)
            key = path
            value = reqs.get(key, None)

            if not value:
                continue
            
            # req/res packets
            req_packet = value
            res_packet = packet

            # session
            session = Session()
            
            reqres = ReqRes(
                req_ts=str(req_packet.sniff_time),
                req_method=req_packet.http.request_method,
                req_path=req_packet.http.request_uri,
                req_headers=None,
                req_payload=getattr(req_packet.http, 'file_data', ''),
                res_ts=str(res_packet.sniff_time),
                res_status=int(res_packet.http.response_code),
                res_content_type=res_packet.http.content_type,
                res_payload=getattr(res_packet.http, 'file_data', ''),
            )

            session.add(reqres)
            session.commit()
            session.close()
            session = None

# for capturing all packets of an given ip
capture_packets()
