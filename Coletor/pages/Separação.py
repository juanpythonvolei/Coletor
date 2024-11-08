from views import *
import streamlit as st
import random



colx,coly = st.columns(2)

with colx:
      if 'selected_option' in st.session_state:
            st.title(f'Usuário logado: {st.session_state.selected_option}')
with coly:
      with st.popover('🤖'):
            assistant()

notas = session.query(Picklist.nota).filter(Picklist.status==True,Picklist.data == str(date.today())).all()
nota_a_remover = session.query(Separacao.nota).filter(Separacao.status == True,Separacao.data == str(date.today())).all()
lista = []
for item in notas:
   if item in nota_a_remover:
      pass
   else:   
      numero= item[0]
      lista.append(numero)
contador = 0
col4,col5,col6 = st.columns(3)
with col4:
   selecoes = st.multiselect(label="Selecione suas notas",options=list(set(lista)),placeholder="Selecione as notas para a separação")
with col5:
   for item in selecoes:
      quantidae_value = session.query(Picklist).filter(Picklist.data == str(date.today()),Picklist.nota == item,Picklist.status == True).first().quantidade
      contador += quantidae_value
   st.metric(label="Total de volumes",value=contador)
with col6:
    st.metric(label="Notas disponíveis",value=len(lista))

st.divider()
st.title("Notas selecionadas")


if selecoes:
   for i,elemento in enumerate(list(set(separation(selecoes)))):
      nota = st.subheader(f"Nota: {elemento.nota} Quantidade: {elemento.quantidade}")
      col1,col2,col3 = st.columns(3)
      with col1:
         posicao = st.text_input(label=f"Posicao: {elemento.endereco}",key=i+2,placeholder="Insira a posição")
      with col2:
         item = st.text_input(label=f"Produto: {elemento.produto}",key=i+100,placeholder="Insira o produto")
      if item == str(elemento.produto) and posicao == str(elemento.endereco):
                  separate(user=st.session_state.selected_option,product=item,data=str(date.today()),note_number=elemento.nota,qtd_coletada=float(1))
      with col3:
            quantidade = 0
            try:
               quantidade = session.query(Separacao).filter(Separacao.produto == item,Separacao.id_mercado == elemento.id,Separacao.data == str(date.today()),Separacao.nota == elemento.nota).first().qtd_coletada
            except:
               pass
            quantidade_coletada = st.metric(label="quantidade coletada",value=quantidade)
      st.divider()