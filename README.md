# crautos-scraper

Extractor asíncrono en Python para recopilar información estructurada de vehículos usados en Costa Rica desde crautos.com. 

⚠️ DESCARGO DE RESPONSABILIDAD LEGAL Y ÉTICA
Este proyecto ha sido desarrollado estrictamente con fines educativos, de aprendizaje personal y de investigación. 
- No está diseñado para realizar ataques de denegación de servicio (DDoS) ni para saturar los servidores del sitio web objetivo.
- El autor no se hace responsable del mal uso de esta herramienta, ni de las consecuencias derivadas de violar los Términos de Servicio de crautos.com.
- Se prohíbe el uso de este código y de los datos generados por el mismo para cualquier fin comercial o de lucro.

## Características

- Extracción Asíncrona: Utiliza asyncio y httpx para procesar múltiples páginas concurrentemente, reduciendo el tiempo de ejecución.
- Limpieza de Datos Integrada: Convierte strings con texto (ej. "91,500 kms") en datos numéricos puros (ej. 91500).
- Manejo de Codificación: Resuelve problemas de caracteres especiales forzando la decodificación UTF-8.
- Exportación a CSV: Genera automáticamente un DataFrame de pandas y lo exporta a un archivo CSV.

## Requisitos e Instalación

1. Asegúrate de tener Python 3.8 o superior instalado.
2. Clona este repositorio:
   git clone https://github.com/miltonials/crautos-scraper.git
   cd crautos-scraper
3. Instala las dependencias necesarias:
   pip install httpx beautifulsoup4 pandas nest-asyncio

## Instrucciones de Uso

El scraper puede ejecutarse de dos maneras: a través de la terminal (script tradicional) o mediante un entorno interactivo como Jupyter Notebook / Google Colab.

Opción A: Uso en Terminal (Script .py)
1. Guarda el código principal en un archivo llamado `scraper.py`.
2. Al final de tu archivo `scraper.py`, asegúrate de tener el bloque de ejecución estándar:

   if __name__ == "__main__":
       import asyncio
       asyncio.run(main())

3. Ejecuta el script desde tu terminal:
   python scraper.py
4. El programa imprimirá el progreso y generará un archivo `crautos_completo.csv` en la misma carpeta.

Opción B: Uso en Jupyter Notebook / Colab
Dado que estos entornos ya corren un ciclo de eventos asíncrono de fondo, no puedes usar `asyncio.run()`. 
1. Pega el código en una celda.
2. Al final, llama a la función principal directamente con `await`:

   await main()

3. Ejecuta la celda. El archivo CSV se guardará en el entorno virtual de tu notebook.

## Contribuciones

¡Las contribuciones son bienvenidas! Por favor, lee el archivo CONTRIBUTING.md para conocer los detalles sobre nuestro código de conducta y el proceso para enviarnos Pull Requests.

## Licencia y Derechos de Autor

Required Notice: Copyright (c) 2026 [Tu Nombre o Usuario de GitHub]

Este proyecto está licenciado bajo la PolyForm Noncommercial License 1.0.0. 
Se permite el uso personal, educativo y de investigación. Queda estrictamente prohibido su uso comercial. Para más detalles, consulta el archivo LICENSE incluido en este repositorio o visita https://polyformproject.org/licenses/noncommercial/1.0.0.
