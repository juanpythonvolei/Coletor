import streamlit as st
from views import* 



image = st.image('https://img.freepik.com/vetores-gratis/modelo-de-logotipo-da-empresa-de-caminhoes_441059-258.jpg?w=996')
if 'selected_option' in st.session_state:
            st.title(f'Usuário logado: {st.session_state.selected_option}')
try:
  logado = st.session_state.selected_option
  assistant()
except:
  st.error('Você deve estar logado para acessar essa página')

