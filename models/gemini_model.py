import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
llm = genai.GenerativeModel("gemini-2.0-flash")

def generate_reply(user_input, predicted_intent, chat_history):
    previous_msgs = "\n".join([
        f"Kullanıcı: {u}\nPsikoBot: {b}" for u, b in chat_history
    ])

    prompt = f"""
            Önceki konuşmalar:
            {previous_msgs}

            Şimdi kullanıcı şöyle dedi: "{user_input}"
            Bu ifade şu kategoriye ait: "{predicted_intent}"

            Lütfen bu bağlama ve duyguya uygun, kısa ve içten bir Türkçe yanıt ver.
            Empatik ve sakin bir tonda konuş. Gerekirse moral ver.
            
            Mesajın başına: Bu mesaj Gemini tarafından veriliyor. ibaresi yaz.

            ❗ Ancak cevabında kategori etiketini (örn. "{predicted_intent}") tekrar etme.
            Yalnızca içerik odaklı, doğal ve samimi bir yanıt ver. 
            """

    try:
        response = llm.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        return f"Üzgünüm Bayım, bir hata oluştu: {e}"
