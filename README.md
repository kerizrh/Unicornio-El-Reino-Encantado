# Unicornio: El Reino Encantado

Juego de plataformas 2D hecho en **Godot 4.7**. Un unicornio debe subir por las murallas del reino
hasta el **Cristal del Reino** antes de 120 segundos, esquivando las rocas que lanza el
**troll de la montaña**, la **lluvia de fuego** y los **lobos sombríos**.

## Descargar y jugar

### En Android
1. Descarga [`apk/UnicornioReino.apk`](apk/UnicornioReino.apk) (botón **Download raw file** en GitHub).
2. Ábrelo en el celular. Si Android lo pide, permite **instalar apps de fuentes desconocidas** para
   el navegador o el administrador de archivos.
3. Requiere Android 7.0 o superior. Funciona en celulares de 64 y 32 bits.

### En PC (proyecto de Godot)
1. Descarga el repositorio (**Code → Download ZIP**) o clónalo con `git clone`.
2. Abre **Godot 4.7** → **Importar** → selecciona `project.godot`.
3. Pulsa **F5** para jugar.

## Controles
- **← / →** (o A / D): moverse · **Espacio** (o ↑): saltar · botón **II**: pausa.
- En Android aparecen botones táctiles.

## Niveles
1. **Las Murallas del Reino** (nivel principal, el que pide la guía): 7 pisos de murallas más la cima,
   con tramos de distinto largo, huecos y alineación alternada; la cámara sube contigo.
   El troll lanza rocas que ruedan y caen por los huecos de piso en piso.
   Hay que **saltar sobre el troll** para tocar el cristal que custodia.
   - **Gemas arcoíris** (+5 s) y un **corazón** (+1 vida) en zonas peligrosas.
   - **Rocas saltarinas** (moradas) que avanzan dando botes.
   - **Furia del troll** desde los 70 s restantes: ruge, lanza más rápido, llueve más fuego y la música se acelera.
   - **Aviso "!"** antes de cada bola de fuego, **sacudida de cámara** al recibir golpes y un **hongo atajo**.
2. **La Torre de las Nubes** (se desbloquea al ganar el nivel 1): subida vertical con plataformas
   **móviles**, **cristales frágiles** que se rompen al pisarlos (se ve su silueta y reaparecen),
   **hongos trampolín**, **murciélagos** que se lanzan en picada y el troll lanzando rocas desde la cima.
   Al ganar el nivel 1, el Cristal le da al unicornio su **poder**: en este nivel puede eliminar
   **lobos y murciélagos saltando sobre ellos** (su estela se vuelve turquesa).
   Incluye también gemas, corazones, hongo atajo, rocas saltarinas y la furia del troll.

> La guía pide un juego "de un solo nivel": el nivel 1 cumple todos los criterios por sí solo;
> el nivel 2 es un añadido opcional que se desbloquea al ganar.

## Cómo cumple la guía
| Criterio | Dónde está |
|---|---|
| 1. Plataforma 2D, un nivel | `niveles/level_1.tscn` |
| 2. Avatar propio | Unicornio (`personaje/`, arte en `assets/fantasia/`) con animaciones quieto/caminar/salto |
| 3. NPCs propios | Troll (`enemigos/troll.tscn`), roca, bola de fuego, lobo sombrío, murciélago |
| 4. Mecánicas y caída por física | `personaje/personaje.gd` (CharacterBody2D + gravedad) |
| 5. Flechas + Espacio | Proyecto → Configuración → Mapa de entrada (`izquierda`, `derecha`, `saltar`) |
| 6. NPCs que corren / caen / ruedan | Lobo **corre** al verte (`lobo.gd`), bolas de fuego **caen** (`lluvia_fuego.gd`), rocas **ruedan** (RigidBody2D, `roca.gd`) |
| 7. GameController | `niveles/GameController.gd`: tiempo 120 s, barra de vida (`ui/canvas_layer_ui.*`), resta vida por choque, pantalla **Game Over** con motivo y botón **Reintentar** (`ui/game_over.tscn`), pantalla de victoria (`ui/scene_finish.tscn`) |
| 8. Música en bucle | Nivel: `reino_encantado.wav`; victoria: `victoria.wav`; derrota: `derrota.wav` (en `assets/audio/musica/`, bucle con `niveles/musica.gd`) |
| 9. Dispositivo físico | `apk/UnicornioReino.apk` (preset **Android** de `export_presets.cfg`) |

## Estructura
| Carpeta | Contenido |
|---|---|
| `niveles/` | Niveles, GameController, música y límites del nivel |
| `personaje/` | Unicornio y cámara |
| `enemigos/` | Troll, rocas, bolas de fuego, lobos, murciélagos |
| `suelos/` | Murallas, tramos de ancho ajustable, nubes, plataformas móviles y frágiles, hongos |
| `objetos/` | Gemas y corazones |
| `ui/` | Interfaz, pausa, Game Over, victoria, controles táctiles |
| `assets/` | Arte y audio |
| `herramientas/` | Scripts de Python que generaron el arte y la música originales |
| `apk/` | APK listo para instalar |

## Volver a generar el arte o la música
Requiere Python 3 con `pillow` y `numpy`. Desde la raíz del repositorio:
```
python herramientas/generar_arte.py .
python herramientas/generar_arte_nivel2.py .
python herramientas/generar_arte_extras.py .
python herramientas/generar_audio.py .
```

## Exportar el APK de nuevo
En Godot: **Proyecto → Exportar → Android → Exportar proyecto**. Hace falta instalar las plantillas
de exportación de Godot 4.7.2 y configurar el SDK de Android y el JDK en
**Editor → Configuración del editor → Exportar → Android**.

## Créditos
- Proyecto base de la tutoría: «Conejo Saltarín móvil» (Ing. Edenilson López, IDS-UES), basado en findemor «aprender-godot» (MIT).
- Arte y música del unicornio, troll, lobos, murciélagos, fuego, escenarios e interfaz: originales,
  generados con los scripts de `herramientas/`.
- Nubes decorativas: Kenney «Scribble Platformer» (CC0).
