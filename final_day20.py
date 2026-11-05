# Задание 34 + звёздочки 1–3
import json
from pathlib import Path
from sentence_transformers import SentenceTransformer

MODEL_NAME = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
STORE_FILE = "vector_store.json"
THRESHOLD = 0.35
TOP_K = 3


class SimpleVectorStore:
    def __init__(self, model):
        self.model = model
        self.items = []

    def add(self, source, chunk_id, text):
        embedding = self.model.encode(text).tolist()
        self.items.append({
            "source": source,
            "chunk_id": chunk_id,
            "text": text,
            "embedding": embedding
        })

    def save(self, filename):
        with open(filename, "w", encoding="utf-8") as file:
            json.dump(self.items, file, ensure_ascii=False, indent=2)

    def load(self, filename):
        with open(filename, "r", encoding="utf-8") as file:
            self.items = json.load(file)

    def search(self, query, top_k=3, threshold=None, source=None):
        items = self.items
        if source is not None:
            items = [item for item in items if item["source"] == source]
        if len(items) == 0:
            return []
        query_embedding = self.model.encode(query)
        embeddings = [item["embedding"] for item in items]
        scores = self.model.similarity(query_embedding, embeddings)[0].tolist()
        results = []
        for i in range(len(items)):
            results.append({
                "source": items[i]["source"],
                "chunk_id": items[i]["chunk_id"],
                "text": items[i]["text"],
                "score": scores[i]
            })
        results = sorted(results, key=lambda item: item["score"], reverse=True)
        if threshold is not None:
            results = [r for r in results if r["score"] >= threshold]
        return results[:top_k]


def load_chunks():
    if Path("chunks.json").exists():
        with open("chunks.json", "r", encoding="utf-8") as file:
            return json.load(file)
    chunks = []
    for file_path in sorted(Path("chunks").glob("*.txt")):
        stem, _, number = file_path.stem.rpartition("_chunk_")
        chunks.append({"source": stem + ".txt", "chunk_id": int(number),
                       "text": file_path.read_text(encoding="utf-8").strip()})
    return chunks


def build(model):
    store = SimpleVectorStore(model)
    for chunk in load_chunks():
        store.add(chunk["source"], chunk["chunk_id"], chunk["text"])
    store.save(STORE_FILE)
    print("Хранилище построено:", len(store.items), "записей")


def print_results(results):
    if len(results) == 0:
        print("Подходящий фрагмент не найден")
        return
    for number, r in enumerate(results, start=1):
        print(f"\n{number}. {r['source']} | chunk {r['chunk_id']} | score {round(r['score'], 4)}")
        print(r["text"])


def main():
    model = SentenceTransformer(MODEL_NAME)
    if not Path(STORE_FILE).exists():
        build(model)

    store = SimpleVectorStore(model)
    store.load(STORE_FILE)
    if len(store.items) == 0:
        print("Хранилище пустое")
        return
    print("Записей:", len(store.items), "| Размерность:", len(store.items[0]["embedding"]))

    tests = ["Как создать список?", "Как сохранить изменения в git?", "Что такое embedding?"]
    for q in tests:
        print("\n========== Тест:", q)
        print_results(store.search(q, top_k=TOP_K, threshold=THRESHOLD))

    sources = sorted(set(item["source"] for item in store.items))
    print("\nИсточники:", ", ".join(sources))
    while True:
        query = input("\nВопрос (или 'выход'): ").strip()
        if query.lower() == "выход":
            break
        if query == "":
            print("Вопрос не должен быть пустым")
            continue
        source = input("Источник (Enter — все): ").strip() or None
        print_results(store.search(query, top_k=TOP_K, threshold=THRESHOLD, source=source))


if __name__ == "__main__":
    main()
