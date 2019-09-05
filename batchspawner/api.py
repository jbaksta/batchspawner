import json
from tornado import web
from jupyterhub.apihandlers import  APIHandler, default_handlers

from batchspawner import BatchSpawnerBase

class BatchSpawnerAPIHandler(APIHandler):
    @web.authenticated
    def post(self):
        """POST set user's spawner port number"""
        user = self.get_current_user()
        data = self.get_json_body()
        port = int(data.get('port', 0))
        spawner = user.spawner
        while not issubclass(spawner,BatchSpawnerBase):
          spawner = spawner.child_spawner
        spawner.current_port = port
        self.finish(json.dumps({"message": "BatchSpawner port configured"}))
        self.set_status(201)

default_handlers.append((r"/api/batchspawner", BatchSpawnerAPIHandler))
