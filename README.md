<h1 align="center">SwiftSupport India 🧡</h1>

<p align="center">
AI-Powered Customer Support Portal using RAG Architecture
</p>

<p align="center">
Built for intelligent retail support, policy-grounded responses, and scalable AI-driven customer interaction.
</p>

---

# 🌐 Live Demo

🔗 https://swiftsupport-india.streamlit.app/

---

# 🎯 Why SwiftSupport India?

Customer support systems often struggle with:

- inaccurate or hallucinated AI responses  
- inconsistent policy handling  
- poor logistics assistance  
- lack of contextual understanding  

SwiftSupport India solves these challenges using a **Retrieval-Augmented Generation (RAG)** architecture that grounds responses strictly on official policy documents while maintaining a fast and intuitive user experience.

---

# 🚀 Core Features

✅ Policy-grounded customer support using RAG  
✅ Intelligent return fee calculation system  
✅ Regional logistics routing for Indian cities  
✅ Intent-driven guided user interface  
✅ Secure AI workflow with multi-stage guardrails  
✅ Fast and scalable Streamlit-based architecture  

---

# 🧠 System Architecture

The application follows a Retrieval-Augmented Generation (RAG) workflow:

1. User query passes through secure input guardrails  
2. Relevant policy context is retrieved  
3. Context is injected into the LLM prompt  
4. Meta-Llama 3.3-70B generates grounded responses  
5. Output guardrails validate response safety  
6. Streamlit UI renders the final response  

---

# 🛠️ Technical Stack

| Category | Technologies |
|----------|--------------|
| Frontend | Streamlit |
| Backend | Python 3.x |
| AI Model | Meta-Llama 3.3-70B |
| AI Architecture | Retrieval-Augmented Generation (RAG) |
| APIs | OpenRouter |
| Security | Guardrails & Prompt Injection Protection |
| Deployment | Streamlit Cloud |

---

# 🔐 Security Features

- Multi-layer prompt injection protection  
- Secure environment variable management  
- Restricted AI response generation  
- Output validation guardrails  
- Policy-grounded retrieval pipeline  

---

# 📦 Installation & Local Setup

## 1️⃣ Clone the Repository

```bash
git clone https://github.com/HG-43/SwiftSupport-India-Production.git
cd SwiftSupport-India-Production
```

---

## 2️⃣ Create Virtual Environment

```bash
python -m venv venv
```

### Activate Environment

#### Windows

```bash
venv\\Scripts\\activate
```

#### macOS/Linux

```bash
source venv/bin/activate
```

---

## 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 4️⃣ Configure Environment Variables

Create a `.env` file and add:

```env
OPENROUTER_API_KEY=your_api_key_here
```

---

## 5️⃣ Run the Application

```bash
streamlit run app.py
```

---

# 🚀 Future Improvements

- Multi-language Indian regional support  
- Voice-enabled AI assistance  
- Vector database integration  
- Agentic workflow automation  
- Real-time order tracking APIs  
- Fine-tuned domain-specific models  

---

# 🧑‍💻 Author

### Hiya Gupta

Full Stack Engineer & AI Engineering Enthusiast

🔗 GitHub: https://github.com/HG-43  
🔗 LinkedIn: https://www.linkedin.com/in/hiya-gupta-99896a244/

---

<p align="center">
✨ Building intelligent AI systems with scalable architecture & clean user experiences ✨
</p>
