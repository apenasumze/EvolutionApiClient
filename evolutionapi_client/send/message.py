from evolutionapi_client.instance.manager import InstanceManager
from evolutionapi_client.tools.func_chat import validate_number
import requests
from time import sleep

class SendMessage():
    def __init__(self, instance: InstanceManager):
        self.base_url = instance.base_url
        self.headers = instance.headers
        self.api_global_key = instance.api_global_key
        self.instance_name = instance.instance_name

    def _message_payload(self, number:str, message: str, link_preview=False):
        """
            Cria o payload padrão da mensagem a ser enviada a um determinado número.

            Args:
                number (str): O número de telefone para o qual a mensagem deve ser enviada.
                message (str): O texto da mensagem que deseja enviar.
                link_preview (bool, optional): Define se a mensagem deve conter uma prévia de link externo. Defaults to False.

            Returns:
                dict: Um dicionário contendo o payload da mensagem.
        """
      
        number = validate_number(number)
        payload = {
            "number": number,
            "text": message,
            "delay": 1000,
            "link_preview": link_preview
        }

        return payload
    
    def _send_message(self, payload:dict, delay:int=5) -> dict:
        """
        realiza o envio de uma mensagem de texto para um determinado número.

        Args:
            number (str): O número de telefone para o qual a mensagem deve ser enviada.
            payload (dict): Um dicionário contendo o payload da mensagem.
            delay (int, optional): O delay em segundos entre o envio de cada mensagem. Defaults to 5.

        Returns:
            dict: Um dicionário contendo a resposta da API.
        """
        url = f"{self.base_url}/message/sendText/{self.instance_name}"
        response = requests.post(url, json=payload, headers=self.headers)
        sleep(delay)
        # try:
        #     return response.json()
        # except ValueError:
        #     # Caso não seja JSON (ex: vazio ou HTML), retorna status e texto
        #     return {
        #         "status_code": response.status_code,
        #         "text": response.text
        #     }
        return response.json()

    def send_text_message(self, number:str, message:str, delay:int=5) -> dict:
        """
        [WARNING] Alto indice de banimentos ao enviar mensagem para grupos.
        [HINT] Utilize a função calculate_send_delay() para calcular ajustar o delay de envios dinamicamente quando usado em loops.

        Envia uma mensagem de texto para o numero especificado.

        Args:
            number (str): Numero de telefone para enviar a mensagem.
            message (str): O texto da mensagem que deseja enviar.
            delay (int): Delay entre o envio de cada mensagem. 
        
        Returns:
            dict: Um dicionário contendo a resposta da API.

            Chaves do conteúdo JSON da resposta (dict) em caso de sucesso:
                key (dict):
                    remoteJid (str): JID do destinatário. Ex. "5511952735931@s.whatsapp.net" ou "group-12345-12345@g.us" ou "broadcast-12345-12345@g.us".
                    fromMe (bool): Indica se a mensagem foi enviada por você.
                    id (str): ID único da mensagem.
                
                pushName (str): Nome de exibição do contato (se disponível).
                status (str): Status atual da mensagem (ex: "PENDING", "SENT", "DELIVERED").
                message (dict):
                    conversation (str): Conteúdo textual da mensagem enviada.
                    contextInfo (dict | None): Informações adicionais do contexto (ex: mensagens anteriores, respostas), pode ser None.
                    messageType (str): Tipo da mensagem enviada (ex: "conversation").
                    messageTimestamp (int): Timestamp UNIX da mensagem (em segundos).
                    instanceId (str): ID da instância do WhatsApp utilizada para envio.
                    source (str): Origem do envio (ex: "unknown").
                    
            Chaves em caso de erro:
                status (int): Código de status HTTP da resposta.
                error (str): Mensagem de erro.
                response (dict): Conteúdo da resposta da API.
                    message (list): Lista de mensagens de erro.
                        exists (bool): Indica se o número de telefone existe.
                        jid (str): JID do destinatário. Ex. "5511952735931@s.whatsapp.net" ou "group-12345-12345@g.us" ou "broadcast-12345-12345@g.us".
                        number (str): Número de telefone.
        """

        payload = self._message_payload(number, message)
        response = self._send_message(payload, delay)
        return response

    def send_quoted_message(self):
        ...

    def send_message_with_link(self, number:str, message:str, link_preview=True, delay:int=5):
        """
            Envia uma mensagem de texto com prévia de um link externo para o numero especificado.
            
            [WARNING] Alto indice de banimentos ao enviar mensagem para grupos.
            [HINT] Utilize a função calculate_send_delay() para calcular ajustar o delay de envios dinamicamente quando usado em loops.

            Args:
                number (str): Numero de telefone para enviar a mensagem.
                message (str): O texto da mensagem que deseja enviar.
                link_preview (bool, optional): Define se a mensagem deve conter uma prévia de link externo. Defaults to True.
                delay (int): Delay entre o envio de cada mensagem.
        """
        payload = self._message_payload(number, message, link_preview)
        response = self._send_message(payload, delay)
        return response
