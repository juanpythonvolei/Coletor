from database import *
from sqlalchemy.orm import sessionmaker
import streamlit as st
from datetime import date
import google.generativeai as genai
import pandas as pd
import xmltodict
import os 
import speech_recognition as sr
from io import BytesIO
from geopy.geocoders import Nominatim
from geopy.distance import geodesic
from time import sleep
import requests

session = sessionmaker(bind=engine)
session = session()
def new_logged_infos(user):
    sleep(2)
    first = st.title('Olá')
    sleep(4)
    first.empty()
    second = st.header(f'Seja Bem vindo,{user},ao aplicativo do coletor')
    sleep(6)
    second.empty()
    third = st.header(f'Sinta-se a vontade para explorar o sistema')
    sleep(6)
    third.empty()
    fourth = st.header(f'Porém, para te ajudar,irei mencionar qual é o fluxo de atividades que fazem o app funcionar!')
    sleep(6)
    fourth.empty()
    fifth = st.header('O Fluxo é o seguinte:')
    sleep(6)
    fifth.empty()
    sixth = st.header('1. Vá para cadastro de produtos, e preencha os campos para que o cadastro seja finalizado')
    sleep(6)
    sixth.empty()
    seventh = st.text('''2. Em Seguida, siga para Recebimento. Na caixa de seleção, 
    escolha o item que você separou, 
    ou os que estão disponíveis, e faço o recebimento de uma quantidade de sua preferência
    ''')
    sleep(6)
    seventh.empty()
    eigth = st.subheader('''
    3. Com o item já recebido, vá para a aba de Transferência. Nesse espaço, para trazer os itens,
    selecione a opção "Recebimento" em "origem". Após isso, Insira, no campo de destino, um endereço 
    no seguinte
    formato: 0>0n<08-0>00n<20-0>0n<05. Na aba seguinte, escolha o item, e a quantidade.
    ''')
    sleep(6)
    eigth.empty()
    nineth = st.text('''4. 
    Agora, você já pode ir para aba de faturamento, e realizar o faturamento manual. Assim, 
    preencha todos os
    campos e, ao fim, o faturamento terá se iniciado. obs: Caso você queira realizar o faturamento 
    com arquivos de 
    notas  fiscais 
    clique no icone maior
    a primeira ação que ele fará é, automaticamente, cadastrar os itens da nota. Depois, 
    você deve realizar o 
    processo de
    recebimento e transferência.
    Quando concluir, é só retornar no icone e reselecionar as notas. Isso fará com que o 
    Faturamento se inicie.
    ''')
    sleep(6)
    nineth.empty()
    tenth = st.subheader('''
    5. Entre na aba de Pickinglist. Para coletar os itens, observe sua localização e quantidade. 
    A coleta se da na ação
    de inserir o código do produto no campo. Se houver apenas 1 item, o processo se encerrará. 
    Se não, 
    o mostrador irá mudar 
    até que você colete
    a quantidade da nota. Se completar esse campo, vá para Separação. Nessa aba, 
    é o mesmo procedimento porém, 
    além do item
    deve-se inserir a posição dele
    no estoque para contabilizar uma coleta
    ''')
    sleep(6)
    tenth.empty()
    eleventh = st.text('''
    6.Pronto, seu faturamento acabou. Agora, vá para Rotas e depois em entregas. Nessa aba selecione 
    a data de hoje, a 
    transportadora e  um carro de tranporte.
    Após isso, serão exibidos todos os pedidos faturados e separados. Para entregar, 
    é só ativar a chave. 
    Nesse caso,você assume o papel do entregador. Ops, esqueci. O carro utilizado também
    deve ser cadastrado. Para isso, vá para a aba "Frota" e lá, preencha os dados do veículo. Eles são 
    importantes 
    para as informações 
    vindas da entrega. 
    ''')
    sleep(6)
    eleventh.empty()
    twelveth = st.text('''7. 
    Pronto!, Esse é o fluxo. Além, dele, você pode acessar diversos outros menus de consulta, 
    falar com o 
    assitente inteligente, 
    ver o histórico etc.
    O assistente possúi uma aba dedicada, mas está em todos os menus na forma de um robozinho. 
    Ele sabe tudo sobre as 
    movimentações 
    feitas no aplicativo
    então se precisar de uma esclarecimento
    ou algo do gênero, pode falar com ele.

    Obs: Este app, não foi desenvolvido para uso empresarial. Por conta disso, algumas etapas, 
    como o faturamento, 
    não podem ser equiparadas a um 
    faturamento real visto que careço 
    da posse de sistemas
    e credenciais que somente estão em posse de empresa. 
    Outro ponto importante é que ele está em constante desenvolvimento, 
    então algumas funções melhorarão ou 
    serão substituidas e até acrescentadas.
    ''')
    sleep(6)
    twelveth.empty()
    final = st.header('''8. Bom, já falei demais. Aproveite sua experiência!
    Se não souber o que fazer, chame o assistente!.
    ''')
    sleep(4)
    final.empty()
def treat_table(df):
    table = pd.read_excel(df)
    return table.to_string()
    
def treat_audio(texto_final,files):
    
    audio_value = st.audio_input(label="Faça sua pergunta",key='assistant')
    if audio_value:
        
        rec = sr.Recognizer()
        with sr.AudioFile(audio_value) as arquivo_audio:
                    audio = rec.record(arquivo_audio)
                    texto = rec.recognize_google(audio,language ='pt-BR ')
        humano = st.chat_message('human')
        humano.write(texto)
        assistente = st.chat_message('assistant')
        if files != None:
            return assistente.write(analisar(
                f"""Você é um analista de dados em larga escala e sua missão é me ajudar a solucionar problemas relacionados ao meu estoque. Estou lhe enviando uma grande quantidade de dados referentes a diferentes aspectos e processo do meu Estoque como desde o faturamento de pedidos e recebimento de mercadorias até a expedição. Essas informações estão em formato de listas.
                Então você deve interpretar o que cada lista mostra de informação e responder a essa questão: {texto}"""
                ,str(texto_final)))
        else:
            return assistente.write(analisar(
                f"""Por favor, analise as tabelas a seguir e, baseando-se nelas, responda ao que se pede: {texto}"""
                ,str(files)))
         
        
def read_ean(ean):
    try:
        produto = session.query(EansProdutos).filter(EansProdutos.codigo_ean == ean).first().produto
        return produto,st.success(f"Item: {produto}")
    except:
        return st.error("o código ean não foi encontrado")

def add_history(action,qtd,data,item,user):
    new_event = Historico(action,qtd,data,item,user)
    session.add(new_event)
    session.commit()

def verify_if_still_exists(code,adress):
    try:
        verificar = session.query(Estoque).filter(Estoque.item==code,Estoque.endereco==adress).first()
        if verificar.quantidade == 0:
            session.delete(verificar)
            session.commit()
    except:
        pass

def verify_if_still_exists_rec(code):
    try:
        verificar = session.query(Recebimento).filter(Recebimento.produto==code).first()
        if verificar.quantidade == 0:
            session.delete(verificar)
            session.commit()
    except:
        pass

def treat_adress(adress):
    adress = str(adress)
    try:
        if "#" in adress:
                adress = adress.replace("#",'').strip()
                if "-" not in adress:
                    return F"O endereço {adress} não é válido"
                else:
                    list = adress.split("-")
                    if len(list[0]) != 2 or int(list[0])>=10:
                        adress = None
                        st.error(f"O endereço {list[0]}-{list[1]}-{list[2]} não é Válido") 
                        return adress
                    if len(list[1]) != 4 or int(list[1]) >= 20:
                        adress = None
                        st.error(f"O endereço {list[0]}-{list[1]}-{list[2]} não é Válido") 
                        return adress
                    if len(list[2]) != 2 or int(list[2]) >= 10:   
                        adress = None
                        st.error(f"O endereço {list[0]}-{list[1]}-{list[2]} não é Válido") 
                        return adress
        else:
                if "-" not in adress:
                    adress = None
                else:
                    list = adress.split("-")
                    if len(list[0]) != 2 or int(list[0]) >= 10:
                        adress = None
                        st.error(f"O endereço {list[0]}-{list[1]}-{list[2]} não é Válido") 
                        return adress
                    if len(list[1]) != 3 or int(list[1]) >= 20:
                        adress = None
                        st.error(f"O endereço {list[0]}-{list[1]}-{list[2]} não é Válido") 
                        return adress
                    if len(list[2]) != 2 or int(list[2]) >= 10:   
                        adress = None
                        st.error(f"O endereço {list[0]}-{list[1]}-{list[2]} não é Válido") 
                        return adress
        return adress
    except:
        st.error(f"O endereço {adress} não é válido")


