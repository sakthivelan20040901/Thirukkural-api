# 📜 Thirukkural API (Tamil Literature API)

A **free, public REST API** for accessing **Tamil Thirukkural (திருக்குறள்)** data with translations, explanations, and powerful search features.

> 🚀 Built using FastAPI | 🌐 Live API | 📚 Educational Use

---

## 🌐 Live API

👉 https://thirukkural-api-jyle.onrender.com

📖 API Docs (Swagger):
👉 https://thirukkural-api-jyle.onrender.com/docs

---

## 📌 Features

* ✅ Get Kural by ID
* ✅ Chapter-wise Kurals (133 chapters)
* ✅ Tamil + English translation
* ✅ Tamil explanations
* ✅ 🔍 Keyword search (Tamil & English)
* ✅ 🔤 Starts-with / Ends-with search (Exam useful)
* ✅ 🎲 Random Kural
* ✅ 📅 Daily Kural
* ✅ 📚 Section-wise filtering (Virtue, Wealth, Love)
* ✅ ⚡ Fast & lightweight (JSON-based)

---

## 📚 About Thirukkural

**Thirukkural (திருக்குறள்)** is a classic Tamil text consisting of:

* 📖 1330 Kurals (couplets)
* 📘 133 Chapters
* 🧠 3 Sections:

  * Virtue (அறம்)
  * Wealth (பொருள்)
  * Love (இன்பம்)

---

## 🚀 API Endpoints

### 🔹 Get Kural by ID

```bash
GET /kural/{id}
```

Example:

```bash
/kural/1
```

---

### 🔹 Get Kurals by Chapter

```bash
GET /kural?chapter=1
```

---

### 🔹 Get Chapter Details

```bash
GET /chapters/{id}
```

---

### 🔹 Search (Tamil / English)

```bash
GET /search?q=அகர
GET /search?q=love
```

---

### 🔹 Starts With (Exam Use)

```bash
GET /search/start?q=அகர
```

---

### 🔹 Ends With (Exam Use)

```bash
GET /search/end?q=உலகு
```

---

### 🔹 Random Kural

```bash
GET /random
```

---

### 🔹 Daily Kural

```bash
GET /daily
```

---

### 🔹 Section Filter

```bash
GET /section?section=virtue
```

---

## 🛠️ Tech Stack

* ⚡ FastAPI (Python)
* 🧠 JSON Dataset (1330 Kurals)
* 🌐 Render (Deployment)
* 🗂️ GitHub (Version Control)

---

## 🧪 Example Response

```json
{
  "id": 1,
  "tamil": "அகர முதல எழுத்தெல்லாம்...",
  "english": "A is the first of the alphabet...",
  "explanation_tamil": "...",
  "explanation_english": "...",
  "chapter_en": "The Praise of God",
  "section_en": "Virtue"
}
```

---


## 📈 Use Cases

* 📱 Mobile apps (Daily Kural apps)
* 🎓 Tamil education platforms
* 🤖 Chatbots & NLP projects
* 🧘 Motivation & wellness apps
* 📚 Exam preparation tools

---

## 🔐 Future Improvements

* API Key authentication
* Rate limiting
* TF-IDF / AI search
* Multi-language support
* Analytics dashboard

---

## 🤝 Contributing

Contributions are welcome!
Feel free to open issues or submit pull requests.

---

## 📜 License

Open-source for educational and development purposes.

---

## 🌟 Keywords

Tamil API, Thirukkural API, Tamil Literature API, திருக்குறள் API,
Tamil NLP dataset, Tamil search API, Thirukkural dataset,
Tamil education API, Tamil REST API, Indian literature API

---

## 👨‍💻 Author

**Sakthivelan**
DevOps Enthusiast | AI Builder | Open Source Contributor

---

⭐ If you found this useful, please star the repo!
