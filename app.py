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

# Función para cargar datos (en una aplicación real, estos vendrían de una base de datos)
@st.cache_data
def cargar_restaurantes():
    # Simulamos datos de restaurantes
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
    return restaurantes

@st.cache_data
def cargar_platos():
    # Simulamos datos de platos
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
def cargar_reservas():
    # Simulamos datos de reservas del usuario actual
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

# Función para mostrar imágenes (simuladas)
def get_imagen_restaurante(restaurante_id):
    # En una app real, estas imágenes vendrían de una base de datos o sistema de archivos
    # Aquí generamos una imagen de color sólido como placeholder
    np.random.seed(restaurante_id)
    r = np.random.randint(100, 200)
    g = np.random.randint(100, 200)
    b = np.random.randint(100, 200)
    
    img = Image.new('RGB', (400, 200), color=(r, g, b))
    
    buffered = BytesIO()
    img.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode()

# Función para mostrar un menú en PDF (simulado)
def mostrar_menu_pdf(restaurante_id):
    # En una aplicación real, esto cargaría un PDF real
    st.info(f"Aquí se mostraría el PDF del menú del restaurante ID {restaurante_id}")
    st.write("(Funcionalidad simulada en esta demo)")

# Estilos CSS personalizados
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

# Cargar datos
restaurantes_df = cargar_restaurantes()
platos_df = cargar_platos()
reservas_df = cargar_reservas()

# Sidebar para navegación
st.sidebar.image("https://via.placeholder.com/150x150.png?text=La+Cuchara", width=150)
st.sidebar.title("La Cuchara")
pagina = st.sidebar.radio("Navegación", ["Buscar Restaurantes", "Mis Reservas", "Valoraciones"])

st.sidebar.markdown("---")
# if st.sidebar.button("Iniciar sesión / Registrarse"):
    # st.sidebar.success("Funcionalidad de inicio de sesión simulada")

# st.sidebar.markdown("---")
# st.sidebar.markdown("© 2025 La Cuchara Restauración SL")

