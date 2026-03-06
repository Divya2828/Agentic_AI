
import os
from dotenv import load_dotenv
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from langchain.agents import create_agent
from prompt import Agent_Prompt

load_dotenv()


@tool
def search(query: str) -> str:
    """Search for information in the document."""
    return f"Search results for '{query}' in the document."


@tool
def get_business(document: str) -> str:
    """Get business information from the document."""
    return f"Business information: {document[:500]}..."


tools = [search, get_business]
agent = None


def _init_agent():
    global agent

    if agent is None:
        api_key = os.environ.get("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY is missing in your environment.")

        llm = ChatOpenAI(
            model=os.environ.get("CHAT_MODEL", "mistralai/mistral-7b-instruct"),
            base_url=os.environ.get("OPENAI_API_BASE", "https://openrouter.ai/api/v1"),
            api_key=api_key,
            temperature=0,
        )

        agent = create_agent(
            model=llm,
            tools=tools,
            system_prompt=Agent_Prompt,
        )


def generate_business_model(document_content: str) -> str:
    """
    Generate a business model based on the provided document content.
    """
    try:
        _init_agent()

        response = agent.invoke(
            {
                "messages": [
                    {
                        "role": "user",
                        "content": (
                            "Generate a comprehensive business model based on the following "
                            "document content. Include key components like value proposition, "
                            "revenue streams, target market, channels, customer segments, "
                            "cost structure, and key partnerships.\n\n"
                            f"{document_content}"
                        ),
                    }
                ]
            }
        )

        # Extract final text safely
        messages = response.get("messages", [])
        if messages:
            last_message = messages[-1]

            # AIMessage usually exposes `.content`
            if hasattr(last_message, "content"):
                return last_message.content

            # fallback if dict-like
            if isinstance(last_message, dict):
                return last_message.get("content", str(last_message))

        return str(response)

    except Exception as e:
        return f"Error generating business model: {e}. Please check your API setup."