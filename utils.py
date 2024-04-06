class DummyResponse:
    def __init__(self, text):
        self.text = text

def join_list_into_string(my_list):
    result = ""
    for i, item in enumerate(my_list):
        result += f"{i+1}. {item}\n\n"
    return result.rstrip()


def separate_last_user_query(conversation):
    """
    Separate the last user query from the conversation.

    Args:
        conversation (str): The conversation to separate the last user query from.

    Returns:
        str or None: The last user query if found, otherwise None.
    """
    lines = conversation.splitlines()

    if not lines:
        return None

    user_queries = [line.split(": ", maxsplit=1)[1] for line in lines if line.startswith("User:")]

    return user_queries[-1] if user_queries else None

def choose_method_for_handling_user_query(conversation_text, GEMINI):

    user_last_query = separate_last_user_query(conversation_text)
    prompt = f"""You are an Assistant and you have a movie database
Given the following conversation:
{conversation_text}

User's last query:
{user_last_query}

What do you need to do to answer the user's last query helpfully and faithfully? (Please ask for clarifications only when necessary)
A. Answer the question directly you already knew how to response (applies to greetings, casual conversation, etc)
B. Get information from the database and answer based on it
C. Ask for clarification question
Note: Please answer using letters (A. or B. or C.)
    """

    response = GEMINI.generate_content(prompt)
    return response


def ask_for_clarification_questions(conversation_text, GEMINI):
    prompt = f"""Given the following conversation
{conversation_text}

Generate a clarification question given the conversation history, with the aim to be as helpful to the user as possible
    """
    response = GEMINI.generate_content(prompt)
    return response


def query_reformulation(conversation_text, GEMINI):
    user_last_query = separate_last_user_query(conversation_text)
    prompt = f"""Given the following conversation
{conversation_text}

User's last query:
{user_last_query}

Please rewrite the last user's query so that the rewritten query can be used to search and satisfy the user's information needs. It is best that the reformulated query is in the form of a question
    """

    response = GEMINI.generate_content(prompt)
    return response


def answer_user_directly(conversation_text, GEMINI):
    selected_conversation_text = conversation_text if len(conversation_text) < 3000 else separate_last_user_query(conversation_text)
    prompt = f"""You are an Assistant
Given the following conversation
{selected_conversation_text}

Please give a response in a faithful and helpful manner
Assistant:
    """

    response = GEMINI.generate_content(prompt)
    return response

def check_if_history_is_complusory(query, GEMINI):
    prompt = f"""Given the current user's query
{query}

In the query, is the conversation history necessary for answering the user's last query? Please answer Yes or No
    """
    response = GEMINI.generate_content(prompt)
    if "Yes" in response.text or "yes" == response.text: return True
    else: return False

def check_if_context_is_relevant(query, string_context, GEMINI):
    prompt = f"""Given the following query and context. Is the context has relevant information to answer the query
Query: {query}

Context: {string_context}

Choose:
A. Yes
B. No
Note: Please answer using letters (A. or B.)
"""
    response = GEMINI.generate_content(prompt)
    if "A." in response.text or "A" == response.text: return True
    else: return False

def answer_query_with_context(query, conversation_text, contexts, GEMINI):
    string_context = join_list_into_string(contexts)

    context_relevant = check_if_context_is_relevant(query, string_context, GEMINI)
    history_require = check_if_history_is_complusory(query, GEMINI)
    if not context_relevant: return DummyResponse(text = "I am very sorry for the inconvenience, I cannot find the right information for your question")

    else:
        print(f"\n--------\nMESSAGE: {string_context}\n--------\n")
        prompt = f"""You are an Assistant
Given the following conversation history, reformulated user's query and context.

Conversation history:
{conversation_text}

Reformulated query:
{query}

Retrieved Context:
{string_context}

Please answer the user based on the information in the context
        """
        response = GEMINI.generate_content(prompt)
        return response




def handle_conversation_turn(conversation_history, my_vectordb, SENTEMB, GEMINI):
    method_for_answering = choose_method_for_handling_user_query(conversation_history, GEMINI)

    if "A." in method_for_answering.text or "A" == method_for_answering.text:
        print("\n--------\nLOGGING: answer query directly\n--------\n")
        return answer_user_directly(conversation_history, GEMINI) # put all history

    elif "B." in method_for_answering.text or "B" == method_for_answering.text:
        reformulated_query = query_reformulation(conversation_history, GEMINI)
        print("\n--------\nLOGGING: answer query with retrieval. Reformulated query:", reformulated_query.text, "\n--------\n")
        query_results = my_vectordb.query(
            query_embeddings=SENTEMB.encode([reformulated_query.text]),
            n_results=5,
        )
        contexts = [f"Movie title: {line.get('title')}\nOverview: {line.get('overview')}\nGenre info: {str(line.get('genres'))}\nRelease date: {line.get('release_date')}\nAveraged vote rating: {line.get('vote_average')}\nVote count: {line.get('vote_count')}" for line in query_results["metadatas"][0]]

        return answer_query_with_context(reformulated_query.text, conversation_history, contexts, GEMINI)

    elif "C." in method_for_answering.text or "C" == method_for_answering.text:
        print("\n--------\nLOGGING: asking clarification question\n--------\n")
        return ask_for_clarification_questions(conversation_history, GEMINI)
