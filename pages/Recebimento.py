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
            donwload_receiving()

tab1,tab2 = st.tabs(['Adicionar itens',"Consultar itens"])

with tab1:
        if tab1:
            adicionar = st.popover("Adicionar")
            with adicionar:
                    produto = st.selectbox(label="Produto",placeholder="Insira o produto",options=[item.codigo for item in session.query(Produtos).all()],index=None,key="receber")
                    if produto:
                                quantidade = st.number_input(label="Quantidade",placeholder="Insira a quantidade",value=None)
                    if produto and quantidade:
                            st.info(add_receiving(code=produto,qtd=quantidade,user=st.session_state.selected_option))
with tab2:
        if tab2:
            consultar = st.popover("🔍")
            with consultar:
                    itens = [item.produto for item in session.query(Recebimento).all()]
                    consulta = st.selectbox(label="Consulta",placeholder="Selecione um Produto",options=itens,index=None)
                    if consulta:
                        query_receiving(consulta)
                    if st.button("🗑️"):
                            item = session.query(Recebimento).filter(Recebimento.produto==consulta).first()
                            if item:
                                    session.delete(item)
                                    session.commit()
                            else:
                                    st.error(f"O item {consulta} não possúi saldo para ser excluído")

                 
