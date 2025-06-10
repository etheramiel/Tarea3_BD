import json
from pymongo import MongoClient
from concurrent.futures import ThreadPoolExecutor
from tqdm import tqdm
# === Configuración ===
# json_file_path = "arxiv-metadata-oai-snapshot.json"
archivos = [f"arxiv-part-{i:02d}.json" for i in range(11)]
batch_size = 400
documentos_totales = 0
# max_workers = 4  # Ajusta según tu CPU y MongoDB
# === Conectar a MongoDB ===
client = MongoClient("mongodb://mongo1:30001,mongo2:30002,mongo3:30003/?replicaSet=my-replica-set&readPreference=primary&appname=MongoDB%20Compass&ssl=false")
db = client["arxiv_db"]
collection = db["articles"]
# === Función para insertar lote ===
def insert_batch(batch):
    try:
        collection.insert_many(batch, ordered=False)
    except Exception as e:
        print("Error al insertar batch:", e)


# === Lectura + carga paralela ===


# for archivo in archivos:
#     print(f"\n📂 Cargando {archivo}...")
#     # Contar líneas para tqdm
#     total_lines = sum(1 for _ in open(archivo, 'r', encoding='utf-8'))

#     with open(archivo, 'r', encoding='utf-8') as f, tqdm(total=total_lines, desc=f"Cargando {archivo}") as pbar:
#         batch = []
#         for line in f:
#             try:
#                 record = json.loads(line)
#                 record["pdf_source"] = f"https://arxiv.org/pdf/{record['id']}"
#                 batch.append(record)
#                 if len(batch) >= batch_size:
#                     insert_batch(batch)
#                     batch = []
#             except json.JSONDecodeError:
#                 continue
#             pbar.update(1)
#         if batch:
#             insert_batch(batch)

# print("🎉 Todos los archivos fueron cargados.")

for archivo in archivos:
    print(f"\n📂 Cargando {archivo}...")
    batch = []
    doc_count = 0

    with open(archivo, 'r', encoding='utf-8') as f:
        for line in f:
            try:
                record = json.loads(line)
                record["pdf_source"] = f"https://arxiv.org/pdf/{record['id']}"
                batch.append(record)
                doc_count += 1
                documentos_totales += 1

                if len(batch) >= batch_size:
                    insert_batch(batch)
                    batch = []

                # Mostrar progreso cada 10.000 documentos
                if doc_count % 10000 == 0:
                    print(f"  🔹 {doc_count} documentos procesados en {archivo}...")

            except json.JSONDecodeError:
                continue

        # Último batch
        if batch:
            insert_batch(batch)

    print(f"✅ Archivo {archivo} cargado con {doc_count} documentos.")

print(f"\n🎉 Todos los archivos cargados. Total insertados: {documentos_totales}")
