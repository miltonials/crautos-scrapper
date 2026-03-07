# Guía de Contribución para crautos-scraper

¡Gracias por tu interés en contribuir a `crautos-scraper`! Este proyecto es de código abierto para fines educativos y de investigación. Toda ayuda para optimizar el código, mejorar la limpieza de datos o hacer la extracción más eficiente es bienvenida.

## Acuerdo de Licencia de Contribución
Al enviar un Pull Request (PR) a este repositorio, aceptas que tus contribuciones se integrarán y distribuirán bajo la misma licencia del proyecto: **PolyForm Noncommercial License 1.0.0**. Esto asegura que el proyecto en su totalidad se mantenga libre de uso comercial.

## Cómo Contribuir

Si deseas aportar código, sigue estos pasos:

1. Haz un Fork del repositorio.
2. Crea una rama para tu característica o corrección de error:
   git checkout -b feature/nombre-de-tu-mejora
3. Escribe tu código. Asegúrate de que siga el estilo del proyecto (ver sección "Estándares de Código").
4. Haz commit de tus cambios con mensajes claros y descriptivos:
   git commit -m "Agrega limpieza para el formato de precios en colones"
5. Haz push a tu rama:
   git push origin feature/nombre-de-tu-mejora
6. Abre un Pull Request (PR) en este repositorio describiendo detalladamente qué cambiaste y por qué.

## Estándares de Código

Para mantener el proyecto limpio y fácil de leer, te pedimos que sigas estas pautas:
- Asincronía: Este es un scraper concurrente. Si agregas nuevas peticiones de red, asegúrate de usar `httpx` de forma asíncrona (`await client.get(...)`) y respeta el semáforo (`async with self.semaphore:`).
- Manejo de Errores: Envuelve las peticiones de red y el parseo de HTML en bloques `try/except` para evitar que el scraper se detenga por completo si una página falla o tiene un formato inesperado.
- Nomenclatura: Usa `snake_case` para variables y funciones, y `PascalCase` para las clases.
- Comentarios: Si utilizas expresiones regulares (RegEx) complejas o lógica de parseo poco convencional, por favor agrega un comentario breve explicando qué hace.

## Reporte de Errores y Sugerencias

Si no quieres escribir código pero encontraste un error o tienes una idea:
1. Ve a la pestaña de "Issues".
2. Verifica que nadie más haya reportado lo mismo.
3. Abre un nuevo Issue. Si es un error (bug), incluye los pasos para reproducirlo, el comportamiento esperado y el mensaje de error de la consola si aplica.

¡Gracias por ayudar a mejorar este proyecto!
