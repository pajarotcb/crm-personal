# Guía de masajes por zona de dolor — Plan

## Alcance (definido)
- **Público:** familia y entorno amplio (adultos, jóvenes, gente que practica deporte).
- **Tono:** español, algo más técnico (nombres de músculos, mecanismo del dolor referido), siempre legible.
- **Se masajea:** uno mismo **y a otros** (cada técnica con variante "auto" y "a otro").
- **Salida:** PDF doble formato — pantalla (con links/índice navegable) e imprimible (A4, márgenes de encuadernación, sin fondos pesados).
- **Piloto:** Cuello y hombros.
- **Fuera de alcance:** diagnóstico, fisiatría, osteopatía, kinesiología, homeopatía.

## Estructura del PDF
A. Cómo usar la guía · B. Principios del masaje casero · C. Señales de alarma ·
D. Capítulos por zona · E. Escenarios por actividad · F. Rutinas express · G. Índice por síntoma

## Zonas (orden de producción)
1. Cuello y hombros (PILOTO)
2. Espalda alta y paletas
3. Zona lumbar
4. Glúteos y cadera
5. Brazo, codo, antebrazo y mano
6. Muslo y rodilla
7. Pantorrilla y pie
8. Cabeza y mandíbula

## Fases
1. Definición (hecho) → 2. Plantilla + piloto → 3. Revisión del piloto →
4. Producción por tandas → 5. Secciones transversales → 6. Armado y revisión PDF

## Parámetros a validar con fuentes (no son definitivos)
- Presión sostenida en punto gatillo: ~30–90 s, intensidad 5–6/10.
- Amasado/fricción: 2–3 min por músculo.
- Sesión por zona: 5–10 min; 1–2 veces/día máximo.

## Ilustraciones
SVG propio, un solo estilo (cuerpo gris, músculo en color, dolor referido en rojo,
punto gatillo en círculo). No se usan imágenes de atlas con derechos.

## Estructura de carpetas
- `capitulos/`  un .md por zona (plantilla: `capitulos/_plantilla.md`)
- `ilustraciones/`  SVG por zona
- `fuentes/`  bibliografía y notas de contraste
- `build/`  scripts de exportación a PDF (pantalla e imprimible)
