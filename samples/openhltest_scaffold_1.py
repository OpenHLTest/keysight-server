'''Sanity scaffolding script

'''
import json
import time
from openhltest_client.httptransport import HttpTransport


OPENHLTEST_SERVER = '10.36.67.212:8443'
#OPENHLTEST_SERVER = 'localhost:443'

CONFIG = [
    {
        'location': '10.36.74.26/2/13',
        'ipv4': {
            "source-address": '1.1.1.1',
            'prefix': 24,
            'gateway-address': '1.1.1.2'
        },
        'bgpv4': {
            'dut-ipv4-address': '1.1.1.2'
        } 
    },
    {
        'location': '10.36.74.26/2/14',
        'ipv4': {
            "source-address": '1.1.1.2',
            'prefix': 24,
            'gateway-address': '1.1.1.1'
        },
        'bgpv4': {
            'dut-ipv4-address': '1.1.1.1'
        }
    }
]


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
config.Clear()

networks = []
for i in range(0, len(CONFIG)):
    port = config.Ports.create(Name='Port %s' % (i + 1), Location=CONFIG[i]['location'])
    transport.info('add port %s' % port.Name)

    transport.info('add %s bgp protocol scenario' % port.Name)
    device_group = config.DeviceGroups.create(Name='Device Group %s' % port.Name, Ports=port)
    device = device_group.Devices.create(Name='Device %s' % port.Name , DeviceCountPerPort=1, ParentLink=None)
    parent = None
    for protocol_type in ['ETHERNET', 'VLAN', 'IPV4', 'BGPV4']:
        protocol = device.Protocols.create(Name='%s %s' % (protocol_type, port.Name), ProtocolType=protocol_type, ParentLink=parent)
        if protocol_type == 'IPV4':
            protocol.Ipv4.SourceAddress.update(PatternType='SINGLE', Single=CONFIG[i]['ipv4']['source-address'])
            protocol.Ipv4.Prefix.update(PatternType='SINGLE', Single=CONFIG[i]['ipv4']['prefix'])
            protocol.Ipv4.GatewayAddress.update(PatternType='SINGLE', Single=CONFIG[i]['ipv4']['gateway-address'])
        elif protocol_type == 'BGPV4':
            protocol.Bgpv4.DutIpv4Address.update(PatternType='SINGLE', Single=CONFIG[i]['bgpv4']['dut-ipv4-address'])
        parent = protocol.Name

    transport.info('add %s bgp route range' % device.Name)
    simulated_network = device_group.SimulatedNetworks.create(Name='Simulated Network %s' % port.Name, ParentLink=device.Name)
    network = simulated_network.Networks.create(Name='Network %s' % port.Name, NetworkType='BGPV4_ROUTE_RANGE', NetworkCountPerPort=5)
    network.Bgpv4RouteRange.Address.update(PatternType='RANDOM').Random.update(Min="10.10.10.1", Max="10.254.254.254", Step="0.0.0.1", Seed=i)
    network.Bgpv4RouteRange.PrefixLength.update(PatternType='SINGLE', Single="32")
    networks.append(network)

traffic = config.DeviceTraffic.create(Name='Device Traffic', Encapsulation='IPV4', BiDirectional=True, MeshType='ONE_TO_ONE', Sources=networks[0], Destinations=networks[1])
transport.info('added %s' % traffic.Name)
tcp = traffic.Frames.create(Name='TCP', FrameType='TCP').Tcp
tcp.SourcePort.update(PatternType='SINGLE', Single='12345')
tcp.DestinationPort.update(PatternType='SINGLE', Single='54321')

transport.info('configure frame length')
traffic.FrameLength.update(LengthType='INCREMENT').Increment.update(Start=68, End=1024, Step=3)

transport.info('configure frame rate')
traffic.FrameRate.update(Mode='FIXED').FixedRate.update(RateType='FRAMES_PER_SECOND', Fps=12345)
config.Commit()

transport.info('connect all ports')
config.PortControl({"mode": "CONNECT", "targets": []})

transport.info("start the device-groups")
config.DeviceGroupsControl({"mode": "START", "targets": []})

transport.info('clear statistics')
sessions.Statistics.Clear()

transport.info('start traffic')
config.TrafficControl({"mode": "START", "targets": []})

time.sleep(5)

transport.info('stop traffic')
config.TrafficControl({"mode": "STOP", "targets": []})

transport.info('wait for aggregate tx rate to go to 0')
while True:
    time.sleep(1)
    tx_rate = 0
    for port in sessions.Statistics.Port.read():
        tx_rate += int(port.TxFrameRate)
    if tx_rate == 0:
        break

transport.info("port statistics")
for port in sessions.Statistics.Port.read():
    transport.info(port)

transport.info("device-traffic statistics")
for traffic in sessions.Statistics.DeviceTraffic.read():
    transport.info(traffic)

transport.info('retrieve the current configuration for property checks')
config.Save({'mode': 'RESTCONF_JSON', 'file-name': 'config.json'})
with open('config.json') as fid:
    json_config = json.load(fid)

transport.info('PASS')
