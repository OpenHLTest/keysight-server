from openhltest_client.httptransport import HttpTransport

OPENHLTEST_SERVER = '127.0.0.1:443'
CONFIG_FILE = 'openhltest_config_1.json'

transport = HttpTransport(OPENHLTEST_SERVER)

transport.info("get an instance of the OpenHlTest module class")
openhltest = transport.OpenHlTest

transport.info("get a list of Sessions")
sessions = openhltest.Sessions.read()
transport.info(sessions)

transport.info("get an instance of the Config class")
config = sessions.Config
config.Clear()

transport.info("load a configuration")
config.Load({'mode': 'RESTCONF_JSON', 'file-name': CONFIG_FILE})

transport.info("commit configuration to vendor hardware")
config.Commit()
