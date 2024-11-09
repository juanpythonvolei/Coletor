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
            donwload_picklist()

mercados_ativos = picking(data=str(date.today()))
for mercado in mercados_ativos:
        col1,col2,col3 = st.columns(3)
        contador = 0
        with col1:
            st.info(f'''
        qtd: {mercado.quantidade}\n
        local: {mercado.posicao}\n
        nota: {mercado.numero_da_nota}
        ''')
        with col2:
            elemento = st.text_input(label=f'Coleta do item {mercado.produto}',placeholder='Insira o produto',key=mercado.id)
            if elemento:
                if str(elemento) == str(mercado.produto):
                    pick(product=mercado.produto,data=str(date.today()),user=st.session_state.selected_option,qtd_coletada=1,note_number=mercado.numero_da_nota)
        with col3:
            valor = None
            try:
                verificar = session.query(Picklist).filter(Picklist.id_faturamento == mercado.id,Picklist.produto == mercado.produto,Picklist.data == mercado.data,Picklist.nota == mercado.numero_da_nota,Picklist.status == mercado.status).first().qtd_coletada
                valor = verificar
            except:
                valor = 0
            st.metric(label="quantidade",value=valor)
        st.divider()
