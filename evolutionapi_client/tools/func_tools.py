import os
import requests
import fitz # PyMuPDF
from PIL import Image
import io
import base64
import json

def get_file_size_mb(caminho_arquivo: str):
    """
    Calcula o tamanho do arquivo infomado em bytes e retorna-o em megabytes.
    """

    return os.path.getsize(caminho_arquivo) / (1024 * 1024)

def compress_pdf_file(input_path: str, output_path: str, quality: int = 50) -> str:
    doc = fitz.open(input_path)
    images = []

    for page in doc:
        pix = page.get_pixmap(dpi=150)  # você pode ajustar o DPI
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
        compressed_io = io.BytesIO()
        img.save(compressed_io, format="JPEG", quality=quality)
        images.append(Image.open(io.BytesIO(compressed_io.getvalue())))
    doc.close()

    # Salvar imagens como um novo PDF
    if images:
        images[0].save(output_path, save_all=True, append_images=images[1:], format="PDF")

    return output_path

# def get_media_data(file_path:str) -> dict:
#     """
#     A partir do caminho de arquivo local, retorna uma dicionário com:
#     media_type, mime_type, base64_string

#     - media_type: 'image', 'video', 'audio' ou 'document'.
#     - mime_type: tipo MIME real, como 'image/jpeg'.
#     - base64_string: conteúdo do arquivo convertido em base64.

#     Args:
#         caminho_arquivo (str): Caminho absoluto ou relativo do arquivo.

#     Returns:
#         dict: Dicionário com os dados da mídia.
#     """

def explain_status_code(status_code: int) -> str:
    """
    Interpreta o status da requisição HTTP e o conteúdo da resposta e retorna uma mensagem de sucesso ou erro.
    """
    mensagens = {
        200: "Sucesso: Requisição processada com êxito.",
        201: "Mensagem enviada.",
        400: "Requisição inválida.",
        401: "Não autorizado. Verifique sua API key.",
        404: "Recurso não encontrado.",
        413: "Tamanho do arquivo excedeu o limite.",
        429: "Limite de requisições excedido.",
        500: "Erro interno do servidor.",
        504: "Tempo de espera excedido."
    }
    return mensagens.get(status_code, f"❓ [{status_code}] Código desconhecido. Conteúdo:")


# def get_api_response(response: requests.Response) -> dict:
#     """
#         Trata a resposta da requisição da API e retorna um dicionário padronizado.

#         Args:
#             response (requests.Response): Objeto de resposta da requisição.

#         Returns:
#             dict: Contendo:
#                 - success (bool): True se status 2xx.
#                 - status_code (int): Código HTTP.
#                 - message (str): Interpretação do status.
#                 - response (dict | str): Conteúdo da resposta (json ou texto).
#     """
#     try:
#         status_code = response.status_code
#         success = 200 <= status_code < 300

#         try:
#             content = response.json()
#         except ValueError:
#             content = response.text

#         message = explain_status_code(status_code)

#         return {
#             "success": success,
#             "status_code": status_code,
#             "message": message,
#             "response": content
#         }

#     except Exception as e:
#         return {
#             "success": False,
#             "status_code": None,
#             "message": f"Erro ao processar resposta: {str(e)}",
#             "response": None
#         }

def get_api_response(response: requests.Response) -> dict:
    """
    Trata a resposta da requisição da API e retorna um dicionário padronizado.
    """
    try:
        status_code = response.status_code
        success = 200 <= status_code < 300

        try:
            content = response.json()
        except (ValueError, json.JSONDecodeError):
            content = response.text

        # 1. Pega a mensagem base ("Requisição inválida.", etc.)
        message = explain_status_code(status_code)

        # 2. Se a requisição falhou, enriquece a mensagem
        if not success and isinstance(content, dict):
            
            # --- NOVA LINHA ADICIONADA AQUI ---
            # Remove o ponto final da mensagem genérica para uma formatação mais limpa
            message = message.rstrip('.')

            detailed_response = content.get('response', {})
            detailed_message_list = detailed_response.get('message')

            if detailed_message_list and isinstance(detailed_message_list, list):
                try:
                    details = ", ".join([item for sublist in detailed_message_list for item in sublist])
                    if details:
                        # Usamos ": " como separador, conforme solicitado
                        message += f": {details}"
                except (TypeError, AttributeError):
                    message += f": {str(detailed_message_list)}"

        return {
            "success": success,
            "status_code": status_code,
            "message": message,
            "response": content
        }

    except Exception as e:
        return {
            "success": False,
            "status_code": None,
            "message": f"Erro ao processar resposta: {str(e)}",
            "response": None
        }

def convert_to_base64(file_path: str) -> str:
    """
    Converte um arquivo em uma string codificada em base64 (sem prefixo MIME).

    Args:
        file_path (str): Caminho absoluto ou relativo do arquivo.

    Returns:
        str: Conteúdo do arquivo codificado em base64 (apenas a string base64, sem prefixos).

    Raises:
        FileNotFoundError: Se o arquivo não for encontrado.
    """
    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"Arquivo não encontrado: {file_path}")

    with open(file_path, "rb") as file:
        encoded_bytes = base64.b64encode(file.read())
        return encoded_bytes.decode("utf-8")


if __name__ == "__main__":
    i_file = 'laudo.pdf'
    o_file = 'c.pdf'
    compress_pdf_file(input_path=i_file, output_path=o_file)