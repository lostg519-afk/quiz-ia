"""
Quiz Master IA — app.py
Dépendances minimales (requirements.txt) :
    streamlit>=1.35.0
    requests>=2.31.0
"""

import json
import re
import requests
import streamlit as st

# ── Configuration page ────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Quiz Master IA",
    page_icon="⚡",
    layout="centered",
    initial_sidebar_state="expanded",
)

# ── CSS ───────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;500;600;700;800&family=DM+Mono:wght@400;500&display=swap');

html, body, [class*="css"] { font-family: 'Syne', sans-serif; }

.stApp {
    background: #06070c;
    background-image:
        radial-gradient(ellipse 65% 40% at 10% 0%,   rgba(120, 60, 255, 0.20) 0%, transparent 60%),
        radial-gradient(ellipse 50% 35% at 90% 100%, rgba(0, 210, 175, 0.13) 0%, transparent 60%);
    color: #d8e0f0;
}

[data-testid="stSidebar"] {
    background: #09090f !important;
    border-right: 1px solid #141620 !important;
}
[data-testid="stSidebar"] * { color: #6a7a9a; }

#MainMenu, footer, header { visibility: hidden; }
.block-container { padding-top: 1.75rem !important; max-width: 800px; }

/* ── Hero ── */
.hero { text-align: center; padding: 1.25rem 0 .5rem; }
.hero h1 {
    font-size: 2.9rem; font-weight: 800; letter-spacing: -.04em; line-height: 1.05; margin: 0;
    background: linear-gradient(125deg, #c084fc 0%, #818cf8 40%, #34d399 100%);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;
}
.hero .sub {
    font-size: .82rem; color: #2e3a55; letter-spacing: .15em;
    text-transform: uppercase; margin-top: .6rem; font-weight: 500;
}

/* ── Badges ── */
.bdg {
    display: inline-block; font-size: .6rem; font-weight: 700; letter-spacing: .12em;
    text-transform: uppercase; padding: .16rem .6rem; border-radius: 999px;
    vertical-align: middle; margin-left: .4rem; font-family: 'DM Mono', monospace;
}
.bdg-free { background: linear-gradient(135deg,#10b981,#059669); color:#fff; }
.bdg-lock { background: linear-gradient(135deg,#ef4444,#dc2626); color:#fff; }
.bdg-vip  { background: linear-gradient(135deg,#8b5cf6,#6d28d9); color:#fff; }

/* ── Textarea ── */
.stTextArea textarea {
    background: #0c0d15 !important; border: 1px solid #181c2e !important;
    border-radius: 14px !important; color: #d8e0f0 !important;
    font-family: 'Syne', sans-serif !important; font-size: .93rem !important;
    padding: 1.1rem !important; transition: border-color .2s; resize: vertical;
}
.stTextArea textarea:focus {
    border-color: #818cf8 !important;
    box-shadow: 0 0 0 3px rgba(129,140,248,.12) !important;
}
.stTextArea textarea::placeholder { color: #252d40 !important; }

/* ── Bouton principal ── */
.stButton > button {
    width: 100%;
    background: linear-gradient(135deg, #5b3ff8 0%, #9b6dff 100%) !important;
    color: #fff !important; border: none !important; border-radius: 14px !important;
    padding: .95rem 2rem !important; font-family: 'Syne', sans-serif !important;
    font-size: 1rem !important; font-weight: 700 !important;
    box-shadow: 0 4px 24px rgba(91,63,248,.4) !important;
    transition: all .2s ease !important; letter-spacing: .01em !important;
}
.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 32px rgba(91,63,248,.58) !important;
}
.stButton > button:active { transform: translateY(0) !important; }

/* ── Carte question ── */
.q-wrap {
    background: #0c0d15; border: 1px solid #14162a;
    border-radius: 18px; padding: 1.5rem 1.8rem;
    margin-bottom: 1.2rem; position: relative; overflow: hidden;
}
.q-wrap::before {
    content: ''; position: absolute; top: 0; left: 0;
    width: 4px; height: 100%;
    background: linear-gradient(180deg, #5b3ff8, #9b6dff);
    border-radius: 4px 0 0 4px;
}
.q-num {
    font-family: 'DM Mono', monospace; font-size: .65rem; font-weight: 500;
    color: #5b3ff8; letter-spacing: .14em; text-transform: uppercase; margin-bottom: .4rem;
}
.q-txt { font-size: 1.02rem; font-weight: 700; color: #eef2ff; line-height: 1.5; margin-bottom: 1rem; }

.opt-row {
    display: flex; align-items: flex-start; gap: .7rem;
    padding: .5rem .7rem; border-radius: 9px; margin-bottom: .3rem;
    transition: background .15s;
}
.opt-row:hover { background: rgba(91,63,248,.07); }
.opt-key {
    font-family: 'DM Mono', monospace; font-size: .72rem; font-weight: 600;
    color: #818cf8; background: rgba(129,140,248,.14);
    border-radius: 6px; padding: .08rem .42rem;
    min-width: 1.55rem; text-align: center; flex-shrink: 0; margin-top: .06rem;
}
.opt-val { color: #b0bcd8; font-size: .9rem; line-height: 1.45; }

/* ── Corrigé (expander) ── */
.ok-box {
    background: rgba(16,185,129,.09); border: 1px solid rgba(16,185,129,.22);
    border-radius: 10px; padding: .75rem 1rem;
    color: #34d399; font-size: .88rem; font-weight: 600;
}
.expl { color: #3a4a66; font-size: .83rem; font-style: italic; margin-top: .5rem; line-height: 1.5; }

/* ── Bandeaux ── */
.info-bar {
    background: rgba(129,140,248,.08); border: 1px solid rgba(129,140,248,.18);
    border-radius: 13px; padding: .9rem 1.15rem;
    color: #9aaaff; font-size: .87rem; margin-bottom: 1.2rem; line-height: 1.5;
}
.lock-panel {
    background: rgba(239,68,68,.07); border: 1px solid rgba(239,68,68,.2);
    border-radius: 16px; padding: 2rem 1.5rem; text-align: center;
}
.lock-panel .ico   { font-size: 2.2rem; margin-bottom: .5rem; }
.lock-panel .title { font-size: 1.05rem; font-weight: 700; color: #f87171; }
.lock-panel .desc  { font-size: .84rem; color: #4a5a78; margin-top: .35rem; line-height: 1.55; }

/* ── Bouton Gumroad sidebar ── */
a.g-btn {
    display: block; margin-top: 1rem; padding: .8rem 1rem;
    background: linear-gradient(135deg, #ef4444, #dc2626);
    color: #fff !important; border-radius: 11px;
    font-family: 'Syne', sans-serif; font-size: .84rem; font-weight: 700;
    text-align: center; text-decoration: none !important;
    box-shadow: 0 4px 18px rgba(239,68,68,.35); transition: box-shadow .2s;
}
a.g-btn:hover { box-shadow: 0 6px 26px rgba(239,68,68,.55); }

/* ── Succès code ── */
.code-ok {
    background: rgba(139,92,246,.1); border: 1px solid rgba(139,92,246,.25);
    border-radius: 10px; padding: .6rem 1rem;
    color: #c4b5fd; font-size: .83rem; margin-top: .5rem;
}
.code-no { color: #ef4444; font-size: .8rem; margin-top: .35rem; }

hr.s { border: none; border-top: 1px solid #14162a; margin: 1.3rem 0; }
.foot { text-align: center; color: #1a2035; font-size: .77rem; margin-top: .75rem; }
</style>
""", unsafe_allow_html=True)

# ── Constantes ────────────────────────────────────────────────────────────────
FREE_LIMIT   = 1
ACCESS_CODE  = "MISTRAL2026"
GUMROAD_URL  = "https://lostgaze.gumroad.com/l/tdjjua"
API_URL      = "https://api.mistral.ai/v1/chat/completions"
MODEL        = "mistral-small-latest"

SYSTEM_PROMPT = (
    "Tu es un expert pédagogique francophone. "
    "Génère exactement 5 questions de QCM basées UNIQUEMENT sur le texte fourni. "
    "N'utilise aucune connaissance externe.\n\n"
    "Règles :\n"
    "- 4 options par question (A, B, C, D).\n"
    "- 1 seule bonne réponse par question.\n"
    "- Les distracteurs doivent être plausibles mais faux selon le texte.\n"
    "- Fournis une explication courte (1-2 phrases) qui justifie la bonne réponse.\n\n"
    "Réponds UNIQUEMENT avec un objet JSON valide, sans texte avant ni après, "
    "sans balises markdown.\n\n"
    "Format attendu :\n"
    '{\n  "questions": [\n    {\n'
    '      "numero": 1,\n'
    '      "question": "...",\n'
    '      "options": { "A": "...", "B": "...", "C": "...", "D": "..." },\n'
    '      "bonne_reponse": "A",\n'
    '      "explication": "..."\n'
    "    }\n  ]\n}"
)

# ── Session state ─────────────────────────────────────────────────────────────
for _k, _v in [("nb_gen", 0), ("unlocked", False), ("quiz_data", None)]:
    if _k not in st.session_state:
        st.session_state[_k] = _v

# ── Fonction d'appel API (requests uniquement) ────────────────────────────────
def call_mistral_api(api_key: str, course: str) -> dict:
    """
    Appelle l'API Mistral via requests.post et retourne le dict JSON du quiz.
    Lève une exception explicite en cas d'erreur HTTP ou de JSON invalide.
    """
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type":  "application/json",
    }
    payload = {
        "model": MODEL,
        "temperature": 0.35,
        "max_tokens":  2048,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {
                "role": "user",
                "content": (
                    f"Voici le texte du cours :\n\n---\n{course}\n---\n\n"
                    "Génère les 5 questions en JSON."
                ),
            },
        ],
    }

    response = requests.post(API_URL, headers=headers, json=payload, timeout=60)

    # Erreur HTTP (4xx / 5xx)
    if not response.ok:
        try:
            detail = response.json().get("message", response.text)
        except Exception:
            detail = response.text
        raise RuntimeError(
            f"Erreur API Mistral [{response.status_code}] : {detail}"
        )

    data = response.json()

    # Extraction du contenu brut
    raw: str = data["choices"][0]["message"]["content"].strip()

    # Nettoyage des éventuels fences markdown ```json … ```
    raw = re.sub(r"^```(?:json)?\s*", "", raw, flags=re.IGNORECASE)
    raw = re.sub(r"\s*```\s*$",       "", raw)
    raw = raw.strip()

    quiz = json.loads(raw)

    if "questions" not in quiz or not isinstance(quiz["questions"], list):
        raise ValueError(
            "La réponse JSON ne contient pas une clé 'questions' valide."
        )

    return quiz

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown(
        "<div style='padding:.8rem 0 .2rem;font-size:1.05rem;"
        "font-weight:700;color:#d8e0f0;'>⚡ Quiz Master IA</div>"
        "<hr class='s'>",
        unsafe_allow_html=True,
    )

    st.markdown(
        "<p style='font-size:.73rem;color:#2e3a55;text-transform:uppercase;"
        "letter-spacing:.12em;font-weight:600;margin-bottom:.4rem;'>"
        "🔑 Code d'accès illimité</p>",
        unsafe_allow_html=True,
    )

    code_saisi = st.text_input(
        "code", type="password",
        placeholder="Entrez votre code…",
        label_visibility="collapsed",
    )

    if code_saisi == ACCESS_CODE:
        st.session_state.unlocked = True
        st.markdown("<div class='code-ok'>✅ Accès illimité activé !</div>", unsafe_allow_html=True)
    elif code_saisi:
        st.markdown("<div class='code-no'>❌ Code incorrect</div>", unsafe_allow_html=True)

    is_locked = (st.session_state.nb_gen >= FREE_LIMIT and not st.session_state.unlocked)

    if is_locked:
        st.markdown(
            f"<a href='{GUMROAD_URL}' target='_blank' class='g-btn'>"
            "🔓 Débloquer l'accès illimité (2€)</a>",
            unsafe_allow_html=True,
        )

    st.markdown("<hr class='s'>", unsafe_allow_html=True)

    # Compteur
    if st.session_state.unlocked:
        cpt = "<span style='color:#a78bfa;'>∞ illimité</span>"
    elif st.session_state.nb_gen < FREE_LIMIT:
        cpt = f"<span style='color:#34d399;'>{FREE_LIMIT - st.session_state.nb_gen} essai gratuit</span>"
    else:
        cpt = "<span style='color:#ef4444;'>Essai épuisé</span>"

    st.markdown(
        f"<div style='font-family:DM Mono,monospace;font-size:.7rem;"
        f"color:#1a2035;text-align:center;'>{cpt}</div>",
        unsafe_allow_html=True,
    )
    st.markdown(
        "<div style='color:#1a2035;font-size:.74rem;line-height:1.75;margin-top:1.1rem;'>"
        "<strong style='color:#252d40;'>Comment ça marche</strong><br>"
        "① Collez votre cours<br>② Générez le quiz<br>③ Révisez !</div>",
        unsafe_allow_html=True,
    )

# ── En-tête ───────────────────────────────────────────────────────────────────
if st.session_state.unlocked:
    badge = "<span class='bdg bdg-vip'>ILLIMITÉ</span>"
elif st.session_state.nb_gen < FREE_LIMIT:
    badge = "<span class='bdg bdg-free'>ESSAI GRATUIT</span>"
else:
    badge = "<span class='bdg bdg-lock'>VERROUILLÉ</span>"

st.markdown(
    f"<div class='hero'><h1>Quiz Master IA {badge}</h1>"
    f"<p class='sub'>Transformez vos notes en quiz de révision en secondes</p></div>",
    unsafe_allow_html=True,
)
st.markdown("<hr class='s'>", unsafe_allow_html=True)

# ── Écran verrou ──────────────────────────────────────────────────────────────
if is_locked:
    st.markdown(
        "<div class='lock-panel'>"
        "<div class='ico'>🔒</div>"
        "<div class='title'>Votre essai gratuit est épuisé</div>"
        "<div class='desc'>Entrez un code d'accès dans la barre latérale<br>"
        "ou débloquez l'accès illimité.</div>"
        "</div>",
        unsafe_allow_html=True,
    )
    st.stop()

# ── Zone de saisie ────────────────────────────────────────────────────────────
st.markdown(
    "<div class='info-bar'>"
    "📋 Collez votre cours ci-dessous. Mistral AI génère <strong>5 questions de QCM</strong> "
    "basées uniquement sur votre texte — sans connaissances externes."
    "</div>",
    unsafe_allow_html=True,
)

course_text = st.text_area(
    "cours", height=240,
    placeholder=(
        "Collez ici votre cours, vos notes, un résumé de chapitre…\n\n"
        "Exemple : « La photosynthèse est le processus par lequel les plantes "
        "convertissent la lumière solaire en énergie chimique via la chlorophylle… »"
    ),
    label_visibility="collapsed",
)

clicked = st.button("⚡ Générer mon Quiz", use_container_width=True)

# ── Génération ────────────────────────────────────────────────────────────────
if clicked:
    if not course_text or len(course_text.strip()) < 60:
        st.warning("⚠️ Veuillez coller un texte plus long (minimum 60 caractères).")
    else:
        try:
            api_key = st.secrets["MISTRAL_API_KEY"]

            with st.spinner("🧠 Mistral analyse votre cours et compose le quiz…"):
                quiz_data = call_mistral_api(api_key, course_text.strip())

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
        st.markdown("<hr class='s'>", unsafe_allow_html=True)
        st.markdown(
            f"<div style='color:#5b3ff8;font-size:.72rem;font-weight:700;"
            f"letter-spacing:.14em;text-transform:uppercase;margin-bottom:1.1rem;'>"
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
                f"<div class='opt-row'>"
                f"<span class='opt-key'>{ltr}</span>"
                f"<span class='opt-val'>{txt}</span>"
                f"</div>"
                for ltr, txt in options.items()
            )

            st.markdown(
                f"<div class='q-wrap'>"
                f"<div class='q-num'>Question {num} / {total}</div>"
                f"<div class='q-txt'>{texte_q}</div>"
                f"{opts_html}"
                f"</div>",
                unsafe_allow_html=True,
            )

            with st.expander("🔍 Voir le corrigé"):
                bonne_txt = options.get(bonne, "")
                if bonne_txt:
                    st.markdown(
                        f"<div class='ok-box'>"
                        f"✅ Bonne réponse : <strong>{bonne}. {bonne_txt}</strong>"
                        f"</div>"
                        f"<div class='expl'>💡 {expl}</div>",
                        unsafe_allow_html=True,
                    )
                else:
                    st.info("Corrigé non disponible pour cette question.")

        st.markdown(
            "<div class='foot'>"
            "Généré par <strong>Quiz Master IA</strong> · Mistral AI · "
            "<code style='font-size:.7rem;color:#252d40;'>requests</code>"
            "</div>",
            unsafe_allow_html=True,
        )