def analisar(pergunta,conteudo):
    
    genai.configure(api_key=st.secrets['ia'])
    model = genai.GenerativeModel('gemini-1.5-flash')
    chat = model.start_chat(history=[{"role": "user", "parts": [{"text": conteudo}]}])
    response = chat.send_message(pergunta)
    return response.text


def carregar_arquivo(pergunta,conteudo):
    genai.configure(api_key=st.secrets['ia']) 
    model = genai.GenerativeModel('gemini-1.5-flash') 
    chat = model.start_chat(history=[{"role":"user","parts":[genai.upload_file(conteudo)]}]) 
    response = chat.send_message(pergunta) 
    return response.text

@st.dialog("Deseja realmente continuar ?")
def confirmar(function,message):
    if st.button('Confirmar'):
        function
        return st.success(message)

def save_table_int_text(table,user,data):
    tabela = table.to_string()
    session.add(Romaneios(romaneio=tabela,data=data,usuario=user))
    session.commit()
    return st.success("Romaneio salvo com sucesso")

def add_product(name,code,price,weigth,user):
    try:
        verificar = session.query(Produtos).filter(Produtos.codigo == code).first()
        return f"O Código {verificar.codigo} já está cadastrado"
    except:
        new_product =Produtos(nome=name,codigo=code,preco=price,peso=weigth)
        session.add(new_product)
        session.commit()
        add_history(action="cadastro",data=str(date.today()),qtd=1,item=code,user=user)
        return f"Produto {name} cadastrado com sucesso"

def query_product(code):
    try:
        try:
            query = session.query(Produtos).filter(Produtos.codigo == code).first()
        except:
            query = session.query(Produtos).filter(Produtos.codigo == read_ean(code)[0]).first()
        return {'nome':query.nome,
                'preco':query.preco,
                'peso':query.peso,
                'status':True}
    except:
        return f"O Código {code} não está cadastrado"

def delete_product(code,user):
    try:
        produto_existente= session.query(Produtos).filter(Produtos.codigo == code).first()
    except:
        produto_existente= session.query(Produtos).filter(Produtos.codigo == read_ean(code)[0]).first()
    if produto_existente:
        session.delete(produto_existente)
        session.commit()
        add_history(action="deleção",data=str(date.today()),qtd=1,item=code,user=user)
        return f"Produto {produto_existente.nome} deletado com sucesso"
    else:
        return f"Código {code} não existe"
    
def update_product(code,elemento,informação,user):
    try:
        produto_existente = session.query(Produtos).filter(Produtos.codigo == code).first()
        correspondente = session.query(EansProdutos).filter(EansProdutos.correspondente == code).first()
    except:
        produto_existente = session.query(Produtos).filter(Produtos.codigo == read_ean(code)[0]).first()
        correspondente = session.query(EansProdutos).filter(EansProdutos.correspondente == read_ean(code)[0]).first()
    if produto_existente:
        if elemento == 'nome': 
            produto_existente.nome = informação
            session.commit()
        elif elemento == 'codigo':
            produto_existente.codigo = informação
            correspondente.correspondente = informação
            session.commit()
        elif elemento == 'preço':
            produto_existente.preco = informação
            session.commit()
        elif elemento == 'peso':
            produto_existente.peso = informação
            session.commit()
        add_history(action=f"atualização do item {produto_existente.codigo} no quesito {elemento}",data=str(date.today()),qtd=1,item=code,user=user)
        return f"Produto {produto_existente.codigo} Atualizado no item {elemento} com sucesso"
    else:
        return f"Usuário {produto_existente} não existe"
    
def tranfer_item_from_storage(code,origin,destiny,qtd,user):
        try:
            try:
                verificar = session.query(Estoque).filter(Estoque.endereco==origin,Estoque.item==code).first()
            except:
                verificar = session.query(Estoque).filter(Estoque.endereco==origin,Estoque.item==read_ean(code)[0]).first()
            if verificar.quantidade >= qtd:
                try:
                    verificar_pos_final = session.query(Estoque).filter(Estoque.endereco==destiny,Estoque.item==verificar.item).first()
                    verificar_pos_final.quantidade += qtd
                    session.commit()
                    verificar.quantidade -= qtd
                    session.commit()
                    verify_if_still_exists(code=code,adress=origin)
                    add_history(action=f"Transferência do item {verificar.item} da posição {origin} para a posição {destiny}",qtd=qtd,data=str(date.today()),item=verificar.item,user=user)
                    return f"O item {verificar.item} foi adicionado na posição {verificar_pos_final.endereco} em {qtd} unidades"
                except:
                    session.add(Estoque(verificar.item,destiny,qtd))
                    session.commit()
                    verificar.quantidade -= qtd
                    session.commit()
                    verify_if_still_exists(code=code,adress=origin)
                    add_history(action=f"Transferência do item {verificar.item} da posição {origin} para a posição {destiny}",qtd=qtd,data=str(date.today()),item=verificar.item,user=user)
                    return f"O item {verificar.item} foi adicionado na posição {destiny} em {qtd} unidades"
            else:
                return st.error(f"A quantidade solicitada {qtd} para o item {code} é maior do que a quantidade em estoque para a posição {origin}")
        except:
            f"O item {code} não está cadastrado"

def transfer_item_from_receiving(code,destiny,qtd,user):
        try:
            try:
                verificar = session.query(Recebimento).filter(Recebimento.produto == code).first()
            except:
                verificar = session.query(Recebimento).filter(Recebimento.produto == read_ean(code)[0]).first()
            if verificar:
                    if verificar.quantidade >= qtd:
                        try:
                            qtd_se_existe_estoque = session.query(Estoque).filter(Estoque.item==verificar.produto,Estoque.endereco==destiny).first()
                            qtd_se_existe_estoque.quantidade += qtd
                            session.commit()
                            verificar.quantidade -= qtd
                            verify_if_still_exists_rec(verificar)
                            session.commit()
                            add_history(action=f"Transferência do item {verificar.produto} do recebimento para a posição {destiny}",qtd=qtd,item=verificar.produto,data=str(date.today()),user=user)
                            return f"Item {verificar.produto} adicionado na posição {destiny} no total de {qtd_se_existe_estoque} unidades"
                        except:
                            session.add(Estoque(item=code,endereco=destiny,quantidade=qtd))
                            session.commit()
                            verificar.quantidade -= qtd
                            session.commit()
                            verify_if_still_exists_rec(verificar)
                            add_history(action=f"Transferência do item {verificar.produto} do recebimento para a posição {destiny}",qtd=qtd,item=verificar.produto,data=str(date.today()),user=user)
                            return f"Item {verificar.produto} adicionado na posição {destiny} no total de {qtd} unidades"
                    else:
                        return st.error(f"A quantidade solicitada {qtd} para o item {code} é maior do que recebimento")
            else:
                    return f"O item {code} não tem saldo para transferência em recebimento"
        except:         

            f"O item {code} não está cadastrado"

def add_receiving(code,qtd,user):
        data = str(date.today())
        try:
            try:
                verificacao = session.query(Produtos).filter(Produtos.codigo==code).first()
            except:
                verificacao = session.query(Produtos).filter(Produtos.codigo==read_ean(code)[0]).first()
            if code != '':
                try:
                    
                    item = session.query(Recebimento).filter(Recebimento.produto==verificacao.codigo).first()
                    item.quantidade += qtd
                    session.commit()
                    add_history("atualização de recebimento",data=str(date.today()),qtd=item.quantidade,item=item.produto,user=user)
                    return f"O item {item.produto} teve sua quantidade em rec alterada para {item.quantidade}"
                except:
                    add_history(action="recebimento",data=str(date.today()),qtd=qtd,item=verificacao.codigo,user=user)
                    session.add(Recebimento(produto=verificacao.codigo,quantidade=qtd,data=data))
                    session.commit()
                    return f"O Produto {verificacao.codigo} foi adicionado com sucesso em {qtd} unidades"
            else:
                return F"A quantidade informada deve ser maior que 0"
        except:
             return f"O produto {code} não está cadastrado"
        
