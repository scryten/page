import streamlit as st

# Инициализация session_state
if "chats" not in st.session_state:
    st.session_state.chats = {"Новый чат": []}
    st.session_state.current_chat = "Новый чат"

# Настройки страницы
st.set_page_config(page_title="Компьютенатор", layout="wide")

# Стилизация
st.markdown("""
    <style>
        .css-1aumxhk {display: none} /* Убирает кнопку "Made with Streamlit"
    </style>
""", unsafe_allow_html=True)

# Боковая панель с чатами
st.sidebar.title("📂 История чатов")
selected_chat = st.sidebar.radio("Выберите чат", list(st.session_state.chats.keys()))

col1, col2 = st.sidebar.columns([2, 1])

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

st.session_state.current_chat = selected_chat

# Заголовок
st.title("Компьютенатор")

# Вывод истории сообщений текущего чата
st.write(f"### {st.session_state.current_chat}")
chat_history = st.session_state.chats[st.session_state.current_chat]

for message in chat_history:
    with st.chat_message(message["role"]):
        st.markdown(message["text"])

if prompt := st.chat_input("I'm your virtual bartender, how may I help you?"):
    # Добавляем сообщение пользователя в историю текущего чата
    chat_history.append({"role": "user", "text": prompt})
    
    # Отображаем ответ заглушку (без ИИ)
    response = "Простите, но ИИ отключен 🤖"
    chat_history.append({"role": "assistant", "text": response})
        
    # Обновляем страницу
    st.rerun()
