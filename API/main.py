from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from PIL import Image
import io
import os
import uvicorn
from Utilities.PromptSender import PromptSender
from openai import OpenAI
from dotenv import load_dotenv 

load_dotenv()

app = FastAPI()

@app.get("/")
def root() -> dict:
    return {"message": "Hello World"}


@app.post("/process_image")
async def process_image(prompts: dict):

    key = os.getenv("OPENAI_API_KEY")

    # GET A DESCRIPTION OF THE IMAGE
    # Instantiate the PromptSender
    prompt_sender = PromptSender(key)
    # Prompt text
    prompt_text = f'''
    You must create a photograph of a fictional animal. 
    
    The animals head must be the head of a:

    {prompts['head']}

    The main part of the animals body must be similar to:

    {prompts['body']}

    The animals arms, legs and extremities must be similar to:

    {prompts['ext']}

    You must create a photograph of this animal. You must merge the head, the body and the animals arms and extremities into one animal.

    Do not show more than one animal
    '''
    # Send the prompt and get the response
    image_url = prompt_sender.create_image(prompt_text)

    #Get animal name and lore
    lore_prompt = '''
    You are about to see a mythical animal. 
    You must come up with lore, stories and a backstory for this animal. 
    You must recount its epic battles and it's long journey through history.
    You must include funny moments and tragic circumstances.
    '''

    name_prompt = '''
    You are about to see an image of a mythical animal and recieve it's backstory.
    You must come up with a name for this animal. You must make it an epic and awesome name.
    You may include suffixes like:
    "... the Great"
    "... the Ferocious"
    "... the Vicious"
    "... the Brave"

    Create a name that desribes the animals features and it's battles.
    '''

    # name = prompt_sender.send_image_url_prompt(False, image_url, name_prompt)

    lore = prompt_sender.send_image_url_prompt(False, image_url, lore_prompt)

    return JSONResponse({
        "Image_URL": f"{image_url}",
        # "Name": f"{name.json()['choices'][0]['message']['content']}",
        "Lore": f"{lore.json()['choices'][0]['message']['content']}"
         })

@app.post("/compare_images")
async def process_image(urls: list):
    key = os.getenv("OPENAI_API_KEY")
    prompt_sender = PromptSender(key)
    comparison_prompt = '''
    You are about to see two images of fictional animals. 
    You must evaluate their strengths and weaknesses based on the images and decide which would win in a fight.
    You must describe the fight in detail.
    The fight could be between 2 or more animals in the pictures.
    You must decide a winner.
    Your response must be less than 100 words long.
    '''
    comparison = prompt_sender.compare_image_url_prompt(False, urls, comparison_prompt)


    return JSONResponse({
        "Comparison": f"{comparison}"
         })

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)