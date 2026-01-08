# DocuMind 🤖

Un assistant conversationnel intelligent développé avec Streamlit et LangChain, capable d'analyser des documents et de répondre à vos questions de manière contextuelle.

## 🌐 Application en ligne

L'application est déployée sur **Streamlit Community Cloud** était accessible directement via ce lien :

**🔗 [https://docmind22.streamlit.app/](https://docmind22.streamlit.app/)**

*Pas besoin d'installation locale ! Utilisez DocuMind directement dans votre navigateur.*

## ✨ Fonctionnalités

- **📄 Analyse de documents** : Support des formats PDF et TXT
- **💬 Chat intelligent** : Conversation naturelle avec l'IA
- **🧠 Contexte documentaire** : Pose des questions spécifiques sur vos documents
- **📊 Résumés automatiques** : Génération de résumés de documents
- **🔄 Historique des conversations** : Suivi complet de vos échanges
- **🎨 Interface moderne** : Design épuré et intuitif
- **⚡ Traitement en temps réel** : Réponses rapides et fluides

## 🚀 Installation

### Option 1 : Utilisation en ligne (Recommandée)

Accédez directement à l'application déployée : [https://docmind22.streamlit.app/](https://docmind22.streamlit.app/)

### Option 2 : Installation locale

#### Prérequis

- Python 3.8 ou supérieur
- Une clé API OpenAI

#### Étapes d'installation

1. **Cloner le projet**

   ```bash
   git clone <url-du-repo>
   cd documind
   ```

2. **Créer un environnement virtuel**

   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   # ou
   venv\Scripts\activate     # Windows
   ```

3. **Installer les dépendances**

   ```bash
   pip install streamlit langchain-openai langchain-community langchain-core python-dotenv pypdf
   ```

4. **Configuration des variables d'environnement**

   Créez un fichier `.env` à la racine du projet :

   ```env
   OPENAI_API_KEY=votre_clé_api_openai_ici
   ```

## 🏃‍♂️ Utilisation

### Accès en ligne

1. Rendez-vous sur [https://docmind22.streamlit.app/](https://docmind22.streamlit.app/)
2. Suivez les instructions à l'écran pour configurer votre clé API OpenAI
3. Commencez à utiliser l'application !

### Démarrage local

```bash
streamlit run chatbot.py
```

L'application sera accessible à l'adresse : `http://localhost:8501`

### Guide d'utilisation

1. **Charger un document**

   - Utilisez la sidebar pour uploader un fichier (PDF ou TXT)
   - Cliquez sur "📄 Charger le document"

2. **Poser des questions**

   - Tapez votre question dans la zone de saisie
   - Cliquez sur "📤 Envoyer" ou appuyez sur Entrée

3. **Types de questions possibles**

   - Questions sur le contenu du document
   - Demandes de résumés
   - Questions générales (sans rapport avec le document)

4. **Gérer la conversation**
   - Réinitialisez la conversation avec le bouton "🗑️ Réinitialiser"
   - Videz les documents avec "🗂️ Vider les documents"

## 🏗️ Architecture

### Structure du projet

```
documind/
├── chatbot.py              # Application principale
├── .env                 # Variables d'environnement
├── requirements.txt     # Dépendances
└── README.md           # Documentation
```

### Classes principales

- **`DocumentLoader`** : Gestion du chargement et traitement des documents
- **`ChatSystem`** : Système de conversation avec l'IA et gestion du contexte

### Technologies utilisées

- **Streamlit** : Interface utilisateur web
- **LangChain** : Framework pour applications LLM
- **OpenAI GPT-3.5-turbo** : Modèle de langage
- **PyPDF** : Lecture des fichiers PDF
- **Python-dotenv** : Gestion des variables d'environnement

## 🚀 Déploiement

### Streamlit Community Cloud

L'application est déployée sur **Streamlit Community Cloud**, ce qui permet :

- **Accès gratuit** : Pas de frais d'hébergement
- **Mise à jour automatique** : Déploiement automatique à chaque push Git
- **Haute disponibilité** : Serveurs fiables et rapides
- **HTTPS sécurisé** : Connexion chiffrée
- **Pas d'installation** : Utilisation directe dans le navigateur

### Configuration pour le déploiement

Pour déployer votre propre version :

1. Créez un compte sur [share.streamlit.io](https://share.streamlit.io)
2. Connectez votre repository GitHub
3. Configurez vos secrets (clé API OpenAI) dans les paramètres Streamlit Cloud
4. Déployez automatiquement !

## 📋 Formats supportés

| Format | Extension | Description         |
| ------ | --------- | ------------------- |
| PDF    | `.pdf`    | Documents PDF       |
| Texte  | `.txt`    | Fichiers texte brut |

## ⚙️ Configuration

### Paramètres du modèle OpenAI

```python
self.llm = ChatOpenAI(
    model="gpt-3.5-turbo",
    temperature=0,
    max_tokens=1000,
    timeout=None,
    streaming=True,
)
```

### Personnalisation du style

L'application utilise du CSS personnalisé pour :

- Couleurs de thème
- Styles des boutons
- Mise en forme des zones de saisie

## 🔧 Développement

### Ajouter de nouveaux formats

Pour supporter un nouveau format de document :

1. Ajouter le loader correspondant dans `DocumentLoader.supported_extensions`
2. Installer la dépendance nécessaire
3. Tester le chargement

### Modifier le modèle IA

Pour changer de modèle OpenAI :

- Modifier le paramètre `model` dans `ChatSystem.__init__()`
- Ajuster `max_tokens` selon les capacités du modèle


## 📈 Améliorations futures

- [ ] Support de plus de formats (DOCX, XLSX, etc.)
- [ ] Système de sauvegarde des conversations
- [ ] Mode multi-documents
- [ ] Génération de rapports
- [ ] Interface multilingue
- [ ] Intégration d'autres modèles LLM

## 🤝 Contribution

Les contributions sont les bienvenues ! Pour contribuer :

1. Forkez le projet
2. Créez une branche pour votre fonctionnalité
3. Committez vos changements
4. Poussez vers la branche
5. Ouvrez une Pull Request

## 👥 Auteurs

- **Geordy NGOUA** - Développeur principal

---

_DocuMind - Transformez vos documents en conversations intelligentes_ 🚀

**🌐 Essayez maintenant : [https://docmind22.streamlit.app/](https://docmind22.streamlit.app/)**
