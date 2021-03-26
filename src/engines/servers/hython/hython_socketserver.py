from src.engines.servers.base.base_socketserver import BaseSocketServer

import hou
import sys

import logging
import socket
import threading
import json

##########################################################
# class server for hython. inherit BaseSocketServer class
##########################################################
class HythonSocketServer(BaseSocketServer):

    def __init__(self):
        super(HythonSocketServer, self).__init__()
        logging.basicConfig(level=logging.DEBUG)

        self.start_with_config()

    def start_with_config(self):
        """!
        To configure server before call startServer, depend on which dcc used
        """    
        config = self.get_config()

        port_start = config.get('dccPortSettings', {}).get('houdiniPortRangeStart', 0)
        port_end = config.get('dccPortSettings', {}).get('houdiniPortRangeEnd', 0)

        sys.path.append(config.get('pipelineSettings', {}).get('hythonActionsPath', 0)) # add hython action in sys path 
        self.start_server(port_start, port_end, self.CONNECTIONS)


    def function_to_process(self, data, client):
        """!
        Function to execute, received command (callback)
        @param data Json: Received Data
        @param client SocketClient: Client Connection
        """

        logging.info("Hython Server, Process Function: {}".format(data))

        out = ""
        if("print" in data):
            data = data.replace("print", "out = str")

        try:
            exec(data)
            client.send(out)

        except hou.Error as e:
            client.send(str(e))
        except Exception as e:
            client.send(str(e))

    def process_update(self, data, client):
        """!
        Redirect execution of data received (onMainThread for maya, for example)
        @param data Json: Received Data
        @param client SocketClient: Client Connection
        """
        
        try:
            self.function_to_process(data, client) # on main thread
        except Exception as e:
            client.send(e)
            logging.error("Houdini Server, Exception processing Function: {}".format(e))


    def on_identify_dcc(self, client):
        """!
        On Identify Dcc Action [Need to be override per dcc]
        @param client SocketClient: Client Connection
        """

        name = hou.hipFile.name() if hou.hipFile.name() != 'untitled.hip' else 'unsaved'
        exec_name = sys.executable.rsplit('\\', 1)[1]
        exec_name = exec_name.split('.')[0]
        data = json.dumps({'filename': name, 'exec_name': exec_name}, sort_keys=True, indent=4)
        #data =  name
        
        client.send(data)

    def on_shutdown(self):
        """!
        On Shutdown Action
        """
        self.serverRunning = False
        sys.exit()