###################################################################################################
# BIBLIOTECAS
import streamlit as st
import bcrypt
from datetime import datetime
import pytz
import json

st.set_page_config(
    page_title="bcrypt hasher",
    page_icon="🔑",
    layout="centered", # centered | wide
    initial_sidebar_state="collapsed" # auto | expanded | collapsed
)
st.markdown("""<style>
    #MainMenu { visibility: hidden; }
    header { visibility: hidden; }
    footer { visibility: hidden; }
</style>""", unsafe_allow_html=True) 

# VARIABLES LOCALES
LOCAL_TZ = pytz.timezone("America/Mexico_City")

# VARIABLES DE SESSION
if 'first_execution' not in st.session_state:
    st.session_state.first_execution = True
if 'show_json_output' not in st.session_state:
    st.session_state.show_json_output = False
if 'plain_password' not in st.session_state:
    st.session_state.plain_password = ""
if 'hashed_password' not in st.session_state:
    st.session_state.hashed_password = ""

# FUNCIONES AUXILIARES
def create_json_state():
    json_state = {
        "hashed_password" : st.session_state.hashed_password,
        "plain_password"  : st.session_state.plain_password,
        "hashed_at"       : st.session_state.created_at,
        "time_zone"       : str(LOCAL_TZ),
    } if st.session_state.show_json_details else {
        "hashed_password" : st.session_state.hashed_password,
    }
    return json_state

###################################################################################################
# INICIO DE LA APLICACION
st.title("Hashing usando Bcrypt")

# CALLBACK PARA CUANDO SE INGRESE UNA CONTRASEÑA EN TEXTO PLANO
def update_hash_password():
    if not st.session_state.first_execution or st.session_state.plain_password != "":
        
        # GENERAMOS NUESTRA CONTRASEÑA HASHEADA
        binary_salt = bcrypt.gensalt(rounds = 12, prefix=b"2b") # rounds from 4 to 31
        st.session_state.hashed_password = bcrypt.hashpw(password = st.session_state.plain_password.encode(), salt = binary_salt).decode()
        st.session_state.created_at = datetime.now(tz = LOCAL_TZ).isoformat(sep='T', timespec='microseconds')
        
        # GENERAMOS EL OUTPUT PARA EL USUARIO
        json_state  = create_json_state()
        json_string = json.dumps(obj = json_state, indent=4)
        hasher_output.json(body = json_state, expanded = True)
        hasher_export.download_button(key="db_1", label="Descargar Contraseña en formato JSON", file_name="hashed_password.json",
                                        mime="application/json", type="primary", data=json_string, use_container_width=True)
        
        # AJUSTAMOS VARIABLES DE SESION
        st.session_state.first_execution = False
        st.session_state.show_json_output = True

# CALLBACK PARA CUANDO CAMBIEN EL INTERRUMPOR DE OBTENER MÁS DETALLES
def update_details():
    json_state  = create_json_state()
    json_string = json.dumps(obj = json_state, indent=4)
    hasher_output.json(body = json_state, expanded = True)
    hasher_export.download_button(key="db_2", label="Descargar Contraseña en formato JSON", file_name="hashed_password.json",
                                    mime="application/json", type="primary", data=json_string, use_container_width=True)
    
# DISEÑO DE INTERFAZ
st.text_input(key="plain_password", label = "Contraseña a hashear", placeholder="Pepito-9978#", type="password", on_change=update_hash_password)
st.toggle(key="show_json_details", label = "Mostrar más detalles", value = False, on_change=update_details)
hasher_output = st.empty()
hasher_export = st.empty()

# SOLO SE CORRERA CUANDO YA SE HAYA HASHEADO ALGUNA CONTRASEÑA
# SOBRE-ESCRIBIENDO LOS EMPTY DE ARRIBA
if not st.session_state.first_execution:
    json_state  = create_json_state()
    json_string = json.dumps(obj = json_state, indent=4)
    hasher_output.json(body = json_state, expanded = True)
    hasher_export.download_button(key="db_3", label="Descargar Contraseña en formato JSON", file_name="hashed_password.json",
                                    mime="application/json", type="primary", data=json_string, use_container_width=True)

# EXPANSOR PARA DARLE MÁS DETALLES AL USUARIO
with st.expander(label="Saber más"):
    st.markdown("""
    **¿Qué es un Hash?**

    Es un texto de longitud fija que sirve para varios propósitos, uno de ellos es el de ocultar contraseñas

    **¿Encriptar y hashear es lo mismo?**

    No. Al aplicar un algoritmo de hash no hay forma de recuperar el contenido original.

    Cuando se encripta se tiene la intención de volver a recuperar la información, es decir, desencriptando la información mediante alguna contraseña

    **¿Qué es Bcrypt?**

    Es un algoritmo enfocado para hashear contraseñas, siendo de los mejores algoritmos que existen.
    """)