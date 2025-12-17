import requests
from .instance.manager import InstanceManager
from .group.manager import GroupManager
from .send.message import SendMessage
from .send.location import SendLocation
from .send.media import SendMedia
from .send.status import SendStatus
from .integrations.chatwoot import ChatwootIntegration

class EvolutionAPIClient():
    def __init__(self, url:str, api_global_key:str, set_instance:str=None):
        self.base_url = url.rstrip('/')
        self.headers = {"apikey": api_global_key, "Content-Type": "application/json"}
        self.instance = InstanceManager(url, api_global_key, set_instance)
        self.group = GroupManager(url, api_global_key, set_instance)
        self.location = SendLocation(self.instance)
        self.message = SendMessage(self.instance)
        self.media = SendMedia(self.instance)
        self.status = SendStatus(self.instance)
        self.chatwoot = ChatwootIntegration(url, api_global_key, set_instance)
    
    def _request(self, method:str, endpoint:str, **kwargs)->requests.Response:
        clean_endpoint = endpoint.strip('/')
        url = f"{self.base_url}/{clean_endpoint}/{self.instance.instance_name}"
        headers = self.headers
        return requests.request(method, url, headers=headers, **kwargs)

