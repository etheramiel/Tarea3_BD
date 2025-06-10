import os

# === Configuración ===
archivo_original = "arxiv-metadata-oai-snapshot.json"
numero_de_partes = 10
prefijo_salida = "arxiv-part"

# === Contar líneas totales ===
print("📏 Contando líneas del archivo original...")
with open(archivo_original, "r", encoding="utf-8") as f:
    total_lineas = sum(1 for _ in f)

lineas_por_archivo = total_lineas // numero_de_partes
print(f"🔢 Total líneas: {total_lineas}")
print(f"📂 Líneas por archivo: ~{lineas_por_archivo}")

# === Dividir el archivo ===
parte = 0
lineas_escritas = 0
salida = None

with open(archivo_original, "r", encoding="utf-8") as entrada:
    for i, linea in enumerate(entrada):
        # Abrir nuevo archivo si corresponde
        if i % lineas_por_archivo == 0:
            if salida:
                salida.close()
                print(f"✅ Archivo {archivo_actual} escrito con {lineas_escritas} líneas.")
                lineas_escritas = 0
            nombre_archivo = f"{prefijo_salida}-{parte:02d}.json"
            archivo_actual = nombre_archivo
            salida = open(nombre_archivo, "w", encoding="utf-8")
            parte += 1
        salida.write(linea)
        lineas_escritas += 1

# Cerrar el último archivo
if salida:
    salida.close()
    print(f"✅ Archivo {archivo_actual} escrito con {lineas_escritas} líneas.")

print("🎉 División completada.")
