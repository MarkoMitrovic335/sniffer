import pyshark
import msgpack
from model import data
from sqlalchemy.orm import sessionmaker

# creating engine from data model function
engine = data.db_create()

# creating session and binding engine
session = sessionmaker(bind=engine)()

def capture_packets():
    
    filtered_capture = pyshark.LiveCapture(interface='enp3s0',display_filter='ip.dst == 192.168.1.106 || http.host == 192.168.1.106') #ip.dst is a destination address and it will recive an ip layer for that address

    # filtered_capture = pyshark.LiveCapture(interface='enp3s0',display_filter='http.host == 192.168.1.106') #this should be used only and it should work without try and catch

    # filtered_capture = pyshark.LiveCapture(interface='enp3s0',display_filter='ip.src == 192.168.1.106') #ip src is an ip as a source address and it will recive and send all packets from that source address

    for packet in filtered_capture.sniff_continuously():

        packet.pretty_print()

        # try and catch using cause of display filter, it will try to cathc http layer
        try:
    #     collecting data from packets
            time_stamp = str(packet.sniff_time)
            source_address = packet.ip.addr
            destination_address = packet.http.host
            method = packet.http.request_method
            destination_api = packet.http.referer
            payload = packet.tcp.payload    
                    
        #   creating data object
            data_obj = data.Data(time_stamp,source_address,destination_address,method,destination_api,payload)

        #   storing in db
            session.add(data_obj)
            session.commit()
                
            # calling a function - reading_from_db()
            reading_from_db()
        except:
           pass

def reading_from_db():
    result = [i for i in session.query(data.Data).all()]

    for d in result:
                
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
        packed_dict_db = msgpack.packb(data_dict_db, use_bin_type=True)
        print(packed_dict_db)
        print("------------------------------------------------------------")
        
# function to capture http requests
def capture_http_request():
    filtered_capture1 = pyshark.LiveCapture(interface='enp3s0', display_filter='http.request || http.host=="192.168.1.160"')
    for packet in filtered_capture1.sniff_continuously():
        packet.pretty_print()
        print("---------------------------------------------------")

# function to capture http responses
def capture_http_response():
    filtered_capture2 = pyshark.LiveCapture(interface='enp3s0', display_filter='http.response || http.host=="192.168.1.160"')
    for packet in filtered_capture2.sniff_continuously():
        packet.pretty_print()
        print("---------------------------------------------------")

# for capturing all packets of an given ip
capture_packets()

# this function is for reading data from db and is been called in capure_packet function
# reading_from_db()

# if we want to capture only http response
# capture_http_response()

# if we want to capture only http request
# capture_http_request()