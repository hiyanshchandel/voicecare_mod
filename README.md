🧠 VoiceCare AI
<p align="center">
<strong>An empathetic, voice-first AI assistant for elderly care, featuring proactive caregiver alerts.</strong>
</p>
<p align="center">
<img src="https://img.shields.io/badge/Python-3.9+-blue?logo=python&logoColor=white" alt="Python Version">
<img src="https://img.shields.io/badge/Flask-2.x-black?logo=flask&logoColor=white" alt="Flask">
<img src="https://img.shields.io/badge/OpenAI-GPT--4o-brightgreen?logo=openai&logoColor=white" alt="OpenAI">
<img src="https://img.shields.io/badge/Pinecone-Vector_DB-blueviolet?logo=pinecone&logoColor=white" alt="Pinecone">
<img src="https://img.shields.io/badge/Twilio-SMS_Alerts-red?logo=twilio&logoColor=white" alt="Twilio">
</p>
💡 Project Vision
VoiceCare AI is an intelligent assistant designed to provide compassionate and reliable support for elderly users, including those with cognitive challenges like dementia. It goes beyond a simple chatbot by creating a personalized memory for each user and proactively monitoring conversations for critical information. The primary goal is to enhance the user's independence while giving caregivers peace of mind through timely SMS alerts.
✨ Core Features
🧠 Personalized Long-Term Memory: Utilizes a Pinecone vector database to remember personal details like medical conditions, medications, appointments, family contacts, and daily routines.
🚨 Proactive Caregiver Alerts: In the background, conversations are analyzed to detect important user-disclosed information (e.g., "I feel dizzy," "I fell down," or "I have a new doctor's appointment"). A concise summary is then sent as an SMS alert to a designated caregiver via Twilio.
🗣️ Empathetic & Simple Conversation: Prompts are engineered to ensure the AI responds in a calm, patient, and reassuring tone, with simple language suitable for elderly users.
📚 Dynamic Learning: The assistant acknowledges and stores new information provided by the user during a conversation, continuously enriching its knowledge base.
🌐 Intelligent Query Routing: Automatically determines whether a query can be answered from its personal knowledge base or if it requires real-time internet access for topics like news or weather.
⚡ High-Speed Responses: Leverages the Groq API for rapid LLM inference, ensuring a smooth and natural conversational experience.
🛠️ Tech Stack
Category	Technology / Service
Backend	Flask
AI & LLMs	OpenAI (GPT-4o, Embeddings), Groq (for speed)
Database	Pinecone (Vector Database for RAG)
Notifications	Twilio (SMS API)
Primary Language	Python
Deployment	Deployed on a cloud platform (as indicated by deployments)
🏗️ Architectural Overview
The application is built on a modular, Retrieval-Augmented Generation (RAG) architecture. The diagram below illustrates the flow of information from user query to response, including the background monitoring system that alerts caregivers.
📈 Future Improvements
While the current system is a robust proof-of-concept, there are several exciting avenues for future development:
Frontend Interface: A simple, accessible web or mobile interface for both users and caregivers to interact with the system.
Caregiver Dashboard: A dedicated portal for caregivers to view conversation summaries, manage user profiles, and update emergency contact information.
Vocal Tone Analysis: Incorporate speech-to-text models that can analyze vocal tone to detect distress, confusion, or pain, triggering a higher-priority alert.
Multi-Language Support: Extend the prompts and models to handle conversations in multiple languages.
Smart Home Integration: Allow the assistant to control smart devices (e.g., lights, thermostats, emergency buttons) for added safety and convenience.
