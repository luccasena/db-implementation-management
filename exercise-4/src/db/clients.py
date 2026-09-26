import streamlit as st
from pymongo import MongoClient

@st.cache_resource
def conectar_mongodb():
    return MongoClient(
        st.secrets["mongodb"]["uri"],
        serverSelectionTimeoutMS=3000,
    )

def obter_banco_mongodb():
    cliente = conectar_mongodb()

    return cliente[
        st.secrets["mongodb"]["database"]
    ]
