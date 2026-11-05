# Задания 8–11, 33 (построение)
from common import get_model, load_chunks, save_store, STORE_FILE

chunks = load_chunks()                                  # Задание 8
print("Загружено чанков:", len(chunks))
if len(chunks) < 10:
    print("Внимание: нужно минимум 10 чанков")

model = get_model()                                     # Задание 9
texts = [chunk["text"] for chunk in chunks]
embeddings = model.encode(texts)

for i in range(len(chunks)):                            # Задание 10
    chunks[i]["embedding"] = embeddings[i].tolist()

save_store(chunks)                                      # Задание 11
print("Сохранено в", STORE_FILE)
print("Размерность:", len(chunks[0]["embedding"]))
