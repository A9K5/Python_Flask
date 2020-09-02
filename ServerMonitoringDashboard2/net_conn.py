# import collections

# NetConn = collections.namedtuple('pconn',['fd','family','type','laddr','raddr','status','pid'])
# P = NetConn(115, AddressFamily.AF_INET: 2, SocketType.SOCK_STREAM: 1, addr(ip='10.0.0.1', port=48776), addr(ip='93.186.135.91', port=80), 'ESTABLISHED', 1254)
# # [pconn(fd=115, family=<AddressFamily.AF_INET: 2>, type=<SocketType.SOCK_STREAM: 1>, laddr=addr(ip='10.0.0.1', port=48776), raddr=addr(ip='93.186.135.91', port=80), status='ESTABLISHED', pid=1254),
# #  pconn(fd=117, family=<AddressFamily.AF_INET: 2>, type=<SocketType.SOCK_STREAM: 1>, laddr=addr(ip='10.0.0.1', port=43761), raddr=addr(ip='72.14.234.100', port=80), status='CLOSING', pid=2987),
# #  pconn(fd=-1, family=<AddressFamily.AF_INET: 2>, type=<SocketType.SOCK_STREAM: 1>, laddr=addr(ip='10.0.0.1', port=60759), raddr=addr(ip='72.14.234.104', port=80), status='ESTABLISHED', pid=None),
# #  pconn(fd=-1, family=<AddressFamily.AF_INET: 2>, type=<SocketType.SOCK_STREAM: 1>, laddr=addr(ip='10.0.0.1', port=51314), raddr=addr(ip='72.14.234.83', port=443), status='SYN_SENT', pid=None)
# #  ...]


import socket
from socket import AF_INET, SOCK_STREAM, SOCK_DGRAM
import psutil


AD = "-"
AF_INET6 = getattr(socket, 'AF_INET6', object())
proto_map = {
    (AF_INET, SOCK_STREAM): 'tcp',
    (AF_INET6, SOCK_STREAM): 'tcp6',
    (AF_INET, SOCK_DGRAM): 'udp',
    (AF_INET6, SOCK_DGRAM): 'udp6',
}


def main():
    templ = "%-5s %-30s %-30s %-13s %-6s %s"
    # print(psutil.net_connections(kind='inet'))
    print(templ % (
        "Proto", "Local address", "Remote address", "Status", "PID",
        "Program name"))
    proc_names = {}
    jsonmsg = []

    for p in psutil.process_iter(attrs=['pid', 'name']):
        proc_names[p.info['pid']] = p.info['name']

    for c in psutil.net_connections(kind='inet'):
        laddr = "%s:%s" % (c.laddr)
        raddr = ""
        if c.raddr:
            raddr = "%s:%s" % (c.raddr)
        jsonmsg.append({"Proto": proto_map[(c.family, c.type)],
                        "Local address": laddr,
                        "Remote address": raddr or AD,
                        "Status": c.status,
                        "PID": c.pid or AD,
                        "Program name": proc_names.get(c.pid, '?')[:15]
                        })
        # print(templ % (
        #     proto_map[(c.family, c.type)],
        #     laddr,
        #     raddr or AD,
        #     c.status,
        #     c.pid or AD,
        #     proc_names.get(c.pid, '?')[:15],
        # ))
    print(jsonmsg)


if __name__ == '__main__':
    main()
