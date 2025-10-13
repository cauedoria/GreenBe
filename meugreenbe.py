import streamlit as st
import greenbe
import grafico

st.set_page_config(page_title='GreenBe - Produtos Naturais', layout='wide', page_icon='https://www.google.com/url?sa=i&url=https%3A%2F%2Fwww.flaticon.com%2Ffree-icon%2Forganic-product_3637233&psig=AOvVaw0avgNA6tVZZWMPdGf3mVO_&ust=1760447556079000&source=images&cd=vfe&opi=89978449&ved=0CBUQjRxqFwoTCNjLo6ugoZADFQAAAAAdAAAAABAE')

st.title('Dashboard - GreenBe')

abas = st.tabs(['Saída de estoque', 'Gráficos', 'Contato'])

with abas [0]:
    greenbe.mostrar()
with abas [1]:
    grafico.mostrar()
with abas [2]:
    st.header('Contato')
    st.write('Desenvolvido por Cauê Dória')
    st.write('Email: cauedoria99@gmail.com')