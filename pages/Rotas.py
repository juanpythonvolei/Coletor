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
                        donwload_deliverys()     
                        
taba,tabb,tabc,tabd,tabe = st.tabs(['Ver rotas','Rotas espefíficas','Roteiro','Entregas','Visão Geral'])
      
if taba:
            with taba:
                        
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
                        st.link_button(label="Acessar Rota",url=result[0])
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
                                    st.link_button(label="Acessar Rota",url=result[0])
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
                                                 texto += f'''
                                                 Rota {i} 
                                                 clinte: {item['cliente']} 
                                                 Destino: {item['descricao']}
                                                 Rota: 
                                                 {text}
                                                 \n'''
                                    
                                    assistant = st.chat_message('assistant')
                                    response = analisar(f"Analise o texto que você está recebendo. Ele é uma representação de rotas. Nele estão os destinos, e o nome dos clientes. Oraganize-os e, baseando-se nele, responda ao que se pede retornando além da resposta, uma rota organizada: {message}",str(texto))
                                    assistant.write(response)
                                    
with tabd:
            data = st.date_input("Selecione uma data",value=None,key='Data_selector_deli')
            if data:
                        veiculo = st.selectbox(label="Veículo",placeholder="Selecione um veículo",options=list(set([item[0] for item in session.query(Veiculos.modelo).all()])),index=None,key='select_car_deli')
                        if veiculo:
                              transp = st.selectbox(label="Trasnportadora",placeholder="Selecione uma transportadora",options=list(set([item[0] for item in session.query(Faturamento.transportadora).filter(Faturamento.status == True).all()])),index=None,key='select_transp_deli')    
                              if transp:
                                    list_deli = []
                                    notas_faturadas = session.query(Faturamento).filter(Faturamento.status == True,Faturamento.transportadora == transp).all()
                                    for fat in notas_faturadas:
                                          if session.query(Entregas).filter(Entregas.cliente == fat.cliente,Entregas.status == True).first():
                                                pass
                                          else:
                                                list_deli.append(fat.numero_da_nota)
                                    notas = st.multiselect(label="notas",placeholder="Selecione uma nota",options=list(set(list_deli)),key='select_notes_deli')    
                                    if notas: 
                                          st.title('Entregas')
                                          response = load_delivery(notas,data,veiculo)
                                          st.metric('Entregas não completas',response[0])
                                          st.metric('Entregas completas',response[1])
with tabe:
            verificar = session.query(Entregas.data).filter(Entregas.status==True).all()
            data = st.date_input("Selecione uma data",value=None,key='Data_selector_one')
            if data:
                  transp = st.selectbox(label="Transportadora",placeholder="Selecione uma transportadora",options=list(set([item[0] for item in session.query(Faturamento.transportadora).filter(Faturamento.status == True).all()])),index=None,key='select_transp_one')    
                  if transp:
                        response = complete_delivery(data,transp)
                        st.table(response[0])
                        st.metric('Total Gasto R$',value=response[1])
                        st.metric('Total Percorrido Km',value=response[2])
                        st.metric('Quantidade total entregue',value=response[3])

