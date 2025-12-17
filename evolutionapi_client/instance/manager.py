import requests
from evolutionapi_client.tools.func_chat import validate_number
from .webhook import WebhookConfig, WebhookEvents
from .proxy import ProxyConfig

class InstanceManager:
    def __init__(self, url:str, api_global_key:str, set_instance: str = None):
        """
        Classe responsável por gerenciar instâncias da API Evolution.

        Args:
            url (str): URL base da API.
            api_global_key (str): Chave de API global para autenticação.
            set_instance (str, optional): Nome da instância a ser setada automaticamente. Defaults to None.
        """
        self.base_url = url.rstrip('/')
        self.api_global_key = api_global_key
        self.headers = {
            "apikey": self.api_global_key,
            "Content-Type": "application/json"
        }
        self.instance_name = None
        self.instance_key = None
        self.instance = None

        if set_instance:
            self.set_instance(set_instance)

    def _request(self, method: str, endpoint: str, **kwargs):
        """
        Método interno para realizar requisições HTTP padronizadas.

        Args:
            method (str): Método HTTP (get, post, put, delete).
            endpoint (str): Caminho do endpoint da API.

        Returns:
            requests.Response | None: Resposta da requisição ou None em caso de erro.
        """
        try:
            url = f"{self.base_url}{endpoint}"
            response = requests.request(method, url, headers=self.headers, **kwargs)
            response.raise_for_status()
            return response
        except Exception as e:
            print(f"[ERRO] {method.upper()} {endpoint}: {e}")
            return None

    def _instance_params(
        self,
        reject_call: bool = True,
        msg_call: str = "Este número não aceita chamadas.",
        groups_ignore: bool = True,
        always_online: bool = True,
        read_messages: bool = True,
        read_status: bool = True,
        sync_full_history: bool = True
    ) -> dict:
        """
        Define as configurações padrão para criação e atualização de instâncias.

        Args:
            reject_call (bool): Define se a instância rejeita chamadas. Defaults to True.
            msg_call (str): Mensagem de rejeição de chamadas. Defaults to "Este número não aceita chamadas.".
            groups_ignore (bool): Define se a instância ignora grupos. Defaults to True.
            always_online (bool): Define se a instância permanece sempre online. Defaults to True.
            read_messages (bool): Define se a instância lê mensagens. Defaults to True.
            read_status (bool): Define se a instância lê status. Defaults to True.
            sync_full_history (bool): Define se a instância sincroniza o histórico completo. Defaults to True.

        Returns:
            dict: Dicionário com os parâmetros configurados.
        """
        return {
            "rejectCall": reject_call,
            "msgCall": msg_call,
            "groupsIgnore": groups_ignore,
            "alwaysOnline": always_online,
            "readMessages": read_messages,
            "readStatus": read_status,
            "syncFullHistory": sync_full_history
        }

    def create_instance(
        self,
        instance_name: str,
        token: str,
        number: str,
        reject_call: bool = True,
        msg_call: str = "Este número não aceita chamadas.",
        groups_ignore: bool = True,
        always_online: bool = True,
        read_messages: bool = True,
        read_status: bool = True,
        sync_full_history: bool = True
    ) -> requests.Response | None:
        """
        Cria uma nova instância.

        Args:
            instance_name (str): Nome da instância.
            token (str): Token da instância.
            number (str): Número de telefone associado à instância.
            reject_call (bool): Se rejeita chamadas. Defaults to True.
            msg_call (str): Mensagem ao rejeitar chamadas. Defaults to "Este número não aceita chamadas.".
            groups_ignore (bool): Se ignora grupos. Defaults to True.
            always_online (bool): Se permanece online. Defaults to True.
            read_messages (bool): Se lê mensagens. Defaults to True.
            read_status (bool): Se lê status. Defaults to True.
            sync_full_history (bool): Se sincroniza histórico completo. Defaults to True.

        Returns:
            requests.Response | None: Resposta da criação ou None em caso de erro.
        """
        payload = {
            "instanceName": instance_name,
            "token": token,
            "qrcode": True,
            "number": validate_number(number),
            "integration": "WHATSAPP-BAILEYS",
            **self._instance_params(
                reject_call,
                msg_call,
                groups_ignore,
                always_online,
                read_messages,
                read_status,
                sync_full_history
            )
        }
        return self._request("post", "/instance/create", json=payload)

    def fetch_instances(self):
        response = self._request("get", "/instance/fetchInstances")
        return response.json() if response else {}

    def connect_instance(self, instance_name: str):
        return self._request("get", f"/instance/connect/{instance_name}")

    def logout_instance(self, instance_name: str):
        return self._request("get", f"/instance/logout/{instance_name}")

    def delete_instance(self, instance_name: str):
        return self._request("delete", f"/instance/delete/{instance_name}")

    def get_connection_state(self, instance_name: str = None) -> dict:
        name = instance_name or self.instance_name
        return self._request("get", f"/instance/connectionState/{name}").json()

    def set_instance_settings(
        self,
        reject_call: bool = True,
        msg_call: str = "Este número não aceita chamadas.",
        groups_ignore: bool = True,
        always_online: bool = True,
        read_messages: bool = True,
        read_status: bool = True,
        sync_full_history: bool = True
    ):
        payload = self._instance_params(
            reject_call,
            msg_call,
            groups_ignore,
            always_online,
            read_messages,
            read_status,
            sync_full_history
        )
        return self._request("put", f"/settings/set/{self.instance_name}", json=payload)

    def find_instance_settings(self, instance_name: str):
        return self._request("get", f"/settings/find/{instance_name}")

    def set_instance(self, instance_name: str) -> dict:
        for instance in self.fetch_instances():
            if instance['name'] == instance_name and instance['connectionStatus'] == 'open':
                self.instance = instance
                self.instance_name = instance['name']
                self.instance_key = instance['token']
                return instance
        print(f"[WARN] Instância '{instance_name}' não encontrada ou desconectada.")
        return None

    # Webhook and Proxy configuration coming soon
    
    
    
   
