# Задания 12–26 (запускать из папки day20 после build_store.py)
import sys
sys.path.insert(0, ".")
from common import get_model, load_store

model = get_model()
store = load_store()

# Задание 12
query = input("Введите вопрос: ").strip()
if query == "":
    print("Вопрос не должен быть пустым")
    sys.exit()

# Задание 13
query_embedding = model.encode(query)

# Задание 14
stored_embeddings = [item["embedding"] for item in store]
scores = model.similarity(query_embedding, stored_embeddings)[0].tolist()

# Задание 15
results = []
for i in range(len(store)):
    results.append({
        "source": store[i]["source"],
        "chunk_id": store[i].get("chunk_id", i),
        "text": store[i]["text"],
        "score": scores[i]
    })

# Задание 16
results = sorted(results, key=lambda item: item["score"], reverse=True)

# Задание 17 — Top-1
best = results[0]
print("\n=== Top-1 ===")
print("Источник:", best["source"], "| Чанк:", best["chunk_id"],
      "| Score:", round(best["score"], 4))
print("Текст:", best["text"])

# Задание 18 — Top-3
print("\n=== Top-3 ===")
for number, result in enumerate(results[:3], start=1):
    print(number, round(result["score"], 4), result["source"], result["chunk_id"])

# Задание 19 — Top-5
print("\n=== Top-5 ===")
top_k = 5
for result in results[:top_k]:
    print(round(result["score"], 4), result["source"], result["chunk_id"])

# Задание 20 — пользовательский K
top_k = int(input("\nСколько результатов вывести? "))
for number, result in enumerate(results[:top_k], start=1):
    print(number, round(result["score"], 4), result["source"], result["chunk_id"])

# Задание 21
threshold = 0.35

# Задание 22
if results[0]["score"] < threshold:
    print("Подходящий фрагмент не найден")

# Задание 23
filtered_results = []
for result in results:
    if result["score"] >= threshold:
        filtered_results.append(result)
print("\nПосле порога:", len(filtered_results))
for result in filtered_results[:3]:
    print(round(result["score"], 4), result["source"], result["chunk_id"])

# Задание 24
selected_source = "python.txt"
filtered_store = [item for item in store if item["source"] == selected_source]
print("\nЗаписей из", selected_source, ":", len(filtered_store))

# Задание 25
counter = {}
for result in results[:5]:
    counter[result["source"]] = counter.get(result["source"], 0) + 1
print("Источники Top-5:", counter)

# Задание 26
for result in results[:5]:
    original = next(item for item in store if item["text"] == result["text"])
    assert original["chunk_id"] == result["chunk_id"]
print("chunk_id в выдаче совпадают с хранилищем")
