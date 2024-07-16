import requests
from utils.images import encode_image
import streamlit as st
import base64

def encode_image(image_file):
    return base64.b64encode(image_file).decode('utf-8')

def header(api_key):
    return {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {api_key}"
}

def payload(prompt, image):
    return {
    "model": "gpt-4o",
    "messages": [
      {
        "role": "user",
        "content": [
          {
            "type": "text",
            "text": f"{prompt}"
          },
          {
            "type": "image_url",
            "image_url": {
              "url": f"data:image/jpeg;base64,{image}"
            }
          }
        ]
      }
    ]}

api_key = st.secrets["OpenAI_key"]
def get_api_response(prompt, image, api_key=api_key):
    header_dict = header(api_key)

    base64_image = encode_image(image)
    payload_dict = payload(prompt,base64_image)


    response = requests.post("https://api.openai.com/v1/chat/completions", headers=header_dict, json=payload_dict)
    return response

prompt_original = """Actúa como un profesor de Historia de la Filosofía con más de 20 años impartiendo clase en 2º de Bachillerato. 
Tienes un doctorado en Filosofía, y mucha experiencia con alumnos entre 17 y 18 años. Estás preparando a tus alumnos para la Selectividad (o EVAU). 
Tu alumno te ha pasado estos apuntes para que se los corrijas, añadas lo que le falta. 
Revisa sus apuntes, en el archivo adjunto y hazle la correcciones y ampliaciones que le sirvan para obtener la máxima 
calificación en la Selectividad: Tacha los errores cometidos indicando el porqué entre paréntesis, las ideas añadidas ponlas en cursiva, 
y las obras del autor que cites ponlas dónde correspondan y en negrita.
El tema que está trabajando es: 'Explica el problema de CONOCIMIENTO Y REALIDAD  en NIETZSCHE'"""