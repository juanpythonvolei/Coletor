import streamlit as st
from views import *
import speech_recognition as sr


colx,coly = st.columns(2)

with colx:
      if 'selected_option' in st.session_state:
            st.title(f'Usuário logado: {st.session_state.selected_option}')
with coly:
      with st.popover('🤖'):
            assistant()

transferencia = st.popover("Transferência")
with transferencia:
        deposito  = st.selectbox(label="Origem",placeholder="Selecione a origem",options=['Estoque','Recebimento'],index=None,key="select_state",on_change=None)
        if deposito == 'Estoque':
            origem = st.selectbox(label="Origem",placeholder="Insira o endereço de origem",index=None,options=[item.endereco for item in session.query(Estoque).all()],)
            destino = st.text_input(label="Destino",placeholder="Insira o endereço de destino")
            destino_valido = treat_adress(destino)
            if origem and destino_valido:
                produto = st.selectbox(label="Produto",placeholder="Selecione um Produto",options=[item.item for item in session.query(Estoque).filter(Estoque.endereco==origem,Estoque.quantidade>0).all()],index=None,key="select_state_outro")
                if produto:
                    quantidade = st.number_input(label="Quantidade",placeholder="Insira a quantidade",value=None)
                    if produto and quantidade:
                        st.info(tranfer_item_from_storage(code=produto,qtd=quantidade,origin=origem,destiny=destino,user=st.session_state.selected_option))
                        deposito = ''
        elif deposito == 'Recebimento':
            destino = st.text_input(label="Destino",placeholder="Insira o endereço de destino")
            destino_valido = treat_adress(destino)
            if destino_valido:
                produto = st.selectbox(label="Consulta",placeholder="Selecione um Produto",options=[item.produto for item in session.query(Recebimento).filter(Recebimento.quantidade>0).all()],index=None,key="seleção produtos")
                if produto:
                    quantidade = st.number_input(label="Quantidade",placeholder="Insira a quantidade",value=None)
                    if produto and quantidade:
                        st.info(transfer_item_from_receiving(code=produto,destiny=destino,qtd=quantidade,user=st.session_state.selected_option))

with st.popover("Consulta"):
        produtos = st.selectbox(label="Produto",placeholder="Insira o produto",options=[item.codigo for item in session.query(Produtos).all()],index=None,key='produtos')
        posicoes = st.selectbox(label="Posição",placeholder="Insira a posição",options=[item.endereco for item in session.query(Estoque).all()],index=None,kwargs='posições')
        if produtos and not posicoes:
            texto = ''
            infos_rec = session.query(Recebimento).filter(Recebimento.produto==produtos).first()
            infos_est = [f'Posição: {item.endereco} Quantidade: {item.quantidade}\n' for item in session.query(Estoque).filter(Estoque.item==produtos).all()]
            for descri in infos_est:
                if descri in texto:
                     pass
                else:
                    texto += f'{descri}\n'
            st.info(f"""Recebimento: \n
                    Quantidade: {infos_rec.quantidade} Data: {infos_rec.data}
Estoque\n
{texto}""")
        elif posicoes and not produtos:
            texto = ''
            infos_est = [f'codigo: {item.item} Quantidade: {item.quantidade}\n' for item in session.query(Estoque).filter(Estoque.endereco==posicoes).all()]
            for descri in infos_est:
                if descri in texto:
                     pass
                else:
                    texto += f'{descri}\n'
            st.info(f"""Estoque: \n
            {texto}""")
        elif produtos and posicoes:
            texto = ''
            infos_est = [f'Quantidade: {item.quantidade}\n' for item in session.query(Estoque).filter(Estoque.endereco==posicoes,Estoque.item==produtos).all()]
            for descri in infos_est:
                if descri in texto:
                     pass
                else:
                    texto += f'{descri}\n'
            st.info(f"""Estoque: \n
            {texto}""")
with st.popover("Assistência"):
        audio_value = st.experimental_audio_input("Faça sua pergunta")
        if audio_value:
                texto_decri = ''
                infos_rec = session.query(Recebimento).all()
                descri_rec = [f'Item Recebimento: {item.produto} Quantidade Recebimento: {item.quantidade}'for item in infos_rec]
                for elemento in descri_rec:
                    if elemento in texto:
                        pass
                    else:
                        texto += elemento
                infos_est = [f'Item: {item.item} Endereço: {item.endereco} Quantidade: {item.quantidade}\n' for item in session.query(Estoque).all()]
                for descri in infos_est:
                    if descri in texto:
                        pass
                    else: 
                        texto += f'{descri}\n'
                assistant = st.chat_message('assistant')
                rec = sr.Recognizer()
                with sr.AudioFile(audio_value) as arquivo_audio:
                    audio = rec.record(arquivo_audio)
                    texto = rec.recognize_google(audio,language ='pt-BR ')
                resposta = analisar(texto,texto_decri)
                assistant.write(resposta)   
        message = st.chat_input(placeholder="Insira sua pegunta")
        if message:
            texto = ''
            infos_rec = session.query(Recebimento).all()
            descri_rec = [f'Item Recebimento: {item.produto} Quantidade Recebimento: {item.quantidade}'for item in infos_rec]
            for elemento in descri_rec:
                if elemento in texto:
                    pass
                else:
                    texto += elemento
            infos_est = [f'Item: {item.item} Endereço: {item.endereco} Quantidade: {item.quantidade}\n' for item in session.query(Estoque).all()]
            for descri in infos_est:
                if descri in texto:
                     pass
                else:
                    texto += f'{descri}\n'
            human = st.chat_message("human")
            ia = st.chat_message("ai")
            human.write(message)
            ia.write(analisar(f"Você é um assisnte de estoque e sua função é me auxiliar na observação do meu armazém. A seguir, você verá um Conjunto de informaçõe que dize respeito ao endereço, quantidade e código de um ou mais itens. Baseando-se nele, responda ao que se pede: {message}",texto))
            
with st.popover("Corrigir item em endereço"):
    item = st.selectbox(label="Item",placeholder="Selecione um item",options=list(set([item.item for item in session.query(Estoque).all()])),index=None)
    if item:
        endereco = st.selectbox(label="Endereço",placeholder="Selecione um endereço",options=[item.endereco for item in session.query(Estoque).filter(Estoque.item == item).all()])
        if endereco:
             quantidade = st.number_input(label="Quantidade",placeholder="Insira a quantidade",value=None,key="quantidade_correção_endereçoS")
             if quantidade:
                  correct_qtd_tranfer_from_receiving(code=item,adress=endereco,qtd=quantidade,user=st.session_state.selected_option)

