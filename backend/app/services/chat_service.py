from langchain_openai import ChatOpenAI
from langchain.agents import AgentExecutor, create_openai_functions_agent
from langchain import hub # To pull prompts easily
from app.core.config import OPENAI_API_KEY
from app.services import vector_store
from app.tools.calculator import calculator # Import your tool

# 1. Initialize LLM
# Make sure the model supports function calling (e.g., gpt-3.5-turbo, gpt-4)
llm = ChatOpenAI(model="gpt-4", temperature=0, api_key=OPENAI_API_KEY)

# 2. Define Tools
tools = [calculator]

# 3. Create Agent
# Pull a recommended prompt template for function calling
# Find prompts at https://smith.langchain.com/hub/
prompt = hub.pull("hwchase17/openai-functions-agent")

agent = create_openai_functions_agent(llm, tools, prompt)

# Create the agent executor by passing in the agent and tools
agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    verbose=True, # Set to True to see agent's thoughts/steps (good for debugging)
    # Add memory here later for bonus points if needed
    # handle_parsing_errors=True # Optional: Helps with potential output format issues
)

def format_context(docs_results):
    """Formats retrieved documents into a string for the prompt."""
    context = "\n---\n".join([
        f"Source: {meta.get('source', 'N/A')}, Page: {meta.get('page', 'N/A')}\nContent: {doc}"
        for doc, meta in zip(docs_results.get('documents', [[]])[0], docs_results.get('metadatas', [[]])[0])
        if doc # Ensure there's content
    ])
    if not context:
         return "No relevant documents found."
    return f"Relevant document context:\n{context}"


async def get_chat_response(query: str):
    """Processes user query: RAG + Agent."""

    # 1. RAG: Retrieve relevant documents
    retrieved_docs_results = vector_store.search_documents(query)
    context = format_context(retrieved_docs_results)

    # 2. Prepare input for the Agent
    # Include both the original query and the retrieved context
    agent_input = {
        "input": f"User Query: {query}\n\n{context}",
        # Add chat_history here if implementing memory
        # "chat_history": [...]
    }

    # 3. Run the Agent
    try:
        # Use await for invoke if the agent executor supports async or run in executor
        # For simplicity here, using synchronous invoke
        # If blocking is an issue, use: await asyncio.get_event_loop().run_in_executor(None, agent_executor.invoke, agent_input)
        response = agent_executor.invoke(agent_input)
        answer = response.get("output", "Agent did not provide an output.")

        # Optional: Include reasoning steps if verbose=True and you capture logs/callbacks
        # For bonus: you might need LangChain callbacks to capture intermediate steps.

    except Exception as e:
        print(f"Agent execution error: {e}")
        # Fallback: Maybe just use LLM directly without agent? Or return error.
        answer = f"Sorry, I encountered an error processing your request: {e}"

    return answer