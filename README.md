# Checklist Aguilar 2025

Aplicación Streamlit para consultar, capturar y exportar checklists de expedientes Aguilar 2025.

## Uso local

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Publicarla para consulta en línea

Opción sencilla:

1. Sube esta carpeta a un repositorio de GitHub.
2. Entra a Streamlit Community Cloud.
3. Crea una app nueva seleccionando el repositorio.
4. Indica `app.py` como archivo principal.
5. Publica la app y comparte el enlace.

También puede desplegarse en Render, Railway, Hugging Face Spaces o un servidor propio que ejecute:

```bash
streamlit run app.py --server.address 0.0.0.0 --server.port 8501
```

## Funciones incluidas

- Checklists por tipo de crédito.
- Casos especiales activables para casados, cónyuge, mancomunado o coacreditado.
- Búsqueda rápida por requisito.
- Comentarios por documento.
- Barra de avance.
- Exportación TXT y CSV.

## Fuente

La base de datos fue armada con referencia en los formatos PDF 2025 proporcionados para:

- Infonavit Tradicional y Total
- Infonavit Línea III
- Cofinavit
- Bancario
- Fovissste
- Fovissste para Todos
- Pensiona2
- Contado
