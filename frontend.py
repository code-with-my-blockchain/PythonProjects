import requests
import streamlit as st

BACKEND_URL = "http://127.0.0.1:8000"


st.set_page_config(
    page_title="Chat-bot",
    page_icon="",
    layout="wide",
)

st.title("Chat-bot")

st.caption(
    "Ask a question regarding your Document."
)


if "messages" not in st.session_state:

    st.session_state.messages = []


    with st.sidebar:

     st.header("Document Management")


    uploaded_files = st.file_uploader(
        "Upload PDF or TXT",
        type=["pdf", "txt"],
        accept_multiple_files=True,
    )

if st.button(
        "⬆Upload Files",
        use_container_width=True,
    ):

        if not uploaded_files:

            st.warning(
                "Please select at least one file."
            )

        else:

            success_count = 0


            for uploaded_file in uploaded_files:

                try:

                    response = requests.post(
                        f"{BACKEND_URL}/upload",
                        files={
                            "file": (
                                uploaded_file.name,
                                uploaded_file.getvalue(),
                            )
                        },
                        timeout=120,
                    )


                    if response.status_code == 200:

                        success_count += 1

                    else:

                        st.error(
                            response.json().get(
                                "detail",
                                "Upload failed."
                            )
                        )

                except Exception as e:

                    st.error(
                        f"Backend error: {e}"
                    )


            if success_count:

                st.success(
                    f"{success_count} file(s) uploaded."
                )

st.divider



if st.button(
        "Index Documents",
        use_container_width=True,
    ):

        with st.spinner(
            "Creating embeddings and vector database..."
        ):

            try:

                response = requests.post(
                    f"{BACKEND_URL}/index",
                    timeout=600,
                )


                if response.status_code == 200:

                    data = response.json()

                    st.success(
                        "Documents indexed & uploaded successfully!"
                    )

                    st.info(
                        f"Documents: {data['documents']}\n\n"
                        f"Chunks: {data['chunks']}"
                    )

                else:

                    st.error(
                        response.json().get(
                            "detail",
                            "Indexing failed."
                        )
                    )

            except Exception as e:

                st.error(
                    f"Backend error: {e}"
                )


st.divider()



st.subheader("uploaded Document")


try:

        response = requests.get(
            f"{BACKEND_URL}/documents",
            timeout=30,
        )


        if response.status_code == 200:

            documents = response.json()[
                "documents"
            ]


            if documents:

                for filename in documents:

                    st.write(
                        f"{filename}"
                    )

            else:
                st.info(
                    "No documents uploaded."
                )

except Exception:
        st.warning(
            "Backend is not running."
        )

st.divider()


if st.button(
        "Clear Chat",
        use_container_width=True,
    ):

        st.session_state.messages = []

        st.rerun()


if st.button(
        "Delete Documents",
        use_container_width=True,
    ):

        try:

            response = requests.delete(
                f"{BACKEND_URL}/documents",
                timeout=60,
            )


            if response.status_code == 200:

                st.session_state.messages = []

                st.success(
                    "Documents deleted."
                )

                st.rerun()

            else:

                st.error(
                    response.json().get(
                        "detail",
                        "Delete failed."
                    )
                )

        except Exception as e:

            st.error(
                f"Backend error: {e}"
            )

for message in st.session_state.messages:

    with st.chat_message(
        message["role"]
    ):

        st.markdown(
            message["content"]
        )


    
        if (
            message["role"] == "assistant"
            and message.get("sources")
        ):

            with st.expander(
                "Sources"
            ):

                shown = set()

                for source in message["sources"]:

                    filename = source["source"]
                    page = source["page"]

                    if page:

                        source_text = (
                            f"{filename} — "
                            f"Page {page}"
                        )

                    else:

                        source_text = (
                            f"{filename}"
                        )


                    if source_text not in shown:

                        st.write(
                            source_text
                        )

                        shown.add(
                            source_text
                        )


question = st.chat_input(
    "Ask a question about your documents"
)

with st.chat_message("user"):

        st.markdown(question)


st.session_state.messages.append(
        {
            "role": "user",
            "content": question,
        }
    )

chat_history = []

messages = st.session_state.messages


for i in range(
        0,
        len(messages) - 1,
        2
    ):

        if (
            messages[i]["role"] == "user"
            and i + 1 < len(messages)
            and messages[i + 1]["role"] == "assistant"
        ):

            chat_history.append(
                {
                    "question": messages[i]["content"],
                    "answer": messages[i + 1]["content"],
                }
            )   

with st.chat_message("assistant"):

        with st.spinner(
            "Searching documents..."
        ):

            try:

                response = requests.post(
                    f"{BACKEND_URL}/chat",

                    json={
                        "question": question,
                        "chat_history": chat_history,
                    },

                    timeout=180,
                )


                if response.status_code == 200:

                    data = response.json()

                    answer = data["answer"]
                    sources = data.get(
                        "sources",
                        []
                    )


                    # Display answer
                    st.markdown(
                        answer
                    )


                    # Display sources
                    if sources:

                        with st.expander(
                            "📚 Sources"
                        ):

                            shown = set()

                            for source in sources:

                                filename = source[
                                    "source"
                                ]

                                page = source[
                                    "page"
                                ]


                                if page:

                                    source_text = (
                                        f"📄 {filename} — "
                                        f"Page {page}"
                                    )

                                else:

                                    source_text = (
                                        f"📄 {filename}"
                                    )


                                if (
                                    source_text
                                    not in shown
                                ):

                                    st.write(
                                        source_text
                                    )

                                    shown.add(
                                        source_text
                                    )


                    # Save assistant response
                    st.session_state.messages.append(
                        {
                            "role": "assistant",
                            "content": answer,
                            "sources": sources,
                        }
                    )


                else:

                    error_message = response.json().get(
                        "detail",
                        "Unknown backend error."
                    )

                    st.error(
                        error_message
                    )


            except requests.exceptions.ConnectionError:

                st.error(
                    "Backend is not running. "
                    "Please start FastAPI first."
                )


            except Exception as e:

                st.error(
                    f"Error: {e}"
                )
    