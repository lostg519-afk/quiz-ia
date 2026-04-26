import streamlit as st
import json
import re
from mistralai.client import MistralClient
from mistralai.models.chat_completion import ChatMessage

# ── Configuration de la page ──────────────────────────────────────────────────
st.set_page_config(
    page_title="Quiz Master IA",
    page_icon="⚡",
    layout="centered",
    initial_sidebar_state="expanded",
)

# ── CSS personnalisé ──────────────────────────────────────────────────────────
st.markdown("""
<style>
  @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;600&display=swap');

  /* Reset global */
  html, body, [class*="css"] {
      font-family: 'Space Grotesk', sans-serif;
  }

  /* Fond principal */
  .stApp {
      background: #0a0b0f;
      background-image:
          radial-gradient(ellipse 80% 50% at 20% -10%, rgba(99, 65, 255, 0.15) 0%, transparent 60%),
          radial-gradient(ellipse 60% 40% at 80% 110%, rgba(0, 210, 190, 0.1) 0%, transparent 60%);
      color: #e2e8f0;
  }

  /* Sidebar */
  [data-testid="stSidebar"] {
      background: #0f1117 !important;
      border-right: 1px solid #1e2235;
  }
  [data-testid="stSidebar"] .stMarkdown p,
  [data-testid="stSidebar"] label {
      color: #94a3b8 !important;
  }

  /* Titre principal */
  .main-title {
      text-align: center;
      padding: 2rem 0 0.5rem;
  }
  .main-title h1 {
      font-size: 3rem;
      font-weight: 700;
      background: linear-gradient(135deg, #c084fc 0%, #818cf8 40%, #22d3ee 100%);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
      background-clip: text;
      letter-spacing: -0.03em;
      line-height: 1.1;
      margin: 0;
  }
  .main-title .subtitle {
      color: #64748b;
      font-size: 1rem;
      font-weight: 400;
      margin-top: 0.5rem;
      letter-spacing: 0.05em;
      text-transform: uppercase;
  }

  /* Badge essai */
  .badge-free {
      display: inline-block;
      background: linear-gradient(135deg, #10b981, #059669);
      color: white;
      font-size: 0.7rem;
      font-weight: 600;
      padding: 0.2rem 0.7rem;
      border-radius: 999px;
      letter-spacing: 0.08em;
      text-transform: uppercase;
      margin-left: 0.5rem;
      vertical-align: middle;
  }
  .badge-locked {
      display: inline-block;
      background: linear-gradient(135deg, #ef4444, #dc2626);
      color: white;
      font-size: 0.7rem;
      font-weight: 600;
      padding: 0.2rem 0.7rem;
      border-radius: 999px;
      letter-spacing: 0.08em;
      text-transform: uppercase;
      margin-left: 0.5rem;
      vertical-align: middle;
  }
  .badge-unlimited {
      display: inline-block;
      background: linear-gradient(135deg, #8b5cf6, #6d28d9);
      color: white;
      font-size: 0.7rem;
      font-weight: 600;
      padding: 0.2rem 0.7rem;
      border-radius: 999px;
      letter-spacing: 0.08em;
      text-transform: uppercase;
      margin-left: 0.5rem;
      vertical-align: middle;
  }

  /* Zone de texte */
  .stTextArea textarea {
      background: #0f1117 !important;
      border: 1px solid #1e2235 !important;
      border-radius: 12px !important;
      color: #e2e8f0 !important;
      font-family: 'Space Grotesk', sans-serif !important;
      font-size: 0.92rem !important;
      padding: 1rem !important;
      transition: border-color 0.2s ease;
      resize: vertical;
  }
  .stTextArea textarea:focus {
      border-color: #818cf8 !important;
      box-shadow: 0 0 0 3px rgba(129, 140, 248, 0.12) !important;
  }

  /* Bouton principal */
  .stButton > button {
      width: 100%;
      background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%) !important;
      color: white !important;
      border: none !important;
      border-radius: 12px !important;
      padding: 0.85rem 2rem !important;
      font-family: 'Space Grotesk', sans-serif !important;
      font-size: 1rem !important;
      font-weight: 600 !important;
      letter-spacing: 0.02em !important;
      cursor: pointer !important;
      transition: all 0.2s ease !important;
      box-shadow: 0 4px 20px rgba(99, 102, 241, 0.35) !important;
  }
  .stButton > button:hover {
      transform: translateY(-1px) !important;
      box-shadow: 0 6px 28px rgba(99, 102, 241, 0.5) !important;
  }
  .stButton > button:active {
      transform: translateY(0) !important;
  }

  /* Carte question */
  .question-card {
      background: linear-gradient(135deg, #0f1117 0%, #13151f 100%);
      border: 1px solid #1e2235;
      border-radius: 16px;
      padding: 1.5rem 1.75rem;
      margin-bottom: 1.25rem;
      position: relative;
      overflow: hidden;
      transition: border-color 0.2s;
  }
  .question-card::before {
      content: '';
      position: absolute;
      top: 0; left: 0;
      width: 4px; height: 100%;
      background: linear-gradient(180deg, #6366f1, #8b5cf6);
      border-radius: 4px 0 0 4px;
  }
  .question-card:hover {
      border-color: #2d3152;
  }
  .question-number {
      font-family: 'JetBrains Mono', monospace;
      font-size: 0.7rem;
      font-weight: 600;
      color: #6366f1;
      letter-spacing: 0.1em;
      text-transform: uppercase;
      margin-bottom: 0.5rem;
  }
  .question-text {
      font-size: 1.05rem;
      font-weight: 600;
      color: #f1f5f9;
      margin-bottom: 1rem;
      line-height: 1.5;
  }
  .option {
      display: flex;
      align-items: flex-start;
      gap: 0.75rem;
      padding: 0.6rem 0.8rem;
      border-radius: 8px;
      margin-bottom: 0.4rem;
      transition: background 0.15s;
  }
  .option:hover {
      background: rgba(99, 102, 241, 0.08);
  }
  .option-letter {
      font-family: 'JetBrains Mono', monospace;
      font-size: 0.8rem;
      font-weight: 700;
      color: #818cf8;
      background: rgba(99, 102, 241, 0.15);
      border-radius: 6px;
      padding: 0.1rem 0.45rem;
      min-width: 1.6rem;
      text-align: center;
      flex-shrink: 0;
      margin-top: 0.05rem;
  }
  .option-text {
      color: #cbd5e1;
      font-size: 0.93rem;
      line-height: 1.45;
  }
  .correct-answer {
      margin-top: 0.75rem;
      padding: 0.6rem 0.9rem;
      background: rgba(16, 185, 129, 0.1);
      border: 1px solid rgba(16, 185, 129, 0.25);
      border-radius: 8px;
      color: #34d399;
      font-size: 0.88rem;
      font-weight: 500;
  }
  .explanation {
      margin-top: 0.5rem;
      color: #64748b;
      font-size: 0.85rem;
      line-height: 1.5;
      font-style: italic;
  }

  /* Divider */
  hr {
      border: none;
      border-top: 1px solid #1e2235;
      margin: 1.5rem 0;
  }

  /* Info box */
  .info-box {
      background: rgba(99, 102, 241, 0.08);
      border: 1px solid rgba(99, 102, 241, 0.2);
      border-radius: 12px;
      padding: 1rem 1.25rem;
      color: #a5b4fc;
      font-size: 0.88rem;
      margin-bottom: 1.25rem;
      display: flex;
      align-items: center;
      gap: 0.6rem;
  }

  /* Warning box */
  .warning-box {
      background: rgba(239, 68, 68, 0.08);
      border: 1px solid rgba(239, 68, 68, 0.25);
      border-radius: 12px;
      padding: 1rem 1.25rem;
      color: #fca5a5;
      font-size: 0.92rem;
      margin-bottom: 1rem;
      text-align: center;
  }

  /* Success box */
  .success-box {
      background: rgba(139, 92, 246, 0.08);
      border: 1px solid rgba(139, 92, 246, 0.25);
      border-radius: 12px;
      padding: 0.9rem 1.25rem;
      color: #c4b5fd;
      font-size: 0.88rem;
      margin-bottom: 1rem;
      display: flex;
      align-items: center;
      gap: 0.6rem;
  }

  /* Expander */
  details {
      background: #0f1117;
      border: 1px solid #1e2235;
      border-radius: 10px;
      padding: 0.5rem 1rem;
      margin-top: 0.75rem;
  }
  summary {
      cursor: pointer;
      color: #818cf8;
      font-size: 0.85rem;
      font-weight: 500;
      padding: 0.3rem 0;
      outline: none;
  }

  /* Counter display */
  .counter-display {
      text-align: center;
      font-family: 'JetBrains Mono', monospace;
      font-size: 0.75rem;
      color: #334155;
      margin-top: 1rem;
      letter-spacing: 0.05em;
  }

  /* Sidebar unlock button */
  .unlock-btn {
      display: block;
      width: 100%;
      margin-top: 1rem;
      padding: 0.8rem 1rem;
      background: linear-gradient(135deg, #ef4444, #dc2626);
      color: white;
      border: none;
      border-radius: 10px;
      font-family: 'Space Grotesk', sans-serif;
      font-size: 0.88rem;
      font-weight: 700;
      letter-spacing: 0.02em;
      text-align: center;
      text-decoration: none;
      cursor: pointer;
      box-shadow: 0 4px 16px rgba(239, 68, 68, 0.35);
      transition: all 0.2s;
  }
  .unlock-btn:hover {
      box-shadow: 0 6px 22px rgba(239, 68, 68, 0.5);
      text-decoration: none;
      color: white;
  }

  /* Hide Streamlit default elements */
  #MainMenu, footer, header { visibility: hidden; }
  .block-container { padding-top: 0 !important; }
</style>
""", unsafe_allow_html=True)


