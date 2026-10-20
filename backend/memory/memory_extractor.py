from rag.generator import load_llm

llm = load_llm()


def extract_memories(user_message):

    prompt = f"""
You are a memory extraction system.

Your task is to decide whether the USER MESSAGE contains
useful information that should be remembered for future conversations.

Useful memories include:
- User preferences
- User goals
- User interests
- Skills
- Career goals
- Education goals
- Long-term project preferences

Do NOT store:
- Questions asked by the user
- Temporary requests
- General knowledge
- Facts about other people
- Greetings
- Casual conversation
- Information that is not useful in future conversations

IMPORTANT:
Only extract information explicitly stated by the user.

Return EXACTLY ONE of these formats:

MEMORY | category | memory

OR

NONE

Allowed categories:
preference
goal
interest
skill
career
education

Examples:

User message:
I prefer Python for my projects.

Output:
MEMORY | preference | I prefer Python for my projects.

User message:
I am preparing for software developer placements.

Output:
MEMORY | career | I am preparing for software developer placements.

User message:
I am interested in artificial intelligence.

Output:
MEMORY | interest | I am interested in artificial intelligence.

User message:
What is machine learning?

Output:
NONE

User message:
Hello, how are you?

Output:
NONE

USER MESSAGE:
{user_message}
"""

    response = llm.invoke(prompt)

    return response.content.strip()


def parse_memory(result):

    if result == "NONE":
        return None

    parts = result.split("|", 2)

    if len(parts) != 3:
        return None

    memory_type = parts[0].strip()
    category = parts[1].strip().lower()
    memory = parts[2].strip()

    if memory_type != "MEMORY":
        return None

    allowed_categories = {
        "preference",
        "goal",
        "interest",
        "skill",
        "career",
        "education"
    }

    if category not in allowed_categories:
        return None

    if not memory:
        return None

    return {
        "category": category,
        "memory": memory
    }