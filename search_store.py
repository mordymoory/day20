# Задание 33 (поиск): только загружает готовое хранилище и ищет
from common import get_model, load_store, search, print_results

store = load_store()
if len(store) == 0:
    print("Хранилище пустое")
else:
    model = get_model()
    query = input("Введите вопрос: ").strip()
    if query == "":
        print("Вопрос не должен быть пустым")
    else:
        print_results(search(model, store, query, top_k=3))
