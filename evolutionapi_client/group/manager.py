import requests
from typing import List
from evolutionapi_client.instance.manager import InstanceManager

class GroupManager(InstanceManager):
    def __init__(self, url, api_global_key, set_instance=None):
        super().__init__(url, api_global_key, set_instance)

    def create_group(self, group_name:str, participants:list, description:str="") -> dict:
        """
            Cria um grupo na instância conectada.

            Args:
                group_name (str): Nome do grupo.
                participants (list): Lista de numeros de telefone dos participantes. Informar JID dos participantes.
                description (str, optional): Descricao do grupo. Defaults to "".

            Returns:
                dict: Dicionário com a resposta da API.
        """
        url = f"{self.base_url}/group/create/{self.instance_name}"
        payload = {
            "subject": group_name,
            "description": description,
            "participants": participants
        }
        r = requests.post(url, json=payload, headers=self.headers)
        return r.json()
    
    def fetch_all_groups(self, get_participants: bool = True) -> List[dict]:
        """
        Busca todos os grupos da instância.

        Args:
            get_participants (bool): Defina como True para incluir a lista de  participantes de cada grupo na resposta. O padrão é True.
        """
        url = f"{self.base_url}/group/fetchAllGroups/{self.instance_name}"
        params = {
            "getParticipants": str(get_participants).lower()
        }
        
        r = requests.get(url, headers=self.headers, params=params)
        return r.json()