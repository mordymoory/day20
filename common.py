import json
from pathlib import Path

MODEL_NAME = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
STORE_FILE = "vector_store.json"
CHUNKS_FILE = "chunks.json"


def get_model():
    from sentence_transformers import SentenceTransformer
    return SentenceTransformer(MODEL_NAME)


def load_chunks():
    # Чанки Дня 18: сначала chunks.json, иначе файлы из папки chunks/
    if Path(CHUNKS_FILE).exists():
        with open(CHUNKS_FILE, "r", encoding="utf-8") as file:
            return json.load(file)
    chunks = []
    for file_path in sorted(Path("chunks").glob("*.txt")):
        stem, _, number = file_path.stem.rpartition("_chunk_")
        chunks.append({
            "source": stem + ".txt",
            "chunk_id": int(number),
            "text": file_path.read_text(encoding="utf-8").strip()
        })
    return chunks


def save_store(store, filename=STORE_FILE):
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(store, file, ensure_ascii=False, indent=2)


def load_store(filename=STORE_FILE):
    with open(filename, "r", encoding="utf-8") as file:
        return json.load(file)


def search(model, store, query, top_k=3, threshold=None, source=None):
    if source is not None:
        store = [item for item in store if item["source"] == source]
    if len(store) == 0:
        return []
    query_embedding = model.encode(query)
    embeddings = [item["embedding"] for item in store]
    scores = model.similarity(query_embedding, embeddings)[0].tolist()
    results = []
    for i in range(len(store)):
        results.append({
            "source": store[i]["source"],
            "chunk_id": store[i].get("chunk_id", i),
            "text": store[i]["text"],
            "score": scores[i]
        })
    results = sorted(results, key=lambda item: item["score"], reverse=True)
    if threshold is not None:
        results = [r for r in results if r["score"] >= threshold]
    return results[:top_k]


def print_results(results):
    for number, result in enumerate(results, start=1):
        print("\nМесто:", number)
        print("Источник:", result["source"])
        print("Чанк:", result["chunk_id"])
        print("Score:", round(result["score"], 4))
        print("Текст:", result["text"])