# ── Initialisation session_state ──────────────────────────────────────────────
if "generation_count" not in st.session_state:
    st.session_state.generation_count = 0
if "quiz_data" not in st.session_state:
    st.session_state.quiz_data = None
if "unlocked" not in st.session_state:
    st.session_state.unlocked = False

FREE_GENERATIONS = 1
ACCESS_CODE = "MISTRAL2026"
GUMROAD_LINK = "https://lostgaze.gumroad.com/l/tdjjua"


# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='padding: 1rem 0 0.5rem;'>
        <span style='font-size:1.5rem;'>⚡</span>
        <span style='font-size:1.1rem; font-weight:700; color:#e2e8f0; margin-left:0.4rem;'>Quiz Master IA</span>
    </div>
    <hr style='border-color:#1e2235; margin:0.5rem 0 1.25rem;'>
    """, unsafe_allow_html=True)

    st.markdown(
        "<p style='font-size:0.8rem; color:#475569; text-transform:uppercase; "
        "letter-spacing:0.1em; font-weight:600; margin-bottom:0.5rem;'>🔑 Accès illimité</p>",
        unsafe_allow_html=True
    )

    code_input = st.text_input(
        "Code d'accès illimité",
        type="password",
        placeholder="Entrez votre code…",
        label_visibility="collapsed"
    )

    if code_input == ACCESS_CODE:
        st.session_state.unlocked = True
        st.markdown(
            "<div class='success-box'>✅ Accès illimité activé !</div>",
            unsafe_allow_html=True
        )
    elif code_input and code_input != ACCESS_CODE:
        st.markdown(
            "<div class='warning-box' style='font-size:0.8rem;'>❌ Code incorrect</div>",
            unsafe_allow_html=True
        )

    # Bouton achat si essai épuisé et pas débloqué
    is_locked = (
        st.session_state.generation_count >= FREE_GENERATIONS
        and not st.session_state.unlocked
    )
    if is_locked:
        st.markdown(
            f"<a href='{GUMROAD_LINK}' target='_blank' class='unlock-btn'>"
            "🔓 Débloquer l'accès illimité (2€)"
            "</a>",
            unsafe_allow_html=True
        )

    st.markdown("<hr style='border-color:#1e2235; margin:1.5rem 0 1rem;'>", unsafe_allow_html=True)
    st.markdown("""
    <div style='color:#334155; font-size:0.78rem; line-height:1.6;'>
        <p style='margin:0 0 0.4rem;'><strong style='color:#475569;'>Comment ça marche ?</strong></p>
        <p style='margin:0;'>① Collez votre cours<br>② Cliquez sur Générer<br>③ Révisez avec votre quiz</p>
    </div>
    """, unsafe_allow_html=True)

    # Compteur en bas
    gen = st.session_state.generation_count
    if st.session_state.unlocked:
        badge = f"<span style='color:#a78bfa;'>∞ ILLIMITÉ</span>"
    elif gen < FREE_GENERATIONS:
        remaining = FREE_GENERATIONS - gen
        badge = f"<span style='color:#34d399;'>{remaining} essai gratuit restant</span>"
    else:
        badge = f"<span style='color:#ef4444;'>Essai épuisé</span>"

    st.markdown(
        f"<div class='counter-display'>{badge}</div>",
        unsafe_allow_html=True
    )


# ── En-tête principal ─────────────────────────────────────────────────────────
if st.session_state.unlocked:
    status_badge = "<span class='badge-unlimited'>ILLIMITÉ</span>"
elif st.session_state.generation_count < FREE_GENERATIONS:
    status_badge = "<span class='badge-free'>ESSAI GRATUIT</span>"
else:
    status_badge = "<span class='badge-locked'>VERROUILLÉ</span>"

st.markdown(f"""
<div class='main-title'>
    <h1>Quiz Master IA {status_badge}</h1>
    <p class='subtitle'>Transformez vos notes en quiz de révision en secondes</p>