def query_receiving(code):
    try:
        try:
            verificacao = session.query(Recebimento).filter(Recebimento.produto==code).first()
        except:
            verificacao = session.query(Recebimento).filter(Recebimento.produto==read_ean(code)[0]).first()
        if verificacao.quantidade > 0:
            return st.info(f"""Data: {verificacao.data}--Quantidade: {verificacao.quantidade}""")
        else:
            return st.error(f"O item {verificacao} não possúi saldo em recebimento")
    except:
        return st.error(f"O item {code} não está cadastrado")

def vizualize_history(data):
    try:
        history = session.query(Historico).filter(Historico.data == data).all()
        df_final = pd.concat([pd.DataFrame({"usuario":item.usuario,"evento":item.evento,"item":item.item,"data":item.data,"quantidade":item.quantidade},index=[i]) for i,item in enumerate(history)])
        return st.table(df_final)
    except:
        return st.error(f"Não há histórico para a data {data}")
        
def correct_qtd_tranfer_from_receiving(code,adress,qtd,user):
    try:
        try:
            item_est = session.query(Estoque).filter(Estoque.item ==code,Estoque.endereco==adress).first()
        except:
            item_est = session.query(Estoque).filter(Estoque.item ==read_ean(code)[0],Estoque.endereco==adress).first()
        try:
            try:
                item_rec = session.query(Recebimento).filter(Recebimento.produto==code).first()
            except:
                item_rec = session.query(Recebimento).filter(Recebimento.produto==read_ean(code)[0]).first()
        except:
            if item_est.quantidade >= qtd:
                item_est.quantidade -= (item_est.quantidade-qtd)
                session.commit()
                session.add(Recebimento(produto=code,quantidade=item_est.quantidade-qtd,data=str(date.today())))
                session.commit()
            else:
                return st.error(f"A quantidade solicitada {qtd} para o item {code} é maior do que a quantidade em estoque para a posição {adress}")
        if item_est.quantidade >= qtd:    
            new_qtd = int(item_est.quantidade - qtd)    
            item_est.quantidade -= new_qtd
            verify_if_still_exists(code=code,adress=adress)
            item_rec.quantidade += new_qtd
            session.commit()
            add_history(action=f"Produto {item_est.item} foi retirado da posição de estoque {adress} para o recebimento",data=str(date.today()),qtd=qtd,item=code,user=user)
            return st.success(f"O Produto {item_est.item} foi alterado na posição {item_est.endereco} para {qtd}. O recebimeno foi atualizado para {item_rec.quantidade} ")
        else:
            return st.error(f"A quantidade solicitada {qtd} para o item {code} é maior do que a quantidade em estoque para a posição {adress}")
    except:
        return st.error(f"O item {code} não existe ou não está presente no endereço {adress}")
    
def add_new_user(user,password):
    if 'selected_option' not in st.session_state:
        st.session_state.selected_option = None
    try:
        verificar = session.query(Usuarios).filter(Usuarios.usuario == user).first()
        return st.error(f"Já existe uma conta com o usuário {verificar.usuario}. Por favor, insira um usuário diferente")
    except:
        session.add(Usuarios(usuario=user,senha=password))
        session.commit()
        st.session_state.selected_option = user
        new_logged_infos(st.session_state.selected_option)
        st.switch_page('pages/Menu.py')
        
        

def login(usuario,senha):
    if 'selected_option' not in st.session_state:
        st.session_state.selected_option = None
    elemento =  session.query(Usuarios).filter(Usuarios.usuario == usuario,Usuarios.senha == senha).first()
    if elemento:
        st.session_state.selected_option = elemento.usuario
        st.switch_page('pages/Menu.py')
    else:
        return st.error(f"O usuário {usuario} não existe ou a senha está incorreta")

def picking(data):
    lista_ok = []
    verificar_se_ativo = session.query(Faturamento).filter(Faturamento.data == data,Faturamento.status == False).all()
    se_mercado_concluido = session.query(Picklist.nota,Picklist.produto).filter(Picklist.data == str(date.today()),Picklist.status == True).all()
    lista_conferencia = [elemento for elemento in se_mercado_concluido]
    for item in list(set(verificar_se_ativo)):
        try:
            if (item.numero_da_nota,item.produto) in lista_conferencia:
                pass
            else:
                lista_ok.append(item)    
        except:
            pass
    return lista_ok      

def billing(code,price,transp,client,data,user,qtd,number,status,data_emition,peso,description,destino):
                try:
                    fat = session.query(Faturamento).filter(Faturamento.status == False,Faturamento.data == str(date.today())).first().id
                    st.warnig(f'Já exsite um Processo de Faturamento de id: {fat}. Por favor conclua-o')
                except:
                    verificar = session.query(Produtos).filter(Produtos.codigo == code).first()
                    if verificar:
                        posicao = session.query(Estoque).filter(Estoque.item == verificar.codigo,Estoque.quantidade >= qtd).first().endereco
                        if posicao:
                            if session.query(Estoque).filter(Estoque.item == verificar.codigo,Estoque.endereco == posicao).first().quantidade >= qtd:
                                session.query(Estoque).filter(Estoque.item == verificar.codigo,Estoque.endereco == posicao).first().quantidade -= qtd
                                session.commit()
                                session.add(Faturamento(produto=verificar.codigo,usuario=user,quantidade=qtd,numero_da_nota=number,data=data,status=status,transportadora=transp,cliente=client,data_emissao=data_emition,posicao=posicao,destino=destino))
                                session.commit()
                                add_history(action=f"Faturamento",qtd=qtd,data=data,item=code,user=user)
                                verify_if_still_exists(code=code,adress=posicao)
                                session.commit()
                                return {'tipo':'faturada','valor':1}
                    else:
                        add_product(code=code,price=price,weigth=peso,name=description,user=user)
                        return{'tipo':'cadastrada','valor':1}
