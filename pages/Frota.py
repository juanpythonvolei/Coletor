import streamlit as st
from views import *

image = st.image('https://img.freepik.com/vetores-gratis/modelo-de-logotipo-da-empresa-de-caminhoes_441059-258.jpg?w=996')

colx,coly,colz = st.columns(3)

with colx:
      if 'selected_option' in st.session_state:
            st.title(f'Usuário logado: {st.session_state.selected_option}')
with coly:
      with st.popover('🤖'):
            assistant()
with colz:
      with st.popover('📂'):
            donwload_billing()


marca = st.text_input(label="Marca",placeholder="Insira a marca do veículo")
modelo = st.text_input(label="Modelo",placeholder="Insira o modelo do veículo")
autonomia = st.number_input(label="Autonomia",placeholder="Insira a Autonomia do veículo",value=None)

if marca and modelo and autonomia:

    
    st.write(session.query(Veiculos).filter(Veiculos.modelo == modelo).first())


