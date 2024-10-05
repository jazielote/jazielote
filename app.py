import streamlit as st
import mysql.connector as mysql
import uuid
from streamlit_calendar import calendar
from io import BytesIO
# Conectar a la base de datos
conexion = mysql.connect(
    host="localhost",
    user="root",
    password="",
    database="rrhh"
)
cursor = conexion.cursor()

def login():
    st.title("Login")

    email = st.text_input("E-mail")
    password = st.text_input("Contraseña", type="password")

    if st.button("Login"):
        cursor.execute("SELECT * FROM users WHERE email = %s AND contrasena = %s", (email, password))
        user = cursor.fetchone()

        if user:
            st.session_state["username"] = user[1]  # Asumiendo que el nombre está en la segunda columna
            st.session_state["userid"] = user[0] # Asumiendo que el id está en la primera columna
            st.success("Login exitoso")
            st.rerun()  # Recargar la página para limpiar el contenido
        else:
            st.error("Credenciales incorrectas")

def register():
    st.title("Registro de usuarios")

    nombre = st.text_input("Nombre")
    email = st.text_input("E-mail")
    telefono = st.text_input("Teléfono")
    password = st.text_input("Contraseña", type="password")

    if st.button("Registrar"):
        # Generar un nuevo UUID para cada registro
        Uuid = str(uuid.uuid4())
        
        cursor.execute("INSERT INTO users (id, nombre, telefono, email, contrasena) VALUES (%s, %s, %s, %s, %s)", (Uuid, nombre, telefono, email, password))
        conexion.commit()  # Confirmar la transacción
        
        if cursor.rowcount == 1:
            st.success("Usuario registrado correctamente")
            st.session_state["username"] = nombre
            st.session_state["userid"] = Uuid
            st.rerun()
            dashboard()
        else:
            st.error("No se pudo registrar el usuario")
def solicitudes(id):
    st.title("Solicitudes")
    cursor.execute("SELECT * FROM postulaciones WHERE vacante_id = %s", (id,))
    postulaciones = cursor.fetchall()

    for postulacion in postulaciones:
        st.write(f"Nombre: {postulacion[2]}")
        st.write(f"Email: {postulacion[3]}")
        st.write(f"Teléfono: {postulacion[4]}")
        
        direccion_delodf = postulacion[5]
        with open(direccion_delodf, 'rb') as file:
            documento = file.read()
            
        st.download_button(label="Descargar CV", data=documento, file_name=direccion_delodf.split('/')[-1])




def vacantes():
    cursor = conexion.cursor()
    st.title("Mis Vacantes")
    cursor.execute("SELECT * FROM vacantes WHERE iduser = %s", (st.session_state["userid"],))
    vacantes = cursor.fetchall()
    st.session_state["vacante_form"] = False

    if st.button("Nueva Vacante"):
        if st.session_state["vacante_form"] == False:
            st.session_state["vacante_form"] = True
        else:
            st.session_state["vacante_form"] = False
    if st.session_state["vacante_form"] == True:
            st.title("Nueva Vacante")
            with st.form(key="formulario"):
                titulo = st.text_input("Titúlo")
                descripcion = st.text_area("Descripción")
                ubicacion = st.text_input("Ubicación")
                salario = st.number_input("Salario", step=100, min_value=0, format="%d", value=0)
                fecha_publicacion = st.date_input("Fecha de publicación")
                fecha_cierre = st.date_input("Fecha de cierre")
                tipo_contrato = st.selectbox("Tipo de contrato", ["Tiempo completo","Medio tiempo","Temporal", "Permanente","Practicante"])
                experiencia_requerida = st.text_input("Experiencia requerida")
                educacion_requerida = st.text_input("Educación requerida")
                habilidades_requeridas = st.text_input("Habilidades requeridas")
                submit_button = st.form_submit_button(label="Registrar")

                if submit_button:
                    Uuid = str(uuid.uuid4())
                    userid = st.session_state["userid"]
                    query = """
                    INSERT INTO `vacantes`(`id`, `iduser`, `titulo`, `descripcion`, `ubicacion`, `salario`, `fecha_publicacion`, `fecha_cierre`, `tipo_contrato`, `experiencia_requerida`, `educacion_requerida`, `habilidades_requeridas`)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """
                    values = (
                        Uuid, 
                        userid, 
                        titulo, 
                        descripcion, 
                        ubicacion, 
                        salario, 
                        fecha_publicacion, 
                        fecha_cierre, 
                        tipo_contrato, 
                        experiencia_requerida, 
                        educacion_requerida, 
                        habilidades_requeridas
                    )
                    cursor.execute(query, values)
                    conexion.commit()
                    if cursor.rowcount == 1:
                        st.success("Vacante registrada correctamente")
                    else:
                        st.error("No se pudo registrar la vacante")

    a = 1
    for vacante in vacantes:
        st.write(vacante[2])
        acciones = st.selectbox(f"Acciones{a}", ["Ver Información", "Ver Solicitudes"])
        if acciones == "Ver Solicitudes":
            solicitudes(vacante[0])
        elif acciones == "Ver Información":
            st.write(f"Titulo: {vacante[2]} - Salario: {vacante[5]}")
        a += 1

