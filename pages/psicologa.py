#Importações das Biblioteca
import streamlit as st
from firebase_admin import firestore
from streamlit_autorefresh import st_autorefresh


#Configurações da Pagina
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


db = firestore.client()

if "user" in st.session_state:
    user = st.session_state.user["email"]
    st_autorefresh(interval=3000, key="chat_update")
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

    st.markdown(
        """
        <style>
        /* Estiliza os botões gerados pelo st.button */
        div.stButton > button {
            background-color: #262730;
            color: white;
            width:100%;
            padding: 30px 24px;
            border: none;
            border-radius: 8px;
            cursor: pointer;
            font-size: 16px;
            transition: background-color 0.3s ease;
        display: block;
                text-align: left;
            
        font-size: 24px;
        
        }
        div.stButton > button:hover {
            background-color: #262730;
            color: white;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    arquivo_ref = db.collection("mensagens")
    arquivo = arquivo_ref.stream()
    st.header("Todas as mensagens",divider=True)
    count = 0
    allemail = []
    alltext = []
    contar = 0
    for arquivo in arquivo:
        arquivo_dict = arquivo.to_dict()
    
        if not arquivo_dict["from"] in allemail and not "psicologa" in arquivo_dict["from"]:
            allemail.append(arquivo_dict["from"])
            alltext.append(arquivo_dict["texto"][:30])
            contar += 1
            if st.button(f"Anonimo {contar} - {arquivo_dict["texto"][:30]}....", key=arquivo_dict["from"]):
                # Armazena a mensagem selecionada no session_state
                st.session_state.selected_message = arquivo_dict["from"]
                st.session_state.numero = contar
                # Navega para a página de histórico
                st.switch_page("pages/historico.py")

        count+=1
    if count < 1:
        st.write("Nenhum arquivo encontrado")
else:
    st.switch_page("home.py")