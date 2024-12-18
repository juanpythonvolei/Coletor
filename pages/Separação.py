from views import *
import streamlit as st
import random

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
                  donwload_separation()
      
      notas = session.query(Picklist).filter(Picklist.status==True,Picklist.data == str(date.today())).all()
      nota_a_remover = session.query(Separacao.nota,Separacao.produto).filter(Separacao.status == True,Separacao.data == str(date.today())).all()
      lista = []
      for item in notas:
         if (item.nota,item.produto) in nota_a_remover:
            pass
         else:   
            numero= item.nota
            lista.append(numero)
      contador = 0
      col4,col5,col6 = st.columns(3)
      with col4:
         selecoes = st.multiselect(label="Selecione suas notas",options=list(set(lista)),placeholder="Selecione as notas para a separação")
      with col5:
         for item in selecoes:
            quantidae_value = session.query(Picklist.quantidade).filter(Picklist.data == str(date.today()),Picklist.nota == item,Picklist.status == True).all()
            lista_quantidade = [item[0] for item in quantidae_value]
            for elemento in lista_quantidade:
                  contador += elemento
         st.metric(label="Total de volumes",value=contador)
      with col6:
          st.metric(label="Notas disponíveis",value=len(set(list(lista))))
      
      st.divider()
      st.title("Notas selecionadas")
      
      
      if selecoes:
         for i,elemento in enumerate(separation(selecoes)):
            nota = st.subheader(f"Nota: {elemento.nota} Quantidade: {elemento.quantidade}")
            col1,col2,col3 = st.columns(3)
            with col1:
               posicao = st.text_input(label=f"Posicao: {elemento.endereco}",key=i+2,placeholder="Insira a posição",help='Exemplo = 01-001-01')
            with col2:
               item = st.text_input(label=f"Produto: {elemento.produto}",key=i+100,placeholder="Insira o produto")
            if item == str(elemento.produto) and posicao == str(elemento.endereco):
                        separate(user=st.session_state.selected_option,product=item,data=str(date.today()),note_number=elemento.nota,qtd_coletada=float(1))
                        with col3:
                                 quantidade_coletada = st.metric(label="quantidade coletada",value=session.query(Separacao).filter(Separacao.produto == item,Separacao.data == str(date.today()),Separacao.nota == elemento.nota).first().qtd_coletada)   

                  
            st.divider()
except:
      st.error('Você deve estar logado para acessar essa página')
