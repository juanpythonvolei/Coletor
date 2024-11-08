import streamlit as st 
from views import *



colx,coly = st.columns(2)

with colx:
      if 'selected_option' in st.session_state:
            st.title(f'Usuário logado: {st.session_state.selected_option}')
with coly:
      with st.popover('🤖'):
            assistant()

tab1,tab2 = st.tabs(['Romaneios', 'Ver Romaneios'])    

if tab1:
     with tab1:
        col3,col4 = st.columns(2)
            
        with col3:    
            transp = st.selectbox(label="Trasnportadora",placeholder="Selecione uma transportadora",options=list(set([item[0] for item in session.query(Faturamento.transportadora).filter(Faturamento.status == True).all()])),index=None,key='select')    
        with col4:
            if transp:
                with st.popover("🗓️ Selecione uma data"):
                    data = st.date_input("Selecione uma data",value=None)

        if transp and data:
            col1,col2 = st.columns(2)
            with col1:
                botao_novo = st.popover(f"Novo Romaneio da tranportadora {transp}")
            with col2:
                botao_ver_automático = st.button(f"Vizualizar Romaneio automátio para a tranpostadora {transp}")
            with botao_novo:
                notas = st.multiselect(label="Seleção",placeholder="Selecione as notas da transportadora",options=[item[0] for item in session.query(Faturamento.numero_da_nota).filter(Faturamento.status == True,Faturamento.data == str(data),Faturamento.transportadora == transp).all()],key='nenhuma')
            if transp and notas and data:
                    
                    if not botao_ver_automático:
                        resposta  = create_itens_relations_for_item(data=str(data),lista=notas,user=st.session_state.selected_option)
                        col6,col7,col8 = st.columns(3)
                        with col6:
                            st.metric(label="Peso Total",value=resposta[1])
                        with col7:
                            st.metric(label="Valor Total",value=resposta[2])
                        with col8:
                            st.metric(label="Total volumes",value=resposta[3])
            if botao_ver_automático and data:
                    resposta = create_itens_relations(data=str(data),transp=transp,user=st.session_state.selected_option)
                    col9,col10,col11 = st.columns(3)
                    with col9:
                            st.metric(label="Peso Total",value=resposta[1])
                    with col10:
                            st.metric(label="Valor Total",value=resposta[2])
                    with col11:
                            st.metric(label="Total volumes",value=resposta[3])
if tab2:
     with tab2:
           try:
                  usuario = st.selectbox(label="Seleção",options=session.query(Usuarios.usuario).all()[0],placeholder="Selecione uma transportadora",index=None,key='Consulta')
                  data  = st.date_input(label="Selecione uma data",value=None,key='dateinput')
                  if usuario and data:
                      romaneio = session.query(Romaneios.romaneio).filter(Romaneios.data,Romaneios.usuario == usuario).all()
                      for item in list(set(romaneio)):
                          st.info(item[0])
            except:
                  pass
