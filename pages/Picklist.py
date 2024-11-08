import streamlit as st 
from views import *



colx,coly = st.columns(2)

with colx:
      if 'selected_option' in st.session_state:
            st.title(f'Usuário logado: {st.session_state.selected_option}')
with coly:
      with st.popover('🤖'):
            assistant()

mercados_ativos = picking(data=str(date.today()))
for mercado in list(set(mercados_ativos)):
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