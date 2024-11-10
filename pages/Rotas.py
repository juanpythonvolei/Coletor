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

col3,col4 = st.columns(2)
            
with col3:    
            transp = st.selectbox(label="Trasnportadora",placeholder="Selecione uma transportadora",options=list(set([item[0] for item in session.query(Faturamento.transportadora).filter(Faturamento.status == True).all()])),index=None,key='select')    
with col4:
            if transp:
                with st.popover("🗓️ Selecione uma data"):
                    data = st.date_input("Selecione uma data",value=None)
if transp and data:
      notas = session.query(Faturamento.numero_da_nota).filter(Faturamento.data == data,Faturamento.transportadora == transp,Faturamento.status == True).all()
      st.write(notas)
      build_google_map(route(define_destiny_list([item[0] for item in notas])))
