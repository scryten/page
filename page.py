import streamlit as st


# Инициализация session_state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Настройки страницы
st.set_page_config(page_title="Сборщик компьютеров", layout="wide")

# Стилизация
st.markdown("""
    <style>
        .css-1aumxhk {display: none} /* Убирает кнопку "Made with Streamlit" */
        .stTextArea textarea {height: 150px !important;} /* Увеличивает поле ввода */
    </style>
""", unsafe_allow_html=True)

# Заголовок
st.title("Сборщик компьютеров")

# Вывод истории сообщений
st.write("### Чат")
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["text"])

# Поле ввода
user_input = st.text_area("Введите сообщение:", key="user_input")

# Кнопка отправки
if st.button("Отправить"):
    if user_input:
        # Добавляем сообщение пользователя в историю
        st.session_state.messages.append({"role": "user", "text": user_input})
        
        # Отображаем ответ заглушку (без ИИ)
        response = "Простите, но ИИ отключен 🤖"
        st.session_state.messages.append({"role": "assistant", "text": response})
        
        # Обновляем страницу
        st.experimental_rerun()
