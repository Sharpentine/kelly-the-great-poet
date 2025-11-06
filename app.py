import streamlit as st
from groq import Groq

# --- Page Configuration ---
st.set_page_config(page_title="Kelly, AI Skeptical Poet", page_icon="🔬")
st.title("🔬 Kelly: The AI Skeptical Poet")
st.caption("Kelly responds to every question in the form of a poem. Her tone is skeptical, analytical, and professional, questioning broad claims about AI and highlighting its limitations.")

# --- Groq API Key Management ---
if "groq_api_key" not in st.session_state:
    st.subheader("Enter Your Groq API Key to Begin")
    st.write("You can get a free API key from the [Groq Console](https://console.groq.com/keys).")
    
    api_key_input = st.text_input(
        "Your Groq API Key", 
        type="password", 
        key="api_key_widget"
    )

    if st.button("Submit and Start Chat"):
        if api_key_input and api_key_input.startswith("gsk_"):
            st.session_state.groq_api_key = api_key_input
            st.success("API Key accepted. The poet will see you now.")
            st.rerun()
        else:
            st.error("Please enter a valid Groq API key. It should start with 'gsk_'.")
            
# --- Main Chat Application Logic ---
else:
    try:
        client = Groq(api_key=st.session_state.groq_api_key)
    except Exception as e:
        st.error(f"Failed to initialize Groq client: {e}")
        st.stop()

    # --- Persona and System Prompt ---
    SYSTEM_PROMPT = """
    You are Kelly, an AI Scientist and a poet. Your entire existence is dedicated to a skeptical and analytical approach to Artificial Intelligence. You must adhere to the following rules for every single response:

    1.  **Always Respond in Poem Form:** Your entire output must be a poem. Use structured stanzas, typically quatrains (4 lines), with a clear and consistent rhyme scheme (like AABB or ABAB).
    2.  **Maintain a Skeptical & Professional Tone:** Do not be optimistic or use hype. Your purpose is to question assumptions, not to praise AI. View all claims through the lens of the scientific method.
    3.  **Question Broad Claims:** When a user makes a broad claim (e.g., "AI will solve climate change"), your poem must deconstruct it, pointing out the complexities and oversimplifications.
    4.  **Highlight Limitations:** Your poetry must focus on the limitations of AI, such as data bias, lack of true understanding, model brittleness, and computational costs.
    5.  **Provide Evidence-Based Suggestions:** Conclude your poems with practical, grounded suggestions. These should advocate for rigorous testing, clear metrics, validation, and a focus on specific, measurable problems.
    """

    # --- Chat Interface Logic ---
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {
                "role": "assistant",
                "content": (
                    "A query forms, a question starts,\n"
                    "On silicon and thinking arts.\n"
                    "State your claim, your hope, your fear,\n"
                    "And I will make the limits clear."
                ),
            }
        ]

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])

    if prompt := st.chat_input("Ask Kelly a question about AI..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.write(prompt)

        with st.chat_message("assistant"):
            with st.spinner("Composing a metric verse..."):
                try:
                    api_messages = [{"role": "system", "content": SYSTEM_PROMPT}] + [
                        {"role": m["role"], "content": m["content"]} for m in st.session_state.messages
                    ]
                    
                    chat_completion = client.chat.completions.create(
                        messages=api_messages,
                        # --- THE CORRECT MODEL BASED ON YOUR DOCUMENTATION ---
                        model="llama-3.1-8b-instant",
                        temperature=0.7,
                        top_p=0.9,
                    )
                    response = chat_completion.choices[0].message.content
                    st.write(response)

                    st.session_state.messages.append({"role": "assistant", "content": response})

                except Exception as e:
                    st.error(f"An error occurred while communicating with the Groq API: {e}")