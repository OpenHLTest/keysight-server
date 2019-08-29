# Keysight OpenHLTest Server
The Keysight OpenHLTest server is designed as a standalone server that will manage IxNetwork sessions according to the OpenHLTest model specifications.  

## What's New!
v0.3.0 
- supports Windows GUI and Linux API Server session management
- additional command line parameters 
- single executable can be deployed on linux64, win64 

## Features
1) The server can be upgraded independently of the IxNetwork installation and server releases will be published as soon as model features are implemented in the server.
2) The server can be driven with a standard auto-generated python client.

## Pre-requisites
1) The Keysight OpenHLTest server supports a minumim version of [IxNetwork 8.52](https://support.ixiacom.com/support-overview/product-support/downloads-updates/versions/68).

## Server Installation
A [binary release with specific platform assets](https://github.com/OpenHLTest/keysight-server/releases) has been provided that contains all the files needed to start the server.  The current binary support is targeted for win64 and linux64.
1) Unzip the contents of a binary asset file into a directory of your choosing.
2) Review the Server Startup to select your startup options that match your IxNetwork environment.

## Server Startup
The OpenHLTest server has command line parameters that allow it to be run in different configurations.
The following are the command line parameters:
- -apikey=<str, an api key from linux api server, not required for windows or connection manager>
- -secured=<bool, default is true, which is https scheme + self signed certificate>
- -restport=<int, default is 443, change it to listen on an alternate port>
- -debug=<bool, default is false, true will display requests and responses in the console>
  
### Windows GUI Session Management
- following command demonstrates windows asset startup and managing a windows GUI IxNetwork Server
``` cmd
OpenHLTest.RestConfServer.exe -ixnetworkserver=https://<GUI Server IpAddress:RestPort>
```

### Linux API Server Session Management
- following command demonstrates linux asset startup and managing multiple IxNetwork API Server sessions
``` cmd
OpenHLTest.RestConfServer -apikey=<api key from linux server> -ixnetworkserver=https://<Linx API Server  IpAddress:RestPort>
```

## Client Installation
The OpenHLTest python client is currently tested against Python versions 2.7.14 to 3.x.  
   - install the latest OpenHLTest python client with "pip install --upgrade --no-cache-dir openhltest"

## Getting Started
Once the Keysight OpenHLTest server is up and running you can use the provided [samples](https://github.com/OpenHLTest/keysight-server/tree/master/samples) to get started.
