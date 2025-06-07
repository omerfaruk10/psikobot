import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

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
            
            Mesajın başına: Bu mesaj OpenAI tarafından veriliyor. ibaresi yaz.

            ❗ Ancak cevabında kategori etiketini (örn. "{predicted_intent}") tekrar etme.
            Yalnızca içerik odaklı, doğal ve samimi bir yanıt ver. 
            """

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Sen deneyimli bir psikolojik danışmansın."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Üzgünüm, bir hata oluştu: {e}"