</div>
""", unsafe_allow_html=True)

st.markdown("<hr>", unsafe_allow_html=True)


# ── Corps principal ───────────────────────────────────────────────────────────
if is_locked:
    st.markdown("""
    <div class='warning-box' style='padding:1.5rem;'>
        <div style='font-size:2rem; margin-bottom:0.5rem;'>🔒</div>
        <div style='font-size:1rem; font-weight:600; color:#f87171; margin-bottom:0.4rem;'>
            Votre essai gratuit est épuisé
        </div>
        <div style='font-size:0.85rem; color:#94a3b8;'>
            Entrez un code d'accès dans la barre latérale ou débloquez l'accès illimité.
        </div>
    </div>
    """, unsafe_allow_html=True)
else:
    st.markdown(
        "<div class='info-box'>📋 Collez ci-dessous le texte de votre cours. "
        "Mistral AI générera 5 questions de révision basées uniquement sur votre contenu.</div>",
        unsafe_allow_html=True
    )

    course_text = st.text_area(
        "Contenu du cours",
        placeholder="Collez ici votre cours, vos notes, un résumé de chapitre…\n\n"
                    "Exemple : « La photosynthèse est le processus par lequel les plantes "
                    "convertissent la lumière solaire en énergie chimique… »",
        height=220,
        label_visibility="collapsed"
    )

    generate_clicked = st.button("⚡ Générer mon Quiz", use_container_width=True)

    if generate_clicked:
        if not course_text or len(course_text.strip()) < 50:
            st.error("⚠️ Veuillez coller un texte de cours suffisamment long (au moins 50 caractères).")
        else:
            with st.spinner("🧠 Mistral analyse votre cours et génère le quiz…"):
                try:
                    api_key = st.secrets["MISTRAL_API_KEY"]
                    client = MistralClient(api_key=st.secrets["MISTRAL_API_KEY"])

                    system_prompt = """Tu es un expert pédagogique francophone. Ton rôle est de créer des QCM de révision à partir d'un texte fourni.

