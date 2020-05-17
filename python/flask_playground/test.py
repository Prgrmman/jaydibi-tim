import requests
import unittest
unittest.TestLoader.sortTestMethodsUsing = None
import json
import time
from multiprocessing import Process
import os
import sys
from main import run_app

## Global defines
# NOTE: the server side loads the same config file
CONFIG_FILE='server_config.json'
class ServiceClient:
    ''' A Client for the service for unit testing purposes '''
    def __init__(self):
        with open(CONFIG_FILE) as f:
            self._config = json.load(f)
        self._baseurl = 'http://{}:{}'.format(self.address, self.port)

    # Property definitions
    @property
    def port(self):
        return self._config['port']
    @property
    def address(self):
        return self._config['address']

    def get(self, resource):
        ''' Send a get request to the service '''
        return requests.get(self._baseurl + resource)

    def wait_server_active(self, time_limit):
        """ Send a ping for time_limit until you get a response
            Returns True if we can ping
        """
        get_time = lambda: int(time.time())
        start_time = get_time()
        connected = False
        while get_time() - start_time < time_limit:
            try:
                r = self.get('/ping')
                connected = r.status_code == 200
                break
            except requests.exceptions.ConnectionError as e:
                # If we get a Connection error, retry
                pass
        return connected

class Server:
    ''' A wrapper around the web server. Meant to be run in the background '''
    def __init__(self):
        self._process = Process(target=self._run_app)

    def start(self):
        ''' Start the server '''
        print('Starting service...')
        self._process.start()

    def stop(self):
        ''' Stop the server '''
        self._process.terminate()
        self._process.join()

    def is_alive(self):
        ''' Test if the server process is alive'''
        # TODO Considering a heart beat to the service instead of 
        # process status
        return self._process.is_alive()

    def _run_app(self):
        ''' Internal version of run app '''
        # suppress output streams
        sys.stdout = open(os.devnull, 'w')
        sys.stderr = open(os.devnull, 'w')
        # Run flask without auto reload
        run_app(False)


client = ServiceClient()
server = Server()

class TestBasicServices(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        server.start()
        client.wait_server_active(2)

    @classmethod
    def tearDownClass(cls):
        server.stop()
        
    def test_port(self):
        ''' Test if the port is valid '''
        # NOTE: not a very useful test
        self.assertTrue(client.port > 0)

    def test_alive(self):
        ''' Test if the service is alive '''
        self.assertTrue(server.is_alive())

    def test_hello(self):
        ''' Test basic GET request '''
        r = client.get('/')
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.text, 'Hello World')

    def test_pizza(self):
        ''' Test pizza GET '''
        r = client.get('/pizza')
        self.assertEqual(r.text, 'Have some pizza!')


def main():
    with open(CONFIG_FILE) as f:
        config = json.load(f)
    print(config)


if __name__ == '__main__':
    unittest.main()
