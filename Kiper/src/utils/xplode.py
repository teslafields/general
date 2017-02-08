import time
import sys
sys.path.append('..')
from kiperserver import *
from commands import IPWALL, USER, SETRF
ipwall = IPWALL
server=KiperServer()
x = 100
print('ipwall ---> ',ipwall)
while True:
    try:
        server.handler.ping()
        print(server.handler.now())
        time.sleep(3)
        server.handler.start_emergency()
        print(server.handler.now())
        time.sleep(3)
        server.handler.stop_emergency()
        print(server.handler.now())
        time.sleep(3)
        for idw in range(x, x+10):
            print('ipwall_id', idw)
            ipwall.update({'ipwall_id': idw})
            ipwall.update({'ip': '10.10.123.'+str(idw)})
            server.handler.insert_ipwall(ipwall)
            print(server.handler.now())
            time.sleep(3)
    except KeyboardInterrupt:
        server.shutdown()
        break

