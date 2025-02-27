# Dashboard de Cobertura de Inmunización

Este proyecto es un **dashboard interactivo** desarrollado con [Streamlit](https://streamlit.io/) para visualizar y analizar datos de cobertura de inmunización. Los datos utilizados provienen de la [plataforma oficial de la OMS (Organización Mundial de la Salud)](https://immunizationdata.who.int/).

## Tabla de Contenidos

1. [Descripción General](#descripción-general)  
2. [Requisitos](#requisitos)  
3. [Estructura del Proyecto](#estructura-del-proyecto)  
4. [Instalación](#instalación)  
5. [Uso](#uso)  
6. [Configuración de Streamlit](#configuración-de-streamlit)  
7. [Licencia](#licencia)  
8. [Autor](#autor)  

---

## Descripción General

Este dashboard permite filtrar y visualizar datos sobre la cobertura de inmunización en distintos países, años y antígenos. A través de un degradado de color, se muestra de forma intuitiva el nivel de cobertura para cada combinación de país y año. Además, se proporciona la opción de descargar los datos filtrados en formato CSV para su posterior análisis o reporte.

### Funcionalidades Principales

- **Filtros interactivos**: Permite seleccionar la categoría de cobertura, antígeno, rango de años y países.
- **Tabla pivotada**: Muestra la información en formato de tabla, con países en filas y años en columnas.
- **Visualización con degradado de color**: Indica la cobertura de inmunización de 0 (rojo) a 100 (blanco).
- **Exportación de datos**: Botón para descargar los datos filtrados en formato CSV.

---

## Requisitos

- **Python 3.x**  
- [**Streamlit**](https://streamlit.io/)  
- [**Pandas**](https://pandas.pydata.org/)  

Opcionalmente, se recomienda el uso de un **entorno virtual** para mantener las dependencias organizadas.

---

## Estructura del Proyecto

La estructura del repositorio es la siguiente:

```
DASHBOARD-IMMUNIZATION-COVERAGE/
│
├── .streamlit/
│   └── config.toml            # Configuración adicional de Streamlit (tema, layout, etc.)
│
├── data/
│   └── coverage-data.csv      # Archivo CSV con los datos de cobertura
│
├── app.py                     # Archivo principal de la aplicación Streamlit
├── LICENSE                    # Archivo de licencia
├── README                     # Este archivo (README.md)
├── requirements               # Archivo con las dependencias (requirements.txt)
└── ...
```

- **`.streamlit/config.toml`**: Contiene la configuración personalizada de la aplicación (por ejemplo, tema, diseño, título, etc.).  
- **`data/coverage-data.csv`**: Archivo CSV con los datos de cobertura de inmunización (separador `;`).  
- **`app.py`**: Código principal de la aplicación Streamlit.  
- **`LICENSE`**: Archivo de licencia del proyecto (por ejemplo, MIT).  
- **`requirements`**: Archivo con la lista de dependencias necesarias (puede ser `requirements.txt`).

---

## Instalación

1. **Clonar el repositorio:**

   ```bash
   git clone https://github.com/cesarvera66/Dashboard-immunization-coverage.git
   cd Dashboard-immunization-coverage
   ```

2. **Crear y activar un entorno virtual (opcional pero recomendado):**

   ```bash
   python -m venv venv
   source venv/bin/activate   # En Windows: venv\Scripts\activate
   ```

3. **Instalar dependencias:**

   ```bash
   pip install -r requirements
   ```
   > Asegúrate de que el archivo `requirements` contenga las librerías `streamlit` y `pandas`, entre otras que uses en tu proyecto.

---

## Uso

Para ejecutar la aplicación, asegúrate de que el archivo `coverage-data.csv` se encuentre en la carpeta `data`, luego corre el siguiente comando:

```bash
streamlit run app.py
```

Esto abrirá el dashboard en tu navegador predeterminado (por lo general en `http://localhost:8501`).

Una vez en la aplicación:

1. **Selecciona** la categoría de cobertura.  
2. **Elige** el antígeno.  
3. **Ajusta** el rango de años.  
4. **(Opcional)** Filtra uno o varios países.  
5. Observa la tabla con la cobertura de inmunización y el degradado de color.  
6. **Descarga** los datos filtrados en formato CSV si lo deseas.

---

## Configuración de Streamlit

El archivo `.streamlit/config.toml` permite personalizar la apariencia y el comportamiento de la aplicación. Ejemplo de configuración:

```toml
[theme]
primaryColor = "#FF4B4B"
backgroundColor = "#FFFFFF"
secondaryBackgroundColor = "#F0F2F6"
textColor = "#262730"
font = "sans serif"

[server]
headless = true
enableCORS = false
port = 8501
```

Modifica estos valores según tus preferencias para personalizar la interfaz (colores, fuentes, etc.).

---

## Licencia

Este proyecto se distribuye bajo la licencia [MIT](LICENSE). Puedes consultar el archivo `LICENSE` para más detalles.

---

## Autor

**Cesar Vera**  
[GitHub](https://github.com/cesarvera66)  
[LinkedIn](https://www.linkedin.com/in/cesar-alfonso-vera-medina-719250189/)  

---

¡Gracias por usar y contribuir a este proyecto! Si tienes preguntas, comentarios o sugerencias, no dudes en abrir un _issue_ o enviar un _pull request_.