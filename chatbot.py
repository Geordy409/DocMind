import os
from typing import List, Optional
import streamlit as st
from datetime import datetime
import tempfile
    


from langchain_openai import ChatOpenAI
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_community.document_loaders import (
    TextLoader,
    PyPDFLoader,
)
from langchain_core.documents import Document
from dotenv import load_dotenv

load_dotenv()

openai_key = os.getenv("OPENAI_API_KEY")

class DocumentLoader:
    supported_extensions = {
        ".txt": TextLoader,
        ".pdf": PyPDFLoader,
    }

    @staticmethod
    def load_from_uploaded_file(uploaded_file) -> Optional[List[Document]]:
        if uploaded_file is None:
            st.warning("⚠️ Aucun fichier uploadé")
            return None

        file_name = uploaded_file.name
        ext = os.path.splitext(file_name)[1].lower()

        loader_class = DocumentLoader.supported_extensions.get(ext)
        if loader_class is None:
            st.error(f"Extension {ext} non supportée")
            return None

        try:
            with tempfile.NamedTemporaryFile(delete=False, suffix=ext) as tmp_file:
                tmp_file.write(uploaded_file.getbuffer())
                temp_path = tmp_file.name

            loader = loader_class(temp_path)
            documents = loader.load()
            return documents

        except Exception as e:
            st.error(f"Erreur lors du chargement du document: {e}")
            return None

        finally:
            if 'temp_path' in locals() and os.path.exists(temp_path):
                os.remove(temp_path)

class ChatSystem:
    def __init__(self):
        self.llm = ChatOpenAI(
            model="gpt-3.5-turbo",
            temperature=0,
            api_key=openai_key,
            max_tokens=1000,
            timeout=None,
            streaming=True,
        )
        self.chat_history = ChatMessageHistory()
        self.loaded_documents = []
        self.document_content = ""

    def load_documents(self, uploaded_file):
        """Charger des documents pour les analyser"""
        documents = DocumentLoader.load_from_uploaded_file(uploaded_file)
        if documents:
            self.loaded_documents = documents
            # Concaténer le contenu de tous les documents
            self.document_content = "\n\n".join([doc.page_content for doc in documents])
            return True
        return False

    def ask_question(self, question: str) -> dict:
        try:
            # Préparer les messages pour l'API
            if self.document_content:
                # Si un document est chargé, créer un contexte intelligent
                system_message = f"""
                Vous êtes un assistant conversationnel intelligent. Un document a été chargé et voici son contenu :
                
                === CONTENU DU DOCUMENT ===
                {self.document_content}
                === FIN DU DOCUMENT ===
                
                Instructions :
                - Si l'utilisateur demande un résumé, une analyse, ou pose des questions sur le document, utilisez le contenu ci-dessus
                - Si l'utilisateur pose une question générale non liée au document, répondez normalement
                - Soyez précis et basez-vous sur le contenu du document quand c'est pertinent
                - Indiquez clairement quand vous vous basez sur le document ou non
                """
                messages = [SystemMessage(content=system_message)]
            else:
                # Pas de document chargé, comportement normal
                messages = [SystemMessage(content="Vous êtes un assistant conversationnel utile et amical.")]
            
            # Ajouter l'historique des conversations
            for msg in self.chat_history.messages:
                messages.append(msg)
            
            # Ajouter la nouvelle question
            messages.append(HumanMessage(content=question))
            
            # Obtenir la réponse
            response = self.llm.invoke(messages)

            # Ajouter à l'historique
            self.chat_history.add_user_message(question)
            self.chat_history.add_ai_message(response.content)

            return {"answer": response.content}
        except Exception as e:
            return {"error": f"Erreur lors du traitement de la question : {e}"}

    def reset_conversation(self):
        if self.chat_history:
            self.chat_history.clear()

    def clear_documents(self):
        """Vider les documents chargés"""
        self.loaded_documents = []
        self.document_content = ""


