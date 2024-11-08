from sqlalchemy import create_engine, Column, Integer, String, Float,ForeignKey,Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import streamlit as st 
from datetime import date
Base = declarative_base()

class Produtos(Base):
    __tablename__ = 'produtos'

    id = Column("id",Integer, primary_key=True,autoincrement=True)
    nome = Column("nome",String)
    codigo = Column("codigo",String)
    preco = Column("preco",Float)
    peso = Column("peso",Float)

    def __init__(self,nome,codigo,preco,peso):
        self.nome = nome
        self.codigo = codigo
        self.preco = preco 
        self.peso = peso

class Estoque(Base):
    __tablename__ = 'estoque'

    id = Column("id_endereco",Integer,primary_key=True,autoincrement=True)
    item = Column("item",ForeignKey('produtos.id'))
    endereco = Column("endereco",String)
    quantidade =  Column('usuario',Float)

    def __init__(self,item,endereco,quantidade):
        self.item = item
        self.endereco = endereco
        self.quantidade = quantidade

class Usuarios(Base):
    __tablename__ = 'usuarios'

    id = Column("id",Integer,primary_key=True,autoincrement=True)
    usuario = Column("usuario",String)
    senha =  Column('senha',String)

    def __init__(self,usuario,senha):
        self.usuario = usuario
        self.senha = senha
class Recebimento(Base):
    __tablename__ = 'recebimento'

    id = Column("id",Integer,primary_key=True,autoincrement=True)
    produto = Column("produto",ForeignKey('produtos.id'))
    quantidade =  Column('quantidade',Float)
    data = Column("data",String)

    def __init__(self,produto,quantidade,data):
        self.produto = produto
        self.quantidade = quantidade
        self.data = data
class Historico(Base):
    __tablename__ = 'historico'

    id = Column("id",Integer,primary_key=True,autoincrement=True)
    usuario = Column("usuario",ForeignKey('usuarios.id'))
    evento = Column("evento",String)
    data = Column("data",String)
    quantidade = Column("quantidade",Float)
    item = Column("item",ForeignKey("produtos.id"))

    def __init__(self,evento,quantidade,data,item,usuario):
        self.evento = evento
        self.quantidade = quantidade
        self.data = data
        self.item = item
        self.usuario = usuario

class Faturamento(Base):
    __tablename__ = 'faturamento'

    id = Column("id",Integer,primary_key=True,autoincrement=True)
    usuario = Column('usuario',ForeignKey('usuarios.id'))
    produto = Column('produto',ForeignKey('produtos.id'))
    quantidade = Column('quantidade',Integer)
    numero_da_nota = Column('numero da nota',Integer)
    cliente = Column('cliente',String)
    transportadora = Column('transportadora',String)
    status = Column('concluido',Boolean)
    data = Column('data',String)
    date_emissao = Column('data de emissão',String)
    posicao = Column('posição',ForeignKey('estoque.endereco'))

    def __init__(self,usuario,produto,quantidade,numero_da_nota,cliente,status,data,transportadora,data_emissao,posicao):
        self.produto = produto
        self.quantidade = quantidade
        self.data = data
        self.numero_da_nota = numero_da_nota
        self.usuario = usuario
        self.cliente = cliente
        self.status = status
        self.transportadora = transportadora
        self.date_emissao = data_emissao
        self.posicao= posicao

class Picklist(Base):
    __tablename__ = 'picklist'

    id = Column("id",Integer,primary_key=True,autoincrement=True)
    id_faturamento  = Column("id faturamento",ForeignKey('faturamento.id'))
    data = Column('data',ForeignKey('faturamento.data'))
    nota = Column('nota',ForeignKey('faturamento.numero da nota'))
    produto = Column('produto',ForeignKey('faturamento.produto'))
    quantidade = Column('quantidade',Float)
    endereco = Column('posição',ForeignKey('faturamento.posição'))
    status = Column('status picklist',Boolean)
    usuario = Column('usuario',ForeignKey('usuarios.id'))
    qtd_coletada = Column('quantidade coletada',Integer)
    

    def __init__(self,usuario,produto,quantidade,nota,status,data,endereco,id_faturamento,qtd_coletada):
        self.produto = produto
        self.quantidade = quantidade
        self.data = data
        self.nota = nota
        self.usuario = usuario
        self.status = status
        self.endereco = endereco
        self.id_faturamento = id_faturamento
        self.qtd_coletada = qtd_coletada
        
class Separacao(Base):
    __tablename__ = 'Separação'

    id = Column("id",Integer,primary_key=True,autoincrement=True)
    id_mercado  = Column("id mercado",ForeignKey('picklist.id'))
    data = Column('data',ForeignKey('faturamento.data'))
    nota = Column('nota',ForeignKey('faturamento.numero da nota'))
    produto = Column('produto',ForeignKey('faturamento.produto'))
    quantidade = Column('quantidade',Float)
    endereco = Column('posição',ForeignKey('faturamento.posição'))
    status = Column('status picklist',Boolean)
    usuario = Column('usuario',ForeignKey('usuarios.id'))
    qtd_coletada = Column('quantidade coletada',Integer)
    status_mercado = Column('status do mercado',ForeignKey('picklist.id'))
    

    def __init__(self,usuario,produto,quantidade,nota,status,data,endereco,id_mercado,qtd_coletada,status_mercado):
        self.produto = produto
        self.quantidade = quantidade
        self.data = data
        self.nota = nota
        self.usuario = usuario
        self.status = status
        self.endereco = endereco
        self.id_mercado = id_mercado
        self.qtd_coletada = qtd_coletada
        self.status_mercado = status_mercado
        
class Romaneios(Base):
    __tablename__ = 'Romaneios'

    id = Column('id',Integer,primary_key=True,autoincrement=True)
    romaneio = Column('Romaneios',String)
    usuario = Column('Usuário',ForeignKey('usuarios.id'))
    data = Column('Data',String)

    def __init__(self,romaneio,data,usuario):
        self.romaneio = romaneio 
        self.usuario = usuario 
        self.data = data

class EansProdutos(Base):
    __tablename__ = 'EansProdutos'

    id = Column('id',Integer,primary_key=True,autoincrement=True,)
    codigo_ean = Column('Código ean',String)
    produto = Column('Código do produto',ForeignKey('produtos.id'))

    def __init__(self,codigo_ean,produto):
        self.codigo_ean = codigo_ean
        self.produto = produto

engine = create_engine(st.secrets(['database']))
base =Base.metadata.create_all(engine)
