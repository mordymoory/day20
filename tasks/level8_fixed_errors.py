# Задания 27–30 (исправленный код)
import json

store = [{"source": "python.txt", "chunk_id": 0, "text": "пример", "score": 0.5}]
results = [{"score": 0.3}, {"score": 0.9}, {"score": 0.6}]
top_k = 2

# Задание 27: json.load -> json.dump, добавлены encoding и ensure_ascii
with open("store.json", "w", encoding="utf-8") as file:
    json.dump(store, file, ensure_ascii=False, indent=2)

# Задание 28: reverse=False -> reverse=True
results = sorted(results, key=lambda item: item["score"], reverse=True)

# Задание 29: results[top_k] -> results[:top_k]
top_results = results[:top_k]
print(top_results)

# Задание 30: = -> ==, добавлен strip()
query = input("Вопрос: ").strip()
if query == "":
    print("Пусто")
