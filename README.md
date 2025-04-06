# 💸 **FinGPT - AI-Powered Financial Assistant**
### Team Sniders
---

## 🔍 Introduction
India is witnessing a surge of new investors—millions stepping into the world of finance. Yet, **financial literacy** remains alarmingly low. Manual advisory isn’t scalable, and most platforms only cater to seasoned investors. That’s where **FinGPT** steps in — an intelligent, accessible, and **AI-powered financial assistant** designed for **everyone.**

---

## 🌟 Unique Selling Proposition (USP)
✅ **100% Free & Scalable** – Powered by Google tools, no fees or hidden charges. 

✅ **Real-Time Insights** – Instant stock data from Yahoo Finance & Google Finance.

✅ **Multi-Language Support** – Chat in **any Indian language** via Gemini AI.  

✅ **Privacy-Focused** – No personal data stored beyond chat history.  

✅ **Personalized Investment Suggestions** – Smart AI-driven recommendations. 

✅ **Jargon-Free Learning** – Simplified finance for absolute beginners.  

---

## ❓ Problem Statement
🚫 New investors struggle with:
- Low financial literacy
- Confusing jargon
- Lack of personalized support
- Overwhelming or technical platforms

💡 **FinGPT** aims to make **finance simple, smart, and accessible** to the masses.

---

## 🛠️ Solution Overview
FinGPT is a **GenAI-Powered Financial Assistant** that:

💬 Answers investment questions in **simple, conversational language**  
📉 Shows **real-time stock data** and **interactive charts**  
📈 Predicts trends with live **buy/sell** suggestions   
🔒 Keeps user data **private & secure**  
📚 Educates users **without technical jargon**

---

## 🧠 Features & Capabilities
✨ Built on top of **Google Gemini AI**, FinGPT can:

🔹 **Classify user queries** into investment-related intents  
🔹 Provide **live stock prices**, graphs, and charts  
🔹 Generate **stock predictions** and personalized tips 
🔹 Send **friendly, beautified replies** for a smooth user experience  

---

## 🧰 Technology Stack

| 🧩 Component                | 🔧 Tool/Technology Used                             | 💡 Purpose                                           |
|----------------------------|-----------------------------------------------------|------------------------------------------------------|
| Conversational AI          | Google Gemini + LangChain                           | Smart finance chat assistant                         |
| NLP & Intent Classification| Fine-tuned Google Gemini + LangChain                | Handling chat flows and intents                      |
| Chat Interface              | React + TypeScript                                 | Frontend chatbot interface                           |
| Data Storage               | MongoDB                      | User history & preferences                 |
| Market Insights            | Yahoo Finance API            | Live stock & mutual fund data              |
| Visualization & Charts     | Google Sheets + Plotly       | Interactive charts & graphs                |
| Financial Data Analysis    | Python + Google Colab        | AI model training and data crunching       |
| Realtime Analytics         | Google Analytics             | Track engagement and visualize performance |
| APIs Integration           | FastAPI                      | Custom endpoints for NLP Chatbot           |

---

## 📊 SWOT Analysis
<table>
  <tr>
    <th style="background-color:#d4edda;">🟩 Strengths</th>
    <th style="background-color:#f8d7da;">🟥 Weaknesses</th>
  </tr>
  <tr>
    <td>
      ✅ Fully AI-powered and automated financial assistant<br>
      ✅ Cost-effective with free, serverless tools (Gemini)<br>
      ✅ Real-time market insights and personalized recommendations<br>
    </td>
    <td>
      ⚠️ Dependent on Google’s ecosystem – limited customization<br>
      ⚠️ No direct trading functionality – purely advisory
    </td>
  </tr>
  <tr>
    <th style="background-color:#fff3cd;">🟨 Opportunities</th>
    <th style="background-color:#d1ecf1;">🟦 Threats</th>
  </tr>
  <tr>
    <td>
      🚀 Massive market of untapped new investors in need of financial guidance<br>
      📱 Expansion to WhatsApp, Google Assistant, and voice platforms<br>
      💼 Potential monetization via premium insights and advisory tiers
    </td>
    <td>
      🧠 Competition from large fintechs with integrated trading & advisory platforms<br>
      ⚖️ Regulatory shifts in financial advisory laws
    </td>
  </tr>
</table>


---

## 📁 Project Structure
```
├── backend/                     # Backend for managing APIs and logic
│   ├── src/                     # Backend source files
│   ├── package.json             # Backend dependencies
│   ├── tsconfig.json            # TypeScript config for backend

├── backend_ai/                  # AI engine for Gemini-based financial assistant
│   ├── app.py                   # Main Flask/FastAPI application entry point
│   ├── model.py                 # AI model logic and setup
│   ├── model_config.py          # Configuration for model parameters
│   ├── requirements.txt         # Python package dependencies
│   ├── tools.py                 # Utility tools for AI processing
│   └── .gitignore               # Git ignore rules for backend_ai

├── frontend/                    # Frontend UI of the application
│   ├── public/                  # Static assets (icons, images, etc.)
│   ├── src/                     # Frontend source code (TypeScript)
│   ├── .gitignore               # Git ignore rules for frontend
│   ├── README.md                # Frontend-specific README
│   ├── eslint.config.js         # ESLint configuration
│   ├── index.html               # Root HTML file
│   ├── package.json             # Frontend dependencies
│   ├── tsconfig.app.json        # TypeScript config for app
│   ├── tsconfig.json            # General TypeScript config
│   ├── tsconfig.node.json       # TypeScript config for node scripts
│   └── vite.config.ts           # Vite config for development server

├── graph/                       # Data visualization and stock graph generation
│   ├── graph.py                 # Script for plotting live charts and predictions
│   └── .gitignore               # Git ignore rules for graph module

├── GenAI-Powered Financial Assistant.pdf   # Project documentation (PDF)
├── README.md                                # Main project documentation
```

## 🚀 How to Run

1. **Clone the repository:**
```bash
git clone https://github.com/SagnikBasak04/finance_bot.git
cd finance_bot
```

2. **Run the AI Agent server:**
```bash
cd backend_ai
pip install -r requirements.txt
python app.py
```

3. **Run the Graph server:**
```bash
cd ../graph
python graph.py
```

4. **Run the backend server:**
```bash
cd ../backend
npm install
npm run dev
```

5. **Run the frontend server:**
```bash
cd ../frontend
npm install
npm run dev
```

---

## 👨‍💻 Contributors

| 👤 Name           | 💼 Role                    | 🔗 GitHub             |
|------------------|----------------------------|------------------------|
| **Tamojit Das** (Team Lead)  | Full-Stack Developer        | [GitHub](https://github.com/Tamoziit)            |
| **Sagnik Basak** | AI Engineer & Data Analyst     | [GitHub](https://github.com/SagnikBasak04)            |
| **Anidipta Pal** | AI & Backend Developer     | [GitHub](https://github.com/Anidipta) |
| **Titas Kabiraj** | UI-UX & Frontend Developer            | [GitHub](https://github.com/titas-kabiraj)            |
