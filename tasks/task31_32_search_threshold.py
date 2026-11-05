# Задания 31–32 (запускать из папки day20)
import sys
from pathlib import Path
sys.path.insert(0, ".")
from common import get_model, load_chunks, load_store, save_store, search, print_results, STORE_FILE

THRESHOLD = 0.35
model = get_model()

if not Path(STORE_FILE).exists():
    chunks = load_chunks()
    embeddings = model.encode([c["text"] for c in chunks])
    for i in range(len(chunks)):
        chunks[i]["embedding"] = embeddings[i].tolist()
    save_store(chunks)

store = load_store()
query = input("Введите вопрос: ").strip()
if query == "":
    print("Вопрос не должен быть пустым")
else:
    results = search(model, store, query, top_k=3, threshold=THRESHOLD)
    if len(results) == 0:
        print("Подходящих фрагментов не найдено")
    else:
        print_results(results)
