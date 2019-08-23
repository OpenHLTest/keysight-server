'''Sanity scaffolding script

'''
import json
import time
from openhltest_client.httptransport import HttpTransport


OPENHLTEST_SERVER = '127.0.0.1:443'


transport = HttpTransport(OPENHLTEST_SERVER)
# transport.set_debug_level()

transport.info('get an instance of the OpenHlTest module class')
openhltest = transport.OpenHlTest

transport.info('get a Sessions instance')
sessions = openhltest.Sessions.read()
if len(sessions) == 0:
    sessions = openhltest.Sessions.create('IxNetwork GUI')
transport.info(sessions)

transport.info('get an instance of the Config class and clear the configuration')
config = sessions.Config

transport.info('clear statistics')
sessions.Statistics.Clear()

transport.info('start traffic')
config.TrafficControl({"mode": "START", "targets": []})

transport.info("port statistics")
for port in sessions.Statistics.Port.read():
	transport.info('%s tx-frames:%s rx-frames:%s' % (port.Name, port.TxFrames, port.RxFrames))

transport.info("port-traffic statistics")
for port_traffic in sessions.Statistics.PortTraffic.read():
	transport.info('%s tx-frames:%s rx-frames:%s' % (port_traffic.Name, port_traffic.TxFrames, port_traffic.RxFrames))

transport.info('PASS')