def process_notes(notes_list,data,usuario,status,peso_recebido):
    contador_ok = 0
    contador_nao = 0
    contador_cadastro = 0
    for nota in notes_list:                                      
        xml_data = nota.read()
        documento = xmltodict.parse(xml_data)
        try:
                codigo_produto = documento['nfeProc']['NFe']['infNFe']['det']['prod']['cProd']
                numero_da_nota = documento['nfeProc']['NFe']['infNFe']['ide']['nNF']
                descricao_produto = documento['nfeProc']['NFe']['infNFe']['det']['prod']['xProd']
                transportadora = documento['nfeProc']['NFe']['infNFe']['transp']['transporta']['xNome']
                quantidade_produto = documento['nfeProc']['NFe']['infNFe']['det']['prod']['qCom']
                valor_produto = documento['nfeProc']['NFe']['infNFe']['det']['prod']['vProd']
                cliente = documento['nfeProc']['NFe']['infNFe']['dest']['xNome']
                data_emit = documento['nfeProc']['NFe']['infNFe']['ide']['dhEmi'][:10]
                destino = f'{documento['nfeProc']['NFe']['infNFe']["dest"]["enderDest"]["xLgr"]},{documento['nfeProc']['NFe']['infNFe']["dest"]["enderDest"]["nro"]}-{documento['nfeProc']['NFe']['infNFe']["dest"]["enderDest"]["xBairro"]},{documento['nfeProc']['NFe']['infNFe']["dest"]["enderDest"]["xMun"]}-{documento['nfeProc']['NFe']['infNFe']["dest"]["enderDest"]["UF"]},{documento['nfeProc']['NFe']['infNFe']["dest"]["enderDest"]["CEP"]}'
                try:
                    peso = float(documento['nfeProc']['NFe']['infNFe']['transp']['vol']['pesoL'])
                except:
                    peso =float(0)
                resultado = billing(code=codigo_produto,price=valor_produto,transp=str(transportadora)[:5].casefold(),client=cliente,data=data,user=usuario,number=numero_da_nota,status=status,qtd=float(quantidade_produto),data_emition=data_emit,description=descricao_produto,peso=peso,destino=destino)
                if resultado['tipo'] == 'cadastrada':
                        contador_cadastro +=1
                contador_ok += 1
        except: 
                produtos_excessao = documento['nfeProc']['NFe']['infNFe']['det']
                for produto in produtos_excessao:
                        try:
                            codigo_produto = produto['prod']['cProd']
                            descricao_produto = produto['prod']['xProd']       
                            quantidade_produto = produto['prod']['qCom']
                            valor_produto = produto['prod']['vProd']
                            cliente = documento['nfeProc']['NFe']['infNFe']['dest']['xNome']
                            transportadora = documento['nfeProc']['NFe']['infNFe']['transp']['transporta']['xNome']
                            numero_da_nota = documento['nfeProc']['NFe']['infNFe']['ide']['nNF']
                            data_emit = documento['nfeProc']['NFe']['infNFe']['ide']['dhEmi'][:10]
                            destino =  f'{documento['nfeProc']['NFe']['infNFe']["dest"]["enderDest"]["xLgr"]},{documento['nfeProc']['NFe']['infNFe']["dest"]["enderDest"]["nro"]}-{documento['nfeProc']['NFe']['infNFe']["dest"]["enderDest"]["xBairro"]},{documento['nfeProc']['NFe']['infNFe']["dest"]["enderDest"]["xMun"]}-{documento['nfeProc']['NFe']['infNFe']["dest"]["enderDest"]["UF"]},{documento['nfeProc']['NFe']['infNFe']["dest"]["enderDest"]["CEP"]}'
                            resultado = billing(code=codigo_produto,price=valor_produto,transp=str(transportadora)[:5].casefold(),client=cliente,data=data,user=usuario,number=numero_da_nota,status=status,qtd=float(quantidade_produto),data_emition=data_emit,description=descricao_produto,peso=peso_recebido,destino=destino)
                            
                        except:
                            pass
                contador_ok +=1
        else:
            contador_nao += 1
    return contador_ok,contador_cadastro,contador_nao    

def pick(product,data,note_number,user,qtd_coletada):
    try:
        verificar = session.query(Faturamento).filter(Faturamento.produto == product,Faturamento.data == data,Faturamento.numero_da_nota==note_number,Faturamento.status == False).first()
        verificar_picklist = session.query(Picklist).filter(Picklist.id_faturamento == verificar.id,Picklist.produto == verificar.produto,Picklist.data == verificar.data,Picklist.nota == verificar.numero_da_nota,Picklist.status == verificar.status).first()
    except:
        verificar = session.query(Faturamento).filter(Faturamento.produto == read_ean(product)[0],Faturamento.data == data,Faturamento.numero_da_nota==note_number,Faturamento.status == False).first()
        verificar_picklist = session.query(Picklist).filter(Picklist.id_faturamento == verificar.id,Picklist.produto ==verificar.produto,Picklist.data == verificar.data,Picklist.nota == verificar.numero_da_nota,Picklist.status == verificar.status).first()
    if verificar_picklist:
        if verificar_picklist.quantidade == verificar_picklist.qtd_coletada:
            session.query(Picklist).filter(Picklist.id_faturamento == verificar.id,Picklist.produto == verificar.produto,Picklist.data == verificar.data,Picklist.nota == verificar.numero_da_nota,Picklist.status == verificar.status).first().status = True
            session.commit()
            add_history(action=f'Mercado {verificar_picklist.id} coletado',qtd=verificar_picklist.quantidade,data=data,item=product,user=user)
            return st.success(F"O mercado {verificar_picklist.id_faturamento} foi concluido com sucesso")
        else:
            verificar_picklist.qtd_coletada += qtd_coletada
            session.commit()
            if session.query(Picklist).filter(Picklist.id_faturamento == verificar.id,Picklist.produto == verificar.produto,Picklist.data == verificar.data,Picklist.nota == verificar.numero_da_nota,Picklist.status == verificar.status).first().quantidade == session.query(Picklist).filter(Picklist.id_faturamento == verificar.id,Picklist.produto == verificar.produto,Picklist.data == verificar.data,Picklist.nota == verificar.numero_da_nota,Picklist.status == verificar.status).first().qtd_coletada:
                session.query(Picklist).filter(Picklist.id_faturamento == verificar.id,Picklist.produto == verificar.produto,Picklist.data == verificar.data,Picklist.nota == verificar.numero_da_nota,Picklist.status == verificar.status).first().status = True
                session.commit()
                add_history(action=f'Mercado {verificar_picklist.id} coletado',qtd=verificar_picklist.quantidade,data=data,item=product,user=user)
                return st.success(F"O mercado {verificar_picklist.id_faturamento} foi concluido com sucesso")
            else:
                return st.info(F"Ainda resta {verificar_picklist.quantidade - verificar_picklist.qtd_coletada} para concluir a coleta")
    else:
        novo_mercado = Picklist(usuario=user,produto=verificar.produto,quantidade=verificar.quantidade,nota=verificar.numero_da_nota,status=False,data=verificar.data,endereco=verificar.posicao,id_faturamento=verificar.id,qtd_coletada=1)
        session.add(novo_mercado)
        session.commit()
        if novo_mercado.qtd_coletada == novo_mercado.quantidade:
            novo_mercado.status = True
            session.commit()
            add_history(action=f'Mercado {novo_mercado.id} coletado',qtd=novo_mercado.quantidade,data=data,item=product,user=user)
            return st.success(F"O mercado {novo_mercado.id_faturamento} foi concluido com sucesso")

def separation(listaa):
    lista = []
    lista_ok = []
    lista_descarte = session.query(Separacao.id_mercado).filter(Separacao.status == True,Separacao.data == str(date.today())).all()
    for item in listaa:
        try:
            mercado  = session.query(Picklist).filter(Picklist.nota == item,Picklist.status == True).all()
            separacao = session.query(Separacao.nota,Separacao.produto).filter(Separacao.data == str(date.today()),Separacao.status==True).all()
            for mercados in mercado:
                if (mercados.nota,mercados.produto) in separacao:
                    pass
                else:
                    lista.append(mercados)
        except:
            pass
    return lista
        
def verify_if_billing_done(id_pickinglist):
    status_picking = session.query(Picklist).filter(Picklist.nota== id_pickinglist.nota,Picklist.produto == id_pickinglist.produto).first().status
    if status_picking == True:
        faturamento = session.query(Faturamento).filter(Faturamento.numero_da_nota == id_pickinglist.nota,Faturamento.data == str(date.today()),Faturamento.produto == id_pickinglist.produto).first()
        faturamento.status = True
        session.commit()   
        return st.success(f"Faturamento {faturamento.id} concluido com sucesso") 

