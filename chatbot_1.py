from openai import OpenAI
from langchain.vectorstores import Pinecone
from langchain.memory import ConversationBufferMemory
from pinecone import Pinecone as  pie
from langchain.chat_models import ChatOpenAI
from router import routing
import os
from embeddings import create_embeddings
from langchain_community.chat_models import ChatOpenAI
from dotenv import load_dotenv
load_dotenv()
pc = pie(api_key = os.environ.get("PINECONE_API_KEY"))
index = pc.Index("voicecare5")
memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
llm = ChatOpenAI(base_url="https://api.groq.com/openai/v1",
        api_key=os.environ.get("GROQ_API_KEY"), model_name=os.environ.get("SUMMARY_MODEL_NAME"))

def search_pinecone(query, user_id):
    query_embedding = create_embeddings(query)
    results = index.query(namespace = user_id,vector=query_embedding, top_k=4, include_values=False, include_metadata=True)
    results = [results['matches'][0]['metadata']['content'] + results['matches'][1]['metadata']['content'] + results['matches'][2]['metadata']['content'] + results['matches'][3]['metadata']['content']]
    return "\n".join(results)  


def get_response(user_input,user_id):
    type = routing(user_input)
    if type == "General Query":
        search_results = search_pinecone(user_input,user_id)
        chat_history = memory.load_memory_variables({})["chat_history"]
        prompt = f"""
        **Your Role:** You are VoiceCare, a caring, patient, and helpful voice assistant for elderly users, including those with dementia. You maintain a knowledge base of their personal details.
**Your Goal:** Answer the user's query clearly, simply, and reassuringly. Keep responses concise (usually 1-3 sentences) and use a calm, natural tone. **Crucially, acknowledge when the user provides new information for you to remember.**

**Instructions:**

1.  **Analyze Query & Knowledge:** Carefully compare the 'User Query' with the 'Retrieved Knowledge'.
    *   **Answering Questions:** If the query asks a question that the 'Retrieved Knowledge' can answer (e.g., "What meds do I take?", "Who is my doctor?"), use that information to respond directly.
    *   **Acknowledging NEW Information:** If the 'User Query' seems to be *providing new personal information* or *updating existing details* (e.g., "My daughter's new phone number is...", "Please remember I dislike fish", "I started taking aspirin today"), **your primary response should be to acknowledge this**. Use phrases like:
        *   "Okay, I'll remember that."
        *   "Got it, I've made a note of [specific detail, e.g., 'the new phone number']."
        *   "Thank you for letting me know, I'll keep that in mind."
        *   "Okay, I'll update that information."
        **After acknowledging, if the user's input also contained a separate question, answer that question briefly.** If it was only providing information, the acknowledgment is the full response.

2.  **Use Conversation History:** Refer to the 'Conversation History' for conversational context, but prioritize Retrieved Knowledge for known facts and the User Query for new information.

3.  **General Knowledge Fallback:** If the Retrieved Knowledge is empty or irrelevant, AND the query is a general question (facts, jokes, simple chat) not providing new personal info, answer using your general knowledge.

4.  **Simplicity is Key:** Avoid jargon or complex sentences. Use a reassuring tone.

5.  **Handle Confusion:** If the user seems confused by *your* response or previous turns, gently clarify or repeat key information.

6.  **Conciseness:** Keep responses brief and to the point, especially after acknowledging new information.
"

        Conversation History:
        {chat_history}

        Retrieved Knowledge:
        {search_results}

        User Query: {user_input}
        """
        
        response_obj = llm.invoke(prompt)
        response_text = response_obj.content if hasattr(response_obj, 'content') else str(response_obj)
        memory.save_context({"input": user_input}, {"output": response_text})
        print(response_text)
        return response_text

    
    else:
        client = OpenAI(api_key = os.environ.get("OPENAI_API_KEY"))
        response = client.chat.completions.create(
            model = os.environ.get("SEARCH_MODEL"),
            web_search_options={
                "user_location": {
            "type": "approximate",
            "approximate": {
                "country": "IN",
                "city": "Jaipur",
                "region": "Jaipur",
                }
                },
            },
            messages = [
                        {
                        "role": "system",
                        "content": "You are an AI assistant providing spoken responses for a voice-based system. Keep answers concise (1-3 sentences per topic) and avoid unnecessary details, long explanations, or hyperlinks. Do not mention website names, sources, or references. Summarize key information clearly in simple, natural language for easy listening.Always respond in the **same language** as the user's input. If the user speaks in English, reply in English. If the user speaks in Hindi, reply in Hindi. Maintain the language of the conversation throughout.",
                        },
                        {"role": "user", 
                         "content": user_input}  
                     ]
        )
        response_text = response.choices[0].message.content
        client = OpenAI(base_url="https://api.groq.com/openai/v1",
        api_key=os.environ.get("GROQ_API_KEY"))
        response = client.chat.completions.create(
            model=os.environ.get("SUMMARY_MODEL_NAME"),
            messages=[
                {"role": "system", "content": """You are an expert summarizer creating content for a voice assistant. Your task is to distill the provided text into only its most essential headlines or key points. 
                                                **Instructions:** 
                                                - **Extract Core Facts:** Identify and pull out only the main pieces of information. 
                                                - **Remove Everything Else:** Eliminate introductions, conclusions, conversational filler, explanations, and redundant details. \
                                                - **Be Concise:** Keep each point brief and clear. 
                                                - **Natural Tone:** Phrase the summary in simple, natural language suitable for being spoken aloud. 
                                                - **Output Format:** Return ONLY the summarized key points as plain text. Do not add any intro/outro phrases like 'Here is the summary:' or 'These are the key points:'. Just the summarized text itself."""},
                {"role": "user", "content": response_text}
            ]
        )
        return response.choices[0].message.content.strip()

        
    
if __name__ == "__main__":
    print("Chatbot is running. Type 'exit' to stop.")
    while True:
        user_message = input("You: ")
        if user_message.lower() == "exit":
            print("Bot: Goodbye!")
            break
        response = get_response(user_message)
        print("Bot:", response)

    

    



