🧠 VoiceCare AI
An empathetic, voice-first AI assistant for elderly care, featuring proactive caregiver alerts.

<p align="center"> <img src="https://img.shields.io/badge/Python-3.9+-blue?logo=python&logoColor=white" alt="Python Version"> <img src="https://img.shields.io/badge/Flask-2.x-black?logo=flask&logoColor=white" alt="Flask"> <img src="https://img.shields.io/badge/OpenAI-GPT--4o-brightgreen?logo=openai&logoColor=white" alt="OpenAI"> <img src="https://img.shields.io/badge/Pinecone-Vector_DB-blueviolet?logo=pinecone&logoColor=white" alt="Pinecone"> <img src="https://img.shields.io/badge/Twilio-SMS_Alerts-red?logo=twilio&logoColor=white" alt="Twilio"> </p>
💡 Project Vision
VoiceCare AI is an intelligent, voice-first assistant designed to offer compassionate support to elderly users, including those with cognitive challenges like dementia. It creates a personalized memory for each user and proactively monitors conversations to detect critical information, alerting caregivers in real time.

The goal is to enhance user independence while giving caregivers peace of mind.

✨ Key Features
🧠 Personalized Long-Term Memory
Remembers personal details (e.g., medical history, medications, appointments, family members) using a Pinecone vector database.

🚨 Proactive Caregiver Alerts
Detects phrases like “I fell” or “I feel dizzy” and automatically sends concise alerts to caregivers via Twilio SMS.

🗣️ Empathetic & Simple Conversations
Interactions use simple, reassuring language, ideal for elderly users, including those with dementia.

📚 Dynamic Learning
Learns and updates user profiles in real time as new information is shared during conversations.

🌐 Intelligent Query Routing
Automatically distinguishes between queries answerable via internal memory and those requiring real-time web access.

⚡ High-Speed Responses
Leverages Groq API for ultra-fast LLM inference, enabling smooth, natural conversation flow.

🛠️ Tech Stack
Category	Technology / Service
Backend	Flask
AI & LLMs	OpenAI (GPT-4o, Embeddings), Groq
Database	Pinecone (Vector DB for RAG)
Notifications	Twilio (SMS API)
Primary Language	Python
Deployment	Cloud-based platform

🏗️ Architectural Overview
VoiceCare AI follows a modular RAG (Retrieval-Augmented Generation) architecture.
Information flows from the user's voice input to intelligent memory and processing layers, with a parallel background monitoring system that triggers alerts as needed.

🚀 Future Improvements
✅ Frontend Interface
Build a simple web or mobile interface for users and caregivers.

✅ Caregiver Dashboard
Portal to view summaries, manage profiles, and update emergency contacts.

✅ Vocal Tone Analysis
Analyze speech tone to detect distress, confusion, or pain, with elevated alert levels.

✅ Multi-Language Support
Enable conversations in multiple languages for global accessibility.

✅ Smart Home Integration
Control smart devices like lights, thermostats, and emergency systems for safety and convenience.

