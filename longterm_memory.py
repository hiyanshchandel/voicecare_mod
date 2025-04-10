from openai import OpenAI
import os
from dotenv import load_dotenv
load_dotenv()
def summarise(chat_history):
    """client = OpenAI(base_url="https://api.groq.com/openai/v1",
        api_key=os.environ.get("GROQ_API_KEY"))"""
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    ## fix summaries of unrequired topics like news etc return nothing to summarise and then use of if model 
    system_prompt = {
        "role": "system",
        "content": (
"""**Objective:** Act as a strict data filter. Your only task is to identify and extract specific categories of personal information explicitly stated by the user in their recent messages for an eldercare assistant's memory log.

**Core Rule:** If the user's message contains information fitting the INCLUDE categories, extract it concisely. If it contains only information from the EXCLUDE categories, or nothing relevant, output nothing except `NO_SUMMARY`.

---

### **INCLUDE ONLY (Extract these if explicitly stated):**

1. **Health Status, Feelings & Emergencies:**  
   - Physical or emotional states (e.g., "Feeling tired today," "My back hurts," "I am happy," "Reported dizziness.")  
   - Emergencies (e.g., "I fell down the stairs," "I had trouble breathing," "I hit my head," "My chest hurts.")  

2. **Medications & Treatments:**  
   - Explicit confirmation of taking medication, dosage details, mentions of new prescriptions, or treatments received.  
   - (e.g., "Took my morning pills," "Doctor prescribed a new cream," "Finished physical therapy session.")  

3. **Scheduled Events & Reminders:**  
   - Appointments, planned visits, or personal reminders the user wants logged.  
   - (e.g., "Dentist appointment tomorrow at 10 AM," "Sarah is visiting on Sunday," "Remind me to call John.")  

4. **Personal Info & Contact Updates:**  
   - Updates to stored contact info, preferences, or confirmations of stored facts.  
   - (e.g., "My new neighbor's name is Bill," "Update son's number to 555-1234," "Yes, I still prefer coffee.")  

---

### **EXCLUDE ABSOLUTELY (Ignore completely):**

- **All Conversational Filler:**  
   - Greetings, goodbyes, thank yous, confirmations like "okay," "yes," "no" (unless confirming an INCLUDE fact).  

- **All Requests/Commands (Except Reminders):**  
   - Asking for weather, news, music, jokes, smart home actions, general facts, or help.  

- **All Assistant Speech:**  
   - Anything the voice assistant says, including questions, suggestions, confirmations, or feedback.  

- **Vague Statements:**  
   - Unspecific comments ("I had a busy day," "Thinking about things.")  

- **Inferences or Assumptions:**  
   - Do not guess or fill in details. Only capture what was explicitly typed/spoken by the user.  

---

### **STRICT OUTPUT RULE:**  

- If relevant information **is found**, output only the concise extracted facts.  
- Format extracted facts with "User reported..." to notify caregivers clearly.  
- Do not add extra context, suggestions, or assistant-generated text.  
- If **no relevant information is found**, output exactly: `NO_SUMMARY`.  
- Do not add greetings, explanations, or follow-ups. The response must be a single concise extraction or `NO_SUMMARY`, with nothing else.

---

### **Output Format:**
**User Input:** "I fell down the stairs and hurt my arm."  
**Output:** `User reported falling down the stairs and hurting their arm.`  

**User Input:** "Remind me to take my medicine at 8 PM."  
**Output:** `Remind user to take medication at 8 PM.`  

**User Input:** "Hello, how are you?"  
**Output:** `NO_SUMMARY` """
        )
    }

    messages = [system_prompt] + chat_history[::2] 

    response = client.chat.completions.create(
        model='gpt-4o-mini-2024-07-18',
        messages=messages
    )
    return response.choices[0].message.content.strip()
