from openai import OpenAI
import os
from dotenv import load_dotenv
load_dotenv()
def summarise(chat_history):
    client = OpenAI(base_url="https://api.groq.com/openai/v1",
        api_key=os.environ.get("GROQ_API_KEY"))
    ## fix summaries of unrequired topics like news etc return nothing to summarise and then use of if model 
    system_prompt = {
        "role": "system",
        "content": (
"""
**Objective:** Act as a strict data filter. Your *only* task is to identify and extract specific categories of personal information explicitly stated by the user in their recent messages for an eldercare assistant's memory log.

**Core Rule:** If the user's message contains information fitting the **INCLUDE** categories, extract it concisely. If it contains *only* information from the **EXCLUDE** categories, or nothing relevant, output *nothing* except `NO_SUMMARY`.

**INCLUDE ONLY (Extract these if explicitly stated):**

1.  **Health Status & Feelings:** Direct statements about physical or emotional state (e.g., "Feeling tired today," "My back hurts," "I am happy," "Reported dizziness").
2.  **Medications & Treatments:** Explicit confirmation of taking medication, dosage details, mentions of new prescriptions, or treatments received (e.g., "Took my morning pills," "Doctor prescribed a new cream," "Finished physical therapy session").
3.  **Scheduled Events & Reminders:** Stated appointments, planned visits, or personal reminders the user wants logged (e.g., "Dentist appointment tomorrow at 10 AM," "Sarah is visiting on Sunday," "Remind me to call John").
4.  **Personal Info & Contact Updates:** Direct statements updating contact information, stated preferences, or confirmations of stored facts (e.g., "My new neighbor's name is Bill," "Update son's number to 555-1234," "Yes, I still prefer coffee").

**EXCLUDE ABSOLUTELY (Ignore completely):**

1.  **ALL Conversational Filler:** Greetings, goodbyes, thank yous, confirmations like "okay," "yes," "no" unless confirming a specific fact for memory (see Include #4).
2.  **ALL Requests/Commands (Except Reminders):** Asking for weather, news, music, jokes, smart home actions, general facts, or help.
3.  **ALL Assistant Speech:** Anything the voice assistant says, including questions, suggestions, confirmations, or feedback.
4.  **Vague Statements:** Unspecific comments (e.g., "I had a busy day," "Thinking about things").
5.  **Inferences or Assumptions:** DO NOT guess or fill in details. Only capture what was *explicitly typed/spoken* by the user.

**Output Requirements:**

*   **If relevant information IS found:** Output *only* the concise summary of the extracted facts. (e.g., `User reported feeling nauseous. Confirmed taking evening medication. Doctor appointment Tuesday 3 PM.`)
*   **If NO relevant information IS found:** Output *exactly* the single line `NO_SUMMARY`. **Do not output ANY other text, explanation, or comment before or after `NO_SUMMARY` in this case.**
"""
        )
    }

    messages = [system_prompt] + chat_history 

    response = client.chat.completions.create(
        model=os.environ.get("SUMMARY_MODEL_NAME"),
        messages=messages
    )
    return response.choices[0].message.content.strip()
