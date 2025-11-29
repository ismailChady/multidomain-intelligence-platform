import streamlit as st
from google import genai

# Layout
st.set_page_config(page_title="AI Assistant")
st.title("Multi-Domain AI Assistant")
st.write(
    "Ask questions about **Cybersecurity**, **Data Science**, or **IT Operations**. "
    "The assistant will adapt its answers based on the domain."
)

# Gemini Client (API Key from secrets.toml)
api_key = st.secrets["GEMINI_API_KEY"]
client = genai.Client(api_key=api_key)

MODEL = "gemini-2.5-flash"

# Domain-specific system prompts
DOMAINS = {
    "Cybersecurity": {
        "system": (
            "You are a cybersecurity expert assistant. Provide incident analysis, "
            "defensive security guidance, security controls, and explain vulnerabilities "
            "in simple actionable language."
        )
    },
    "Data Science": {
        "system": (
            "You are a data science assistant. Help with data cleaning, analysis, "
            "visualizations, statistics, and machine learning. Explain everything clearly "
            "with examples when possible."
        )
    },
    "IT Operations": {
        "system": (
            "You are an IT operations expert. Provide practical troubleshooting advice, "
            "automation strategies, monitoring best practices, and infrastructure guidance."
        )
    }
}

if "current_domain" not in st.session_state:
    st.session_state.current_domain = "Cybersecurity"

if "messages_by_domain" not in st.session_state:
    st.session_state.messages_by_domain = {}


def get_messages(domain: str):
    """Return message history for domain, initializing with its system prompt."""
    msgs = st.session_state.messages_by_domain.get(domain)

    if not msgs:
        msgs = [
            {"role": "user", "content": DOMAINS[domain]["system"]}
        ]
        st.session_state.messages_by_domain[domain] = msgs

    return msgs


# Sidebar: domain selector + clear chat
with st.sidebar:
    st.header("Settings")

    domain = st.radio(
        "Active domain",
        list(DOMAINS.keys()),
        index=list(DOMAINS.keys()).index(st.session_state.current_domain),
    )

    if domain != st.session_state.current_domain:
        st.session_state.current_domain = domain

    msgs = get_messages(domain)
    st.write(f"Messages: **{len(msgs) - 1}**")  

    if st.button("Clear chat history"):
        st.session_state.messages_by_domain[domain] = [
            {"role": "user", "content": DOMAINS[domain]["system"]}
        ]
        st.success("History cleared.")
        st.rerun()


# Main Chat UI
active_domain = st.session_state.current_domain
domain_info = DOMAINS[active_domain]
messages = get_messages(active_domain)

st.subheader(f"{active_domain} Assistant")

# Display chat history
for m in messages[1:]:
    with st.chat_message("assistant" if m["role"] == "assistant" else "user"):
        st.markdown(m["content"])

# Handle user input
user_input = st.chat_input(f"Ask something about {active_domain}...")

if user_input:
    # Show user's message
    with st.chat_message("user"):
        st.markdown(user_input)
    messages.append({"role": "user", "content": user_input})

    # Build a single prompt string for Gemini
    prompt = (
        f"{DOMAINS[active_domain]['system']}\n\n"
        f"User question:\n{user_input}"
    )

    with st.chat_message("assistant"):
        output = st.empty()

        response = client.models.generate_content(
            model=MODEL,
            contents=prompt,
        )

        complete_text = response.text
        output.markdown(complete_text)

    messages.append({"role": "assistant", "content": complete_text})


        
        


