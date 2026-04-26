"""
Quiz Master IA — app.py
Dépendances (requirements.txt) :
    streamlit>=1.35.0
    mistralai>=1.0.0
"""

import json
import re

import streamlit as st

# ── Import SDK Mistral ────────────────────────────────────────────────────────
try:
    from mistralai import Mistral
except ImportError as _import_err:
    st.error(
        "❌ Le package `mistralai` est introuvable. "
        "Ajoutez `mistralai>=1.0.0` dans votre fichier `requirements.txt` "
        "puis redéployez l'application sur Streamlit Cloud."
    )
    st.stop()

# ── Configuration de la page ──────────────────────────────────────────────────
st.set_page_config(
    page_title="Quiz Master IA",
    page_icon="⚡",
    layout="centered",
    initial_sidebar_state="expanded",
)

# ── CSS ───────────────────────────────────────────────────────────────────────
st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600;700&family=DM+Mono:wght@400;500&display=swap');

html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; }

.stApp {
    background: #07080d;
    background-image:
        radial-gradient(ellipse 70% 45% at 15% 0%,   rgba(111,76,255,.18) 0%, transparent 65%),
        radial-gradient(ellipse 55% 35% at 85% 100%, rgba(0,200,180,.12)  0%, transparent 65%);
    color: #dce3ef;
}

