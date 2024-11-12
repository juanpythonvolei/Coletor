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
            donwload_billing()


marca = st.text_input(label="Marca",placeholder="Insira a marca do veículo")
modelo = st.text_input(label="Modelo",placeholder="Insira o modelo do veículo")
autonomia = st.number_input(label="Autonomia",placeholder="Insira a Autonomia do veículo",value=None)

if marca and modelo and autonomia:
    verificar = session.query(Veiculos).filter(Veiculos.modelo==modelo).first()
    if verificar:
          st.error(f'O modelo: {verificar.modelo} já está cadastrado')
    else:  
          session.add(Veiculos(marca=marca,modelo=modelo,autonomia=autonomia))
          session.commit()    
          st.success(f'O veículo modelo: {modelo} foi cadastrado com sucesso')

botao_mudar = st.popover('Alterar informações ⚙️')
with botao_mudar:
      veiculo = st.selectbox(label='Seleção',placeholder="Selecione o veículo",options=[item[0] for item in session.query(Veiculos.modelo).all()],key='escolha',index=None)
      if veiculo:
            alteracao = st.selectbox(label='Seleção',placeholder="Selecione o veículo",options=['Marca','Modelo','Autonomia'],key='alteração',index=None)
            if alteracao:
                  valor = st.text_input(label='Alteração',placeholder='Insira sua alteração')
                  if valor:
                        verificar = session.query(Veiculos).filter(Veiculos.modelo==veiculo).first()
                        if alteracao == 'Marca':
                              verificar.marca = valor
                              session.commit()
                              st.success(f'Alteração no campo {alteracao} para o veículo: {veiculo} realizada com sucesso')
                        elif alteracao == 'Modelo':
                              verificar.modelo = valor
                              session.commit()
                              st.success(f'Alteração no campo {alteracao} para o veículo: {veiculo} realizada com sucesso')
                        elif alteracao == 'Autonomia':
                              verificar.autonomia = float(valor)
                              session.commit()
                              st.success(f'Alteração no campo {alteracao} para o veículo: {veiculo} realizada com sucesso')
                  
botao_excluir = st.popover('Excluir informações 🗑️')
with botao_excluir:
      veiculo = st.selectbox(label='Seleção',placeholder="Selecione o veículo",options=[item[0] for item in session.query(Veiculos.modelo).all()],key='deletar',index=None)
      if veiculo:
            senha = st.text_input(label='Insira a senha do administrador');
            if senha == '1020':
                  session.delete(session.query(Veiculos).filter(Veiculos.modelo==veiculo).firts())
                  session.commit()
                  st.success(f'O Veículo de modelo: {veiculo} foi deletado com sucesso')

with st.popover('Ver Frota 🔍'):
      dist = 0
      val = 0 
      veiculo = st.selectbox(label='Seleção',placeholder="Selecione o veículo",options=[item[0] for item in session.query(Veiculos.modelo).all()],key='ver',index=None)
      entregas = session.query(Entregas).filter(Entregas.veiculo==veiculo).all()
      for entrega in entregas:
            distancia = build_google_map(route(define_destiny_list([session.query(Faturamento).filter(Faturamento.status==True,Faturamento.numero_da_nota == entrega.nota).first().numero_da_nota])))[2][0]['Distância']
            if ' k' in distancia:
                distancia = float(distancia.replace('k', '').replace(',', '.').strip()) 
            dist += distancia
            val += (float(distancia)/float(veiculo.autonomia)*5.50)
      if veiculo:
                  verificar = session.query(Veiculos).filter(Veiculos.modelo==veiculo).first()
                  st.info(f'''
                  Marca: {verificar.marca}\n
                  autonomia: {verificar.autonomia} km/l\n
                  Total gasto: R$ {val}
                  Total percorrido: Km: {dist}
                  ''')
