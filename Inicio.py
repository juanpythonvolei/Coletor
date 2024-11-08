import streamlit as st
from views import *

image = st.image('https://logos-world.net/wp-content/uploads/2023/03/Thule-Logo.png')
st.markdown("""
    <style>
    .sidebar .sidebar-content {
        background-color: #FFA421;
        color: white; /* Cor do texto na barra lateral */
    }
    </style>
""", unsafe_allow_html=True)

st.markdown(
    """
    <style>
    body {
        background-color: #000000;
    }
    </style>
    """,
    unsafe_allow_html=True
)
st.markdown("""
    <style>
       [aria-expanded='true'] {
            display: none;
        }
    </style>
""", unsafe_allow_html=True)

css = """
<style>
.centered-image {
    display: block;
    margin: 0 auto;
}
</style>
"""
if 'selected_option' in st.session_state:
        st.session_state.selected_option = None

existe = st.popover("Já tenho uma conta")
novo = st.popover("Cadastrar novo usuário")
with existe:
    if existe:
        usuario = st.text_input(label="Usuário",placeholder="Insira seu usuário",key="login_usuairo")
        senha = st.text_input(label="Senha",placeholder="Insira sua senha",key='senha_usuario')
        if usuario and senha:
            login(usuario=usuario,senha=senha)
with novo:
    if novo:
        novo_usuario = st.text_input(label="Novo Usuário",placeholder="Insira um novo usuário",key="novo_usuario")
        nova_senha = st.text_input(label="Nova Senha",placeholder="Insira uma nova senha",key="senha_novo_usuario")
        if novo_usuario and nova_senha:
            add_new_user(novo_usuario,nova_senha)
