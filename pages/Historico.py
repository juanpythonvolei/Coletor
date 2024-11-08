import streamlit as st 
from views import *



colx,coly,colz = st.columns(3)

with colx:
      if 'selected_option' in st.session_state:
            st.title(f'Usuário logado: {st.session_state.selected_option}')
with coly:
      with st.popover('🤖'):
            assistant()
with colz:
      with st.popover('📂'):
            donwload_history()

tab1,tab2 = st.tabs(["Histórico","Assistente"])
with tab1:
    if tab1:
        data = st.date_input(label="Selecione uma data",value=None)
        if data:
            vizualize_history(str(data))
with tab2:
    if tab2:
        message = st.chat_input(placeholder="Faça a sua pegunta")
        if message:
            texto = ''
            infos = session.query(Historico).all()
            descri_rec = [f"usuário: {item.usuario} evento:{item.evento}, item:{item.item}, data:{item.data} quantidade :{item.quantidade}" for item in infos]
            for elemento in descri_rec:
                if elemento in texto:
                    pass
                else:
                    texto += elemento
            human = st.chat_message("human")
            ia = st.chat_message("ai")
            human.write(message)
            ia.write(analisar(f"Você é um assisnte de estoque e sua função é me auxiliar na observação do meu armazém. A seguir, você verá um Conjunto de informaçõe que diz respeito a diversas movimentações feitas no estoque em períodos de tempo específicos. Baseando-se nele, responda ao que se pede: {message}",texto))