[data-testid="stSidebar"] {
    background: #0b0c12 !important;
    border-right: 1px solid #181c2a !important;
}
[data-testid="stSidebar"] * { color: #7a8aaa; }

#MainMenu, footer, header { visibility: hidden; }
.block-container { padding-top: 1.5rem !important; max-width: 780px; }

/* Titre */
.app-hero { text-align:center; padding:1.5rem 0 .25rem; }
.app-hero h1 {
    font-size:2.75rem; font-weight:700;
    background: linear-gradient(130deg,#b48cff 0%,#7b8fff 45%,#22d4c8 100%);
    -webkit-background-clip:text; -webkit-text-fill-color:transparent;
    background-clip:text; letter-spacing:-.03em; line-height:1.1; margin:0;
}
.app-hero .tagline {
    font-size:.88rem; font-weight:400; color:#3d4a62;
    letter-spacing:.12em; text-transform:uppercase; margin-top:.55rem;
}

/* Badges */
.badge {
    display:inline-block; font-size:.65rem; font-weight:700;
    letter-spacing:.1em; text-transform:uppercase;
    padding:.18rem .65rem; border-radius:999px;
    vertical-align:middle; margin-left:.45rem;
    font-family:'DM Mono',monospace;
}
.badge-free     { background:linear-gradient(135deg,#10b981,#059669); color:#fff; }
.badge-locked   { background:linear-gradient(135deg,#ef4444,#dc2626); color:#fff; }
.badge-infinite { background:linear-gradient(135deg,#8b5cf6,#6d28d9); color:#fff; }

/* Textarea */
.stTextArea textarea {
    background:#0e1018 !important;
    border:1px solid #1c2133 !important;
    border-radius:12px !important;
    color:#dce3ef !important;
    font-family:'DM Sans',sans-serif !important;
    font-size:.93rem !important;
    padding:1rem !important;
    transition:border-color .2s;
    resize:vertical;
}
.stTextArea textarea:focus {
    border-color:#7b8fff !important;
    box-shadow:0 0 0 3px rgba(123,143,255,.12) !important;
}
.stTextArea textarea::placeholder { color:#2e3650 !important; }

/* Bouton générer */
.stButton > button {
    width:100%;
    background:linear-gradient(135deg,#6a4fff 0%,#9b6dff 100%) !important;
    color:#fff !important; border:none !important;
    border-radius:12px !important; padding:.9rem 2rem !important;
    font-family:'DM Sans',sans-serif !important;
    font-size:1rem !important; font-weight:600 !important;
    box-shadow:0 4px 22px rgba(106,79,255,.38) !important;
    transition:all .2s ease !important;
}
.stButton > button:hover {
    transform:translateY(-2px) !important;
    box-shadow:0 7px 30px rgba(106,79,255,.55) !important;
}

/* Carte question */
.q-card {
    background:#0e1018; border:1px solid #181c2a;
    border-radius:16px; padding:1.5rem 1.75rem;
    margin-bottom:1.25rem; position:relative; overflow:hidden;
}
.q-card::before {
    content:''; position:absolute; top:0; left:0;
    width:4px; height:100%;
    background:linear-gradient(180deg,#6a4fff,#9b6dff);
    border-radius:4px 0 0 4px;
}
.q-num {
    font-family:'DM Mono',monospace; font-size:.68rem;
    font-weight:500; color:#6a4fff;
    letter-spacing:.12em; text-transform:uppercase; margin-bottom:.4rem;
}
.q-text { font-size:1rem; font-weight:600; color:#f0f4ff; line-height:1.5; margin-bottom:1rem; }
.opt {
    display:flex; align-items:flex-start; gap:.7rem;
    padding:.55rem .75rem; border-radius:8px; margin-bottom:.35rem;
}
.opt:hover { background:rgba(106,79,255,.07); }
.opt-ltr {
    font-family:'DM Mono',monospace; font-size:.75rem;
    font-weight:600; color:#7b8fff;
    background:rgba(123,143,255,.14);
    border-radius:6px; padding:.1rem .45rem;
    min-width:1.6rem; text-align:center;
    flex-shrink:0; margin-top:.05rem;
}
.opt-txt { color:#c0cbdf; font-size:.91rem; line-height:1.45; }

/* Corrigé */
.corrige-box {
    background:rgba(16,185,129,.08);
    border:1px solid rgba(16,185,129,.22);
    border-radius:10px; padding:.75rem 1rem;
    color:#34d399; font-size:.88rem; font-weight:500;
}
.expl-txt { color:#4a5a7a; font-size:.84rem; font-style:italic; margin-top:.5rem; line-height:1.5; }

/* Strips */
.info-strip {
    background:rgba(123,143,255,.08);
    border:1px solid rgba(123,143,255,.18);
    border-radius:12px; padding:.85rem 1.1rem;
    color:#9aaaff; font-size:.87rem; margin-bottom:1.2rem;
}
.lock-strip {
    background:rgba(239,68,68,.07);
    border:1px solid rgba(239,68,68,.22);
    border-radius:14px; padding:1.5rem;
    text-align:center; margin-bottom:1rem;
}
.lock-strip .lock-icon  { font-size:2rem; margin-bottom:.4rem; }
.lock-strip .lock-title { font-size:1rem; font-weight:600; color:#f87171; }
.lock-strip .lock-sub   { font-size:.84rem; color:#64748b; margin-top:.3rem; }

/* Bouton Gumroad */
a.gumroad-btn {
    display:block; margin-top:.9rem; padding:.78rem 1rem;
    background:linear-gradient(135deg,#ef4444,#dc2626);
    color:#fff !important; border-radius:10px;
    font-family:'DM Sans',sans-serif; font-size:.86rem; font-weight:700;
    text-align:center; text-decoration:none !important;
    box-shadow:0 4px 18px rgba(239,68,68,.35); transition:box-shadow .2s;
}
a.gumroad-btn:hover { box-shadow:0 6px 24px rgba(239,68,68,.55); }

/* Succès code */
.ok-strip {
    background:rgba(139,92,246,.1);
    border:1px solid rgba(139,92,246,.25);
    border-radius:10px; padding:.65rem 1rem;
    color:#c4b5fd; font-size:.84rem; margin-top:.5rem;
}

hr.sep { border:none; border-top:1px solid #181c2a; margin:1.4rem 0; }
.footer-note { text-align:center; color:#1e2840; font-size:.78rem; margin-top:.5rem; }
</style>
""",
    unsafe_allow_html=True,
)

# ── Constantes ────────────────────────────────────────────────────────────────
FREE_LIMIT    = 1
ACCESS_CODE   = "MISTRAL2026"
GUMROAD_URL   = "https://lostgaze.gumroad.com/l/tdjjua"
MISTRAL_MODEL = "mistral-small-latest"

SYSTEM_PROMPT = """Tu es un expert pédagogique francophone. Génère exactement 5 questions de QCM basées UNIQUEMENT sur le texte fourni par l'utilisateur. N'utilise aucune connaissance externe.

Règles :
- 4 options par question (A, B, C, D).
- 1 seule bonne réponse par question.
- Les mauvaises réponses doivent être plausibles mais incorrectes selon le texte.
- Fournis une explication courte (1-2 phrases) qui cite ou paraphrase le cours.

Réponds UNIQUEMENT avec un objet JSON valide, sans texte avant ni après, sans balises markdown.

Format JSON attendu :
{
  "questions": [
    {
      "numero": 1,
      "question": "...",
      "options": { "A": "...", "B": "...", "C": "...", "D": "..." },
      "bonne_reponse": "A",
      "explication": "..."
    }
  ]
}"""

# ── Session state ─────────────────────────────────────────────────────────────
if "nb_gen"    not in st.session_state: st.session_state.nb_gen    = 0
if "unlocked"  not in st.session_state: st.session_state.unlocked  = False
if "quiz_data" not in st.session_state: st.session_state.quiz_data = None

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown(
        "<div style='padding:.9rem 0 .3rem;font-size:1.1rem;font-weight:700;"
        "color:#dce3ef;'>⚡ Quiz Master IA</div>"
        "<hr class='sep'>",
        unsafe_allow_html=True,
    )

    st.markdown(
        "<p style='font-size:.75rem;color:#3d4a62;text-transform:uppercase;"
        "letter-spacing:.1em;font-weight:600;margin-bottom:.45rem;'>"
        "🔑 Code d'accès illimité</p>",
        unsafe_allow_html=True,
    )

    code_saisi = st.text_input(
        "Code",
        type="password",
        placeholder="Entrez votre code…",
        label_visibility="collapsed",
    )

    if code_saisi == ACCESS_CODE:
        st.session_state.unlocked = True
        st.markdown("<div class='ok-strip'>✅ Accès illimité activé !</div>", unsafe_allow_html=True)
    elif code_saisi:
        st.markdown(
            "<div style='color:#ef4444;font-size:.8rem;margin-top:.3rem;'>❌ Code incorrect</div>",
            unsafe_allow_html=True,
        )

    is_locked = st.session_state.nb_gen >= FREE_LIMIT and not st.session_state.unlocked

    if is_locked:
        st.markdown(
            f"<a href='{GUMROAD_URL}' target='_blank' class='gumroad-btn'>"
            "🔓 Débloquer l'accès illimité (2€)</a>",
            unsafe_allow_html=True,
        )

    st.markdown("<hr class='sep'>", unsafe_allow_html=True)

    if st.session_state.unlocked:
        compteur_html = "<span style='color:#a78bfa;'>∞ illimité</span>"
    elif st.session_state.nb_gen < FREE_LIMIT:
        compteur_html = f"<span style='color:#34d399;'>{FREE_LIMIT - st.session_state.nb_gen} essai gratuit</span>"
    else:
        compteur_html = "<span style='color:#ef4444;'>Essai épuisé</span>"

    st.markdown(
        f"<div style='font-family:DM Mono,monospace;font-size:.72rem;"
        f"color:#1e2840;text-align:center;'>{compteur_html}</div>",
        unsafe_allow_html=True,
    )
    st.markdown(
        "<div style='color:#1e2840;font-size:.76rem;line-height:1.7;margin-top:1.2rem;'>"
        "<strong style='color:#2e3a52;'>Comment ça marche</strong><br>"
        "① Collez votre cours<br>② Générez le quiz<br>③ Révisez !</div>",
        unsafe_allow_html=True,
    )

# ── En-tête ───────────────────────────────────────────────────────────────────
if st.session_state.unlocked:
    badge = "<span class='badge badge-infinite'>ILLIMITÉ</span>"
elif st.session_state.nb_gen < FREE_LIMIT:
    badge = "<span class='badge badge-free'>ESSAI GRATUIT</span>"
else:
    badge = "<span class='badge badge-locked'>VERROUILLÉ</span>"

st.markdown(
    f"<div class='app-hero'>"
    f"<h1>Quiz Master IA {badge}</h1>"
    f"<p class='tagline'>Transformez vos notes en quiz de révision en secondes</p>"
    f"</div>",
    unsafe_allow_html=True,
)
st.markdown("<hr class='sep'>", unsafe_allow_html=True)

# ── Interface verrouillée ─────────────────────────────────────────────────────
if is_locked:
    st.markdown(
        "<div class='lock-strip'>"
        "<div class='lock-icon'>🔒</div>"
        "<div class='lock-title'>Votre essai gratuit est épuisé</div>"
        "<div class='lock-sub'>Entrez un code d'accès dans la barre latérale<br>"
        "ou débloquez l'accès illimité.</div>"
        "</div>",
        unsafe_allow_html=True,
    )
    st.stop()

# ── Interface de génération ───────────────────────────────────────────────────
st.markdown(
    "<div class='info-strip'>"
    "📋 Collez le texte de votre cours ci-dessous. "
    "Mistral AI génère 5 questions basées <strong>uniquement</strong> sur votre contenu."
    "</div>",
    unsafe_allow_html=True,
)

course_text = st.text_area(
    "Cours",
    placeholder=(
        "Collez ici votre cours, vos notes, un résumé de chapitre…\n\n"
        "Exemple : « La photosynthèse est le processus par lequel les plantes "
        "convertissent la lumière solaire en énergie chimique… »"
    ),
    height=240,
    label_visibility="collapsed",
)

clicked = st.button("⚡ Générer mon Quiz", use_container_width=True)

if clicked:
    if not course_text or len(course_text.strip()) < 60:
        st.warning("⚠️ Veuillez coller un texte suffisamment long (minimum 60 caractères).")
    else:
        # ── Bloc de génération — intégralement dans try/except ────────────────
        try:
            api_key = st.secrets["MISTRAL_API_KEY"]
            client  = Mistral(api_key=api_key)

            with st.spinner("🧠 Mistral analyse votre cours et compose le quiz…"):
                response = client.chat.complete(
                    model=MISTRAL_MODEL,
                    messages=[
                        {"role": "system", "content": SYSTEM_PROMPT},
                        {
                            "role": "user",
                            "content": (
                                f"Voici le texte du cours :\n\n---\n{course_text.strip()}\n---\n\n"
                                "Génère les 5 questions en JSON."
                            ),
                        },
                    ],
                    temperature=0.35,
                    max_tokens=2048,
                )

            raw: str = response.choices[0].message.content.strip()

            # Nettoyage des fences markdown éventuelles
            raw = re.sub(r"^```(?:json)?\s*", "", raw, flags=re.IGNORECASE)
            raw = re.sub(r"\s*```\s*$",       "", raw)
            raw = raw.strip()

            quiz_data = json.loads(raw)

            if "questions" not in quiz_data or not isinstance(quiz_data["questions"], list):
                raise ValueError("Réponse JSON invalide : clé 'questions' manquante ou malformée.")

            st.session_state.quiz_data = quiz_data
            st.session_state.nb_gen   += 1

        except Exception as e:
            st.error(f"❌ Erreur lors de la génération : {e}")
            st.session_state.quiz_data = None

# ── Affichage du quiz ─────────────────────────────────────────────────────────
if st.session_state.quiz_data:
    questions = st.session_state.quiz_data.get("questions", [])

    if not questions:
        st.warning("Le quiz retourné est vide. Réessayez avec un texte plus détaillé.")
    else:
        st.markdown("<hr class='sep'>", unsafe_allow_html=True)
        st.markdown(
            f"<div style='color:#6a4fff;font-size:.75rem;font-weight:600;"
            f"letter-spacing:.12em;text-transform:uppercase;margin-bottom:1rem;'>"
            f"📊 Quiz — {len(questions)} questions générées</div>",
            unsafe_allow_html=True,
        )

        for q in questions:
            num     = q.get("numero", "?")
            total   = len(questions)
            texte_q = q.get("question", "")
            options = q.get("options", {})
            bonne   = q.get("bonne_reponse", "")
            expl    = q.get("explication", "")

            opts_html = "".join(
                f"<div class='opt'>"
                f"<span class='opt-ltr'>{ltr}</span>"
                f"<span class='opt-txt'>{txt}</span>"
                f"</div>"
                for ltr, txt in options.items()
            )

            st.markdown(
                f"<div class='q-card'>"
                f"<div class='q-num'>Question {num} / {total}</div>"
                f"<div class='q-text'>{texte_q}</div>"
                f"{opts_html}"
                f"</div>",
                unsafe_allow_html=True,
            )

            with st.expander("🔍 Voir le corrigé"):
                bonne_txt = options.get(bonne, "")
                if bonne_txt:
                    st.markdown(
                        f"<div class='corrige-box'>"
                        f"✅ Bonne réponse : <strong>{bonne}. {bonne_txt}</strong>"
                        f"</div>"
                        f"<div class='expl-txt'>💡 {expl}</div>",
                        unsafe_allow_html=True,
                    )
                else:
                    st.info("Corrigé non disponible pour cette question.")

        st.markdown(
            "<div class='footer-note'>"
            "Généré par <strong>Quiz Master IA</strong> · Propulsé par Mistral AI"
            "</div>",
            unsafe_allow_html=True,
        )
