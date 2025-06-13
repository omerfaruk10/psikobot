# Ψ PsikoBot

PsikoBot, kullanıcı mesajlarını duygu ve niyet bağlamında analiz eden, empatik ve psikolojik destek odaklı yanıtlar üreten bir yapay zekâ sohbet botudur.

![PsikoBot Arayüzü](docs/psikobot_ui.png)

Bu projede iki büyük dil modeli karşılaştırmalı olarak entegre edilmiştir:

**🔹 Gemini (gemini-2.0-flash)**  
**🔹 OpenAI (gpt-3.5-turbo)**

---

🧭 Desteklenen Niyet (Intent) Sınıfları

PsikoBot, kullanıcının yazdığı ifadeyi aşağıdaki duygusal niyet kategorilerinden birine sınıflandırarak, bu bağlamda empatik bir yanıt üretir:

🎯 Niyet (Intent)	📝 Açıklama

greeting	Selamlaşma, tanışma ifadeleri
goodbye	Veda, sohbeti sonlandırma
anxiety	Kaygı, stres, huzursuzluk belirtileri
depression	Mutsuzluk, isteksizlik, depresif ruh hali
relationship	Aile, arkadaşlık ya da romantik ilişkilerle ilgili duygular
self-esteem	Özgüven eksikliği, kendini yetersiz hissetme
motivation	Umut, hedef koyma, yeniden deneme arzusu
anger	Öfke, sinirlilik, patlama eğilimi
confusion	Kararsızlık, belirsizlik, zihinsel bulanıklık
gratitude	Teşekkür, minnettarlık, olumlu geri bildirim


Bu sınıflar, TF-IDF ile vektörleştirilmiş ve lojistik regresyon modeli ile eğitilmiştir. Ayrıca seçilen modele (GPT veya Gemini) iletilerek bağlama uygun cevap üretilmesini sağlar.


---


## 📂 Klasör Yapısı
```plaintext
chatbot_project/
│
├── app/ # Streamlit arayüzü ve giriş noktası
│ └── streamlit_app.py
│
├── models/ # Model cevap fonksiyonları
│ ├── gpt_model.py
│ └── gemini_model.py
│
├── data/ # Eğitim verileri
│ └── psikobot_veri_seti.csv
│
├── .streamlit/ # Tema ve ayarlar (opsiyonel)
│ └── config.toml
│
├── .env # API anahtarları
├── requirements.txt # Gerekli paketler
└── README.md # Bu dosya
```
## ⚙️ Kurulum ve Çalıştırma

1. Gerekli kütüphaneleri yükleyin:

```bash
pip install -r requirements.txt
```
2. .env dosyasına API anahtarlarınızı girin:
```bash
OPENAI_API_KEY=sk-...
GOOGLE_API_KEY=AIza...
```
3. Uygulamayı başlatın:
streamlit run app/streamlit_app.py

```bash
🎯 Özellikler
- 🌐 GPT ve Gemini arasında kolay geçiş
- 💬 Gerçek zamanlı sohbet geçmişi
- 🧠 TF-IDF + Lojistik Regresyon ile niyet tahmini
- 📊 Model metriklerinin terminale yazdırılması
- 🎨 Özel temalı görsel arayüz
```

