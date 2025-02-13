#Importações das Biblioteca
import streamlit as st
from firebase_admin import firestore

db = firestore.client()
st.set_page_config(
    page_title="Projecto",
    page_icon="🧊",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://www.extremelycoolapp.com/help',
        'Report a bug': "https://www.extremelycoolapp.com/bug",
        'About': "# This is a header. This is an *extremely* cool app!"
    }
)

if "user" in st.session_state:
    user = st.session_state.user["email"]
    def criar_div(titulo, texto,tempo):
        st.markdown(
            f"""
            <div style="
                background-color: #262730;
                padding: 10px 10px 4px;
                border-radius: 10px;
                margin: 10px 0;
            ">
                <h2 style="color: white;">{titulo}</h2>
                <p style="color: white;">{texto}</p>
                <p style="color: #717275;text-align:right">{tempo}</p>
            </div>
            """,
            unsafe_allow_html=True
        )
    arquivo_ref = db.collection("arquivos")
    arquivo = arquivo_ref.stream()

    count = 0

    for arquivo in arquivo:
        arquivo_dict = arquivo.to_dict()
        criar_div(arquivo_dict["tipo"], arquivo_dict["texto"],arquivo_dict["tempo"])
        count+=1
    if count < 1:
        st.write("Nenhum arquivo encontrado")
else:
    st.switch_page("home.py")