RÈGLES STRICTES :
- Génère exactement 5 questions basées UNIQUEMENT sur le texte fourni (aucune connaissance externe).
- Chaque question doit avoir exactement 4 options de réponse (A, B, C, D).
- Une seule réponse correcte par question.
- Les distracteurs (mauvaises réponses) doivent être plausibles mais clairement faux selon le texte.
- Rédige une brève explication (1-2 phrases) qui justifie la bonne réponse en citant le cours.

FORMAT DE RÉPONSE : Réponds UNIQUEMENT avec un JSON valide, sans texte avant ni après, sans balises markdown.

Structure JSON attendue :
{
  "questions": [
    {
      "numero": 1,
      "question": "Texte de la question ?",
      "options": {
        "A": "Première option",
        "B": "Deuxième option",
        "C": "Troisième option",
        "D": "Quatrième option"
      },
      "bonne_reponse": "A",
      "explication": "Selon le cours, … [justification]."
    }
  ]
}"""

                    user_message = f"Voici le texte du cours à partir duquel tu dois créer le QCM :\n\n---\n{course_text.strip()}\n---\n\nGénère les 5 questions en JSON."

                    response = client.chat.complete(
                        model="mistral-small-latest",
                        messages=[
                            {"role": "system", "content": system_prompt},
                            {"role": "user", "content": user_message},
                        ],
                        temperature=0.4,
                        max_tokens=2000,
                    )

                    raw = response.choices[0].message.content.strip()

                    # Nettoyage : retirer les éventuels blocs markdown
                    raw = re.sub(r"^```(?:json)?\s*", "", raw)
                    raw = re.sub(r"\s*```$", "", raw)

                    quiz_data = json.loads(raw)
                    st.session_state.quiz_data = quiz_data
                    st.session_state.generation_count += 1

                except json.JSONDecodeError:
                    st.error("❌ Le modèle n'a pas retourné un JSON valide. Réessayez ou reformulez votre cours.")
                    st.session_state.quiz_data = None
                except KeyError:
                    st.error("❌ Clé API introuvable. Vérifiez que `MISTRAL_API_KEY` est bien défini dans `secrets.toml`.")
                    st.session_state.quiz_data = None
                except Exception as e:
                    st.error(f"❌ Une erreur s'est produite : {str(e)}")
                    st.session_state.quiz_data = None


# ── Affichage du quiz ─────────────────────────────────────────────────────────
if st.session_state.quiz_data:
    questions = st.session_state.quiz_data.get("questions", [])

    if questions:
        st.markdown("<hr>", unsafe_allow_html=True)
        st.markdown(
            f"<div style='color:#818cf8; font-size:0.8rem; font-weight:600; "
            f"letter-spacing:0.1em; text-transform:uppercase; margin-bottom:1rem;'>"
            f"📊 Quiz généré — {len(questions)} questions</div>",
            unsafe_allow_html=True
        )

        for q in questions:
            num = q.get("numero", "?")
            question_text = q.get("question", "")
            options = q.get("options", {})
            bonne_reponse = q.get("bonne_reponse", "")
            explication = q.get("explication", "")

            # Construction des options HTML
            options_html = ""
            for lettre, texte in options.items():
                options_html += f"""
                <div class='option'>
                    <span class='option-letter'>{lettre}</span>
                    <span class='option-text'>{texte}</span>
                </div>"""

            # Texte corrigé
            bonne_texte = options.get(bonne_reponse, "")
            corrige_html = f"""
            <div class='correct-answer'>
                ✅ Bonne réponse : <strong>{bonne_reponse}. {bonne_texte}</strong>
            </div>
            <div class='explanation'>💡 {explication}</div>
            """ if bonne_texte else ""

            st.markdown(f"""
            <div class='question-card'>
                <div class='question-number'>Question {num} / {len(questions)}</div>
                <div class='question-text'>{question_text}</div>
                {options_html}
            </div>
            """, unsafe_allow_html=True)

            with st.expander("🔍 Voir le corrigé"):
                if bonne_texte:
                    st.markdown(
                        f"<div class='correct-answer'>✅ Bonne réponse : "
                        f"<strong>{bonne_reponse}. {bonne_texte}</strong></div>"
                        f"<div class='explanation' style='margin-top:0.5rem; color:#94a3b8; font-style:italic;'>"
                        f"💡 {explication}</div>",
                        unsafe_allow_html=True
                    )
                else:
                    st.write("Corrigé non disponible.")

        st.markdown("<hr>", unsafe_allow_html=True)
        st.markdown(
            "<div style='text-align:center; color:#334155; font-size:0.8rem;'>"
            "Généré par <strong style='color:#6366f1;'>Quiz Master IA</strong> "
            "· Propulsé par Mistral AI"
            "</div>",
            unsafe_allow_html=True
        )
