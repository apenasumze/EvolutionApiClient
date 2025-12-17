import requests
from typing import List
from enum import IntEnum
# from evolutionapi.instance.manager import InstanceManager

class WebhookEvents(IntEnum):
    APPLICATION_STARTUP = 1
    QRCODE_UPDATED = 2
    MESSAGES_SET = 3
    MESSAGES_UPSERT = 4
    MESSAGES_UPDATE = 5
    MESSAGES_DELETE = 6
    SEND_MESSAGE = 7
    CONTACTS_SET = 8
    CONTACTS_UPSERT = 9
    CONTACTS_UPDATE = 10
    PRESENCE_UPDATE = 11
    CHATS_SET = 12
    CHATS_UPSERT = 13
    CHATS_UPDATE = 14
    CHATS_DELETE = 15
    GROUPS_UPSERT = 16
    GROUP_UPDATE = 17
    GROUP_PARTICIPANTS_UPDATE = 18
    CONNECTION_UPDATE = 19
    CALL = 20
    NEW_JWT_TOKEN = 21
    TYPEBOT_START = 22
    TYPEBOT_CHANGE_STATUS = 23

class WebhookConfig:
    # def __init__(self):
    #     self.instance = instance
    #     self.base_url = instance.base_url
    #     self.headers = instance.headers
    #     self.api_global_key = instance.api_global_key
    #     self.instance_name = instance.instance_name
        
    #     print(self.instance_name)
    #     print(self.base_url)

    def set_webhook(self, webhook_url: str, event_codes: List[int] = None) -> dict:
        """
        Configura o webhook para eventos da instância conectada.

        Args:
            webhook_url (str): URL que receberá os webhooks da EvolutionAPI.
            event_codes (List[int], opcional): Lista de códigos numéricos correspondentes aos eventos desejados.

                Eventos disponíveis:
                    1 - APPLICATION_STARTUP
                    2 - QRCODE_UPDATED
                    3 - MESSAGES_SET
                    4 - MESSAGES_UPSERT
                    5 - MESSAGES_UPDATE
                    6 - MESSAGES_DELETE
                    7 - SEND_MESSAGE
                    8 - CONTACTS_SET
                    9 - CONTACTS_UPSERT
                   10 - CONTACTS_UPDATE
                   11 - PRESENCE_UPDATE
                   12 - CHATS_SET
                   13 - CHATS_UPSERT
                   14 - CHATS_UPDATE
                   15 - CHATS_DELETE
                   16 - GROUPS_UPSERT
                   17 - GROUP_UPDATE
                   18 - GROUP_PARTICIPANTS_UPDATE
                   19 - CONNECTION_UPDATE
                   20 - CALL
                   21 - NEW_JWT_TOKEN
                   22 - TYPEBOT_START
                   23 - TYPEBOT_CHANGE_STATUS

                O evento "APPLICATION_STARTUP" (1) é sempre incluído por padrão.

        Returns:
            dict: Resposta da EvolutionAPI.
            Payload para configuração do webhook.
        """
        selected = {WebhookEvents.APPLICATION_STARTUP.name}

        if event_codes:
            for code in event_codes:
                try:
                    selected.add(WebhookEvents(code).name)
                except ValueError:
                    raise ValueError(f"Código de evento inválido: {code}")

        # url = f"{self.base_url}/webhook/set/{self.instance_name}"

        # print(url)
        
        payload = {
            "enabled": True,
            "url": webhook_url,
            "webhookByEvents": True,
            "webhookBase64": True,
            "events": list(selected)
        }

        # # r = requests.post(url, json=payload, headers=self.headers)
        return {"webhook": payload}
    
    # def remove_webhook(self):
    #     url = f"{self.base_url}/webhook/set/{self.instance_name}"
    #     r = requests.post(url, headers=self.headers)
    #     return r.json()

    # def find_webhook(self) -> dict:
    #     url = f"{self.base_url}/webhook/find/{self.instance_name}"
    #     r = requests.get(url, headers=self.headers)
    #     return r.json()

if __name__ == "__main__":
    from dotenv import load_dotenv
    import os
    
    # Carregar variaveis de ambiente
    load_dotenv()

    # Instancia da classe
    # api_key = os.getenv("GLOBAL_API_KEY")
    # url = os.getenv("URL")
    # nome_instancia = os.getenv("INSTANCIA_ITALBOT2") # Define qual instancia sera utilizada
    # im = InstanceManager(url, api_key, nome_instancia)
    wb = WebhookConfig()
    
    settings = wb.set_webhook("https://webhook.site/3d9b4c8e-0e1e-4f3a-9d2c-1f2a3b4c5d6e", [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23])
    
    print(settings)