# Página principal
if pagina == "Buscar Restaurantes":
    st.markdown("<h1 class='main-header'>Encuentra tu restaurante ideal</h1>", unsafe_allow_html=True)
    
    # Filtros en varias columnas
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
        
        # Aquí iría la lógica real de filtrado
        # Por ahora mostramos resultados simulados
        restaurantes_filtrados = restaurantes_df.copy()
        
        if tipo_restaurante != "Todos":
            restaurantes_filtrados = restaurantes_filtrados[restaurantes_filtrados['tipo'] == tipo_restaurante]
        
        if solo_promocionados:
            restaurantes_filtrados = restaurantes_filtrados[restaurantes_filtrados['promocionado'] == True]
        
        restaurantes_filtrados = restaurantes_filtrados[
            (restaurantes_filtrados['precio_min'] >= rango_precio[0]) & 
            (restaurantes_filtrados['precio_max'] <= rango_precio[1])
        ]
        
        # Mostrar resultados
        for _, rest in restaurantes_filtrados.iterrows():
            col1, col2 = st.columns([1, 2])
            
            with col1:
                st.markdown(f"""
                <div style="width:100%;height:200px;background-image:url(data:image/png;base64,{get_imagen_restaurante(rest['id'])});
                background-size:cover;border-radius:10px;"></div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.markdown(f"<div class='card'>", unsafe_allow_html=True)
                
                # Encabezado con promoción si aplica
                if rest['promocionado']:
                    st.markdown(f"""
                    <div class='promocionado'>✨ PROMOCIONADO</div>
                    """, unsafe_allow_html=True)
                
                st.markdown(f"<h3>{rest['nombre']} {'⭐' * int(rest['valoracion'])}</h3>", unsafe_allow_html=True)
                st.markdown(f"<p>📍 {rest['ubicacion']} | 🍽️ {rest['tipo']} | 💰 {rest['precio_min']}€ - {rest['precio_max']}€</p>", unsafe_allow_html=True)
                
                # Mostrar platos del restaurante
                platos_rest = platos_df[platos_df['restaurante_id'] == rest['id']]
                if not platos_rest.empty:
                    st.markdown("<h4>Platos destacados:</h4>", unsafe_allow_html=True)
                    for _, plato in platos_rest.iterrows():
                        promocion = "✨ " if plato['promocionado'] else ""
                        etiquetas = []
                        if plato['celiaco']: etiquetas.append("Sin gluten")
                        if plato['vegetariano']: etiquetas.append("Vegetariano")
                        if plato['vegano']: etiquetas.append("Vegano")
                        etiquetas_text = f" ({', '.join(etiquetas)})" if etiquetas else ""
                        
                        st.markdown(f"""
                        <div class='menu-item'>
                            {promocion}{plato['nombre']} - {plato['precio']}€ {'⭐' * int(plato['valoracion'])}
                            <small>{etiquetas_text}</small>
                        </div>
                        """, unsafe_allow_html=True)
                
                col1, col2 = st.columns(2)
                with col1:
                    if st.button(f"📅 Reservar mesa", key=f"reservar_{rest['id']}"):
                        st.success(f"Reserva simulada para {rest['nombre']}")
                with col2:
                    if st.button(f"📋 Ver menú completo", key=f"menu_{rest['id']}"):
                        mostrar_menu_pdf(rest['id'])
                
                st.markdown("</div>", unsafe_allow_html=True)
            
            st.markdown("---")

elif pagina == "Mis Reservas":
    st.markdown("<h1 class='main-header'>Mis Reservas</h1>", unsafe_allow_html=True)
    
    if reservas_df.empty:
        st.info("No tienes reservas activas")
    else:
        for _, reserva in reservas_df.iterrows():
            rest = restaurantes_df[restaurantes_df['id'] == reserva['restaurante_id']].iloc[0]
            
            st.markdown("<div class='card'>", unsafe_allow_html=True)
            col1, col2, col3 = st.columns([3, 1, 1])
            
            with col1:
                st.markdown(f"<h3>{rest['nombre']}</h3>", unsafe_allow_html=True)
                fecha_str = reserva['fecha'].strftime("%d/%m/%Y")
                st.markdown(f"<p>📅 {fecha_str} a las {reserva['hora']} | 👥 {reserva['num_personas']} personas</p>", unsafe_allow_html=True)
                st.markdown(f"<p>📍 {rest['ubicacion']}</p>", unsafe_allow_html=True)
                st.markdown("<h4>Platos reservados:</h4>", unsafe_allow_html=True)
                platos_list = reserva['platos'].split(", ")
                for plato in platos_list:
                    st.markdown(f"<div class='menu-item'>{plato}</div>", unsafe_allow_html=True)
                
                st.markdown(f"<p><b>Estado:</b> {reserva['estado']}</p>", unsafe_allow_html=True)
            
            with col2:
                if st.button("✏️ Modificar", key=f"mod_{reserva['id']}"):
                    st.info("Modificación de reserva simulada")
            
            with col3:
                if st.button("❌ Cancelar", key=f"canc_{reserva['id']}"):
                    st.warning("Cancelación de reserva simulada")
            
            st.markdown("</div>", unsafe_allow_html=True)
        
        if st.button("➕ Nueva reserva"):
            st.success("Creación de nueva reserva simulada")

elif pagina == "Valoraciones":
    st.markdown("<h1 class='main-header'>Valorar mi experiencia</h1>", unsafe_allow_html=True)
    
    # Simulamos una visita reciente
    restaurante_id = 1
    rest = restaurantes_df[restaurantes_df['id'] == restaurante_id].iloc[0]
    platos_rest = platos_df[platos_df['restaurante_id'] == restaurante_id]
    
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown(f"<h3>Valorar visita a {rest['nombre']}</h3>", unsafe_allow_html=True)
    st.markdown("<p>Visitado el 26/02/2025</p>", unsafe_allow_html=True)
    
    # Valoración general
    st.markdown("<h4>Valoración general del restaurante:</h4>", unsafe_allow_html=True)
    valoracion_general = st.slider("", 1, 5, 4, key="val_general")
    st.write(f"{'⭐' * valoracion_general}")
    
    comentario_general = st.text_area("Comentario sobre el restaurante", 
                                     placeholder="Comparte tu experiencia en este restaurante...")
    
    # Valoración de platos
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

# Pie de página
st.markdown("<div class='footer'>© 2025 La Cuchara Restauración SL. Todos los derechos reservados.</div>", unsafe_allow_html=True)
