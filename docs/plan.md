# Plan de port a Minecraft Java 26.3

Este proyecto se desarrollará de a poco, en varias sesiones. Cada sesión abordará
una tarea acotada de un issue; un issue grande se dividirá antes de ampliar el alcance.
No se intentará completar toda la hoja de ruta en una sola sesión.

## Objetivo y límites

Mantener Minecraft 26.3 y portar Cobblemon conservando su comportamiento y sus datos.
El cargador del servidor todavía no está confirmado. Fabric se usó únicamente para
las comprobaciones preliminares; no se ha cambiado el servidor del usuario.

`main` conserva la base importada de GitLab. Los ajustes iniciales y este plan están
en `port/26.3`. Todavía no existe un JAR jugable validado para 26.3.

## Trabajo por etapas

| Issue | Entregable | Dependencias | Estado |
| --- | --- | --- | --- |
| [#1](https://github.com/mariam6697/cobblemon-26.3/issues/1) | Obtener una compilación base reproducible y habilitar CI | — | Pendiente |
| [#2](https://github.com/mariam6697/cobblemon-26.3/issues/2) | Confirmar cargador del servidor y auditar dependencias para 26.3 | — | Pendiente |
| [#3](https://github.com/mariam6697/cobblemon-26.3/issues/3) | Migrar la compilación a 26.3 y registrar los errores reales | #1, #2 | Pendiente |
| [#4](https://github.com/mariam6697/cobblemon-26.3/issues/4) | Adaptar entidades, registros y serialización del núcleo | #3 | Pendiente |
| [#5](https://github.com/mariam6697/cobblemon-26.3/issues/5) | Migrar bloques, componentes y generación del mundo | #3 | Pendiente |
| [#6](https://github.com/mariam6697/cobblemon-26.3/issues/6) | Mostrar un Pokémon y adaptar renderizado e interfaz | #4 | Pendiente |
| [#7](https://github.com/mariam6697/cobblemon-26.3/issues/7) | Completar captura, equipo y cajas con persistencia | #4, #5, #6 | Pendiente |
| [#8](https://github.com/mariam6697/cobblemon-26.3/issues/8) | Recuperar un combate completo con Showdown | #7 | Pendiente |
| [#9](https://github.com/mariam6697/cobblemon-26.3/issues/9) | Validar multijugador y preparar una primera versión experimental | #5, #6, #7, #8 | Pendiente |

Los issues incluyen tareas y criterios de aceptación. La estimación de esfuerzo
se revisará cuando el issue #3 produzca el inventario real del compilador. Los
issues de subsistemas son puntos de partida y se dividirán si resultan demasiado grandes.

## Estado al cerrar la sesión de planificación — 2026-10-18

Hecho:

- Repositorio importado con historial, licencia y créditos del upstream.
- Rama `port/26.3` creada; primeros ajustes conservados como trabajo preparatorio.
- Versión Java del compilador tomada de la configuración.
- Selección opcional de plataformas mediante `enabled_platforms`; por defecto se conservan ambas.
- Constantes de Enter del widget de diálogo cambiadas de GLFW a `InputConstants`.
- Nueve issues creados, con dependencias y criterios de aceptación.

Validado:

- Las convenciones de Gradle modificadas compilan con Java 21.
- Una prueba aislada compila contra Minecraft 26.3 con Java 25, Gradle 9.6.0,
  Architectury Loom 1.17.493 sin remapeo, Kotlin 2.4.21, Fabric Loader 0.19.5 y
  Fabric API 0.163.0+26.3.
- En esa prueba existen las constantes de Enter, `DataComponents.COMPOSTABLE`
  y la clase `net.fabricmc.fabric.api.item.v1.BlockTransformerHelper`.
- Las constantes de Enter también existen en la base 1.21.1.
- `git diff --check` pasa para los cambios iniciales.

Pendiente:

- La compilación completa de la base se detuvo para pasar a planificación; no tiene resultado validado.
- No se ha intentado compilar Cobblemon completo contra 26.3.
- No se ha abierto un cliente ni probado captura, combate o servidor dedicado.
- No se ha configurado GitHub Actions todavía.
- Falta confirmar el cargador del servidor antes de fijar la migración.

## Próxima sesión propuesta

Tomar únicamente la primera parte del [issue #1](https://github.com/mariam6697/cobblemon-26.3/issues/1):
obtener una compilación de referencia y documentar su resultado. La caché local se
conservó en `.gradle/user-home`; los registros anteriores están en `.ignored/porting-logs/`.
Dejar CI para otro incremento si completar la referencia consume la sesión.

Al cerrar cada incremento: guardar cambios revisables, registrar qué se probó,
actualizar el issue y dejar un próximo paso concreto. No marcar un issue como
terminado por haber completado solo una de sus subtareas.

Para detalles técnicos y fuentes oficiales, consultar [las notas de migración](porting-26.3.md).
