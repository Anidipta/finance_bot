# FinGPT - AI-Powered Financial Assistant

## Table of Contents
1. [Introduction](#introduction)
2. [Unique Selling Proposition (USP)](#unique-selling-proposition)
3. [Problem Statement](#problem-statement)
4. [Market Opportunity](#market-opportunity)
5. [Solution Overview](#solution-overview)
6. [Technology Stack](#technology-stack)
7. [SWOT Analysis](#swot-analysis)
8. [Project Structure](#project-structure)
9. [How to Run](#how-to-run)
10. [Contributors](#contributors)

## Introduction
India has hundreds of millions of new investors, but financial literacy remains low. There is no scalable way to educate and guide these users. Manual advisory is impractical, and existing platforms focus on experienced investors.

## Unique Selling Proposition (USP)
✅ 100% Free Google Tools – No payments required, forever scalable.  
✅ Serverless Deployment – No hosting cost using Firebase.  
✅ Real-time Market Insights – Using Google Finance API.  
✅ Multi-Language Support – Gemini AI understands local languages.  
✅ Privacy Focused – No sensitive data stored beyond chat history.  
✅ Personalized Investment Recommendations – AI-driven tailored suggestions.  
✅ Simplified Learning – Financial education without jargon.  

## Problem Statement
Many new investors in India lack financial literacy and are unable to make informed investment decisions. Existing solutions cater to experienced investors, leaving a massive gap in accessible, beginner-friendly financial guidance.

## Market Opportunity
- India has over **200 million retail investors**, growing rapidly due to digital platforms.
- Financial literacy remains **below 30%**, creating a need for educational tools.
- The mutual fund industry in India is worth **₹40 trillion+** and continues to expand.
- **Mobile-first financial services** are in high demand, with increasing smartphone penetration.

## Solution Overview
We are building a GenAI-powered Financial Assistant that:
- Answers investment-related questions in simple language.
- Guides users on financial literacy without technical jargon.
- Suggests suitable investment options based on their needs.
- Provides real-time market insights using free Google tools.
- Ensures scalability and accessibility without paid APIs or infrastructure.

## Technology Stack
| Component                 | Google Free Tool Used            | Purpose |
|---------------------------|--------------------------------|--------------------------------------------------|
| Conversational AI         | Google Gemini API             | AI-powered chatbot for answering finance questions. |
| Chat Interface           | Google Dialogflow CX          | Manages structured conversations with users. |
| Hosting & Deployment     | Google Firebase Hosting      | Deploys the web & mobile app without server costs. |
| Backend Processing       | Google Cloud Functions       | Executes AI queries dynamically. |
| User Data Storage        | Google Firestore             | Stores user interactions, preferences, and chat history. |
| Market Insights         | Yahoo Finance API | Retrieves live stock market & mutual fund data. |
| Data Analysis           | Google Colab                 | Performs financial trend analysis using Python. |
| User Interaction Analytics | Google Analytics           | Tracks user engagement & app performance. |
| Dashboard & Reports     | Google Looker Studio        | Creates reports for insights on user behavior. |

## SWOT Analysis
### Strengths
- Fully automated and AI-powered financial assistant.
- Uses **free, serverless** Google tools, making it cost-effective.
- Provides **real-time market insights** and personalized recommendations.
- Supports **multi-language** interactions for broader accessibility.

### Weaknesses
- Relies on Google’s ecosystem, which may limit customization.
- No direct trading functionality (only educational guidance and recommendations).

### Opportunities
- Huge market of **new investors** in need of financial education.
- Can expand to WhatsApp, Google Assistant, and voice-based services.
- Potential for monetization via premium advisory features.

### Threats
- Competition from established fintech apps with integrated trading services.
- Regulatory changes in financial advisory laws.

## Project Structure
```
├── /src                 # Main source code
│   ├── /components      # UI components for chatbot
│   ├── /services        # API calls and data processing
│   ├── /utils           # Utility functions for AI & finance calculations
├── /public              # Static assets
├── /firebase            # Firebase cloud functions & hosting configuration
├── README.md            # Project documentation
```

## How to Run
1. Clone the repository:
   ```bash
   git clone https://github.com/your-repo/GenAI-Financial-Assistant.git
   cd GenAI-Financial-Assistant
   ```
2. Install dependencies:
   ```bash
   npm install
   ```
3. Set up Firebase:
   - Create a Firebase project.
   - Enable Firestore and Hosting.
   - Deploy using:
   ```bash
   firebase deploy
   ```
4. Start the development server:
   ```bash
   npm start
   ```

## Contributors
| Name        | Role                   | GitHub Profile  |
|------------|------------------------|-----------------|
| Sagnik Basak | Project Lead           | [GitHub](https://github.com/user1) |
| Anidipta Pal | AI & Backend Developer | [GitHub](https://github.com/user2) |
| Tamojit Das | Frontend Developer    | [GitHub](https://github.com/user3) |
| Tutas Khabiraj | Data Analyst          | [GitHub](https://github.com/user4) |


