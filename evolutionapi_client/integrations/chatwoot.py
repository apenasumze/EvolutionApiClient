from evolutionapi_client.instance.manager import InstanceManager
import requests

class ChatwootIntegration(InstanceManager):
    def __init__(self, url, api_global_key, instance_name=None):
        super().__init__(url, api_global_key, instance_name)

    def create_chatwoot_integration(self, account_id:int, chatwoot_token:str, chatwoot_url:str, sign_msg:bool = True, reopen_conversation:bool = True, conversation_pending:bool = False, import_contacts:bool = True, import_messages:bool = True, days_limit_import_messages:int = 1, auto_create:bool = True):
        chatwoot_url = chatwoot_url.rstrip('/')
        url = f"{self.base_url}/chatwoot/set/{self.instance_name}"
        payload = {
            "enabled": True,
            "accountId": str(account_id),
            "token": chatwoot_token,
            "url": chatwoot_url,
            "signMsg": sign_msg,
            "reopenConversation": reopen_conversation, 
            "conversationPending": False,
            "nameInbox": self.instance_name,
            "mergeBrazilContacts": conversation_pending,
            "importContacts": import_contacts,
            "importMessages": import_messages,
            "daysLimitImportMessages": days_limit_import_messages,
            "signDelimiter": "\n",
            "autoCreate": auto_create,
            "organization": "Ital Leste",
            "logo": ""
        }
        r = requests.post(url, json=payload, headers=self.headers)
        status_code = r.status_code
        print(r.status_code)


if __name__ == '__main__':
    from dotenv import load_dotenv
    import os

    # Carregar variaveis de ambiente
    load_dotenv()

    # Instancia a classe
    api_key = os.getenv("GLOBAL_API_KEY")
    url = os.getenv("URL")
    nome_instancia = os.getenv("INSTANCIA_ITALBOT2") # Define qual instancia sera utilizada

    print("URL: ", url)
    print("API Key: ", api_key)
    print("Instancia: ", nome_instancia)
  
    # Cria a integracao com chatwoot
    chatwoot_account_id = os.getenv("CHATWOOT_ACCONUNT_ID")
    chatwoot_token = os.getenv("CHATWOOT_TOKEN")
    chatwoot_url = os.getenv("CHATWOOT_URL")

    print("Chatwoot Account ID: ", chatwoot_account_id)
    print("Chatwoot Token: ", chatwoot_token)
    print("Chatwoot URL: ", chatwoot_url)

    # client = EvolutionChatwootIntegration(url, api_key, nome_instancia)
    # client.create_chatwoot_integration(chatwoot_account_id, chatwoot_token, chatwoot_url)