import streamlit as st
from views import *



colx,coly = st.columns(2)

with colx:
      if 'selected_option' in st.session_state:
            st.title(f'Usuário logado: {st.session_state.selected_option}')
with coly:
      with st.popover('🤖'):
            assistant()

col1,col2,col3,col4 = st.columns(4)

with col1:
    cadastrar_produtos = st.popover("➕ Cadastrar Produtos")
    with cadastrar_produtos:
        nome = st.text_input(label = "Descrição",placeholder="Insira o nome do Produto")
        codigo = st.text_input(label = "SKU",placeholder="Insira o código do produto")
        preco = st.number_input(label = "Preço",placeholder="Insira o Preço do produto",value=None)
        peso = st.number_input(label = "Peso",placeholder="Insira o Peso do produto",value=None)
        if nome and codigo and preco and peso:
             st.info(add_product(nome,codigo,preco,peso,user=st.session_state.selected_option))       
        else:
             st.error("Campos ausentes")
             
with col2:
    alteracoes = st.popover("⚙️ Ajutar informações")
    with alteracoes:
        item = st.selectbox(label='Seleção',placeholder="Selecione um produto para alterar informações",options=[item.codigo for item in session.query(Produtos).all()],index=None,key='item')
        if item:
            elemento = st.selectbox(label="Alteração",placeholder="Selecione o tipo de alteração",index=None,options=['nome','codigo','preço','peso'],key='opção')
            if elemento == 'preço' or elemento == 'peso':
                valor = st.number_input(label="Valor",placeholder = "Insira o valor da alteração")
            else:
                valor  = st.text_input(label="Valor",placeholder="Insira o valor da alteração")
            deletar = st.button("🗑️")
            if deletar:
              st.info(delete_product(item,user=st.session_state.selected_option))
            if item and elemento and valor:
                st.info(update_product(item,elemento,valor,user=st.session_state.selected_option))

with col3:
      pesquisa = st.popover("🔍 Pesquisar Produtos")
      with pesquisa:
            ativo = st.selectbox(label='Seleção',placeholder="Selecione um produto para alterar informações",options=[item.codigo for item in session.query(Produtos).all()],index=None,key='ativo')
            if ativo:
                infos = query_product(ativo)
                st.info(f'''
            Nome: {infos['nome']}\n
            Preço: {infos['preco']}R$\n
            Peso: {infos['peso']} Kg\n''')

with col4:
    ean = st.popover("📖 Cadastrar Código Ean de produtos")
    with ean:
        x = st.selectbox(label='Seleção',placeholder="Selecione um produto para alterar informações",options=[item.codigo for item in session.query(Produtos).all()],index=None,key='x')
        codigo_ean = st.text_input(label="EAN",placeholder="Insira seu código ean")
        if x and codigo_ean:
            query_and_register_ean(x,codigo_ean)
            if st.button("⚙️ Consultar código ean"):
                query_and_update_ean(x,codigo_ean)