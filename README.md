VoiceCare AI 🧠
<p align="center">
<img src="https://img.shields.io/badge/Python-3.9+-blue?logo=python&logoColor=white" alt="Python Version">
<img src="https://img.shields.io/badge/Flask-2.x-black?logo=flask&logoColor=white" alt="Flask">
<img src="https://img.shields.io/badge/OpenAI-GPT--4-brightgreen?logo=openai&logoColor=white" alt="OpenAI">
<img src="https://img.shields.io/badge/Pinecone-Vector_DB-blueviolet?logo=pinecone&logoColor=white" alt="Pinecone">
<img src="https://img.shields.io/badge/Twilio-SMS_Alerts-red?logo=twilio&logoColor=white" alt="Twilio">
<img src="https://img.shields.io/badge/License-MIT-green" alt="License">
</p>
VoiceCare AI is an empathetic, voice-first AI assistant designed specifically for elderly users, including those with dementia. It combines a personalized knowledge base with proactive monitoring to provide reliable assistance and peace of mind for caregivers.
The system is built to understand and remember user-specific information, answer questions simply and clearly, and intelligently identify critical information from conversations to alert caregivers in near real-time.
✨ Core Features
🧠 Personalized Long-Term Memory: Utilizes a Pinecone vector database to store and retrieve personal details like medical conditions, medications, appointments, family contacts, and daily routines.
🚨 Proactive Caregiver Alerts: In the background, conversations are analyzed to detect important user-disclosed information (e.g., "I feel dizzy," "I fell down," "I have a new doctor's appointment"). A concise summary is then sent as an SMS alert to a designated caregiver via Twilio.
🗣️ Empathetic & Simple Conversation: Prompts are engineered to ensure the AI responds in a calm, patient, and reassuring tone, with simple language suitable for elderly users.
📚 Dynamic Learning: The assistant can acknowledge and store new information provided by the user during a conversation, continuously enriching its knowledge base.
🌐 Intelligent Query Routing: Automatically determines whether a query requires its personal knowledge base (General Query) or real-time internet access for topics like news or weather (Internet Lookup).
⚡ High-Speed Responses: Leverages the Groq API for rapid LLM inference, ensuring a smooth and natural conversational experience.
📝 Easy Onboarding: A simple form-based endpoint allows caregivers to quickly set up a user's initial knowledge base.
🏗️ Architectural Overview
The application follows a modular, RAG (Retrieval-Augmented Generation) based architecture. The core logic flow is as follows:
Generated mermaid
graph TD
    subgraph User Interaction
        A[User Speaks/Types Query] --> B{Flask API Server};
    end

    subgraph Core Logic
        B --> C{Router};
        C -- "General Query" --> D[Retrieve Context from Pinecone];
        D --> E[Build Prompt with History & Context];
        E --> F{LLM (Groq)};
        F --> G[Generate Empathetic Response];
        C -- "Internet Lookup" --> H{Web Search LLM (OpenAI)};
        H --> I[Summarize for Voice];
        I --> G;
    end
    
    subgraph Background Monitoring
        J[Conversation History]-- every 2 turns --> K{Long-Term Memory Summarizer};
        K -- "Is Summary Relevant?" --> L{If Yes};
        L --> M[Upsert Summary to Pinecone];
        L --> N[Send SMS Alert via Twilio];
        K -- "Not Relevant (NO_SUMMARY)" --> O[Do Nothing];
    end

    subgraph Output
        G --> P[Send Response to User];
    end

    style F fill:#87CEEB
    style H fill:#87CEEB
    style K fill:#FFD700
    style N fill:#FF6347
Use code with caution.
Mermaid
🛠️ System Components
main.py: The Flask web server that exposes API endpoints, manages chat histories, and orchestrates the background summarization tasks.
chatbot_1.py: The core chatbot logic. It handles routing, context retrieval from Pinecone, prompt construction, and interaction with the primary LLM.
router.py: A classification module that categorizes user input into General Query or Internet Lookup.
longterm_memory.py: A specialized summarization module that filters chat history to extract only critical personal and health-related information stated by the user.
summary_upsertion.py: Upserts the critical summaries into Pinecone and triggers the Twilio SMS notification to caregivers.
vectordb_upsertion.py: Handles the initial data ingestion from the setup form, creating and storing embeddings for the user's core information.
embeddings.py: A helper utility to generate vector embeddings using OpenAI's models.
messaging.py: A simple wrapper for the Twilio API to send SMS messages.
