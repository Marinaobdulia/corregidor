import streamlit as st
import numpy as np
from utils.gpt_api import get_api_response, prompt_original


st.set_page_config(
    page_title="Corregidor by CMR",
    page_icon="🚩"
)

st.markdown("""<h1 style="text-align: center; color: black;">
    Corregidor<sub>by CMR</sub>
</h1>""", unsafe_allow_html=True)
st.markdown('---')

## prompt modificable - input texto
with st.form('form_1'):
    images = st.file_uploader('Suba todas las imágenes que desee analizar', type= ['.jpg', '.jpeg'], accept_multiple_files=True)
    prompt = st.text_area('Introduzca el prompt que desea ejecutar', prompt_original)
    ok_button = st.form_submit_button('Ok')

if ok_button:
    ## ejecutar prompt
    my_bar = st.progress(0, text='Leyendo imágenes y generando respuestas...')

    # images = os.listdir('./data')
    images = [ (image.read(), image.name) for image in images if '.jpg' in image.name or '.jpeg'in image.name]

    divide_percent = len(images)
    for i in range(divide_percent):
        image, image_name = images[i]

        response = get_api_response(prompt, image)
        response_md = response.json()['choices'][0]['message']['content']

        st.markdown(response_md)

        complete_name = image_name.split('.')[0]+image_name.split('.')[1]
        output_file = './data/output/'+complete_name+'.md'
        with open(output_file, 'w', encoding='utf-8') as archivo:
            archivo.write(response_md)

        my_bar.progress((i+1)/divide_percent, text='Leyendo imágenes y generando respuestas...')


    ## resultados análisis (nr ficheros procesados)
    st.success(f'{len(images)} ficheros procesados correctamente')


