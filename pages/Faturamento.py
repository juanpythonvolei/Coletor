import streamlit as st
from views import *
import xmltodict
from datetime import date



colx,coly,colz = st.columns(3)

with colx:
      if 'selected_option' in st.session_state:
            st.title(f'Usuário logado: {st.session_state.selected_option}')
with coly:
      with st.popover('🤖'):
            assistant()
with colz:
      with st.popover('📂'):
            donwnload_billig()

uploaded_files = st.file_uploader("Seleção", type=[f'xml'], accept_multiple_files=True,help='Insira suas notas aqui')
if uploaded_files:
              resultado = process_notes(notes_list=uploaded_files,data=str(date.today()),usuario=st.session_state.selected_option,status=False,peso_recebido=float(1))
              if resultado:
                    col1,col2,col3 = st.columns(3)
                    with col1:
                          st.metric(label="Notas Faturadas",value=resultado[0])
                    with col2:
                          st.metric(label="Notas não faturadas",value=resultado[2])
                    with col3:
                          st.metric(label='Cadastros',value=resultado[1])