def separate(product,data,note_number,user,qtd_coletada):
    try:
        try:
            verificar_separacao = session.query(Separacao).filter(Separacao.produto == product,Separacao.nota == note_number,Separacao.data == data).first()
        except:
            verificar_separacao = session.query(Separacao).filter(Separacao.produto == read_ean(product)[0],Separacao.nota == note_number,Separacao.data == data).first()
        if verificar_separacao.quantidade == verificar_separacao.qtd_coletada:
            verificar_separacao.status = True
            session.commit()
            verify_if_billing_done(session.query(Separacao).filter(Separacao.status == True,Separacao.nota == note_number,Separacao.data == str(date.today()),Separacao.produto == product).first())
            add_history(action=f"Separação e conclusão de Faturamento {session.query(Picklist).filter(Picklist.nota == verificar_separacao.nota,Picklist.data == str(date.today()),Picklist.id == verificar_separacao.id_mercado).first().id_faturamento}",qtd=session.query(Picklist).filter(Picklist.nota == verificar_separacao.nota,Picklist.data == str(date.today()),Picklist.id == verificar_separacao.id_mercado).first().quantidade,data=data,item=product,user=user)
            return st.success(f"Separação {verificar_separacao.id} concluida com sucesso")
        else: 
            session.query(Separacao).filter(Separacao.produto == product,Separacao.nota == note_number,Separacao.data == data).first().qtd_coletada += qtd_coletada
            session.commit()
            if verificar_separacao.quantidade == verificar_separacao.qtd_coletada:
                verificar_separacao.status = True
                session.commit()
                add_history(action=f"Separação e conclusão de Faturamento {session.query(Picklist).filter(Picklist.nota == verificar_separacao.nota,Picklist.data == str(date.today()),Picklist.id == verificar_separacao.id_mercado).first().id_faturamento}",qtd=session.query(Picklist).filter(Picklist.nota == verificar_separacao.nota,Picklist.data == str(date.today()),Picklist.id == verificar_separacao.id_mercado).first().quantidade,data=data,item=product,user=user)
                verify_if_billing_done(session.query(Separacao).filter(Separacao.status == True,Separacao.nota == note_number,Separacao.data == str(date.today()),Separacao.produto == product).first())
                return st.success(f"Separação {verificar_separacao.id} concluida com sucesso")
    except:
        try:
            product = product
        except:
            product = read_ean(product)[0]
        item_separado = Separacao(
                                produto=product,
                                id_mercado=session.query(Picklist).filter(Picklist.nota == note_number,Picklist.produto==product).first().id_faturamento,
                                qtd_coletada=qtd_coletada,
                                quantidade=session.query(Picklist).filter(Picklist.nota == note_number,Picklist.produto==product).first().quantidade,
                                data = str(date.today()),
                                endereco=session.query(Picklist).filter(Picklist.nota == note_number,Picklist.produto==product).first().endereco,
                                status=False,
                                status_mercado=session.query(Picklist).filter(Picklist.nota == note_number,Picklist.produto==product).first().status,
                                usuario=user,
                                nota=note_number
                            )
        session.add(item_separado)
        session.commit()
        if item_separado.quantidade == item_separado.qtd_coletada:
            item_separado.status = True
            session.commit()
            add_history(action=f"Separação e conclusão do faturamento {session.query(Picklist).filter(Picklist.nota == note_number,Picklist.data == str(date.today())).first().id_faturamento}",qtd=session.query(Picklist).filter(Picklist.nota == note_number,Picklist.data == str(date.today())).first().quantidade,data=data,item=product,user=user)
            verify_if_billing_done(session.query(Separacao).filter(Separacao.status == True,Separacao.nota == note_number,Separacao.data == str(date.today()),Separacao.produto == product).first())
            return st.success(f"Separação {item_separado.id} concluida com sucesso")

def create_itens_relations(data,transp,user):
    lista = []
    total_valor = 0
    total_peso = 0
    total_volumes = 0
    verificar_transps = session.query(Faturamento).filter(Faturamento.data == data,Faturamento.transportadora == transp,Faturamento.status == True).all()
    for i,item in enumerate(verificar_transps):
        valor = session.query(Produtos).filter(Produtos.codigo == item.produto).first().preco
        peso = session.query(Produtos).filter(Produtos.codigo == item.produto).first().peso
        total_peso += peso*item.quantidade
        total_valor += valor*item.quantidade
        total_volumes += item.quantidade
        infos = pd.DataFrame({
            'volumes':item.quantidade,
            'Cliente':item.cliente,
            'Data de Emissão da nota': item.date_emissao,
            'Transportadora':item.transportadora,
            'Nota':item.numero_da_nota
        },index=[i])
        lista.append(infos)
    add_history(action=f"Criação de Romaneio para tranportadora {transp}",qtd=1,data=data,item='romaneio',user=user)
    return st.table(pd.concat(lista,ignore_index=True)),total_peso,total_valor,total_volumes

def create_itens_relations_for_item(data,lista,user):
    listagem = []
    total_valor = 0
    total_peso = 0
    total_volumes = 0
    for i,item in enumerate(lista):
        verificar_items = session.query(Faturamento).filter(Faturamento.data == data,Faturamento.status == True,Faturamento.numero_da_nota == item).all()
    for i,espec in enumerate(verificar_items):
        valor = session.query(Produtos).filter(Produtos.codigo == espec.produto).first().preco
        peso = session.query(Produtos).filter(Produtos.codigo ==espec.produto).first().peso
        total_peso += peso*espec.quantidade
        total_valor += valor*espec.quantidade
        total_volumes +=espec.quantidade
        infos = pd.DataFrame({
            'volumes':total_volumes,
            'Cliente':espec.cliente,
            'Data de Emissão da nota': espec.date_emissao,
            'Transportadora':espec.transportadora,
            'Nota':espec.numero_da_nota
        },index=[i])
        listagem.append(infos)
    add_history(action=f"Criação de Romaneio para tranportadora",qtd=1,data=data,item='romaneio',user=user)    
    return st.table(pd.concat(listagem,ignore_index=True)),total_peso,total_valor,total_volumes

def query_and_register_ean(code,ean):
    try:
        produto = session.query(Produtos).filter(Produtos.codigo == code).first()
        if session.query(EansProdutos).filter(EansProdutos.produto == code).first():
            return st.error(f"O item {code} já está com as informações preenchidas")
        session.add(EansProdutos(codigo_ean=ean,produto=produto.codigo))
        session.commit()
        return st.success(f"O item {code} teve seu código ean cadastrado com sucesso")
    except:
        return st.error(f"O item {code} não está cadastrado")
    
def query_and_update_ean(code,ean):
    try:
        elemento = session.query(Produtos).filter(Produtos.codigo == code).first()
        if elemento:
            produto = session.query(EansProdutos).filter(EansProdutos.produto == code).first()
            produto.codigo_ean = ean
            session.commit()
    except:
        return st.error(f"O item {code} não está cadastrado")
    
