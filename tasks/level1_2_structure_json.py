# Задания 1–7
import json

# Задание 1
record = {
    "source": "python.txt",
    "chunk_id": 0,
    "text": "Списки Python создаются через квадратные скобки.",
    "embedding": [0.12, -0.08, 0.44, 0.31]
}

# Задание 2
records = [
    record,
    {"source": "git.txt", "chunk_id": 0,
     "text": "git commit сохраняет изменения в истории.",
     "embedding": [0.05, 0.27, -0.13, 0.62]},
    {"source": "rag.txt", "chunk_id": 0,
     "text": "RAG ищет фрагменты и передаёт их модели.",
     "embedding": [-0.21, 0.09, 0.38, 0.14]},
]

# Задание 3
for item in records:
    print(item["source"], len(item["embedding"]))

# Задание 4
dims = set(len(item["embedding"]) for item in records)
print("Размерность одинакова:", len(dims) == 1)

# Задание 5 + 7
with open("test_store.json", "w", encoding="utf-8") as file:
    json.dump(records, file, ensure_ascii=False, indent=2)

# Задание 6
with open("test_store.json", "r", encoding="utf-8") as file:
    loaded = json.load(file)
print("Записей:", len(loaded))
