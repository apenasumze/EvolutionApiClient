from evolutionapi_client.instance.manager import InstanceManager
from evolutionapi_client.tools.func_chat import validate_number
from evolutionapi_client.tools.func_tools import get_file_size_mb, get_api_response, convert_to_base64
import requests
import os
import mimetypes
from time import sleep

class SendMedia():
    def __init__(self, instance: InstanceManager):
        self.base_url = instance.base_url
        self.headers = instance.headers
        self.api_global_key = instance.api_global_key
        self.instance_name = instance.instance_name
        # print(self.instance_name)
        # print(self.instance_key)
    
    def send_media(self, number:str, file_path:list, file_name:str="", caption:str="", delay:int=10) -> dict:
        """
            [WARNING] Alto indice de banimentos ao enviar mensagem para grupos.
           
            Envia uma mensagem contendo mídia para o numero especificado.
            Aceita immagems, videos e documentos.

            Args:
                number (str): Numero de telefone para enviar a mensagem.
                file_path (str): Caminho do arquivo a ser enviado.
                file_name (str, optional): Nome do arquivo a ser enviado. Defaults to "".
                caption (str, optional): Texto a ser enviado junto com a média. Defaults to "".
                delay (int, optional): Delay entre o envio de cada mensagem. Defaults to 10.

            Returns:
                dict: Dicionário com a resposta da API.
        """

        # Validate file path
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Arquivo '{file_path}' não encontrado.")
        if not os.path.isfile(file_path):
            raise ValueError(f"O caminho '{file_path}'  não aponta para um arquivo.")
        
        # Get mimetype file.
        mime_type, _ = mimetypes.guess_type(file_path)
        if not mime_type:
            raise ValueError("Não foi possível determinar o MIME type do arquivo.")
        
        # get media_type.
        if mime_type.startswith("image/"):
            media_type = "image"
        elif mime_type.startswith("video/"):
            media_type = "video"
        elif mime_type.startswith("audio/"):
            media_type = "audio"
        else:
            media_type = "document"

        # Convert file to base64
        base64_string = convert_to_base64(file_path)

        # Prepare to send midia
        number = validate_number(number)
        url = f"{self.base_url}/message/sendMedia/{self.instance_name}"
        payload = {
            "number": number,
            "mediatype": media_type,
            "mimetype": mime_type,
            "caption": caption,
            "media": base64_string,
            "fileName": file_name,
            "delay": 1000,
        }

        try:
            r = requests.post(url, json=payload, headers=self.headers)
            # print(r.text)
            # print(r.json())
            sleep(delay)
            result = get_api_response(r)
        except Exception as e:
            print(f"Erro ao enviar mensagem de mídia: {e}")
            return {
                "success": False,
                "status_code": None,
                "message": str(e),
                "response": None
            }
        # print(result["message"])
        return result
    
if __name__ == "__main__":
    from dotenv import load_dotenv
    import os

    # Carregar variaveis de ambiente
    load_dotenv()

    # Instancia da classe
    api_key = os.getenv("GLOBAL_API_KEY")
    url = os.getenv("URL")
    nome_instancia = os.getenv("INSTANCIA_ITALBOT2") # Define qual instancia sera utilizada

    client = SendMedia(url, api_key, nome_instancia)
    file_path = r"C:\Users\RT-DESKTOP\Downloads\Guilherme Lima Malhão.pdf"
    response = client.send_media('5511952735931', file_path, "Guilherme Lima Malhão", "Curriculo", 10)
    print(response)

        