def assistant():
    if 'selected_option' in st.session_state:
            Usuario_logado = st.session_state.selected_option
         
    carregar = st.toggle('Carregar arquivo')
    
    if carregar:
        uploaded_files = st.file_uploader("Seleção", type=['xlsx'], accept_multiple_files=True,help='Insira seus arquivos excel aqui')
    texto_estoque = '' 
    texto_usuarios = ''
    texto_historico = ''
    texto_romaneios =''
    texto_faturamento = ''
    texto_picklist = ''
    texto_separacao = ''
    texto_recebimento = ''
    texto_produtos = ''
    texto_veiculos = ''
    texto_entregas = ''

    estoque = session.query(Estoque).all()
    faturamento = session.query(Faturamento).all()
    picklist = session.query(Picklist).all()
    separacao = session.query(Separacao).all()
    romaneios = session.query(Romaneios).all()
    historico = session.query(Historico).all()
    usuarios = session.query(Usuarios).all()
    recebimento = session.query(Recebimento).all()
    produtos = session.query(Produtos).all()
    veiculos = session.query(Veiculos).all()
    entregas = session.query(Entregas).all()

    for item in list(set(estoque)):
        texto_estoque += f'produto:{item.item}, endereço: {item.endereco} , quantidade:{item.quantidade}\n'

    for item in list(set(faturamento)):
        texto_faturamento += f'produto:{item.produto}, endereço: {item.posicao} , quantidade:{item.quantidade},numero da nota: {item.numero_da_nota}, cliente: {item.cliente}, transportadora:{item.transportadora}, data: {item.data}\n'

    for item in list(set(picklist)):
        texto_picklist += f'produto:{item.produto}, endereço: {item.endereco} , quantidade:{item.quantidade},numero da nota: {item.nota}, data: {item.data}\n'

    for item in list(set(separacao)):
        texto_separacao +=  f'produto:{item.produto}, endereço: {item.endereco} , quantidade:{item.quantidade},numero da nota: {item.nota}, data: {item.data}\n'

    for item in list(set(romaneios)):
        texto_romaneios += f'romaneio:{item.romaneio}, data: {item.data} , usuario:{item.usuario}\n'

    for item in list(set(usuarios)):
        texto_usuarios += f'Usuário:{item.usuario}\n'

    for item in list(set(recebimento)):
        texto_recebimento += f'produto:{item.produto} , quantidade:{item.quantidade}\n,data{item.data}'

    for item in list(set(produtos)):
        texto_produtos += f'produto:{item.codigo} , valor: {item.preco}R$ ,peso{item.peso} Kg ,descrição:{item.nome}\n'

    for item in list(set(historico)):
        texto_historico += f'Evento:{item.evento} , quantidade:{item.quantidade},data{item.data},usuário:{item.usuario},item:{item.item}\n'
        
    for item in list(set(veiculos)):
        texto_veiculos += f'Modelo:{item.modelo} , Marca:{item.marca}, Autonomia: {item.autonomia}\n'
        
    for item in list(set(entregas)):
        texto_entregas += f'Nota:{item.nota} , Cliente:{item.cliente},data{item.data},Veiculo:{item.veiculo}\n'    
        



    texto_final = F"""
            Faturamento: {texto_faturamento}\n 
            Estoque: {texto_estoque}\n
            Processo de pré separação: {texto_picklist} \n
            Separação de itens: {texto_separacao}\n
            Romaneios: {texto_romaneios}\n
            Usuários: {texto_usuarios}\n
            Recebimento: {texto_recebimento}\n
            Histórico: {texto_historico}\n
            Produtos: {texto_produtos}\n
            Entregas: {texto_entregas}\n
            Veículos: {texto_veiculos}\n
            Intruções de uso desse app:
            1.Vá para cadastro de produtos, e preencha os campos para que o cadastro seja finalizado
            2. Em Seguida, siga para Recebimento. Na caixa de seleção, 
                escolha o item que você separou, 
                ou os que estão disponíveis, e faço o recebimento de uma quantidade de sua preferência
            3. Com o item já recebido, vá para a aba de Transferência. Nesse espaço, para trazer os itens,
                selecione a opção "Recebimento" em "origem". Após isso, Insira, no campo de destino, um endereço 
                no seguinte
                formato: 0>0n<08-0>00n<20-0>0n<05. Na aba seguinte, escolha o item, e a quantidade.
             4.Agora, você já pode ir para aba de faturamento, e realizar o faturamento manual. Assim, 
                preencha todos os
                campos e, ao fim, o faturamento terá se iniciado. obs: Caso você queira realizar o faturamento 
                com arquivos de 
                notas  fiscais 
                clique no icone maior
                a primeira ação que ele fará é, automaticamente, cadastrar os itens da nota. Depois, 
                você deve realizar o 
                processo de
                recebimento e transferência.
                Quando concluir, é só retornar no icone e reselecionar as notas. Isso fará com que o 
                Faturamento se inicie.   
            5. Entre na aba de Pickinglist. Para coletar os itens, observe sua localização e quantidade. 
                A coleta se da na ação
                de inserir o código do produto no campo. Se houver apenas 1 item, o processo se encerrará. 
                Se não, 
                o mostrador irá mudar 
                até que você colete
                a quantidade da nota. Se completar esse campo, vá para Separação. Nessa aba, 
                é o mesmo procedimento porém, 
                além do item
                deve-se inserir a posição dele
                no estoque para contabilizar uma coleta 
            6.Pronto, seu faturamento acabou. Agora, vá para Rotas e depois em entregas. Nessa aba selecione 
                a data de hoje, a 
                transportadora e  um carro de tranporte.
                Após isso, serão exibidos todos os pedidos faturados e separados. Para entregar, 
                é só ativar a chave. 
                Nesse caso,você assume o papel do entregador. Ops, esqueci. O carro utilizado também
                deve ser cadastrado. Para isso, vá para a aba "Frota" e lá, preencha os dados do veículo. Eles são 
                importantes 
                para as informações 
                vindas da entrega. 
            """
    cola,colb = st.columns(2)
    with cola:
        pergunta = st.chat_input(placeholder='Faça sua pergunta')
    with colb:
        try:
            if uploaded_files:
                texto = ''
                for item in uploaded_files:
                    tabela = treat_table(item)
                    texto += f'{tabela}\n'
                treat_audio(None,texto)
        except:
             treat_audio(texto_final,None)
    if pergunta:
       try:
            texto = ''
            for item in uploaded_files:
                tabela = treat_table(item)
                texto += f'{tabela}\n'
            humano = st.chat_message('human')
            humano.write(pergunta)
            assistente = st.chat_message('assistant')
            assistente.write(analisar(f"Por favor observe o arquivo ou arquivos que você está recebendo e baseando-se nele ou neles, faça o que se pede.Além disso você também é o assistente de um aplicativo de estoque, de onde vem e para onde vaõ todas essas informações. Sendo assim, além de vizualizar os dados, estou te enviando um texto com uma orientação de uso do app, para que se alguém pergunte, você a ajude a se orientar no aplicativo. Responda se referindo ao indivíduo {Usuario_logado}: {pergunta}",str(texto)))
       except:
            humano = st.chat_message('human')
            humano.write(pergunta)
            assistente = st.chat_message('assistant')
            assistente.write(analisar(
                f"""Você é um analista de dados em larga escala e sua missão é me ajudar a solucionar problemas relacionados ao meu estoque. Estou lhe enviando uma grande quantidade de dados referentes a diferentes aspectos e processo do meu Estoque como desde o faturamento de pedidos e recebimento de mercadorias até a expedição. Essas informações estão em formato de listas.Apenas uma observação, o termo mercado,se aparecer, se refere ao processo de pré-separação.Além disso, quanto há mercado e separação de um item ou de vários itens de mesma nota, considere o faturamento completo sendo o produto faturado e quantidade faturada a quantidade constante tanto no picklist ou mercado, quanto na separação.Porém, um item só pode ser faturado 1 vez.Caso exista mais de um faturamento para um mesmo item de uma mesma nota, considere apenas um faturamento
                Então você deve interpretar o que cada lista mostra de informação e responder a essa questão.Além disso você também é o assistente de um aplicativo de estoque, de onde vem e para onde vaõ todas essas informações. Sendo assim, além de vizualizar os dados, estou te enviando um texto com uma orientação de uso do app, para que se alguém pergunte, você a ajude a se orientar no aplicativo. Responda a esta pergunta se referindo ao índividuo {Usuario_logado}: {pergunta}"""
                ,str(texto_final)))

@st.cache_data
def convert_df_to_excel(df):
            output = BytesIO()
            with pd.ExcelWriter(output, engine='openpyxl') as writer:
                df.to_excel(writer, index=False, sheet_name='Sheet1')
            processed_data = output.getvalue()
            return processed_data

def download_button(df,nome):
    download = st.download_button(
                                    label=f"Faça o download do {nome} no formato Excel",
                                    data=convert_df_to_excel(df),
                                    file_name=f"Pesquisa do produto {nome}.xlsx",
                                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                                    )

def donwload_storage():
    try:
        list = []
        estoque = session.query(Estoque).all()    
        for i,item in enumerate(estoque):
            texto_estoque = {'produto':{item.item}, 'endereço': {item.endereco} , 'quantidade':{item.quantidade}}
            list.append(pd.DataFrame(texto_estoque,index=[i]))
        download_button(pd.concat(list),f'Estoque {date.today()}') 
    except:
        pass
    
def donwload_billing():
    try:
        list = []
        billing = session.query(Faturamento).all()    
        for i,item in enumerate(billing):
            texto_billing = {f'produto':item.produto, 'endereço': item.posicao , 'quantidade':item.quantidade,'numero da nota': item.numero_da_nota, 'cliente': item.cliente, 'transportadora':item.transportadora, 'data': item.data}
            list.append(pd.DataFrame(texto_billing,index=[i]))
        download_button(pd.concat(list),f'Faturamento {date.today()}') 
    except:
        pass
    
def donwload_picklist():
    try:
        list = []
        picklist = session.query(Picklist).all()    
        for i,item in enumerate(picklist):
            texto_picklist = {'produto':item.produto, 'endereço': item.endereco , 'quantidade':item.quantidade,'numero da nota': item.nota, 'data': item.data}
            list.append(pd.DataFrame(texto_picklist,index=[i]))
        download_button(pd.concat(list),f'Picklist {date.today()}')       
    except:
        pass
    