def main():
    st.set_page_config(
        page_title="DocuMind",
        page_icon="🎈",
        layout="wide"
    )
    
    st.markdown(
         """
        <style>
    .stApp {
        background-color: white;
        
    }
    .stButton button {
        background-color: #666666;
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.5em 1em;
        font-weight: bold;
    }
    .stMarkdown h1, .stMarkdown h2, .stMarkdown h3 {
        color: yellow ;
    }
    div[data-baseweb="input"] > input {
        color: white !important;
        background-color: #999999;
    }
    div[data-baseweb="input"] > input::placeholder {
        color: white !important;
        opacity: 1 !important;
    }
    </style>
        """,
        unsafe_allow_html=True
    )
    
    st.title("🤖 DocuMind... (●'◡'●)")
    
    # Vérification de la clé API
    if not openai_key:
        st.error("❌ Clé OpenAI manquante. Vérifiez votre fichier .env")
        return

    # Initialisation du système de chat
    if "chat_system" not in st.session_state:
        st.session_state.chat_system = ChatSystem()
    
    # Initialisation de l'historique des conversations pour l'affichage
    if "conversation_history" not in st.session_state:
        st.session_state.conversation_history = []
    
    # Initialisation du statut des documents
    if "documents_loaded" not in st.session_state:
        st.session_state.documents_loaded = False
    
    # Sidebar pour les options et chargement de documents
    with st.sidebar:
        st.header("📁 Import de Documents")
        
        # Upload de fichier
        uploaded_file = st.file_uploader(
            "Choisissez un fichier", 
            type=["txt", "pdf"],
            help="Formats supportés : .txt, .pdf"
        )
        
        # Bouton pour charger le document
        if st.button("📄 Charger le document", use_container_width=True):
            if uploaded_file:
                with st.spinner("Chargement en cours..."):
                    if st.session_state.chat_system.load_documents(uploaded_file):
                        st.success("✅ Document chargé avec succès !")
                        st.session_state.documents_loaded = True
                        st.info(f"📄 Fichier : {uploaded_file.name}")
                        st.info("💡 Vous pouvez maintenant poser des questions sur le document ou demander un résumé !")
                    else:
                        st.error("❌ Erreur lors du chargement")
                        st.session_state.documents_loaded = False
            else:
                st.warning("⚠️ Veuillez sélectionner un fichier")
        
        st.markdown("---")
        
        st.header("⚙️ Options")
        
        # Bouton pour réinitialiser la conversation
        if st.button("🗑️ Réinitialiser la conversation", use_container_width=True):
            st.session_state.chat_system.reset_conversation()
            st.session_state.conversation_history = []
            st.success("✅ Conversation réinitialisée")
            st.rerun()
        
        # Bouton pour vider les documents
        if st.session_state.documents_loaded:
            if st.button("🗂️ Vider les documents", use_container_width=True):
                st.session_state.chat_system.clear_documents()
                st.session_state.documents_loaded = False
                st.success("✅ Documents vidés")
                st.rerun()
        
        st.markdown("---")
        
    # Interface principale
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.header("💬 Conversation")
        
        # Zone de conversation avec hauteur fixe
        conversation_container = st.container(height=500)
        
        # Affichage de l'historique des conversations
        with conversation_container:
            if st.session_state.conversation_history:
                for i, (q, a, timestamp) in enumerate(st.session_state.conversation_history):
                    # Question de l'utilisateur
                    with st.chat_message("user"):
                        st.write(f"**{timestamp}**")
                        st.write(q)
                    
                    # Réponse de l'IA
                    with st.chat_message("assistant"):
                        st.write(a)
            else:
                st.info("👋 Posez votre première question pour commencer la conversation !")
    
    with col2:
        st.header("ℹ️ Informations")
        
        # Statut des documents
        if st.session_state.documents_loaded:
            st.success("✅ Document chargé")
            st.info(f"📄 {len(st.session_state.chat_system.loaded_documents)} document(s)")
        else:
            st.warning("⚠️ Aucun document chargé")
        
        # Statistiques
        if st.session_state.conversation_history:
            st.metric("💬 Messages", len(st.session_state.conversation_history))
        else:
            st.metric("💬 Messages", 0)
        
        # Instructions
    
    
    # Zone de saisie de question (fixée en bas)
    st.markdown("---")
    
    # Utilisation d'un form pour une meilleure gestion
    with st.form("question_form", clear_on_submit=True):
        col_input, col_button = st.columns([4, 1])
        
        with col_input:
            placeholder_text = "Tapez votre question ici..."
            if st.session_state.documents_loaded:
                placeholder_text = "Posez une question sur le document ou demandez un résumé..."
            
            question = st.text_input(
                "Posez votre question :",
                placeholder=placeholder_text,
                label_visibility="collapsed"
            )
        
        with col_button:
            ask_button = st.form_submit_button("📤 Envoyer", use_container_width=True)
    
    # Traitement de la question
    if ask_button and question.strip():
        with st.spinner("🤔 Réflexion en cours..."):
            result = st.session_state.chat_system.ask_question(question)
            
            if "error" in result:
                st.error(f"❌ {result['error']}")
            else:
                # Ajouter à l'historique
                timestamp = datetime.now().strftime("%H:%M:%S")
                st.session_state.conversation_history.append((
                    question,
                    result["answer"],
                    timestamp
                ))
                
                # Actualiser la page
                st.rerun()
    
    elif ask_button and not question.strip():
        st.warning("⚠️ Veuillez saisir une question")

if __name__ == "__main__":
    main()