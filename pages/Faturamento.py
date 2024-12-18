import streamlit as st
from views import *
import xmltodict
from datetime import date
image = st.image('https://img.freepik.com/vetores-gratis/modelo-de-logotipo-da-empresa-de-caminhoes_441059-258.jpg?w=996')

try:
      logado = st.session_state.selected_option
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
      
      uploaded_files = st.file_uploader("Seleção", type=[f'xml'], accept_multiple_files=True,help='Insira suas notas aqui',key='Faturamento')
      with st.popover('Faturar Manualmente'):
                        lista = []
                        produtos = [item.codigo for item in session.query(Produtos).all()]
                        for produto in produtos:
                              try:
                                    outro = session.query(Recebimento).filter(Recebimento.produto == produto).first().produto
                                    outro_estoque = session.query(Estoque).filter(Estoque.item== outro).first().item
                                    lista.append(outro_estoque)
                              except:
                                    pass
                        produto = st.selectbox(label='Produto',placeholder='Insira o Produto',key='Produto',options=lista,index=None)
                        transp = st.text_input(label='transp',placeholder='Insira a transportadora',key='transp')
                        qtd = st.number_input(label='Quantidade',placeholder='Insira a quantidade',key='Quantidade',value=None)
                        cliente = st.text_input(label='cliente',placeholder='Insira o cliente',key='cliente')
                        nota = st.text_input(label='Nota',placeholder='Insira a nota',key='Nota')
                        destino = st.text_input(label='Destino',placeholder='Insira o destino',key='Destino')
                        if produto and transp and qtd and cliente and nota and destino:
                              manual_billing(code=produto,transp=transp,client=cliente,user=st.session_state.selected_option,qtd=qtd,number=int(nota),destino=destino)
                        else:
                              st.error('Ainda há campos a serem preenchidos')
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
except:
      st.error('Você deve estar logado para acessar a essa página')
      
