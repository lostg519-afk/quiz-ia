"""
Quiz Master IA — main.py
requirements.txt :
    streamlit>=1.35.0
    requests>=2.31.0
"""

import json
import re
import requests
import streamlit as st

# ─────────────────────────────────────────────────────────────────────────────
# CONFIGURATION PAGE
# ─────────────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Quiz Master IA",
    page_icon="⚡",
    layout="centered",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────────────────────────────────────
# CSS
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;500;600;700;800&family=DM+Mono:wght@400;500&display=swap');

html, body, [class*="css"] { font-family: 'Syne', sans-serif; }

.stApp {
    background: #06070c;
    background-image:
        radial-gradient(ellipse 65% 40% at 10% 0%,   rgba(120,60,255,.20) 0%, transparent 60%),
        radial-gradient(ellipse 50% 35% at 90% 100%, rgba(0,210,175,.13)  0%, transparent 60%);
    color: #d8e0f0;
}
[data-testid="stSidebar"] {
    background: #09090f !important;
    border-right: 1px solid #141620 !important;
}
[data-testid="stSidebar"] * { color: #6a7a9a; }
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding-top: 1.75rem !important; max-width: 820px; }

/* ── Hero ── */
.hero { text-align:center; padding:1.25rem 0 .5rem; }
.hero h1 {
    font-size:2.85rem; font-weight:800; letter-spacing:-.04em; line-height:1.05; margin:0;
    background: linear-gradient(125deg,#c084fc 0%,#818cf8 40%,#34d399 100%);
    -webkit-background-clip:text; -webkit-text-fill-color:transparent; background-clip:text;
}
.hero .sub {
    font-size:.82rem; color:#2e3a55; letter-spacing:.15em;
    text-transform:uppercase; margin-top:.6rem; font-weight:500;
}

/* ── Badges ── */
.bdg {
    display:inline-block; font-size:.6rem; font-weight:700; letter-spacing:.12em;
    text-transform:uppercase; padding:.15rem .6rem; border-radius:999px;
    vertical-align:middle; margin-left:.4rem; font-family:'DM Mono',monospace;
}
.bdg-free { background:linear-gradient(135deg,#10b981,#059669); color:#fff; }
.bdg-lock { background:linear-gradient(135deg,#ef4444,#dc2626); color:#fff; }
.bdg-vip  { background:linear-gradient(135deg,#8b5cf6,#6d28d9); color:#fff; }

/* ── Textarea ── */
.stTextArea textarea {
    background:#0c0d15 !important; border:1px solid #181c2e !important;
    border-radius:14px !important; color:#d8e0f0 !important;
    font-family:'Syne',sans-serif !important; font-size:.93rem !important;
    padding:1.1rem !important; transition:border-color .2s; resize:vertical;
}
.stTextArea textarea:focus {
    border-color:#818cf8 !important;
    box-shadow:0 0 0 3px rgba(129,140,248,.12) !important;
}
.stTextArea textarea::placeholder { color:#252d40 !important; }

/* ── Boutons ── */
.stButton > button {
    width:100%;
    background:linear-gradient(135deg,#5b3ff8 0%,#9b6dff 100%) !important;
    color:#fff !important; border:none !important; border-radius:14px !important;
    padding:.9rem 2rem !important; font-family:'Syne',sans-serif !important;
    font-size:1rem !important; font-weight:700 !important;
    box-shadow:0 4px 24px rgba(91,63,248,.4) !important; transition:all .2s !important;
}
.stButton > button:hover {
    transform:translateY(-2px) !important;
    box-shadow:0 8px 32px rgba(91,63,248,.58) !important;
}

/* ── Radio buttons ── */
.stRadio > div { gap:.3rem !important; }
.stRadio label {
    background:#0e0f18; border:1px solid #1a1d2e;
    border-radius:10px; padding:.55rem .9rem !important;
    cursor:pointer; transition:all .18s; width:100%; display:block;
    font-size:.92rem !important; color:#b0bcd8 !important;
}
.stRadio label:hover { border-color:#5b3ff8; background:#131424; color:#eef2ff !important; }
[data-testid="stRadio"] [aria-checked="true"] + div label,
.stRadio [data-checked="true"] label {
    border-color:#5b3ff8 !important; background:rgba(91,63,248,.1) !important;
    color:#eef2ff !important;
}

/* ── Carte question ── */
.q-wrap {
    background:#0c0d15; border:1px solid #14162a;
    border-radius:18px; padding:1.5rem 1.8rem 1.2rem;
    margin-bottom:1.2rem; position:relative; overflow:hidden;
}
.q-wrap::before {
    content:''; position:absolute; top:0; left:0; width:4px; height:100%;
    background:linear-gradient(180deg,#5b3ff8,#9b6dff); border-radius:4px 0 0 4px;
}
.q-num {
    font-family:'DM Mono',monospace; font-size:.65rem; font-weight:500; color:#5b3ff8;
    letter-spacing:.14em; text-transform:uppercase; margin-bottom:.4rem;
}
.q-txt { font-size:1.02rem; font-weight:700; color:#eef2ff; line-height:1.5; margin-bottom:.9rem; }

/* ── Feedback ── */
.fb-ok {
    background:rgba(16,185,129,.1); border:1px solid rgba(16,185,129,.25);
    border-radius:10px; padding:.7rem 1rem; color:#34d399;
    font-size:.88rem; font-weight:600; margin-top:.75rem;
}
.fb-ko {
    background:rgba(239,68,68,.09); border:1px solid rgba(239,68,68,.25);
    border-radius:10px; padding:.7rem 1rem; color:#f87171;
    font-size:.88rem; font-weight:600; margin-top:.75rem;
}
.fb-expl { color:#3a4a66; font-size:.82rem; font-style:italic; margin-top:.4rem; line-height:1.5; }
.fb-warn {
    background:rgba(251,191,36,.09); border:1px solid rgba(251,191,36,.25);
    border-radius:10px; padding:.65rem 1rem; color:#fbbf24;
    font-size:.85rem; margin-top:.75rem;
}

/* ── Score final ── */
.score-box {
    background:linear-gradient(135deg,#0f1020,#13152a);
    border:1px solid #2a2d4a; border-radius:20px;
    padding:2rem 2rem 1.75rem; text-align:center; margin:1.5rem 0 .5rem;
}
.score-num {
    font-size:4rem; font-weight:800; letter-spacing:-.04em;
    background:linear-gradient(130deg,#c084fc,#818cf8 50%,#34d399);
    -webkit-background-clip:text; -webkit-text-fill-color:transparent; background-clip:text;
    line-height:1;
}
.score-label { font-size:.85rem; color:#3a4a66; margin-top:.5rem; letter-spacing:.1em; text-transform:uppercase; }
.score-msg { font-size:1rem; font-weight:600; color:#d8e0f0; margin-top:.8rem; }

/* ── Bandeaux ── */
.info-bar {
    background:rgba(129,140,248,.08); border:1px solid rgba(129,140,248,.18);
    border-radius:13px; padding:.9rem 1.15rem;
    color:#9aaaff; font-size:.87rem; margin-bottom:1.2rem; line-height:1.5;
}
.lock-panel {
    background:rgba(239,68,68,.07); border:1px solid rgba(239,68,68,.2);
    border-radius:16px; padding:2rem 1.5rem; text-align:center;
}
.lock-panel .ico   { font-size:2.2rem; margin-bottom:.5rem; }
.lock-panel .title { font-size:1.05rem; font-weight:700; color:#f87171; }
.lock-panel .desc  { font-size:.84rem; color:#4a5a78; margin-top:.35rem; line-height:1.55; }

/* ── Sidebar ── */
a.g-btn {
    display:block; margin-top:1rem; padding:.8rem 1rem;
    background:linear-gradient(135deg,#ef4444,#dc2626);
    color:#fff !important; border-radius:11px;
    font-family:'Syne',sans-serif; font-size:.84rem; font-weight:700;
    text-align:center; text-decoration:none !important;
    box-shadow:0 4px 18px rgba(239,68,68,.35); transition:box-shadow .2s;
}
a.g-btn:hover { box-shadow:0 6px 26px rgba(239,68,68,.55); }
.code-ok {
    background:rgba(139,92,246,.1); border:1px solid rgba(139,92,246,.25);
    border-radius:10px; padding:.6rem 1rem; color:#c4b5fd; font-size:.83rem; margin-top:.5rem;
}
.code-no { color:#ef4444; font-size:.8rem; margin-top:.4rem; }
.verif-loading { color:#818cf8; font-size:.82rem; margin-top:.4rem; font-style:italic; }

hr.s { border:none; border-top:1px solid #14162a; margin:1.3rem 0; }
.foot { text-align:center; color:#1a2035; font-size:.77rem; margin-top:.75rem; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# CONSTANTES
# ─────────────────────────────────────────────────────────────────────────────
FREE_LIMIT      = 1
GUMROAD_URL     = "https://lostgaze.gumroad.com/l/tdjjua"
GUMROAD_PRODUCT = "Jea3JmwYkYgLzLySngidiw=="
GUMROAD_API     = "https://api.gumroad.com/v2/licenses/verify"
MISTRAL_API     = "https://api.mistral.ai/v1/chat/completions"
MODEL           = "mistral-small-latest"
OPTIONS         = ["A", "B", "C", "D"]

SYSTEM_PROMPT = (
    "Tu es un expert pédagogique francophone. "
    "Génère exactement 5 questions de QCM basées UNIQUEMENT sur le texte fourni. "
    "N'utilise aucune connaissance externe.\n\n"
    "Règles :\n"
    "- 4 options par question (A, B, C, D).\n"
    "- 1 seule bonne réponse par question.\n"
    "- Les distracteurs doivent être plausibles mais faux selon le texte.\n"
    "- Fournis une explication courte (1-2 phrases) qui justifie la bonne réponse.\n\n"
    "Réponds UNIQUEMENT avec un objet JSON valide, sans texte avant ni après, sans balises markdown.\n\n"
    'Format : {"questions":[{"numero":1,"question":"...","options":{"A":"...","B":"...","C":"...","D":"..."},"bonne_reponse":"A","explication":"..."}]}'
)

SCORE_MSGS = {
    5: "🏆 Parfait ! Maîtrise totale du cours.",
    4: "🎯 Excellent ! Très bonne compréhension.",
    3: "👍 Bien ! Quelques points à revoir.",
    2: "📖 Passable. Relisez les explications.",
    1: "💪 Courage ! Repassez le cours en détail.",
    0: "😅 Il faut tout reprendre depuis le début !",
}

# ─────────────────────────────────────────────────────────────────────────────
# SESSION STATE — initialisation
# ─────────────────────────────────────────────────────────────────────────────
DEFAULTS = {
    "nb_gen":     0,
    "unlocked":   False,
    "quiz_data":  None,
    "validated":  False,   # True après clic sur "Valider le quiz"
    "gumroad_ok": False,   # True si licence Gumroad vérifiée
}
for k, v in DEFAULTS.items():
    if k not in st.session_state:
        st.session_state[k] = v


# ─────────────────────────────────────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────────────────────────────────────
def verify_gumroad_license(license_key: str) -> tuple[bool, str]:
    """
    Vérifie une clé de licence Gumroad via l'API officielle.
    Retourne (success: bool, message: str).
    """
    try:
        r = requests.post(
            GUMROAD_API,
            data={"product_id": GUMROAD_PRODUCT, "license_key": license_key.strip()},
            timeout=10,
        )
        data = r.json()
        if data.get("success"):
            return True, "✅ Licence valide — Accès illimité activé !"
        else:
            msg = data.get("message", "Licence invalide ou déjà utilisée.")
            return False, f"❌ {msg}"
    except requests.exceptions.Timeout:
        return False, "❌ Délai dépassé — vérifiez votre connexion."
    except Exception as exc:
        return False, f"❌ Erreur de vérification : {exc}"


def call_mistral(api_key: str, course: str) -> dict:
    """Appelle l'API Mistral via requests et retourne le dict du quiz."""
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
            {"role": "user",   "content": (
                f"Voici le texte du cours :\n\n---\n{course}\n---\n\n"
                "Génère les 5 questions en JSON."
            )},
        ],
    }
    r = requests.post(MISTRAL_API, headers=headers, json=payload, timeout=60)
    if not r.ok:
        try:
            detail = r.json().get("message", r.text)
        except Exception:
            detail = r.text
        raise RuntimeError(f"Erreur API Mistral [{r.status_code}] : {detail}")

    raw: str = r.json()["choices"][0]["message"]["content"].strip()
    raw = re.sub(r"^```(?:json)?\s*", "", raw, flags=re.IGNORECASE)
    raw = re.sub(r"\s*```\s*$",       "", raw)
    raw = raw.strip()

    quiz = json.loads(raw)
    if "questions" not in quiz or not isinstance(quiz["questions"], list):
        raise ValueError("JSON invalide : clé 'questions' manquante ou malformée.")
    return quiz


def reset_quiz():
    """Remet à zéro les données du quiz et les réponses."""
    st.session_state.quiz_data = None
    st.session_state.validated  = False
    # Supprime les clés de réponses individuelles
    for i in range(10):
        st.session_state.pop(f"ans_{i}", None)


def get_score(questions: list) -> int:
    """Calcule le nombre de bonnes réponses."""
    score = 0
    for i, q in enumerate(questions):
        user_ans = st.session_state.get(f"ans_{i}")
        if user_ans and user_ans[0] == q.get("bonne_reponse", ""):
            score += 1
    return score


# ─────────────────────────────────────────────────────────────────────────────
# SIDEBAR — Licence & statut
# ─────────────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown(
        "<div style='padding:.8rem 0 .2rem;font-size:1.05rem;"
        "font-weight:700;color:#d8e0f0;'>⚡ Quiz Master IA</div>"
        "<hr class='s'>",
        unsafe_allow_html=True,
    )

    # ── Vérification licence Gumroad ──────────────────────────────────────────
    st.markdown(
        "<p style='font-size:.73rem;color:#2e3a55;text-transform:uppercase;"
        "letter-spacing:.12em;font-weight:600;margin-bottom:.4rem;'>"
        "🔑 Clé de licence</p>",
        unsafe_allow_html=True,
    )

    license_input = st.text_input(
        "licence", type="password",
        placeholder="XXXX-XXXX-XXXX-XXXX",
        label_visibility="collapsed",
        key="license_field",
    )

    if st.button("Vérifier la licence", use_container_width=True):
        if license_input.strip():
            with st.spinner("Vérification en cours…"):
                ok, msg = verify_gumroad_license(license_input)
            if ok:
                st.session_state.unlocked   = True
                st.session_state.gumroad_ok = True
            st.markdown(
                f"<div class='{'code-ok' if ok else 'code-no'}'>{msg}</div>",
                unsafe_allow_html=True,
            )
        else:
            st.markdown("<div class='code-no'>Entrez une clé de licence.</div>",
                        unsafe_allow_html=True)

    if st.session_state.gumroad_ok:
        st.markdown("<div class='code-ok'>✅ Licence active — accès illimité</div>",
                    unsafe_allow_html=True)

    # ── Bouton Gumroad si verrouillé ─────────────────────────────────────────
    is_locked = (
        st.session_state.nb_gen >= FREE_LIMIT
        and not st.session_state.unlocked
    )
    if is_locked:
        st.markdown(
            f"<a href='{GUMROAD_URL}' target='_blank' class='g-btn'>"
            "🔓 Obtenir ma licence (2€)</a>",
            unsafe_allow_html=True,
        )

    st.markdown("<hr class='s'>", unsafe_allow_html=True)

    # ── Compteur ──────────────────────────────────────────────────────────────
    if st.session_state.unlocked:
        cpt = "<span style='color:#a78bfa;'>∞ illimité</span>"
    elif st.session_state.nb_gen < FREE_LIMIT:
        cpt = (f"<span style='color:#34d399;'>"
               f"{FREE_LIMIT - st.session_state.nb_gen} essai gratuit</span>")
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
        "① Collez votre cours<br>② Générez le quiz<br>"
        "③ Sélectionnez vos réponses<br>④ Validez et voyez votre score</div>",
        unsafe_allow_html=True,
    )


# ─────────────────────────────────────────────────────────────────────────────
# EN-TÊTE PRINCIPAL
# ─────────────────────────────────────────────────────────────────────────────
if st.session_state.unlocked:
    badge = "<span class='bdg bdg-vip'>ILLIMITÉ</span>"
elif st.session_state.nb_gen < FREE_LIMIT:
    badge = "<span class='bdg bdg-free'>ESSAI GRATUIT</span>"
else:
    badge = "<span class='bdg bdg-lock'>VERROUILLÉ</span>"

st.markdown(
    f"<div class='hero'><h1>Quiz Master IA {badge}</h1>"
    f"<p class='sub'>Transformez vos notes en quiz de révision interactif</p></div>",
    unsafe_allow_html=True,
)
st.markdown("<hr class='s'>", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# ÉCRAN VERROU
# ─────────────────────────────────────────────────────────────────────────────
if is_locked:
    st.markdown(
        "<div class='lock-panel'>"
        "<div class='ico'>🔒</div>"
        "<div class='title'>Votre essai gratuit est épuisé</div>"
        "<div class='desc'>Entrez votre clé de licence dans la barre latérale<br>"
        "ou obtenez un accès illimité sur Gumroad.</div>"
        "</div>",
        unsafe_allow_html=True,
    )
    st.stop()


# ─────────────────────────────────────────────────────────────────────────────
# ZONE DE GÉNÉRATION (masquée si quiz déjà chargé)
# ─────────────────────────────────────────────────────────────────────────────
if not st.session_state.quiz_data:
    st.markdown(
        "<div class='info-bar'>"
        "📋 Collez votre cours ci-dessous. Mistral AI génère <strong>5 questions interactives</strong> "
        "basées uniquement sur votre texte."
        "</div>",
        unsafe_allow_html=True,
    )

    course_text = st.text_area(
        "cours", height=230,
        placeholder=(
            "Collez ici votre cours, vos notes, un résumé de chapitre…\n\n"
            "Exemple : « La photosynthèse est le processus par lequel les plantes "
            "convertissent la lumière solaire en énergie chimique via la chlorophylle… »"
        ),
        label_visibility="collapsed",
    )

    if st.button("⚡ Générer mon Quiz", use_container_width=True):
        if not course_text or len(course_text.strip()) < 60:
            st.warning("⚠️ Texte trop court (minimum 60 caractères).")
        else:
            try:
                api_key = st.secrets["MISTRAL_API_KEY"]
                with st.spinner("🧠 Mistral compose votre quiz…"):
                    quiz = call_mistral(api_key, course_text.strip())
                st.session_state.quiz_data = quiz
                st.session_state.validated  = False
                st.session_state.nb_gen    += 1
                st.rerun()
            except Exception as e:
                st.error(f"❌ Erreur : {e}")

# ─────────────────────────────────────────────────────────────────────────────
# QUIZ INTERACTIF
# ─────────────────────────────────────────────────────────────────────────────
if st.session_state.quiz_data:
    questions = st.session_state.quiz_data.get("questions", [])

    if not questions:
        st.warning("Quiz vide. Réessayez avec un texte plus détaillé.")
        st.stop()

    # ── En-tête du quiz ───────────────────────────────────────────────────────
    st.markdown(
        f"<div style='color:#5b3ff8;font-size:.72rem;font-weight:700;"
        f"letter-spacing:.14em;text-transform:uppercase;margin-bottom:1.1rem;'>"
        f"📊 Quiz — {len(questions)} questions</div>",
        unsafe_allow_html=True,
    )

    validated = st.session_state.validated

    # ── Rendu de chaque question ──────────────────────────────────────────────
    for i, q in enumerate(questions):
        num      = q.get("numero", i + 1)
        total    = len(questions)
        texte_q  = q.get("question", "")
        options  = q.get("options", {})
        bonne    = q.get("bonne_reponse", "")
        expl     = q.get("explication", "")

        # Labels radio : "A — Texte de l'option"
        radio_labels = [f"{ltr} — {txt}" for ltr, txt in options.items()]
        key_ans      = f"ans_{i}"

        st.markdown(
            f"<div class='q-wrap'>"
            f"<div class='q-num'>Question {num} / {total}</div>"
            f"<div class='q-txt'>{texte_q}</div>"
            f"</div>",
            unsafe_allow_html=True,
        )

        # Radio désactivé une fois validé
        user_choice = st.radio(
            f"q{i}",
            options=radio_labels,
            index=None,
            key=key_ans,
            label_visibility="collapsed",
            disabled=validated,
        )

        # ── Feedback (après validation) ───────────────────────────────────────
        if validated:
            selected_letter = user_choice[0] if user_choice else None
            bonne_txt = options.get(bonne, "")

            if selected_letter is None:
                st.markdown(
                    "<div class='fb-warn'>⚠️ Vous n'avez pas répondu à cette question.</div>",
                    unsafe_allow_html=True,
                )
            elif selected_letter == bonne:
                st.markdown(
                    "<div class='fb-ok'>✅ Correct !</div>"
                    f"<div class='fb-expl'>💡 {expl}</div>",
                    unsafe_allow_html=True,
                )
            else:
                st.markdown(
                    f"<div class='fb-ko'>❌ Faux — La bonne réponse était "
                    f"<strong>{bonne}. {bonne_txt}</strong></div>"
                    f"<div class='fb-expl'>💡 {expl}</div>",
                    unsafe_allow_html=True,
                )

        st.markdown("<hr class='s'>", unsafe_allow_html=True)

    # ── Bouton Valider ────────────────────────────────────────────────────────
    if not validated:
        col1, col2 = st.columns([3, 1])
        with col1:
            if st.button("✅ Valider mon quiz", use_container_width=True):
                st.session_state.validated = True
                st.rerun()
        with col2:
            if st.button("🔄 Nouveau", use_container_width=True):
                reset_quiz()
                st.rerun()

    # ── Score final (affiché après validation) ────────────────────────────────
    if validated:
        score = get_score(questions)
        total = len(questions)
        msg   = SCORE_MSGS.get(score, "")

        pct_color = "#34d399" if score >= 4 else "#818cf8" if score >= 2 else "#f87171"

        st.markdown(
            f"<div class='score-box'>"
            f"<div class='score-num' style='color:{pct_color};-webkit-text-fill-color:{pct_color};'>"
            f"{score}/{total}</div>"
            f"<div class='score-label'>Score final</div>"
            f"<div class='score-msg'>{msg}</div>"
            f"</div>",
            unsafe_allow_html=True,
        )

        if st.button("🔄 Générer un nouveau quiz", use_container_width=True):
            reset_quiz()
            st.rerun()

    st.markdown(
        "<div class='foot'>"
        "Quiz Master IA · Mistral AI · Gumroad Licensing"
        "</div>",
        unsafe_allow_html=True,
    )
