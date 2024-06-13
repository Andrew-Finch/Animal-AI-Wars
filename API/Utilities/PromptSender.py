import base64
import requests
import os
from PIL import Image
import io
from openai import OpenAI
from dotenv import load_dotenv 

load_dotenv()

client = OpenAI()

class PromptSender:

    def __init__(self, api_key: str):
        self.api_key = api_key

    def encode_image(self, image_data: bytes) -> str:
        return base64.b64encode(image_data).decode('utf-8')


    def send_image_prompt(self, as_json: bool, image_data: bytes, prompt_text: str, model: str = "gpt-4o", max_tokens: int = 1500) -> str:
        base64_image = self.encode_image(image_data)
    
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }

        payload = {
            "model": model,
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": prompt_text
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/png;base64,{base64_image}"
                            }
                        }
                    ]
                }
            ],
            "max_tokens": max_tokens
        }

        if as_json:
            payload["response_format"] = {"type": "json_object"}
        response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)

        return response
    
    def create_image(self, prompt):

        response = client.images.generate(
            model="dall-e-3",
            prompt=prompt,
            size="1024x1024",
            quality="standard",
            n=1,
        )
        image_url = response.data[0].url

        return image_url

    def send_image_url_prompt(self, as_json: bool, image_url: str, prompt_text: str, model: str = "gpt-4o", max_tokens: int = 1500) -> str:
    
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }

        payload = {
            "model": model,
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": prompt_text
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"{image_url}"
                            }
                        }
                    ]
                }
            ],
            "max_tokens": max_tokens
        }

        if as_json:
            payload["response_format"] = {"type": "json_object"}
        response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)

        return response
    
    def compare_image_url_prompt(self, as_json: bool, image_urls: list, prompt_text: str, model: str = "gpt-4o", max_tokens: int = 1500) -> str:
    
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }

        content = [{"type": "text","text": prompt_text}]

        for url in image_urls:
            content.append({"type": "image_url","image_url": {"url": f"{url}"}})

        payload = {
            "model": model,
            "messages": [
                {
                    "role": "user",
                    "content":content
                }
            ],
            "max_tokens": max_tokens
        }

        if as_json:
            payload["response_format"] = {"type": "json_object"}
        response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)

        return response




