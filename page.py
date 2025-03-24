import streamlit as st
import speech_recognition as sr
from gtts import gTTS
import os

# Инициализация session_state
if "chats" not in st.session_state:
    st.session_state.chats = {"Новый чат": []}
    st.session_state.current_chat = "Новый чат"
    
if "sidebar_expanded" not in st.session_state:
    st.session_state.sidebar_expanded = True

if "renaming_chat" not in st.session_state:
    st.session_state.renaming_chat = None

# Настройки страницы
st.set_page_config(page_title="Компьютенатор", layout="wide")

# Функция для голосового ввода
def recognize_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        st.write("🎙 Говорите...")
        audio = recognizer.listen(source)
    try:
        text = recognizer.recognize_google(audio, language="ru-RU")
        with open("voice_input.txt", "w", encoding="utf-8") as file:
            file.write(text)
        return text
    except sr.UnknownValueError:
        return "Не удалось распознать речь"
    except sr.RequestError:
        return "Ошибка сервиса распознавания"

# Функция для озвучки ответа
def text_to_speech(text, filename="response.mp3"):
    tts = gTTS(text=text, lang="ru")
    tts.save(filename)
    return filename


# Стилизация
st.markdown("""
    <style>
        .css-1aumxhk {display: none} /* Убирает кнопку "Made with Streamlit"
    </style>
""", unsafe_allow_html=True)

# Боковая панель
if st.session_state.sidebar_expanded:
    with st.sidebar:
        st.title("📂 История чатов")
        #if st.button("🔽 Свернуть / Развернуть панель"):
        #    st.session_state.sidebar_expanded = False
        #    st.rerun()
        selected_chat = st.radio("Выберите чат", list(st.session_state.chats.keys()))

        col1, col2 = st.columns([2, 1])
        if col1.button("➕ Новый чат"):
            new_chat_name = f"Чат {len(st.session_state.chats)}"
            st.session_state.chats[new_chat_name] = []
            st.session_state.current_chat = new_chat_name
            st.rerun()
        if col2.button("🗑 Удалить чат"):
            if selected_chat in st.session_state.chats:
                del st.session_state.chats[selected_chat]
                if not st.session_state.chats:
                    st.session_state.chats["Новый чат"] = []
                st.session_state.current_chat = list(st.session_state.chats.keys())[0]
                st.rerun()
        if col3.button("✏ Переименовать чат"):
            st.session_state.renaming_chat = selected_chat
            st.rerun()

        if st.session_state.renaming_chat:
            new_name = st.text_input("Новое название:", st.session_state.renaming_chat)
            rename_col1, rename_col2 = st.columns([1, 1])
            if rename_col1.button("✅ Сохранить"):
                if new_name and new_name not in st.session_state.chats:
                    st.session_state.chats[new_name] = st.session_state.chats.pop(st.session_state.renaming_chat)
                    st.session_state.current_chat = new_name
                st.session_state.renaming_chat = None
                st.rerun()
            if rename_col2.button("❌ Отмена"):
                st.session_state.renaming_chat = None
                st.rerun()

        
st.session_state.current_chat = selected_chat if st.session_state.sidebar_expanded else st.session_state.current_chat

# Заголовок
st.title("Компьютенатор")

# Вывод истории сообщений текущего чата
st.write(f"### {st.session_state.current_chat}")
chat_history = st.session_state.chats[st.session_state.current_chat]

for message in chat_history:
    with st.chat_message(message["role"]):
        st.markdown(message["text"])

# Кнопки голосового ввода
if st.button("🎙 Голосовой ввод"):
    user_input = recognize_speech()
    st.session_state.user_input = user_input
    st.rerun()

if prompt := st.chat_input("Behold, Perry the Platopus! I'm Computenator"):
    # Добавляем сообщение пользователя в историю текущего чата
    chat_history.append({"role": "user", "text": prompt})
    
    # Отображаем ответ заглушку (без ИИ)
    response = "Простите, но ИИ отключен 🤖"
    chat_history.append({"role": "assistant", "text": response})

    # Озвучивание ответа
        audio_file = text_to_speech(response)
        st.audio(audio_file, format="audio/mp3")

    # Обновляем страницу
    st.rerun()