def donwload_separation():
    try:
        list = []
        separacao = session.query(Separacao).all()    
        for i,item in enumerate(separacao):
            texto_separaco = {'produto':item.produto, 'endereço': item.endereco , 'quantidade':item.quantidade,'numero da nota': item.nota, 'data': item.data}
            list.append(pd.DataFrame(texto_separacao,index=[i]))
        download_button(pd.concat(list),f'Separações {date.today()}') 
    except:
        pass
def donwload_ralation():
    try:
        list = []
        romaneios = session.query(Romaneios).all()    
        for i,item in enumerate(romaneios):
            texto_romaneios = {'romaneio':item.romaneio, 'data': item.data , 'usuario':item.usuario}
            list.append(pd.DataFrame(texto_romaneios,index=[i]))
        download_button(pd.concat(list),f'Romaneios {date.today()}') 
    except:
        pass
    
def donwload_history():
    try:
        list = []
        historico = session.query(Historico).all()    
        for i,item in enumerate(historico):
            texto_historico = {'Evento':item.evento, 'quantidade':item.quantidade,'data':item.data,'usuário':item.usuario,'item':item.item}
            list.append(pd.DataFrame(texto_historico,index=[i]))
        download_button(pd.concat(list),f'Histórico {date.today()}') 
    except:
        pass
    
def donwload_users():
    try:
        list = []
        usuarios = session.query(Usuarios).all()    
        for i,item in enumerate(usuarios):
            texto_estoque = {'Usuário':item.usuario}
            list.append(pd.DataFrame(texto_usuarios,index=[i]))
        download_button(pd.concat(list),f'Usuários {date.today()}') 
    except:
        pass
    
def donwload_receiving():
    try:
        list = []
        recebimento = session.query(Recebimento).all()    
        for i,item in enumerate(recebimento):
            texto_recebimento = {'produto':item.produto , 'quantidade':item.quantidade,'data':item.data}
            list.append(pd.DataFrame(texto_recebimento,index=[i]))
        download_button(pd.concat(list),f'Recebimento {date.today()}') 
    except:
        pass
    
def donwload_product():
    try:
        list = []
        produtos = session.query(Produtos).all()    
        for i,item in enumerate(produtos):
            texto_produtos = {'produto':item.codigo , 'valor': item.preco ,'peso':item.peso  ,'descrição':item.nome}
            list.append(pd.DataFrame(texto_produtos,index=[i]))
        download_button(pd.concat(list),f'Produtos {date.today()}') 
    except:
        pass

def donwload_deliverys():
    try:
        list = []
        entregas = session.query(Entregas).all()    
        for i,item in enumerate(entregas):
            texto_entregas = {'Data':item.data , 'Cliente': item.cliente ,'Nota':item.nota  ,'Veículo':item.veiculo}
            list.append(pd.DataFrame(texto_entregas,index=[i]))
        download_button(pd.concat(list),f'Entregas {date.today()}') 
    except:
        pass

def calculate_distance(destiny,origem):
        texto = '' 
        url = 'https://maps.googleapis.com/maps/api/directions/json'
        params = {
                'origin': f'{origem}', 
                'destination': f'{destiny}', 
                'key': st.secrets['chave_api_googlemaps']
                }
        response = requests.get(url, params=params)
        if response.status_code == 200:
            data = response.json()
            route = data['routes']
            for step in route[0]['legs'][0]['steps']:
                text = step['html_instructions']
                texto += text
            distance = route[0]['legs'][0]['distance']['text']
            if 'km' in distance:
                distancia = float(distance.replace('km', '').replace(',', '.'))
            distancia = str(distance.replace('m','')).strip()
            duration = route[0]['legs'][0]['duration']['text'] 
            return texto,distancia,duration   
        else:
            st.error('erro')
def define_destiny_list(note):
        destinos = []
        origem = 'Itupeva,sp'
        for item in list(set(note)):
                    verificar = session.query(Faturamento).filter(Faturamento.numero_da_nota == item,Faturamento.status == True).first()
                    distancia = calculate_distance(verificar.destino,origem)
                    location = str(verificar.destino).split(',')
                    descricao = verificar.destino
                    nota = verificar.numero_da_nota
                    cliente = verificar.cliente
                    dict= {
                        'distancia':distancia[1],
                        'nota':nota,
                        'cliente':cliente,
                        'origem':'Itupeva,sp',
                        'descricao':descricao,
                        'tempo':distancia[2],
                        'rotas':distancia[0]        
                        }
                    if dict in destinos:
                        pass
                    else:
                        destinos.append(dict)
                    origem = verificar.destino
                    sleep(1)
        return sorted(destinos,key=lambda x:x['distancia'],reverse=True)
def route(list):
        origem = 'Itupeva,sp'
        lista = []
        for i,item in enumerate(list):
            dict = {
                f'Distância':item['distancia'],
                 'nota':item['nota'],
                 'cliente':item['cliente'],   
                 'descricao':item['descricao'],
                 'tempo': item['tempo'],
                 'rotas':str(item['rotas'])   
                }
            if dict in lista:
                pass
            else:
                lista.append(dict)
            origem = item['descricao']
            sleep(1)
        return lista
        
def build_google_map(list):

        base_url = f"https://www.google.com/maps/dir/Itupeva,sp/"
        final=base_url + '/'.join([str(f'{item['descricao']}').replace(' ','+') for item in list])
        return final,pd.concat([pd.DataFrame({'nota':elemento['nota'],'cliente':elemento['cliente'],'Distância em km':elemento['Distância'],'tempo em minutos':elemento['tempo']},index=[i]) for i,elemento in enumerate(list)]),list

def save_route(routes,data,transp):
        texto = ''
        for item in routes:
            text = item['rotas']
            texto += text
        try:
            existe = session.query(Rotas).filter(Rotas.transportadora == transp,Rotas.data == data).first()
            existe.rota = str(texto)
            existe.commit()
        except:
            session.add(Rotas(data==data,transp==transp,rota=str(texto)))
            session.commit()

def complete_delivery(data,transp):
        verificar = session.query(Entregas).filter(Entregas.data==data,Entregas.transportadora == transp,Entregas.status==True).all()
        verificar_car = session.query(Entregas).filter(Entregas.data==data,Entregas.transportadora == transp,Entregas.status==True).first().veiculo
        autonomia_itupeva = session.query(Veiculos).filter(Veiculos.modelo == verificar_car).first().autonomia
        distancia_a = calculate_distance(session.query(Faturamento).filter(Faturamento.status==True,Faturamento.numero_da_nota==verificar[0].nota).first().destino,'Itupeva,sp')[1]
        if ' k' in distancia_a:
                distancia_a = float(distancia_a.replace('k', '').replace(',', '.').strip()) 
        if len(list(set(verificar))) > int(1):
            origem = 'Itupeva,sp'
            gasto = 0
            distancia_per = 0
            distancia_per += distancia_a*2
            gasto += round(float((distancia_per/autonomia_itupeva)*5.50))
            qtd = 0
            lista = []
            for i,item in enumerate(list(set(verificar))):
                destino = session.query(Faturamento).filter(Faturamento.status==True,Faturamento.numero_da_nota == item.nota,Faturamento.data==item.data).first().destino
                distancia = calculate_distance(destino,origem)[1]
                if ' k' in distancia:
                    distancia = float(distancia.replace('k', '').replace(',', '.').strip()) 
                kml = session.query(Veiculos).filter(Veiculos.modelo==item.veiculo).first().autonomia
                dict={
                    'Cliente':item.cliente,
                    'Nota':item.nota,
                    'Produto':item.produto,
                    'distancia km':distancia,
                    'Valor': round(float((distancia/kml)*5.50))
                }
                gasto += round(float((distancia/kml)*5.50))
                distancia_per += distancia
                qtd += session.query(Faturamento).filter(Faturamento.status==True,Faturamento.numero_da_nota==item.nota).first().quantidade
                if dict in lista:
                    pass
                else:
                    lista.append(dict)
                origem = destino
            return pd.concat([pd.DataFrame(elemento,index=[i]) for i,elemento in enumerate(lista)]),gasto,distancia_per,qtd
        else:
            origem = 'Itupeva,sp'
            gasto = 0
            distancia_total = 0
            qtd = 0
            lista = []
            verificarr = session.query(Entregas).filter(Entregas.data==data,Entregas.transportadora == transp,Entregas.status==True).first()
            destinor = session.query(Faturamento).filter(Faturamento.status==True,Faturamento.numero_da_nota == verificarr.nota,Faturamento.data==verificarr.data).first().destino
            verificarr_car = session.query(Entregas).filter(Entregas.data==data,Entregas.transportadora == transp,Entregas.status==True).first().veiculo
            autonomia = session.query(Veiculos).filter(Veiculos.modelo == verificarr_car).first().autonomia
            distancia = calculate_distance(destinor,'Itupeva,sp')[1]
            if ' k' in distancia:
                distancia = float(distancia.replace('k', '').replace(',', '.').strip()) 
            dict={
                    'Cliente':verificarr.cliente,
                    'Nota':verificarr.nota,
                    'Produto':verificarr.produto,
                    'distancia km':distancia*2,
                    'Valor': round(float((distancia/autonomia)*5.50))
                }
            gasto = round(float((distancia*2/autonomia)*5.50))
            distancia_total = distancia
            qtd = session.query(Faturamento).filter(Faturamento.status==True,Faturamento.numero_da_nota==verificarr.nota).first().quantidade
            if dict in lista:
                    pass
            else:
                    lista.append(dict)
            return pd.concat([pd.DataFrame(elemento,index=[i]) for i,elemento in enumerate(lista)]),gasto,distancia_total,qtd


