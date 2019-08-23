import time
from openhltest_client.httptransport import HttpTransport

# create an instance of the transport class
# by default the HttpTransport will use the internal MockServer to allow for baseline testing
# to connect to a vendor server implementation pass in a valid hostname or ip address
transport = HttpTransport() #'127.0.0.1:443')
transport.set_debug_level()

transport.info("get an instance of the OpenHlTest module class")
openhltest = transport.OpenHlTest

transport.info("get a list of Sessions")
sessions = openhltest.Sessions.read()
sessions = openhltest.Sessions.create(Name='IxNetwork GUI')
print(sessions)

transport.info("get an instance of the Config class")
config = sessions.Config

transport.info("clear any existing configuration")
config.Clear()

transport.info("load a vendor specific binary configuration")
config.Load({'mode': 'VENDOR_BINARY', 'file-name': 'c:/users/anbalogh/downloads/openhltest.ixncfg'})

transport.info("save the configuration as an openhltest json file")
json_config = config.Save({'mode': 'RESTCONF_JSON', 'file-name': 'openhltest.json'})

transport.info("print all the port resources")
for port in config.Ports.read():
    print('- ports %s [location: %s]' % (port.Name, port.Location))

transport.info("print the device-groups resources")
for device_group in config.DeviceGroups.read():
    print('- device-groups %s [ports: %s]' % (device_group.Name, " ".join(device_group.Ports)))
    for device in device_group.Devices.read():
        print('\t- devices %s [device-count-per-port: %s]' % (device.Name, device.DeviceCountPerPort))
        for protocol in device.Protocols.read():
            print('\t\t- protocol %s [link: %s]' % (protocol.Name, protocol.ParentLink))

transport.info("print the device-traffic resources")
for traffic_item in config.DeviceTraffic.read():
    print('- device-traffic %s' % traffic_item.Name)
    for frame in traffic_item.Frames.read():
        print('\t- frame %s [type: %s]' % (frame.Name, frame.FrameType))

transport.info("connect the abstract ports to test ports")
config.PortControl({"mode": "CONNECT", "targets": []})

transport.info("start the device-groups")
config.DeviceGroupsControl({"mode": "START", "targets": []})

transport.info("start the device-traffic")
config.TrafficControl({"mode": "START", "targets": []})

time.sleep(15)

transport.info("print the port statistics")
for port in sessions.Statistics.Port.read():
	transport.info('%s tx-frames:%s rx-frames:%s' % (port.Name, port.TxFrames, port.RxFrames))

transport.info("print the device-traffic statistics")
for device_traffic in sessions.Statistics.DeviceTraffic.read():
	transport.info('%s tx-frames:%s rx-frames:%s' % (device_traffic.Name, device_traffic.TxFrames, device_traffic.RxFrames))

