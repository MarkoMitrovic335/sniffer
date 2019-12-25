import pcap


sniffer = pcap.pcap(name='enp3s0', promisc=True, immediate=True, timeout_ms=50)

def parse_address(pkt, offset):
    return pkt[offset:offset+4]

def format_address(addr):
    return f'{addr[0]}.{addr[1]}.{addr[2]}.{addr[3]}'

for ts, pkt in sniffer:
    src_addr = parse_address(pkt, sniffer.dloff + 12)
    dst_addr = parse_address(pkt, sniffer.dloff + 16)
    f_src_addr = format_address(src_addr)
    f_dst_addr = format_address(dst_addr)
    # if f_src_addr != '192.168.1.182': continue
    if f_dst_addr != '192.168.1.160': continue
    print(f'{ts}\t{f_src_addr}\t{f_dst_addr}')
    print(ts, pkt)
    print()