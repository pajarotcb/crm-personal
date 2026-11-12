#!/usr/bin/env python3
"""Genera el texto de Carta Poder + mensaje de WhatsApp + link mailto.

Uso individual:
  python3 generar_poderes.py --poderdante "Juan Pérez" --lote-poderdante 123 \
      --apoderado "Ana Gómez" --lote-apoderado 45 --celular 5491155550000

Uso por lote (CSV con columnas: poderdante,dni,lote_poderdante,apoderado,lote_apoderado,celular):
  python3 generar_poderes.py --csv poderes.csv

Salida: carpeta ./salida/ con un .txt por poder y registro.csv (control de cupos).
"""
import argparse, csv, os, sys, urllib.parse
from collections import Counter

DESTINO = "secretariabavillage@gmail.com"
FECHA_ASAMBLEA = "26 de noviembre de 2026"
FECHA_APERTURA = "23 de noviembre de 2026"  # apertura del registro de poderes
MAX_PODERES = 10
ASUNTO = "Carta Poder - Lote {lp} - {pod}"

CARTA = """CARTA PODER

Fecha: {fecha}

Yo, {pod}, DNI {dni}, propietario del lote {lp}, otorgo poder a {apo}, propietario del lote {la}, para que me represente y vote en mi nombre en la Asamblea del {asamblea}.

Firma: {pod}
DNI: {dni}
Lote: {lp}"""

WHATSAPP = """Hola {nombre}! Gracias por tu apoyo. Para dejar tu voto representado hacé esto (2 minutos):

1) Abrí tu mail **desde la casilla donde recibís las expensas** (tiene que ser esa, es la registrada en la administración).
2) Mandá un mail a {destino} con el asunto: {asunto}
3) Pegá este texto como cuerpo del mail:

{carta}

Listo, eso es todo. Si algo no te sale, avisame."""

def fecha_hoy():
    meses = "enero febrero marzo abril mayo junio julio agosto septiembre octubre noviembre diciembre".split()
    import datetime as d
    h = d.date.today()
    return f"{h.day} de {meses[h.month-1]} de {h.year}"

def armar(row, fecha=None):
    ctx = dict(pod=row["poderdante"].strip(), dni=(row.get("dni") or "xxxxxxxx").strip(), lp=row["lote_poderdante"].strip(),
               apo=row["apoderado"].strip(), la=row["lote_apoderado"].strip(),
               fecha=fecha or fecha_hoy(), asamblea=FECHA_ASAMBLEA)
    carta = CARTA.format(**ctx)
    asunto = ASUNTO.format(**ctx)
    mailto = "mailto:%s?subject=%s&body=%s" % (
        DESTINO, urllib.parse.quote(asunto), urllib.parse.quote(carta))
    wa = WHATSAPP.format(nombre=ctx["pod"].split()[0], destino=DESTINO,
                         asunto=asunto, carta=carta)
    cel = "".join(c for c in row.get("celular", "") if c.isdigit())
    link_wa = f"https://wa.me/{cel}?text={urllib.parse.quote(wa)}" if cel else "(sin celular cargado)"
    return ctx, carta, asunto, mailto, wa, link_wa

def validar(rows):
    avisos = []
    cupo = Counter(r["apoderado"].strip().lower() for r in rows)
    for apo, n in cupo.items():
        if n > MAX_PODERES:
            avisos.append(f"⚠ {apo}: {n} poderes (máximo {MAX_PODERES}).")
    lotes = Counter(r["lote_poderdante"].strip() for r in rows)
    for l, n in lotes.items():
        if n > 1:
            avisos.append(f"⚠ Lote {l} figura {n} veces como poderdante.")
    for r in rows:
        if r["poderdante"].strip().lower() == r["apoderado"].strip().lower():
            avisos.append(f"⚠ {r['poderdante']}: poderdante y apoderado son la misma persona.")
    return avisos

def seguro(s):
    return "".join(c if c.isalnum() or c in " -_" else "" for c in s).strip()

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--csv")
    ap.add_argument("--poderdante"); ap.add_argument("--lote-poderdante")
    ap.add_argument("--apoderado"); ap.add_argument("--lote-apoderado")
    ap.add_argument("--celular", default="")
    ap.add_argument("--dni", default="")
    ap.add_argument("--salida", default="salida")
    a = ap.parse_args()
    if a.csv:
        with open(a.csv, newline="", encoding="utf-8-sig") as f:
            rows = list(csv.DictReader(f))
    elif a.poderdante and a.lote_poderdante and a.apoderado and a.lote_apoderado:
        rows = [dict(poderdante=a.poderdante, lote_poderdante=a.lote_poderdante,
                     apoderado=a.apoderado, lote_apoderado=a.lote_apoderado, celular=a.celular, dni=a.dni)]
    else:
        ap.error("Pasá --csv o los 4 datos del poder.")
    os.makedirs(a.salida, exist_ok=True)
    for av in validar(rows):
        print(av)
    with open(os.path.join(a.salida, "registro.csv"), "w", newline="", encoding="utf-8") as reg:
        w = csv.writer(reg)
        w.writerow(["poderdante", "lote_poderdante", "apoderado", "lote_apoderado", "estado"])
        for r in rows:
            for etiqueta, fecha in (("fecha de hoy", None), ("fecha 23-11", FECHA_APERTURA)):
                ctx, carta, asunto, mailto, wa, link_wa = armar(r, fecha)
                nombre = f"Poder - Lote {ctx['lp']} - {seguro(ctx['pod'])} ({etiqueta}).txt"
                with open(os.path.join(a.salida, nombre), "w", encoding="utf-8") as f:
                    f.write(f"=== MENSAJE PARA WHATSAPP ===\n{wa}\n\n")
                    f.write(f"=== LINK DIRECTO A WHATSAPP (abre el chat con el mensaje listo) ===\n{link_wa}\n\n")
                    f.write(f"=== LINK MAILTO (alternativa: se abre el mail ya armado) ===\n{mailto}\n\n")
                    f.write(f"=== ASUNTO ===\n{asunto}\n\n=== TEXTO DEL PODER ===\n{carta}\n")
                print("OK ->", nombre)
            w.writerow([ctx["pod"], ctx["lp"], ctx["apo"], ctx["la"], "enviado a propietario"])

if __name__ == "__main__":
    main()
