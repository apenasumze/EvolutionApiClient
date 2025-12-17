import requests
from time import sleep
from evolutionapi_client.instance.manager import InstanceManager
from evolutionapi_client.tools.func_tools import convert_to_base64

class SendStatus():
    def __init__(self, instance: InstanceManager):
        self.base_url = instance.base_url
        self.headers = instance.headers
        self.api_global_key = instance.api_global_key
        self.instance_name = instance.instance_name

    def _status_payload(self, type: str, content: str, caption: str = "", background_color="#D3D3D3", font=5, all_contacts=True, status_Jid_List=["551125611600@c.us"]) -> dict:
        """
            Gera o payload base para envio de status, baseado no tipo (text, image, video, audio).

            Args:
                tipo (str): Tipo de status a ser enviado. Pode ser:
                    - "text": Status de texto.
                    - "image": Status com imagem ou vídeo (em base64).
                    - "audio": Status com áudio (em base64).

                content (str): Conteúdo principal do status.
                    - Para "text": o próprio texto da mensagem.
                    - Para "image", "video" e "audio": conteúdo em base64 do arquivo. 
                
                caption (str, optional): Texto complementar exibido abaixo da mídia (imagem, vídeo). Não se aplica a "text". Padrão: "".

                background_color (str, optional): Cor de fundo usada apenas em status de texto. Formato hexadecimal (ex: "#D3D3D3"). Padrão: "#D3D3D3".

                font (int, optional): Fonte do texto usada apenas em status de texto. Valores suportados:
                    - 1 = SERIF
                    - 2 = NORICAN_REGULAR
                    - 3 = BRYNDAN_WRITE
                    - 4 = BEBASNEUE_REGULAR
                    - 5 = OSWALD_HEAVY
                    Padrão: 5.

                all_contacts (bool, optional): Define se o status deve ser enviado para todos os contatos. Padrão: True. Se False, deve ser fornecido uma lista de contatos.

                statusJidList (list, optional): Lista de contatos para os quais o status deve ser enviado. Por padrão, deve conter um numero de telefone no formato JID.

            Returns:
                dict: Um dicionário com o payload formatado, pronto para ser enviado via API Evolution no endpoint /message/sendStatus/{instance_name}.
            """
        payload = {
            "type": type,
            "content": content,
            "caption": caption,
            "allContacts": all_contacts,
            "statusJidList": status_Jid_List,
            "backgroundColor": background_color,
            "font": font
        }

        # if type == "text":
        #     payload["backgroundColor"] = background_color
        #     payload["font"] = font

        return payload

    def _send_status(self, payload: dict, delay: int = 2) -> requests.Response:
        """
            Realiza o envio de um status (texto, imagem, vídeo ou áudio) utilizando a instância da API Evolution.

            Args:
                payload (dict): Dicionário contendo os dados do status a ser enviado. Deve seguir o formato esperado pela API Evolution incluindo campos como "type", "content", "caption", etc.
                delay (int, optional): Tempo de espera (em segundos) após o envio da requisição. Pode ser usado para evitar sobrecarga ou respeitar limites de envio. Padrão: 2 segundos.

            Returns:
                requests.Response: Objeto de resposta HTTP da biblioteca `requests`, contendo status code, 
                    corpo da resposta e outros dados úteis sobre o envio.

            Raises:
                Exception: Qualquer exceção levantada durante o processo de envio será capturada, exibida no terminal 
                    e relançada para permitir tratamento posterior.
            """
        url = f"{self.base_url}/message/sendStatus/{self.instance_name}"

        try:
            r = requests.post(url, json=payload, headers=self.headers)
            sleep(delay)
            return r
        except Exception as e:
            print(f"[ERRO] Falha ao enviar status: {e}")
            raise

    def send_status_text(self, content: str, background_color="#D3D3D3", font=5, delay=2) -> requests.Response:
        payload = self._status_payload("text", content, background_color=background_color, font=font)
        return self._send_status(payload, delay)

    def send_status_image(self, image_path: str, caption="", delay=2) -> dict:
        # image_base64 = convert_to_base64(image_path)
        payload = self._status_payload("image", image_path, caption=caption)
        return self._send_status(payload, delay).json()

    # def send_status_video(self, video_path: str, caption="", delay=2):
    #     return self.send_status_image(video_path, caption=caption, delay=delay)
    
    def send_status_video(self, video_path: str, caption="", delay=2):
        video_base64 = convert_to_base64(video_path)
        payload = self._status_payload("video", video_base64, caption=caption)
        return self._send_status(payload, delay=delay)

    def send_status_audio(self, audio_path: str, caption="", delay=2):
        audio_base64 = convert_to_base64(audio_path)
        payload = self._status_payload("audio", audio_base64, caption=caption)
        return self._send_status(payload, delay)


if __name__ == "__main__":
    from dotenv import load_dotenv
    import os

    load_dotenv()

    api_key = os.getenv("GLOBAL_API_KEY")
    url = os.getenv("URL")
    nome_instancia = os.getenv("INSTANCIA_ITALBOT2")
    instance = InstanceManager(url, api_key, nome_instancia)
    client = SendStatus(instance)

    response = client.send_status_text("Ital Leste Inspeção Veicular!", "#FF0000", 5)
    print(response.json())

    # try:
    #     print("Resposta JSON:")
    #     print(response.json())
    # except Exception:
    #     print("Resposta (raw):")
    #     print(response.text)
