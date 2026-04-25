import requests
import os
from dotenv import load_dotenv

# --- Настройки ---
load_dotenv()
API_KEY = os.getenv("DEEPSEEK_API_KEY")
API_URL = "https://api.deepseek.com/chat/completions"
MODEL = "deepseek-chat"
HISTORY_LIMIT = 20

HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json",
}

SYSTEM_PROMPT = {
    "role": "system",
    "content": (
        "Ты дружелюбный помощник для изучения Python."
        "Объясняй просто, приводи короткие примеры кода."
        "Отвечай на русском."
    ),
}


def send_message(messages: list[dict]) -> str:
    """Отправить историю сообщений в API, вернуть текст ответа."""

    # Шаг 1: сформируй тело запроса
    body = {
        "model": MODEL,
        "messages": messages,
        # TODO: добавь "model" и "messages"
    }
    response = requests.post(API_URL, headers=HEADERS, json=body, timeout=30)
    response.raise_for_status()
    return response.json()["choices"][0]["message"]["content"]

def main():
    print("Чат с DeepSeek. Введите 'exit' для выхода.\n")

    history = []  # список сообщений - история диалога

    while True:
        # TODO: реализуй цикл диалога по алгоритму выше
        try:
            user_input = input("ВЫ: ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\nПока!")
            break

        if not user_input:
            continue

        if user_input.lower() == "exit":
            print("Пока!")
            break

        try:
            user_input.encode("utf-8").decode("utf-8")
        except UnicodeError:
            print("[Ошибка]: введённый текст содержит недопустимые символы.")
            continue

        history.append({"role": "user", "content": user_input})

        try:
            message = [SYSTEM_PROMPT] + history[-HISTORY_LIMIT:]
            reply = send_message(message)
        except requests.HTTPError as e:
            print(f"[Ошибка API]: {e.response.status_code} - {e.response.text}")
            history.pop()
            continue
        except requests.RequestException as e:
            print(f"[Сетевая ошибка]: {e}")
            history.pop()
            continue

        history.append({"role": "system", "content": reply})

        print(f"\nDeepSeek: {reply}\n")

        with open("chat_log.txt", "a", encoding="utf-8") as f:
            f.write(f"Вы: {user_input}\n")
            f.write(f"DeepSeek: {reply}\n")
            f.write("-" * 40 + "\n")



if __name__ == "__main__":
    main()



def score_pinterest_pin(user, pin):
    score = 0

    # Совпадение с интересами пользователя
    score += similarity(user.saved_pins, pin.image_style) * 30

    # Совпадение с поисковыми запросами
    score += similarity(user.search_history, pin.keywords) * 25

    # Похожесть на доски пользователя
    score += similarity(user.boards, pin.topic) * 35

    # Популярность пина
    score += pin.save_rate * 20
    score += pin.click_rate * 15

    return score