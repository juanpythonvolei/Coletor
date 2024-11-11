import streamlit as st 
from views import *

image = st.image('https://img.freepik.com/vetores-gratis/modelo-de-logotipo-da-empresa-de-caminhoes_441059-258.jpg?w=996')

taba,tabb,tabc = st.tabs(['Ver rotas','Rotas espefíficas','Roteiro'])

if taba:
      with taba:
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
                  notas = session.query(Faturamento.numero_da_nota).filter(Faturamento.data==str(data),Faturamento.status==True,Faturamento.transportadora == transp).all()
                  result = build_google_map(route(define_destiny_list(item[0] for item in notas)))
                  save_route(data=data,transp=transp,routes=result[2])
                  st.table(result[1])
with tabb:
            data = st.date_input("Selecione uma data",value=None,key='Data_selector_epecific')
            if data:
                  transp = st.selectbox(label="Trasnportadora",placeholder="Selecione uma transportadora",options=list(set([item[0] for item in session.query(Faturamento.transportadora).filter(Faturamento.status == True).all()])),index=None,key='select_transp')    
                  if transp:
                        nota = st.selectbox(label="Nota",placeholder="Selecione uma nota",options=list(set([item[0] for item in session.query(Faturamento.numero_da_nota).filter(Faturamento.status == True,Faturamento.data==data,Faturamento.transportadora==transp).all()])),index=None,key='select_note')    
                        if nota:
                              texto = ''
                              infos = session.query(Faturamento).filter(Faturamento.numero_da_nota==nota,Faturamento.status == True,Faturamento.data == data).all()
                              for item in infos:
                                  info=  f'''
                                    Cliente: {item.cliente}\n
                                    Destino: {item.destino}\n
                                    quantidade: {item.quantidade}\n
                                    '''
                                  texto += info
                              st.info(texto)
                              result = build_google_map(route(define_destiny_list([item.numero_da_nota])))
                              save_route(data=data,transp=transp,routes=result[2])
                  
with tabc:
      texto = ''
      data = st.date_input("Selecione uma data",value=None,key='Data_selector_ia')
      if data:
                  transp = st.selectbox(label="Trasnportadora",placeholder="Selecione uma transportadora",options=list(set([item[0] for item in session.query(Faturamento.transportadora).filter(Faturamento.status == True).all()])),index=None,key='select_transp_ia')    
                  if transp:
                        message = st.chat_input('escreva o que você quer especificar')
                        if message:
                              human = st.chat_message('human')
                              human.write(message)
                              resultado = build_google_map(route(define_destiny_list(item[0] for item in session.query(Faturamento.numero_da_nota).filter(Faturamento.data==data,Faturamento.status==True,Faturamento.transportadora==transp))))
                              for i,item in enumerate(resultado[2]):
                                    text = item['rotas']
                                    if text in texto:
                                           pass
                                    else:
                                           texto += f'Rota {i}: {text}\n'
                              
                                    assistant = st.chat_message('assistant')
                                    assistant.write(analisar(f"Analise o texto que você está recebendo e, baseando-se nele, responda ao que se pede: {message}",str(texto)))
                        