def deliver(car,product,qtd,data,transp,note,client,user):
    try:
        verificar = session.query(Entregas).filter(Entregas.data == data,Entregas.nota == note, Entregas.cliente == client,Entrega.status == True).firts()
        return st.info(f'A entrega do cliente {client} já foi realizada')
    except:
        session.add(Entregas(veiculo=car,produto=product,quantidade=qtd,data=data,transportadora=transp,cliente=client,status=True,nota=note))
        session.commit()
        add_history(action=f"Entrega realizada para o cliente: {client}",data=str(date.today()),qtd=qtd,item=product,user=user)
        return st.success(f'Entrega do cliente {client} realizada com sucesso')   

def load_delivery(notes,data,veiculo,user):
    contador_nao = 0
    contador_sim = 0
    for i,item in enumerate(list(set(notes))):
            verificar = session.query(Faturamento).filter(Faturamento.numero_da_nota == item,Faturamento.data == data,Faturamento.status == True).first()
            if verificar:
                if session.query(Entregas).filter(Entregas.data == verificar.data,Entregas.cliente == verificar.cliente,Entregas.status==True).first():
                    return st.warning(f'A entrega do cliente :{session.query(Entregas).filter(Entregas.data == verificar.data,Entregas.cliente == verificar.cliente,Entregas.status==True).first().cliente} já foi realizada')
                else:
                    st.info(f'''
                    Cliente:{verificar.cliente}\n
                    Nota:{verificar.numero_da_nota}\n
                    Quantidade: {verificar.quantidade}\n
                    ''')
                    contador_nao += 1 
                    completa = st.toggle('Entrega Completa',key=i)
                    if completa:
                        contador_sim += 1 
                        deliver(car=veiculo,product=verificar.produto,qtd=verificar.quantidade,client=verificar.cliente,note=verificar.numero_da_nota,transp=verificar.transportadora,data=data,user=user)
                    st.divider()
    return contador_nao,contador_sim
    
def complete_desciption(car):
        
        verificar = session.query(Entregas).filter(Entregas.veiculo == car,Entregas.status==True).all()
        verificar_car = session.query(Veiculos).filter(Veiculos.modelo == car).first().autonomia
        distancia_a = calculate_distance(session.query(Faturamento).filter(Faturamento.status==True,Faturamento.numero_da_nota==verificar[0].nota).first().destino,'Itupeva,sp')[1]
        if ' k' in distancia_a:
                distancia_a = float(distancia_a.replace('k', '').replace(',', '.').strip()) 
        if len(list(set(verificar))) > int(1):
            origem = 'Itupeva,sp'
            gasto = 0
            distancia_per = 0
            qtd = 0
            lista = []
            distancia_per += 2*distancia_a
            gasto += round(float((distancia_per/verificar_car)*5.50))
            for i,item in enumerate(list(set(verificar))):
                destino = session.query(Faturamento).filter(Faturamento.status==True,Faturamento.numero_da_nota == item.nota).first().destino
                distancia = calculate_distance(destino,origem)[1]
                if ' k' in distancia:
                    distancia = float(distancia.replace('k', '').replace(',', '.').strip())  
                kml = session.query(Veiculos).filter(Veiculos.modelo==item.veiculo).first().autonomia
                dict={
                    'Cliente':item.cliente,
                    'Nota':item.nota,
                    'Produto':item.produto,
                    'Quantidade':item.quantidade,
                    'Gasto em R$': round(float((float(distancia)/float(kml))*5.50)),
                    'Distância percorrida':distancia
                }
                gasto += round(float((distancia/kml)*5.50))
                distancia_per += distancia
                qtd += item.quantidade
                if dict in lista:
                    pass
                else:
                    lista.append(dict)
                origem =  destino
            return gasto,distancia_per,qtd
        else:
            origem = 'Itupeva,sp'
            gasto = 0
            distancia_total = 0
            qtd = 0
            lista = []
            verificarr = session.query(Entregas).filter(Entregas.veiculo == car,Entregas.status==True).first()
            destinor = session.query(Faturamento).filter(Faturamento.status==True,Faturamento.numero_da_nota == verificarr.nota,Faturamento.data==verificarr.data).first().destino
            verificarr_car = session.query(Entregas).filter(Entregas.data==verificarr.data,Entregas.status==True).first().veiculo
            autonomia = session.query(Veiculos).filter(Veiculos.modelo == verificarr_car).first().autonomia
            distancia = calculate_distance(destinor,'Itupeva,sp')[1]
            if ' k' in distancia:
                distancia = float(distancia.replace('k', '').replace(',', '.').strip()) 
            dict={
                    'Cliente':verificarr.cliente,
                    'Nota':verificarr.nota,
                    'Produto':verificarr.produto,
                    'distancia km':distancia*2,
                    'Valor': round(float((distancia/autonomia)*5.50))
                }
            gasto = round(float((distancia*2/autonomia)*5.50))
            distancia_total = distancia*2
            qtd = session.query(Faturamento).filter(Faturamento.status==True,Faturamento.numero_da_nota==verificarr.nota).first().quantidade
            if dict in lista:
                    pass
            else:
                    lista.append(dict)
            return gasto,distancia_total,qtd
    
def manual_billing(code,transp,client,user,qtd,number,destino):
                    verificar = session.query(Produtos).filter(Produtos.codigo == code).first()
                    if verificar:
                        posicao = session.query(Estoque).filter(Estoque.item == verificar.codigo,Estoque.quantidade >= qtd).first().endereco
                        if posicao:
                            if session.query(Estoque).filter(Estoque.item == verificar.codigo,Estoque.endereco == posicao).first().quantidade >= qtd:
                                session.query(Estoque).filter(Estoque.item == verificar.codigo,Estoque.endereco == posicao).first().quantidade -= qtd
                                session.commit()
                                session.add(Faturamento(produto=verificar.codigo,usuario=user,quantidade=qtd,numero_da_nota=number,data=str(date.today()),status=False,transportadora=transp,cliente=client,data_emissao=str(date.today()),posicao=posicao,destino=destino))
                                session.commit()
                                add_history(action=f"Faturamento manual",qtd=qtd,data=str(date.today()),item=code,user=user)
                                verify_if_still_exists(code=code,adress=posicao)
                                session.commit()
                                st.success(f"O Item {code}, foi faturado com sucesso e já está disponível para ser coletado")
                        else:
                            st.error(f'O item: {codigo} não possúi quantidade suficiente em estoque para ser faturado')
                    else:
                        st.error(f'O Código: {code} não está cadastrado')

