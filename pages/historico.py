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

if "selected_message" in st.session_state :
    db = firestore.client()
    st_autorefresh(interval=3000, key="chat_update")
    mensagens_from = db.collection("mensagens").where("from", "==", st.session_state.selected_message).stream()

        # Consulta 2: Mensagens onde "to" é "pedro"
    mensagens_to = db.collection("mensagens").where("to", "==", st.session_state.selected_message).stream()

        # Combina os resultados das duas consultas
    mensagens = list(mensagens_from) + list(mensagens_to)
    mensagens_ordenadas = sorted(
        mensagens, 
        key=lambda x: x.to_dict().get("tempo", ""),  # Obtém o campo "tempo" e previne erro se estiver ausente
        reverse=False
    )

    st.markdown(
        """
        <style>
        /* Estiliza os botões gerados pelo st.button */
        div.stButton > button {
            background-color: #262730;
            color: white;
        
            padding: 0px 24px;
            border: none;
            border-radius: 8px;
            cursor: pointer;
            font-size: 16px;
            transition: background-color 0.3s ease;
        display: block;
                text-align: left;
            
        font-size: 24px;
        
        }
    
        </style>
        """,
        unsafe_allow_html=True
    )

    if st.button("<"):
        st.switch_page("pages/psicologa.py")
    for arquivo in mensagens_ordenadas:
        elements = st.container(border=True,)
        arquivo_dict = arquivo.to_dict()
        if arquivo_dict["to"] == "psicologa":
        
            eu = elements.chat_message("🙂") 
            eu.markdown(arquivo_dict["texto"])   
        else:
            eu = elements.chat_message("👩🏻‍⚕️") 
            eu.markdown(arquivo_dict["texto"])

    st1,st2 = st.columns(2) 

    txt = st.chat_input("Diz alguma coisa")
    if txt:
            dados = {
                "to": st.session_state.selected_message,
                "texto":txt ,
                "from":"psicologa",
                "tempo":firestore.SERVER_TIMESTAMP
                            
                }
            db.collection("mensagens").add(dados)
            st.rerun()
else:
     st.switch_page("home.py")