import streamlit as st
import pandas as pd
import os
import sys
from dotenv import load_dotenv
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix, precision_score, recall_score, f1_score

from models.gpt_model import generate_reply as gpt_reply
from models.gemini_model import generate_reply as gemini_reply

# --- Tema ---
def set_modern_barca_theme_fullscreen():
    css = """
    <style>
    html, body {
        height: 100%;
        margin: 0;
        padding: 0;
        background: linear-gradient(135deg, #0A1128, #004D98, #A50044);
        background-size: 400% 400%;
        animation: gradientBG 20s ease infinite;
    }

    @keyframes gradientBG {
        0% {background-position: 0% 50%;}
        50% {background-position: 100% 50%;}
        100% {background-position: 0% 50%;}
    }

    [data-testid="stAppViewContainer"], .stApp {
        background: transparent !important;
        height: 100vh !important;
    }

    header, footer, .block-container {
        background: transparent !important;
    }

    div[data-testid="stChatInput"] {
        background: transparent !important;
        backdrop-filter: blur(10px);
        box-shadow: none !important;
    }

    .stTextInput > div > input {
        color: white;
        background-color: rgba(255, 255, 255, 0.05);
        border: 1px solid #444;
    }

    .stChatMessage {
        backdrop-filter: blur(10px);
        background-color: rgba(10, 17, 40, 0.5);
        border-radius: 1rem;
        padding: 1rem;
    }

    h1 {
        color: #FFD700;
        text-shadow: 1px 1px 3px rgba(0,0,0,0.6);
    }
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

# --- Başlık ve Tema ---
set_modern_barca_theme_fullscreen()
st.title("𝚿 PsikoBot")

# --- Model Seçimi ---
model_choice = st.sidebar.selectbox("Model Seçiniz", ["OpenAI (GPT)", "Gemini"])

# --- Chat Geçmişi ---
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# --- Veri Yükleme ---
df = pd.read_csv(os.path.join(os.path.dirname(__file__), '..', 'data', 'psikobot_veri_seti.csv'))
X = df["Sentence"]
y = df["Intent"]

vectorizer = TfidfVectorizer()
X_vec = vectorizer.fit_transform(X)
X_train, X_test, y_train, y_test = train_test_split(X_vec, y, test_size=0.2, random_state=42)

# --- GPT Modeli ---
model_gpt = LogisticRegression(max_iter=1000)
model_gpt.fit(X_train, y_train)
y_pred_gpt = model_gpt.predict(X_test)

# --- Gemini Modeli ---
model_gemini = LogisticRegression(max_iter=1000)
model_gemini.fit(X_train, y_train)
y_pred_gemini = model_gemini.predict(X_test)

# --- Metrikler ---
gpt_precision = precision_score(y_test, y_pred_gpt, average="weighted")
gpt_recall = recall_score(y_test, y_pred_gpt, average="weighted")
gpt_f1 = f1_score(y_test, y_pred_gpt, average="weighted")

gemini_precision = precision_score(y_test, y_pred_gemini, average="weighted")
gemini_recall = recall_score(y_test, y_pred_gemini, average="weighted")
gemini_f1 = f1_score(y_test, y_pred_gemini, average="weighted")

# --- Terminalde Yazdır ---
print("\n📊 --- Model Performans Karşılaştırması ---")

print("\n🧠 GPT Modeli:")
print("Precision:", round(gpt_precision, 2))
print("Recall   :", round(gpt_recall, 2))
print("F1 Score :", round(gpt_f1, 2))
print("Confusion Matrix:\n", confusion_matrix(y_test, y_pred_gpt))
print("\n📋 GPT Modeli - Classification Report")
print(classification_report(y_test, y_pred_gpt))


print("\n🧠 Gemini Modeli:")
print("Precision:", round(gemini_precision, 2))
print("Recall   :", round(gemini_recall, 2))
print("F1 Score :", round(gemini_f1, 2))
print("Confusion Matrix:\n", confusion_matrix(y_test, y_pred_gemini))
print("\n📋 Gemini Modeli - Classification Report")
print(classification_report(y_test, y_pred_gemini))

# --- Önceki Mesajları Göster ---
for user_msg, bot_msg in st.session_state.chat_history:
    with st.chat_message("user"):
        st.markdown(user_msg)
    with st.chat_message("PsikoBot"):
        st.markdown(bot_msg)

# --- Yeni Girdi ---
user_input = st.chat_input("Bir şeyler yazınız...")

if user_input:
    # Mesajı vektöre dönüştür
    X_input = vectorizer.transform([user_input])

    # Seçilen modele göre tahmin ve yanıt üretimi
    if model_choice == "OpenAI (GPT)":
        predicted_intent = model_gpt.predict(X_input)[0]
        response = gpt_reply(user_input, predicted_intent, st.session_state.chat_history)
    else:
        predicted_intent = model_gemini.predict(X_input)[0]
        response = gemini_reply(user_input, predicted_intent, st.session_state.chat_history)

    # Geçmişe ekle
    st.session_state.chat_history.append((user_input, f"**({predicted_intent})** {response}"))

    # Görsel arayüze yazdır
    with st.chat_message("user"):
        st.markdown(user_input)
    with st.chat_message("PsikoBot"):
        st.markdown(f"**({predicted_intent})** {response}")