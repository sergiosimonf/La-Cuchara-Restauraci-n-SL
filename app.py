import streamlit as st
import pandas as pd
import numpy as np
import base64
from PIL import Image
from io import BytesIO
from datetime import datetime, timedelta

# Configuración de la página
st.set_page_config(
    page_title="La Cuchara Restauración",
    page_icon="🍽️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -----------------------------
# Funciones de carga de datos (simulados)
# -----------------------------
@st.cache_data
def cargar_restaurantes():
    restaurantes = pd.DataFrame({
        'id': range(1, 6),
        'nombre': [
            'El Rincón Mediterráneo', 
            'Sabores de Asia', 
            'La Trattoria', 
            'El Asador', 
            'Veggie Garden'
        ],
        'valoracion': [4.8, 4.5, 4.3, 4.7, 4.2],
        'ubicacion': [
            'Calle Gran Vía, 34', 
            'Calle Serrano, 45', 
            'Plaza Mayor, 12', 
            'Avenida de la Constitución, 78', 
            'Calle Velázquez, 23'
        ],
        'tipo': [
            'Mediterráneo', 
            'Asiático', 
            'Italiano', 
            'Español', 
            'Vegetariano'
        ],
        'precio_min': [15, 12, 10, 18, 12],
        'precio_max': [25, 20, 18, 30, 16],
        'promocionado': [True, False, False, True, False],
        'menu_diario': [True, True, True, False, True],
        'menu_celiaco': [True, False, True, True, True],
        'menu_vegetariano': [True, True, True, False, True],
        'menu_vegano': [False, False, False, False, True]
    })
    restaurantes["descripcion"] = ""
    return restaurantes

@st.cache_data
def cargar_platos():
    platos = pd.DataFrame({
        'id': range(1, 16),
        'restaurante_id': [1, 1, 1, 2, 2, 2, 3, 3, 3, 4, 4, 5, 5, 5, 5],
        'nombre': [
            'Gazpacho andaluz', 'Paella valenciana', 'Tarta de queso',
            'Gyozas de pollo', 'Pad Thai', 'Helado de té verde',
            'Pasta carbonara', 'Pizza margarita', 'Tiramisú',
            'Chuletón a la brasa', 'Cochinillo asado',
            'Ensalada de quinoa', 'Hamburguesa vegana', 'Curry de garbanzos', 'Brownie sin gluten'
        ],
        'tipo': ['Entrante', 'Principal', 'Postre', 'Entrante', 'Principal', 'Postre',
                 'Principal', 'Principal', 'Postre', 'Principal', 'Principal',
                 'Entrante', 'Principal', 'Principal', 'Postre'],
        'valoracion': [4.7, 4.9, 4.6, 4.4, 4.6, 4.3, 4.5, 4.8, 4.7, 4.9, 4.8, 4.2, 4.4, 4.6, 4.3],
        'precio': [6, 12, 5, 7, 10, 4, 9, 11, 6, 22, 18, 7, 10, 9, 5],
        'en_menu_hoy': [True, True, True, True, True, True, True, True, True, False, False, True, True, True, True],
        'promocionado': [False, True, False, False, True, False, False, False, False, True, True, False, True, False, False],
        'celiaco': [True, True, False, False, True, True, False, False, False, True, True, True, False, True, True],
        'vegetariano': [True, False, True, False, True, True, False, True, True, False, False, True, True, True, True],
        'vegano': [True, False, False, False, False, True, False, False, False, False, False, True, True, True, False]
    })
    return platos

@st.cache_data
def cargar_reservas_iniciales():
    reservas = pd.DataFrame({
        'id': range(1, 3),
        'restaurante_id': [1, 3],
        'fecha': [datetime.now() + timedelta(days=1), datetime.now() + timedelta(days=3)],
        'hora': ['14:00', '21:00'],
        'num_personas': [2, 4],
        'platos': [
            'Gazpacho andaluz, Paella valenciana, Tarta de queso',
            'Pasta carbonara, Pizza margarita, Tiramisú'
        ],
        'estado': ['Confirmada', 'Pendiente']
    })
    return reservas

# -----------------------------
# Inicialización del estado de sesión
# -----------------------------
if 'reservas_df' not in st.session_state:
    st.session_state.reservas_df = cargar_reservas_iniciales()

if 'nuevos_restaurantes' not in st.session_state:
    st.session_state.nuevos_restaurantes = pd.DataFrame(columns=[
        'id', 'nombre', 'valoracion', 'ubicacion', 'tipo', 'precio_min', 'precio_max', 
        'promocionado', 'menu_diario', 'menu_celiaco', 'menu_vegetariano', 'menu_vegano', 'descripcion'
    ])

if 'menu_pdfs' not in st.session_state:
    st.session_state.menu_pdfs = {}

if 'active_reservation' not in st.session_state:
    st.session_state.active_reservation = None
if 'modify_reservation' not in st.session_state:
    st.session_state.modify_reservation = None
if 'new_reservation' not in st.session_state:
    st.session_state.new_reservation = False

# Combinar restaurantes precargados y los agregados manualmente
restaurantes_df = pd.concat([cargar_restaurantes(), st.session_state.nuevos_restaurantes], ignore_index=True)
platos_df = cargar_platos()

# -----------------------------
# Funciones auxiliares
# -----------------------------
def get_imagen_restaurante(restaurante_id):
    np.random.seed(restaurante_id)
    r = np.random.randint(100, 200)
    g = np.random.randint(100, 200)
    b = np.random.randint(100, 200)
    img = Image.new('RGB', (400, 200), color=(r, g, b))
    buffered = BytesIO()
    img.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode()

def mostrar_menu_pdf(restaurante_id):
    # Si se subió un PDF, se muestra incrustado en un iframe.
    if restaurante_id in st.session_state.menu_pdfs:
        pdf_bytes = st.session_state.menu_pdfs[restaurante_id]
        pdf_base64 = base64.b64encode(pdf_bytes).decode('utf-8')
        pdf_display = f'<iframe src="data:application/pdf;base64,{pdf_base64}" width="700" height="1000" type="application/pdf"></iframe>'
        st.markdown(pdf_display, unsafe_allow_html=True)
    else:
        # En caso de no existir un PDF, se muestra una simulación del menú a partir de los platos.
        st.info("No se encontró un PDF para este restaurante. Se muestra un menú simulado:")
        platos_rest = platos_df[platos_df['restaurante_id'] == restaurante_id]
        if platos_rest.empty:
            st.warning("No se encontraron platos para este restaurante.")
        else:
            for _, plato in platos_rest.iterrows():
                st.markdown(f"**{plato['nombre']}** - {plato['precio']}€")
                st.markdown(f"*Tipo:* {plato['tipo']} | *Valoración:* {'⭐' * int(plato['valoracion'])}")
                st.markdown("---")

def local_css():
    st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem !important;
        color: #1E88E5 !important;
        padding-bottom: 1rem;
        border-bottom: 2px solid #1E88E5;
        margin-bottom: 2rem;
    }
    .subheader {
        font-size: 1.8rem !important;
        color: #333 !important;
        padding-bottom: 0.5rem;
        margin-bottom: 1rem;
    }
    .card {
        background-color: white;
        border-radius: 10px;
        padding: 1.5rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin-bottom: 1rem;
    }
    .promocionado {
        background-color: #FFF9C4;
        border-left: 4px solid #FBC02D;
        padding: 0.5rem;
        margin-bottom: 0.5rem;
    }
    .footer {
        text-align: center;
        color: #666;
        padding: 1rem;
        border-top: 1px solid #eee;
        margin-top: 2rem;
    }
    .menu-item {
        padding: 0.5rem;
        margin-bottom: 0.2rem;
        border-bottom: 1px solid #eee;
    }
    </style>
    """, unsafe_allow_html=True)

local_css()

# -----------------------------
# Sidebar de navegación
# -----------------------------
st.sidebar.image("https://via.placeholder.com/150x150.png?text=La+Cuchara", width=150)
st.sidebar.title("La Cuchara")
pagina = st.sidebar.radio("Navegación", ["Buscar Restaurantes", "Mis Reservas", "Valoraciones", "Agregar Restaurante"])
st.sidebar.markdown("---")

# -----------------------------
# Página: Buscar Restaurantes
# -----------------------------
if pagina == "Buscar Restaurantes":
    st.markdown("<h1 class='main-header'>Encuentra tu restaurante ideal</h1>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        busqueda_plato = st.text_input("🍽️ Buscar plato", placeholder="Paella, sushi, pasta...")
        ubicacion = st.text_input("📍 Ubicación", placeholder="Barrio, calle, zona...")
    with col2:
        tipo_restaurante = st.selectbox("👨‍🍳 Tipo de restaurante", 
                                       ["Todos"] + sorted(restaurantes_df['tipo'].unique().tolist()))
        rango_precio = st.slider("💰 Rango de precio (€)", 5, 40, (10, 25))
    with col3:
        opciones_menu = st.multiselect("🍲 Tipo de menú", 
                                      ["Sin restricciones", "Celíaco", "Vegetariano", "Vegano"],
                                      default=["Sin restricciones"])
        solo_promocionados = st.checkbox("Ver solo restaurantes con promociones")
    
    if st.button("🔍 Buscar restaurantes"):
        st.markdown("<h2 class='subheader'>Resultados de búsqueda</h2>", unsafe_allow_html=True)
        restaurantes_filtrados = restaurantes_df.copy()
        if tipo_restaurante != "Todos":
            restaurantes_filtrados = restaurantes_filtrados[restaurantes_filtrados['tipo'] == tipo_restaurante]
        if solo_promocionados:
            restaurantes_filtrados = restaurantes_filtrados[restaurantes_filtrados['promocionado'] == True]
        restaurantes_filtrados = restaurantes_filtrados[
            (restaurantes_filtrados['precio_min'] >= rango_precio[0]) & 
            (restaurantes_filtrados['precio_max'] <= rango_precio[1])
        ]
        
        for _, rest in restaurantes_filtrados.iterrows():
            col_img, col_info = st.columns([1, 2])
            with col_img:
                st.markdown(f"""
                <div style="width:100%;height:200px;background-image:url(data:image/png;base64,{get_imagen_restaurante(rest['id'])});
                background-size:cover;border-radius:10px;"></div>
                """, unsafe_allow_html=True)
            with col_info:
                st.markdown("<div class='card'>", unsafe_allow_html=True)
                if rest['promocionado']:
                    st.markdown("<div class='promocionado'>✨ PROMOCIONADO</div>", unsafe_allow_html=True)
                st.markdown(f"<h3>{rest['nombre']} {'⭐' * int(rest['valoracion'])}</h3>", unsafe_allow_html=True)
                st.markdown(f"<p>📍 {rest['ubicacion']} | 🍽️ {rest['tipo']} | 💰 {rest['precio_min']}€ - {rest['precio_max']}€</p>", unsafe_allow_html=True)
                
                # Mostrar platos destacados
                platos_rest = platos_df[platos_df['restaurante_id'] == rest['id']]
                if not platos_rest.empty:
                    st.markdown("<h4>Platos destacados:</h4>", unsafe_allow_html=True)
                    for _, plato in platos_rest.iterrows():
                        promo = "✨ " if plato['promocionado'] else ""
                        etiquetas = []
                        if plato['celiaco']: etiquetas.append("Sin gluten")
                        if plato['vegetariano']: etiquetas.append("Vegetariano")
                        if plato['vegano']: etiquetas.append("Vegano")
                        etiquetas_text = f" ({', '.join(etiquetas)})" if etiquetas else ""
                        st.markdown(f"<div class='menu-item'>{promo}{plato['nombre']} - {plato['precio']}€ {'⭐' * int(plato['valoracion'])} <small>{etiquetas_text}</small></div>", unsafe_allow_html=True)
                
                # Sección de información adicional
                with st.expander("Más información"):
                    if rest['descripcion']:
                        st.markdown(f"**Descripción:** {rest['descripcion']}")
                    else:
                        st.markdown("No hay información adicional.")
                    st.markdown("**Menú PDF:**")
                    mostrar_menu_pdf(rest['id'])
                
                col_accion1, col_accion2 = st.columns(2)
                with col_accion1:
                    if st.button("📅 Reservar mesa", key=f"reservar_{rest['id']}"):
                        st.session_state.active_reservation = rest['id']
                with col_accion2:
                    if st.button("📋 Ver menú completo", key=f"menu_{rest['id']}"):
                        mostrar_menu_pdf(rest['id'])
                st.markdown("</div>", unsafe_allow_html=True)
            st.markdown("---")
    
    if st.session_state.active_reservation is not None:
        rest_id = st.session_state.active_reservation
        rest_sel = restaurantes_df[restaurantes_df['id'] == rest_id].iloc[0]
        st.markdown(f"<h2 class='subheader'>Reservar en {rest_sel['nombre']}</h2>", unsafe_allow_html=True)
        fecha = st.date_input("Selecciona la fecha", min_value=datetime.now().date(), value=datetime.now().date() + timedelta(days=1))
        hora = st.time_input("Selecciona la hora", value=datetime.now().time().replace(second=0, microsecond=0))
        num_personas = st.number_input("Número de personas", min_value=1, max_value=20, value=2, step=1)
        comentario = st.text_area("Comentario o petición especial (opcional)")
        if st.button("Confirmar Reserva", key=f"confirma_{rest_id}"):
            nuevo_id = st.session_state.reservas_df['id'].max() + 1 if not st.session_state.reservas_df.empty else 1
            nueva_reserva = {
                'id': nuevo_id,
                'restaurante_id': rest_id,
                'fecha': datetime.combine(fecha, hora),
                'hora': hora.strftime("%H:%M"),
                'num_personas': num_personas,
                'platos': "",
                'estado': 'Confirmada'
            }
            st.session_state.reservas_df = st.session_state.reservas_df.append(nueva_reserva, ignore_index=True)
            st.success(f"Reserva confirmada en {rest_sel['nombre']} para el {fecha.strftime('%d/%m/%Y')} a las {hora.strftime('%H:%M')}")
            st.session_state.active_reservation = None

# -----------------------------
# Página: Mis Reservas
# -----------------------------
elif pagina == "Mis Reservas":
    st.markdown("<h1 class='main-header'>Mis Reservas</h1>", unsafe_allow_html=True)
    
    if st.button("➕ Nueva reserva"):
        st.session_state.new_reservation = True

    if st.session_state.new_reservation:
        st.markdown("<h2 class='subheader'>Crear nueva reserva</h2>", unsafe_allow_html=True)
        rest_options = restaurantes_df[['id', 'nombre']]
        rest_seleccion = st.selectbox("Selecciona un restaurante", options=rest_options['id'], format_func=lambda x: rest_options[rest_options['id'] == x]['nombre'].values[0])
        fecha = st.date_input("Selecciona la fecha", min_value=datetime.now().date(), value=datetime.now().date() + timedelta(days=1))
        hora = st.time_input("Selecciona la hora", value=datetime.now().time().replace(second=0, microsecond=0))
        num_personas = st.number_input("Número de personas", min_value=1, max_value=20, value=2, step=1)
        comentario = st.text_area("Comentario o petición especial (opcional)")
        if st.button("Confirmar Reserva", key="confirma_nueva"):
            nuevo_id = st.session_state.reservas_df['id'].max() + 1 if not st.session_state.reservas_df.empty else 1
            nueva_reserva = {
                'id': nuevo_id,
                'restaurante_id': rest_seleccion,
                'fecha': datetime.combine(fecha, hora),
                'hora': hora.strftime("%H:%M"),
                'num_personas': num_personas,
                'platos': "",
                'estado': 'Confirmada'
            }
            st.session_state.reservas_df = st.session_state.reservas_df.append(nueva_reserva, ignore_index=True)
            nombre_rest = restaurantes_df[restaurantes_df['id'] == rest_seleccion]['nombre'].values[0]
            st.success(f"Reserva confirmada en {nombre_rest} para el {fecha.strftime('%d/%m/%Y')} a las {hora.strftime('%H:%M')}")
            st.session_state.new_reservation = False

    if st.session_state.reservas_df.empty:
        st.info("No tienes reservas activas")
    else:
        for idx, reserva in st.session_state.reservas_df.iterrows():
            rest = restaurantes_df[restaurantes_df['id'] == reserva['restaurante_id']].iloc[0]
            st.markdown("<div class='card'>", unsafe_allow_html=True)
            col1, col2, col3 = st.columns([3, 1, 1])
            with col1:
                fecha_str = reserva['fecha'].strftime("%d/%m/%Y")
                st.markdown(f"<h3>{rest['nombre']}</h3>", unsafe_allow_html=True)
                st.markdown(f"<p>📅 {fecha_str} a las {reserva['hora']} | 👥 {reserva['num_personas']} personas</p>", unsafe_allow_html=True)
                st.markdown(f"<p>📍 {rest['ubicacion']}</p>", unsafe_allow_html=True)
                st.markdown("<h4>Platos reservados:</h4>", unsafe_allow_html=True)
                for plato in reserva['platos'].split(", "):
                    if plato:
                        st.markdown(f"<div class='menu-item'>{plato}</div>", unsafe_allow_html=True)
                st.markdown(f"<p><b>Estado:</b> {reserva['estado']}</p>", unsafe_allow_html=True)
            with col2:
                if st.button("✏️ Modificar", key=f"mod_{reserva['id']}"):
                    st.session_state.modify_reservation = reserva['id']
            with col3:
                if st.button("❌ Cancelar", key=f"canc_{reserva['id']}"):
                    st.session_state.reservas_df = st.session_state.reservas_df[st.session_state.reservas_df['id'] != reserva['id']]
                    st.warning("Reserva cancelada")
            st.markdown("</div>", unsafe_allow_html=True)

    if st.session_state.modify_reservation is not None:
        res_id = st.session_state.modify_reservation
        reserva_actual = st.session_state.reservas_df[st.session_state.reservas_df['id'] == res_id].iloc[0]
        rest_mod = restaurantes_df[restaurantes_df['id'] == reserva_actual['restaurante_id']].iloc[0]
        st.markdown(f"<h2 class='subheader'>Modificar reserva en {rest_mod['nombre']}</h2>", unsafe_allow_html=True)
        fecha_mod = st.date_input("Fecha", value=reserva_actual['fecha'].date(), key="fecha_mod")
        hora_mod = st.time_input("Hora", value=datetime.strptime(reserva_actual['hora'], "%H:%M").time(), key="hora_mod")
        num_personas_mod = st.number_input("Número de personas", min_value=1, max_value=20, value=reserva_actual['num_personas'], step=1, key="num_mod")
        if st.button("Guardar cambios", key="guardar_mod"):
            idx_mod = st.session_state.reservas_df.index[st.session_state.reservas_df['id'] == res_id][0]
            st.session_state.reservas_df.at[idx_mod, 'fecha'] = datetime.combine(fecha_mod, hora_mod)
            st.session_state.reservas_df.at[idx_mod, 'hora'] = hora_mod.strftime("%H:%M")
            st.session_state.reservas_df.at[idx_mod, 'num_personas'] = num_personas_mod
            st.success("Reserva modificada correctamente")
            st.session_state.modify_reservation = None

# -----------------------------
# Página: Valoraciones
# -----------------------------
elif pagina == "Valoraciones":
    st.markdown("<h1 class='main-header'>Valorar mi experiencia</h1>", unsafe_allow_html=True)
    restaurante_id = 1  # Simulación: se valora un restaurante ya visitado
    rest = restaurantes_df[restaurantes_df['id'] == restaurante_id].iloc[0]
    platos_rest = platos_df[platos_df['restaurante_id'] == restaurante_id]
    
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown(f"<h3>Valorar visita a {rest['nombre']}</h3>", unsafe_allow_html=True)
    st.markdown("<p>Visitado el 26/02/2025</p>", unsafe_allow_html=True)
    
    st.markdown("<h4>Valoración general del restaurante:</h4>", unsafe_allow_html=True)
    valoracion_general = st.slider("", 1, 5, 4, key="val_general")
    st.write(f"{'⭐' * valoracion_general}")
    comentario_general = st.text_area("Comentario sobre el restaurante", 
                                      placeholder="Comparte tu experiencia en este restaurante...")
    
    st.markdown("<h4>Valorar platos consumidos:</h4>", unsafe_allow_html=True)
    for _, plato in platos_rest.head(3).iterrows():
        col1, col2 = st.columns([1, 2])
        with col1:
            st.markdown(f"<p><b>{plato['nombre']}</b></p>", unsafe_allow_html=True)
            valoracion_plato = st.slider("", 1, 5, 4, key=f"val_plato_{plato['id']}")
            st.write(f"{'⭐' * valoracion_plato}")
        with col2:
            st.text_area("Comentario", placeholder=f"¿Qué te pareció el {plato['nombre'].lower()}?", 
                          key=f"com_plato_{plato['id']}")
    st.markdown("</div>", unsafe_allow_html=True)
    
    if st.button("📤 Enviar valoraciones"):
        st.success("¡Gracias por tus valoraciones! Se han guardado correctamente.")

# -----------------------------
# Página: Agregar Restaurante
# -----------------------------
elif pagina == "Agregar Restaurante":
    st.markdown("<h1 class='main-header'>Agregar Restaurante</h1>", unsafe_allow_html=True)
    st.markdown("Completa la siguiente información para añadir un nuevo restaurante a la plataforma.")
    
    nombre = st.text_input("Nombre del restaurante")
    valoracion = st.number_input("Valoración (1-5)", min_value=1.0, max_value=5.0, value=4.0, step=0.1)
    ubicacion = st.text_input("Ubicación")
    tipo = st.selectbox("Tipo de cocina", ["Mediterráneo", "Asiático", "Italiano", "Español", "Vegetariano", "Otro"])
    precio_min = st.number_input("Precio mínimo (€)", min_value=1, value=10)
    precio_max = st.number_input("Precio máximo (€)", min_value=1, value=25)
    promocionado = st.checkbox("Restaurante promocionado")
    menu_diario = st.checkbox("Menú diario disponible")
    menu_celiaco = st.checkbox("Menú para celíacos")
    menu_vegetariano = st.checkbox("Menú vegetariano")
    menu_vegano = st.checkbox("Menú vegano")
    descripcion = st.text_area("Descripción o información adicional", placeholder="Escribe una breve descripción del restaurante...")
    pdf_menu = st.file_uploader("Subir menú en PDF", type=["pdf"])
    
    if st.button("Agregar Restaurante"):
        nuevo_id = restaurantes_df['id'].max() + 1 if not restaurantes_df.empty else 1
        nuevo_rest = {
            'id': nuevo_id,
            'nombre': nombre,
            'valoracion': valoracion,
            'ubicacion': ubicacion,
            'tipo': tipo,
            'precio_min': precio_min,
            'precio_max': precio_max,
            'promocionado': promocionado,
            'menu_diario': menu_diario,
            'menu_celiaco': menu_celiaco,
            'menu_vegetariano': menu_vegetariano,
            'menu_vegano': menu_vegano,
            'descripcion': descripcion
        }
        st.session_state.nuevos_restaurantes = st.session_state.nuevos_restaurantes.append(nuevo_rest, ignore_index=True)
        if pdf_menu is not None:
            st.session_state.menu_pdfs[nuevo_id] = pdf_menu.read()
        st.success(f"Restaurante '{nombre}' agregado exitosamente.")

# -----------------------------
# Pie de página
# -----------------------------
st.markdown("<div class='footer'>© 2025 La Cuchara Restauración SL. Todos los derechos reservados.</div>", unsafe_allow_html=True)
