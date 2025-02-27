import streamlit as st
import pandas as pd

# Configuración inicial de la página
st.set_page_config(
    page_title="Immunization Coverage Dashboard",
    layout="wide"
)

@st.cache_data
def cargar_datos():
    """
    Carga y limpia los datos del archivo CSV desde la ruta especificada.
    """
    file_path = "data/coverage-data.csv"  # Ruta fija al archivo CSV
    try:
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
            "COVERAGE": "COVERAGE",
            
        }
        df.rename(columns=column_mapping, inplace=True)
    except Exception as e:
        st.error(f"Error al leer el archivo: {e}")
        st.stop()

    # Limpiar espacios en blanco en los nombres de las columnas
    df.columns = df.columns.str.strip()
    return df

# Título y descripción
st.title("Immunization Coverage Dashboard")
st.markdown("""
This interactive dashboard provides a comprehensive view of immunization coverage data by country and year. You can filter the data using the controls at the top based on Coverage Category, Antigen, Year Range, WHO Region, and Countries.  
The dashboard displays a pivot table with color gradients that visually represent coverage levels, making it easier to analyze trends and differences across regions and years.

At the bottom of the page, you will find the **About the Project** section, which includes additional details about the dashboard, the data source, a disclaimer, and creator contact information.
""")

# Cargar datos
df = cargar_datos()

# Verificar columnas necesarias
required_columns = [
    "ANTIGEN",
    "YEAR",
    "NAME",
    "COVERAGE",
    "COVERAGE_CATEGORY",
    "ANTIGEN_DESCRIPTION",
    "WHO REGIONS"  # Asegúrate de que esta columna exista en tu CSV
]
if not set(required_columns).issubset(df.columns):
    st.error(
        f"El DataFrame debe contener las columnas {required_columns}. "
        f"Columnas detectadas: {df.columns.tolist()}"
    )
    st.stop()

# --- Filtros en la parte superior en una misma línea (5 columnas) ---
col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    coverage_categories = sorted(df["COVERAGE_CATEGORY"].dropna().unique())
    selected_coverage_category = st.selectbox("Coverage Category", options=coverage_categories)

with col2:
    # Filtrar por categoría para obtener los antígenos disponibles
    df_filtered_by_category = df[df["COVERAGE_CATEGORY"] == selected_coverage_category]
    antigens = sorted(df_filtered_by_category["ANTIGEN"].dropna().unique())
    selected_antigen = st.selectbox("Antigen", options=antigens)

with col3:
    min_year, max_year = int(df["YEAR"].min()), int(df["YEAR"].max())
    year_range = st.slider("Year Range", min_value=min_year, max_value=max_year, value=(2010, 2024))

with col4:
    # Filtro de WHO Region (selección única, con opción "All"), basado en la categoría
    df_filtered_by_category = df[df["COVERAGE_CATEGORY"] == selected_coverage_category]
    who_regions_list = sorted(df_filtered_by_category["WHO REGIONS"].dropna().unique())
    who_regions_options = ["All"] + who_regions_list
    selected_who_region = st.selectbox("WHO Region", options=who_regions_options)

with col5:
    # Filtro de Países: depende del filtro de WHO Region
    if selected_who_region == "All":
        available_countries = sorted(df["NAME"].dropna().unique())
    else:
        available_countries = sorted(df[df["WHO REGIONS"] == selected_who_region]["NAME"].dropna().unique())
    selected_countries = st.multiselect("Countries", options=available_countries)

# Obtener la descripción del antígeno seleccionado
antigen_description_arr = df_filtered_by_category.loc[
    df_filtered_by_category["ANTIGEN"] == selected_antigen,
    "ANTIGEN_DESCRIPTION"
].unique()

if len(antigen_description_arr) > 0:
    antigen_description_text = antigen_description_arr[0]
else:
    antigen_description_text = "No hay descripción disponible para este antígeno."

# Filtrado final del DataFrame
df_filtered = df[
    (df["ANTIGEN"] == selected_antigen) &
    (df["COVERAGE_CATEGORY"] == selected_coverage_category) &
    (df["YEAR"] >= year_range[0]) &
    (df["YEAR"] <= year_range[1])
]

if selected_countries:
    df_filtered = df_filtered[df_filtered["NAME"].isin(selected_countries)]

# Aplicar filtro de WHO Region solo si no se seleccionó "All"
if selected_who_region != "All":
    df_filtered = df_filtered[df_filtered["WHO REGIONS"] == selected_who_region]

if df_filtered.empty:
    st.warning("No hay datos para los filtros seleccionados.")
else:
    # Pivotar el DataFrame: filas = País, columnas = Año, valores = Cobertura
    df_pivot = df_filtered.pivot(index="NAME", columns="YEAR", values="COVERAGE")

    # Función para formatear valores
    def format_value(val):
        if pd.isna(val):
            return "NaN"
        elif isinstance(val, float):
            return f"{val:.2f}".rstrip('0').rstrip('.')
        else:
            return str(val)
    df_pivot = df_pivot.applymap(format_value)

    # Función para aplicar el degradado de colores
    def color_gradient(val):
        if val == "NaN":
            return 'background-color: white'
        else:
            val = float(val) if val.replace('.', '', 1).isdigit() else 0
            red_intensity = int(255 * (val / 100))
            return f'background-color: rgba(255, {red_intensity}, {red_intensity}, 1)'
    styled_df = df_pivot.style.applymap(color_gradient)

    # Mostrar leyenda (izquierda) y descripción del antígeno (derecha)
    col_legend, col_desc = st.columns([1, 2])

    with col_legend:
        legend_html = """
        <div style="display: flex; align-items: center; margin-bottom: 10px;">
            <span style="margin-right: 10px; font-weight: bold;">0</span>
            <div style="width: 200px; height: 20px; background: linear-gradient(to right, red, white); margin-right: 10px;"></div>
            <span style="margin-right: 10px; font-weight: bold;">100</span>
            <span style="font-style: italic; margin-left: 10px;">% Coverage</span>
        </div>
        """
        st.markdown(legend_html, unsafe_allow_html=True)

    with col_desc:
        st.subheader("Antigen Description")
        st.write(antigen_description_text)

    st.markdown(styled_df.to_html(), unsafe_allow_html=True)

    st.download_button(
        label="Download CSV",
        data=df_filtered.to_csv(index=False),
        file_name="filtered_table.csv",
        mime="text/csv"
    )

# --- About the Project Section ---
st.markdown("---")
st.markdown("### About the Project")
st.markdown("""
This dashboard was developed to provide an interactive visualization of immunization coverage data by country and year.

**Data Source:**  
Data is sourced from the [World Health Organization's Immunization Data portal](https://immunizationdata.who.int/).

**Disclaimer:**  
This dashboard is for informational purposes only and does not represent an official report by the World Health Organization.

**Created by:**  
**Cesar Vera**  
Data Analyst and Visualization Specialist              
Email: [cesarvera6@gmail.com](mailto:cesarvera6@gmail.com)  
Portfolio: [https://cesarvera66.github.io/portfolio_cesarvera/](https://cesarvera66.github.io/portfolio_cesarvera/)
""")