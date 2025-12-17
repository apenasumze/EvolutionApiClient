from evolutionapi_client.instance.manager import InstanceManager
from evolutionapi_client.tools.func_chat import validate_number
import requests
from typing import Optional, List, Dict, Any

class SendLocation:
    def __init__(self, instance: InstanceManager):
        self.base_url = instance.base_url
        self.headers = instance.headers
        self.instance_name = instance.instance_name

    def _location_payload(
        self,
        number: str,
        name: str,
        address: str,
        latitude: float,
        longitude: float,
        delay: int = 1000,
        link_preview: bool = True,
        mentionsEveryOne: Optional[List[str]] = None,
        mentioned: Optional[List[str]] = None,
        quoted: Optional[Dict[str, Any]] = None
    ) -> dict:
        payload = {
            "number": number,
            "name": name,
            "address": address,
            "latitude": latitude,
            "longitude": longitude,
            "delay": delay,
            "linkPreview": link_preview
        }

        if mentionsEveryOne:
            payload["mentionsEveryOne"] = mentionsEveryOne
        if mentioned:
            payload["mentioned"] = mentioned
        if quoted:
            payload["quoted"] = quoted

        return payload

    def send_location(
        self,
        number: str,
        name: str,
        address: str,
        latitude: float,
        longitude: float,
        delay: int = 1000,
        link_preview: bool = True,
        mentionsEveryOne: Optional[List[str]] = None,
        mentioned: Optional[List[str]] = None,
        quoted: Optional[Dict[str, Any]] = None
    ) -> dict:
        number = validate_number(number)
        url = f"{self.base_url}/message/sendLocation/{self.instance_name}"
        payload = self._location_payload(
            number, name, address, latitude, longitude,
            delay, link_preview, mentionsEveryOne, mentioned, quoted
        )

        try:
            response = requests.post(url, json=payload, headers=self.headers)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            return {
                "success": False,
                "status_code": response.status_code if response else None,
                "message": str(e),
                "response": getattr(response, "text", None)
            }
