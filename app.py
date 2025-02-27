import streamlit as st
import pandas as pd

# Configuración inicial de la página
st.set_page_config(
    page_title="Tabla de Cobertura de Inmunización",
    layout="wide"
)

@st.cache_data
def cargar_datos():
    """
    Carga y limpia los datos del archivo CSV desde la ruta especificada.
    """
    file_path = "data/coverage-data.csv"  # Ruta fija al archivo CSV
    try:
        # Intenta leer el archivo CSV con el delimitador ';'
        df = pd.read_csv(file_path, delimiter=';', on_bad_lines='skip')
        
        # Renombrar columnas para que coincidan con los nombres esperados
        column_mapping = {
            "GROUP": "GROUP",
            "CODE": "CODE",
            "NAME": "NAME",
            "YEAR": "YEAR",
            "ANTIGEN": "ANTIGEN",
            "ANTIGEN_DESCRIPTION": "ANTIGEN_DESCRIPTION",
            "COVERAGE_CATEGORY": "COVERAGE_CATEGORY",
            "COVERAGE_CATEGORY_DESCRIPTION": "COVERAGE_CATEGORY_DESCRIPTION",
            "TARGET_NUMBER": "TARGET_NUMBER",
            "DOSES": "DOSES",
            "COVERAGE": "COVERAGE"
        }
        df.rename(columns=column_mapping, inplace=True)
    except Exception as e:
        st.error(f"Error al leer el archivo: {e}")
        st.stop()
    # Limpiar espacios en blanco en los nombres de las columnas
    df.columns = df.columns.str.strip()
    return df

# Título y descripción
st.title("Tabla de Cobertura de Inmunización")
st.markdown("""
Esta aplicación muestra la cobertura de inmunización por país y año.
Usa los controles de la barra lateral para filtrar la información.
""")

# Cargar datos
df = cargar_datos()

# Verificar que existan las columnas necesarias
required_columns = ["ANTIGEN", "YEAR", "NAME", "COVERAGE", "COVERAGE_CATEGORY"]
if not set(required_columns).issubset(df.columns):
    st.error(
        f"El DataFrame debe contener las columnas {required_columns}. "
        f"Columnas detectadas: {df.columns.tolist()}"
    )
    st.stop()

# --- Filtros en la parte superior en una misma línea ---
st.markdown("### Filtros")
col1, col2, col3, col4 = st.columns(4)

with col1:
    coverage_categories = sorted(df["COVERAGE_CATEGORY"].dropna().unique())
    selected_coverage_category = st.selectbox(
        "Categoría", options=coverage_categories
    )

with col2:
    # Filtrar el DataFrame según la categoría seleccionada para obtener los antígenos
    df_filtered_by_category = df[df["COVERAGE_CATEGORY"] == selected_coverage_category]
    antigens = sorted(df_filtered_by_category["ANTIGEN"].dropna().unique())
    selected_antigen = st.selectbox("Antígeno", antigens)

with col3:
    min_year, max_year = int(df["YEAR"].min()), int(df["YEAR"].max())
    year_range = st.slider(
        "Años", min_value=min_year, max_value=max_year, value=(2010, 2024)
    )

with col4:
    countries = sorted(df["NAME"].dropna().unique())
    selected_countries = st.multiselect(
        "Países", options=countries
    )

# Filtrado final del DataFrame
df_filtered = df[
    (df["ANTIGEN"] == selected_antigen) &
    (df["COVERAGE_CATEGORY"] == selected_coverage_category) &
    (df["YEAR"] >= year_range[0]) &
    (df["YEAR"] <= year_range[1])
]

if selected_countries:
    df_filtered = df_filtered[df_filtered["NAME"].isin(selected_countries)]

if df_filtered.empty:
    st.warning("No hay datos para los filtros seleccionados.")
else:
    # Pivotar el DataFrame: filas = País, columnas = Año, valores = Cobertura
    df_pivot = df_filtered.pivot(index="NAME", columns="YEAR", values="COVERAGE")

    # Formatear los valores para evitar decimales innecesarios
    def format_value(val):
        if pd.isna(val):
            return "NaN"  # Mostrar "NaN" como texto
        elif isinstance(val, float):
            return f"{val:.2f}".rstrip('0').rstrip('.')  # Elimina ceros innecesarios
        else:
            return str(val)

    df_pivot = df_pivot.applymap(format_value)

    # Función para aplicar el degradado de colores (0 = Rojo, 100 = Blanco)
    def color_gradient(val):
        if val == "NaN":  # Ignorar valores "NaN" para no aplicar color
            return 'background-color: white'
        else:
            # Convertir el valor a float para calcular el degradado
            val = float(val) if val.replace('.', '', 1).isdigit() else 0
            # Degradado de rojo (0) a blanco (100)
            red_intensity = int(255 * (val / 100))
            color = f'background-color: rgba(255, {red_intensity}, {red_intensity}, 1)'
            return color

    styled_df = df_pivot.style.applymap(color_gradient)

    st.subheader("Tabla de Cobertura de Inmunización")

    # --- LEYENDA ---
    # Agrega aquí la leyenda del gradiente antes de mostrar la tabla
    legend_html = """
    <div style="display: flex; align-items: center; margin-bottom: 10px;">
        <span style="margin-right: 10px; font-weight: bold;">0</span>
        <div style="
            width: 200px;
            height: 20px;
            background: linear-gradient(to right, red, white);
            margin-right: 10px;">
        </div>
        <span style="margin-right: 10px; font-weight: bold;">100</span>
        <span style="font-style: italic; margin-left: 10px;">% Coverage</span>
    </div>
    """
    st.markdown(legend_html, unsafe_allow_html=True)

    # Mostrar la tabla pivotada con estilo
    st.markdown(styled_df.to_html(), unsafe_allow_html=True)

    # Botón para descargar datos como CSV
    st.download_button(
        label="Descargar tabla como CSV",
        data=df_filtered.to_csv(index=False),
        file_name="tabla_filtrada.csv",
        mime="text/csv"
    )

# Pie de página
st.write("")
st.write("")
