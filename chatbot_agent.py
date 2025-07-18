import os
import re
from datetime import datetime
from dateutil.relativedelta import relativedelta, MO, TU, WE, TH, FR, SA, SU
from dotenv import load_dotenv

from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain_groq import ChatGroq

from resources.rag_query import get_relevant_chunks
from tools.book_appointment import book_appointment_sync
from prompt_template import template

# Load environment variables
load_dotenv()

# ------------------------ Groq LLM Setup ------------------------ #
llm = ChatGroq(
    model_name="llama3-70b-8192",
    api_key=os.getenv("GROQ_API_KEY")
)


prompt = PromptTemplate.from_template(template)
chain = LLMChain(llm=llm, prompt=prompt)


# Remove global chat_history
def run_agent(user_input: str, chat_history: list) -> tuple:
    # Step 1: Add user message to history
    chat_history.append(f"You: {user_input}")
    history = "\n".join(chat_history[-10:])  # limit to last 10 messages

    # Step 2: Fetch context from RAG (if any)
    chunks = get_relevant_chunks(user_input)
    context = "\n".join([doc.page_content for doc in chunks])


    # Step 4: Run the chain
    response = chain.run({
        "question": user_input,
        "context": context,
        "history": history
    }).strip()

    # Step 5: Add bot response to history
    chat_history.append(f"Thara: {response}")

    # Step 6: Check and handle TOOL:book(...)
    if response.startswith("TOOL:book("):
        try:
            booking_result = book_appointment_sync(response)
            # Generate a user-friendly confirmation message
            # Try to extract name, date, and time from the tool call
            import re
            match = re.match(r"TOOL:book\\((.*?), (.*?), (.*?)\\)", response)
            if match:
                name, date, time = match.groups()
                confirmation = f"Your appointment is booked for {date} at {time}, {name}!"
            else:
                confirmation = booking_result
            # Do not append the tool call, just append the confirmation as a new bot message
            chat_history.append(f"Thara: {confirmation}")
            return confirmation, chat_history
        except Exception as e:
            return f"❌ Failed to parse TOOL:book(...) input: {e}", chat_history

    # TODO: Handle TOOL:update(...) or TOOL:cancel(...) if needed

    return response, chat_history