def ver_entrevistas():
    st.title("Entrevistas")
    userid = st.session_state["userid"]
    
    # Ejecutando la consulta para obtener las vacantes del usuario
    query = "SELECT * FROM vacantes WHERE `iduser` = %s"
    cursor.execute(query, (userid,))
    vacantes = cursor.fetchall()

    # Creando un cuadro de selección con los datos obtenidos
    vacantes_select = st.selectbox("Vacante seleccionada", [vacante[2] for vacante in vacantes])

    # Obteniendo el id de la vacante seleccionada
    vacante_id = [vacante[0] for vacante in vacantes if vacante[2] == vacantes_select][0]
    
    # Ejecutando la consulta para obtener las postulaciones de la vacante seleccionada
    query_postulaciones = "SELECT * FROM entrevistas WHERE `vacante_id` = %s"
    cursor.execute(query_postulaciones, (vacante_id,))
    entrevistas = cursor.fetchall()

    # Preparando los eventos para el calendario
    eventos = []
    for entrevista in entrevistas:
        id_postulante = entrevista[1].decode('utf-8')
        query = f"SELECT * FROM postulaciones WHERE vacante_id = '{id_postulante}'"
        cursor.execute(query)
        postulante = cursor.fetchone()

        evento = {
            'title': postulante[2],
            "start": entrevista[3].strftime("%Y-%m-%dT%H:%M:%S"),  # Convertir datetime a string
            "end": entrevista[3].strftime("%Y-%m-%dT%H:%M:%S")  # Convertir datetime a string
        }
        eventos.append(evento)
    # Mostrando el calendario
    st.write(calendar(events=eventos))


def entrevistas():
    st.title("Agendar Entrevistas")
    opciones = st.selectbox("Acciones", ["Ver Entrevistas", "Agendar Entrevista"])
    if opciones == "Ver Entrevistas":
        ver_entrevistas()
    elif opciones == "Agendar Entrevista":
        userid = st.session_state["userid"]
        # Ejecutando la consulta para obtener las vacantes del usuario
        query = "SELECT * FROM vacantes WHERE `iduser` = %s"
        cursor.execute(query, (userid,))
        vacantes = cursor.fetchall()

        # Creando un cuadro de selección con los datos obtenidos
        vacantes_select = st.selectbox("Vacante", [vacante[2] for vacante in vacantes])

        # Obteniendo el id de la vacante seleccionada
        vacante_id = [vacante[0] for vacante in vacantes if vacante[2] == vacantes_select][0]

        # Ejecutando la consulta para obtener las postulaciones de la vacante seleccionada
        query_postulaciones = "SELECT * FROM postulaciones WHERE `vacante_id` = %s"
        cursor.execute(query_postulaciones, (vacante_id,))
        postulaciones = cursor.fetchall()
            
        # Creando un select con las postulaciones obtenidas
        postulaciones_select = st.selectbox("Postulación", [postulacion[2] for postulacion in postulaciones])

        # Obteniendo el id de la postulación seleccionada
        postulacion_id = [postulacion[0] for postulacion in postulaciones if postulacion[2] == postulaciones_select][0]
        
        fecha = st.date_input("Fecha de la entrevista")
        
        Uuid = str(uuid.uuid4())

        # Agendando la entrevista
        if st.button("Agendar"):
            cursor.execute("INSERT INTO entrevistas (id, vacante_id, postulacion_id, fecha) VALUES (%s, %s, %s, %s)", (Uuid, vacante_id, postulacion_id, fecha))
            conexion.commit()
            if cursor.rowcount == 1:
                st.success("Entrevista agendada correctamente")
            else:
                st.error("No se pudo agendar la entrevista")

def dashboard():
    if "username" in st.session_state:
        st.title("Dashboard")
        st.header(f"Hola {st.session_state['username']}!")
    else:
        st.error("No has iniciado sesión")

def main():
    st.sidebar.title("Menu")
    if "username" in st.session_state:
        menu_option = st.sidebar.selectbox("Selecciona una opción", ["Dashboard", "Vacantes","Entrevistas"])
    else:
        menu_option = st.sidebar.selectbox("Selecciona una aplicación", ["Iniciar sesión", "Registro"])

    if menu_option == "Dashboard":
        dashboard()
    elif menu_option == "Vacantes":
        vacantes()
    elif menu_option == "Iniciar sesión":
        login()
    elif menu_option == "Registro":
        register()
    elif menu_option == "Entrevistas":
        entrevistas()


if __name__ == "__main__":
    main()