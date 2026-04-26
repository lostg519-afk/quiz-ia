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
# CONFIG PAGE
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

/* ── Fond principal ── */
.stApp {
    background: #06070c;
    background-image:
        radial-gradient(ellipse 65% 40% at 10% 0%,   rgba(120,60,255,.20) 0%, transparent 60%),
        radial-gradient(ellipse 50% 35% at 90% 100%, rgba(0,210,175,.13)  0%, transparent 60%);
    color: #d8e0f0;
}

/* ── Sidebar — TOUJOURS VISIBLE ── */
[data-testid="stSidebar"] {
    background: #09090f !important;
    border-right: 1px solid #1e2235 !important;
    min-width: 280px !important;
}
[data-testid="stSidebar"] > div { padding: 1.5rem 1.25rem !important; }
section[data-testid="stSidebar"] { display: block !important; visibility: visible !important; }

#MainMenu, footer, header { visibility: hidden; }
.block-container { padding-top: 1.75rem !important; max-width: 820px; }

/* ── Sidebar éléments ── */
.sb-title {
    font-size: 1.1rem; font-weight: 800; color: #c4b5fd;
    letter-spacing: -.01em; margin-bottom: .2rem;
}
.sb-price {
    font-size: .92rem; color: #d8e0f0; margin: .5rem 0 1rem;
    line-height: 1.5;
}
.sb-price strong { color: #34d399; font-size: 1.05rem; }
.sb-divider { border: none; border-top: 1px solid #1e2235; margin: 1.1rem 0; }

/* Bouton Gumroad dans la sidebar */
a.buy-btn {
    display: block; width: 100%; padding: .82rem 1rem;
    background: linear-gradient(135deg, #5b3ff8, #9b6dff);
    color: #fff !important; border-radius: 12px;
    font-family: 'Syne', sans-serif; font-size: .92rem; font-weight: 700;
    text-align: center; text-decoration: none !important;
    box-shadow: 0 4px 20px rgba(91,63,248,.4);
    transition: box-shadow .2s, transform .2s;
    margin-bottom: 1.1rem;
}
a.buy-btn:hover { box-shadow: 0 6px 28px rgba(91,63,248,.6); transform: translateY(-1px); }

/* Bouton vérification licence */
.stButton > button {
    width: 100%;
    background: linear-gradient(135deg, #1e2235, #252d42) !important;
    color: #a5b4fc !important; border: 1px solid #2e3a5a !important;
    border-radius: 10px !important; padding: .6rem 1rem !important;
    font-family: 'Syne', sans-serif !important; font-size: .85rem !important;
    font-weight: 600 !important; transition: all .2s !important;
}
.stButton > button:hover {
    background: linear-gradient(135deg, #252d42, #2e3a5a) !important;
    border-color: #5b3ff8 !important; color: #c4b5fd !important;
}

/* Statut licence */
.lic-ok  { background: rgba(16,185,129,.1); border: 1px solid rgba(16,185,129,.25);
           border-radius: 9px; padding: .55rem .85rem; color: #34d399;
           font-size: .82rem; font-weight: 600; margin-top: .5rem; }
.lic-err { background: rgba(239,68,68,.08); border: 1px solid rgba(239,68,68,.22);
           border-radius: 9px; padding: .55rem .85rem; color: #f87171;
           font-size: .82rem; margin-top: .5rem; }
.lic-inf { background: rgba(91,63,248,.08); border: 1px solid rgba(91,63,248,.2);
           border-radius: 9px; padding: .55rem .85rem; color: #a5b4fc;
           font-size: .82rem; margin-top: .5rem; }

/* Compteur sidebar */
.cpt-box {
    text-align: center; font-family: 'DM Mono', monospace;
    font-size: .75rem; color: #2a3248; margin-top: .9rem; line-height: 1.6;
}

/* ── Hero ── */
.hero { text-align: center; padding: 1.25rem 0 .5rem; }
.hero h1 {
    font-size: 2.85rem; font-weight: 800; letter-spacing: -.04em; line-height: 1.05; margin: 0;
    background: linear-gradient(125deg, #c084fc 0%, #818cf8 40%, #34d399 100%);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;
}
.hero .sub {
    font-size: .82rem; color: #2e3a55; letter-spacing: .15em;
    text-transform: uppercase; margin-top: .6rem; font-weight: 500;
}

/* Badges */
.bdg { display: inline-block; font-size: .6rem; font-weight: 700; letter-spacing: .12em;
       text-transform: uppercase; padding: .15rem .6rem; border-radius: 999px;
       vertical-align: middle; margin-left: .4rem; font-family: 'DM Mono', monospace; }
.bdg-free { background: linear-gradient(135deg,#10b981,#059669); color:#fff; }
.bdg-lock { background: linear-gradient(135deg,#ef4444,#dc2626); color:#fff; }
.bdg-vip  { background: linear-gradient(135deg,#8b5cf6,#6d28d9); color:#fff; }

/* ── Mur de paiement (page principale) ── */
.paywall {
    background: rgba(239,68,68,.06); border: 1.5px solid rgba(239,68,68,.22);
    border-radius: 18px; padding: 2.25rem 2rem; text-align: center; margin: .5rem 0 1.5rem;
}
.paywall .ico   { font-size: 2.6rem; margin-bottom: .6rem; }
.paywall .title { font-size: 1.1rem; font-weight: 700; color: #f87171; margin-bottom: .4rem; }
.paywall .desc  {
    font-size: .9rem; color: #4a5a78; line-height: 1.65; margin-bottom: 1.2rem;
}
.paywall .arrow {
    font-size: .85rem; color: #5b3ff8; font-weight: 600; letter-spacing: .05em;
    animation: pulse 2s infinite;
}
@keyframes pulse { 0%,100% { opacity:1; } 50% { opacity:.4; } }

/* ── Textarea ── */
.stTextArea textarea {
    background: #0c0d15 !important; border: 1px solid #181c2e !important;
    border-radius: 14px !important; color: #d8e0f0 !important;
    font-family: 'Syne', sans-serif !important; font-size: .93rem !important;
    padding: 1.1rem !important; resize: vertical;
}
.stTextArea textarea:focus {
    border-color: #818cf8 !important;
    box-shadow: 0 0 0 3px rgba(129,140,248,.12) !important;
}
.stTextArea textarea::placeholder { color: #252d40 !important; }

/* ── Bouton Générer (page principale) ── */
.gen-btn > button {
    background: linear-gradient(135deg, #5b3ff8 0%, #9b6dff 100%) !important;
    border: none !important; border-radius: 14px !important;
    padding: .95rem 2rem !important; font-size: 1rem !important; font-weight: 700 !important;
    box-shadow: 0 4px 24px rgba(91,63,248,.4) !important; transition: all .2s !important;
    color: #fff !important;
}
.gen-btn > button:hover { transform: translateY(-2px) !important;
    box-shadow: 0 8px 32px rgba(91,63,248,.58) !important; }

/* ── Radio ── */
.stRadio label {
    background: #0e0f18; border: 1px solid #1a1d2e;
    border-radius: 10px; padding: .55rem .9rem !important; cursor: pointer;
    transition: all .18s; font-size: .92rem !important; color: #b0bcd8 !important;
}
.stRadio label:hover { border-color: #5b3ff8; background: #131424; color: #eef2ff !important; }

/* ── Carte question ── */
.q-wrap {
    background: #0c0d15; border: 1px solid #14162a; border-radius: 18px;
    padding: 1.5rem 1.8rem 1.2rem; margin-bottom: .4rem;
    position: relative; overflow: hidden;
}
.q-wrap::before {
    content: ''; position: absolute; top: 0; left: 0;
    width: 4px; height: 100%;
    background: linear-gradient(180deg, #5b3ff8, #9b6dff);
    border-radius: 4px 0 0 4px;
}
.q-num { font-family: 'DM Mono', monospace; font-size: .65rem; font-weight: 500;
         color: #5b3ff8; letter-spacing: .14em; text-transform: uppercase; margin-bottom: .4rem; }
.q-txt { font-size: 1.02rem; font-weight: 700; color: #eef2ff; line-height: 1.5; margin-bottom: .9rem; }

/* ── Feedback ── */
.fb-ok  { background: rgba(16,185,129,.1); border: 1px solid rgba(16,185,129,.25);
          border-radius: 10px; padding: .7rem 1rem; color: #34d399;
          font-size: .88rem; font-weight: 600; margin-top: .6rem; }
.fb-ko  { background: rgba(239,68,68,.09); border: 1px solid rgba(239,68,68,.25);
          border-radius: 10px; padding: .7rem 1rem; color: #f87171;
          font-size: .88rem; font-weight: 600; margin-top: .6rem; }
.fb-skip{ background: rgba(251,191,36,.08); border: 1px solid rgba(251,191,36,.22);
          border-radius: 10px; padding: .65rem 1rem; color: #fbbf24;
          font-size: .85rem; margin-top: .6rem; }
.fb-expl{ color: #3a4a66; font-size: .82rem; font-style: italic; margin-top: .4rem; line-height: 1.5; }

/* ── Score final ── */
.score-box {
    background: linear-gradient(135deg, #0f1020, #13152a);
    border: 1px solid #2a2d4a; border-radius: 20px;
    padding: 2rem; text-align: center; margin: 1.5rem 0 .5rem;
}
.score-num {
    font-size: 4.5rem; font-weight: 800; letter-spacing: -.04em;
    background: linear-gradient(130deg, #c084fc, #818cf8 50%, #34d399);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;
    line-height: 1;
}
.score-label { font-size: .8rem; color: #2e3a55; margin-top: .4rem;
               letter-spacing: .12em; text-transform: uppercase; }
.score-msg   { font-size: 1rem; font-weight: 600; color: #d8e0f0; margin-top: .8rem; }

.info-bar {
    background: rgba(129,140,248,.08); border: 1px solid rgba(129,140,248,.18);
    border-radius: 13px; padding: .9rem 1.15rem;
    color: #9aaaff; font-size: .87rem; margin-bottom: 1.2rem; line-height: 1.5;
}
hr.s { border: none; border-top: 1px solid #14162a; margin: 1.2rem 0; }
.foot { text-align: center; color: #1a2035; font-size: .77rem; margin-top: .75rem; }
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

SYSTEM_PROMPT = (
    "Tu es un expert pédagogique francophone. "
    "Génère exactement 5 questions de QCM basées UNIQUEMENT sur le texte fourni. "
    "N'utilise aucune connaissance externe.\n\n"
    "Règles :\n"
    "- 4 options par question (A, B, C, D).\n"
    "- 1 seule bonne réponse par question.\n"
    "- Les distracteurs doivent être plausibles mais faux selon le texte.\n"
    "- Fournis une explication courte (1-2 phrases) justifiant la bonne réponse.\n\n"
    "Réponds UNIQUEMENT avec un JSON valide, sans texte avant ni après, sans balises markdown.\n"
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
# SESSION STATE
# ─────────────────────────────────────────────────────────────────────────────
DEFAULTS = {
    "nb_gen":      0,
    "unlocked":    False,
    "quiz_data":   None,
    "validated":   False,
    "lic_status":  None,   # None | "ok" | "err"
    "lic_message": "",
}
for k, v in DEFAULTS.items():
    if k not in st.session_state:
        st.session_state[k] = v


# ─────────────────────────────────────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────────────────────────────────────
def verify_gumroad(key: str) -> tuple[bool, str]:
    """Vérifie la clé de licence via l'API Gumroad. Retourne (ok, message)."""
    try:
        r = requests.post(
            GUMROAD_API,
            data={"product_id": GUMROAD_PRODUCT, "license_key": key.strip()},
            timeout=10,
        )
        data = r.json()
        if data.get("success"):
            return True, "✅ Licence valide — Accès illimité activé !"
        return False, "❌ " + data.get("message", "Licence invalide ou déjà utilisée.")
    except requests.exceptions.Timeout:
        return False, "❌ Délai dépassé — vérifiez votre connexion."
    except Exception as exc:
        return False, f"❌ Erreur : {exc}"


def call_mistral(api_key: str, course: str) -> dict:
    """Appelle l'API Mistral via requests et retourne le dict quiz."""
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": MODEL, "temperature": 0.35, "max_tokens": 2048,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": (
                f"Voici le texte du cours :\n\n---\n{course}\n---\n\n"
                "Génère les 5 questions en JSON."
            )},
        ],
    }
    r = requests.post(MISTRAL_API, headers=headers, json=payload, timeout=60)
    if not r.ok:
        try:    detail = r.json().get("message", r.text)
        except: detail = r.text
        raise RuntimeError(f"Erreur API Mistral [{r.status_code}] : {detail}")
    raw = r.json()["choices"][0]["message"]["content"].strip()
    raw = re.sub(r"^```(?:json)?\s*", "", raw, flags=re.IGNORECASE)
    raw = re.sub(r"\s*```\s*$", "", raw).strip()
    quiz = json.loads(raw)
    if "questions" not in quiz or not isinstance(quiz["questions"], list):
        raise ValueError("JSON invalide : clé 'questions' absente.")
    return quiz


def reset_quiz():
    st.session_state.quiz_data  = None
    st.session_state.validated  = False
    for i in range(10):
        st.session_state.pop(f"ans_{i}", None)


def get_score(questions: list) -> int:
    return sum(
        1 for i, q in enumerate(questions)
        if (st.session_state.get(f"ans_{i}") or "")[:1] == q.get("bonne_reponse", "")
    )


# ─────────────────────────────────────────────────────────────────────────────
# ███  SIDEBAR — TOUJOURS VISIBLE (rendu avant tout st.stop éventuel)  ███
# On n'utilise JAMAIS st.stop() dans ce fichier.
# ─────────────────────────────────────────────────────────────────────────────
with st.sidebar:

    # ── Titre ─────────────────────────────────────────────────────────────────
    st.markdown(
        "<div class='sb-title'>🔑 ACCÈS ILLIMITÉ</div>",
        unsafe_allow_html=True,
    )

    # ── Prix + lien achat ──────────────────────────────────────────────────────
    st.markdown(
        "<div class='sb-price'>Prix : <strong>2€ seulement</strong><br>"
        "<span style='color:#4a5a78;font-size:.8rem;'>Accès illimité à vie, "
        "activé instantanément.</span></div>",
        unsafe_allow_html=True,
    )
    st.markdown(
        f"<a href='{GUMROAD_URL}' target='_blank' class='buy-btn'>"
        "🛒 Acheter ma clé ici</a>",
        unsafe_allow_html=True,
    )

    # ── Champ licence ─────────────────────────────────────────────────────────
    st.markdown(
        "<p style='font-size:.73rem;color:#2e3a55;text-transform:uppercase;"
        "letter-spacing:.1em;font-weight:600;margin-bottom:.35rem;'>"
        "Entrer ma clé de licence</p>",
        unsafe_allow_html=True,
    )
    lic_key = st.text_input(
        "lic", type="password",
        placeholder="XXXX-XXXX-XXXX-XXXX",
        label_visibility="collapsed",
        key="lic_field",
    )

    if st.button("✔ Vérifier ma clé", use_container_width=True):
        if lic_key.strip():
            with st.spinner("Vérification…"):
                ok, msg = verify_gumroad(lic_key)
            if ok:
                st.session_state.unlocked   = True
                st.session_state.lic_status  = "ok"
            else:
                st.session_state.lic_status  = "err"
            st.session_state.lic_message = msg
            st.rerun()
        else:
            st.session_state.lic_status  = "inf"
            st.session_state.lic_message = "Collez votre clé de licence ci-dessus."
            st.rerun()

    # Affichage statut licence (persistant)
    if st.session_state.lic_status == "ok":
        st.markdown(
            f"<div class='lic-ok'>{st.session_state.lic_message}</div>",
            unsafe_allow_html=True,
        )
    elif st.session_state.lic_status == "err":
        st.markdown(
            f"<div class='lic-err'>{st.session_state.lic_message}</div>",
            unsafe_allow_html=True,
        )
    elif st.session_state.lic_status == "inf":
        st.markdown(
            f"<div class='lic-inf'>{st.session_state.lic_message}</div>",
            unsafe_allow_html=True,
        )

    # ── Séparateur + compteur ─────────────────────────────────────────────────
    st.markdown("<hr class='sb-divider'>", unsafe_allow_html=True)

    if st.session_state.unlocked:
        cpt_html = "<span style='color:#a78bfa;'>∞ Accès illimité actif</span>"
    elif st.session_state.nb_gen < FREE_LIMIT:
        left = FREE_LIMIT - st.session_state.nb_gen
        cpt_html = f"<span style='color:#34d399;'>{left} essai gratuit restant</span>"
    else:
        cpt_html = "<span style='color:#ef4444;'>Essai épuisé</span>"

    st.markdown(
        f"<div class='cpt-box'>{cpt_html}<br>"
        "<span style='color:#1e2840;'>— Quiz Master IA —</span></div>",
        unsafe_allow_html=True,
    )


# ─────────────────────────────────────────────────────────────────────────────
# EN-TÊTE PRINCIPAL
# ─────────────────────────────────────────────────────────────────────────────
is_locked = (st.session_state.nb_gen >= FREE_LIMIT and not st.session_state.unlocked)

if st.session_state.unlocked:
    badge = "<span class='bdg bdg-vip'>ILLIMITÉ</span>"
elif not is_locked:
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
# CORPS — bifurcation is_locked  (PAS de st.stop() !)
# ─────────────────────────────────────────────────────────────────────────────
if is_locked:
    # ── Mur de paiement ── page principale bloquée, sidebar libre ────────────
    st.markdown(
        "<div class='paywall'>"
        "<div class='ico'>🔒</div>"
        "<div class='title'>Votre essai gratuit est épuisé</div>"
        "<div class='desc'>"
        "Pour continuer à générer des quiz illimités,<br>"
        "obtenez votre clé d'accès pour <strong style='color:#34d399;'>2€</strong>.<br><br>"
        "👉 Cliquez sur <em>« Acheter ma clé ici »</em> dans le panneau à gauche,<br>"
        "puis collez la clé reçue dans le champ et validez."
        "</div>"
        "<div class='arrow'>← Regardez la barre latérale</div>"
        "</div>",
        unsafe_allow_html=True,
    )

else:
    # ── Interface de génération ──────────────────────────────────────────────
    if not st.session_state.quiz_data:
        st.markdown(
            "<div class='info-bar'>"
            "📋 Collez votre cours ci-dessous. Mistral AI génère "
            "<strong>5 questions interactives</strong> basées uniquement sur votre texte."
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
        st.markdown("<div class='gen-btn'>", unsafe_allow_html=True)
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
        st.markdown("</div>", unsafe_allow_html=True)

    # ── Quiz interactif ──────────────────────────────────────────────────────
    if st.session_state.quiz_data:
        questions = st.session_state.quiz_data.get("questions", [])
        validated = st.session_state.validated

        st.markdown(
            f"<div style='color:#5b3ff8;font-size:.72rem;font-weight:700;"
            f"letter-spacing:.14em;text-transform:uppercase;margin-bottom:1.1rem;'>"
            f"📊 Quiz — {len(questions)} questions</div>",
            unsafe_allow_html=True,
        )

        for i, q in enumerate(questions):
            num      = q.get("numero", i + 1)
            total    = len(questions)
            texte_q  = q.get("question", "")
            options  = q.get("options", {})
            bonne    = q.get("bonne_reponse", "")
            expl     = q.get("explication", "")
            labels   = [f"{ltr} — {txt}" for ltr, txt in options.items()]

            st.markdown(
                f"<div class='q-wrap'>"
                f"<div class='q-num'>Question {num} / {total}</div>"
                f"<div class='q-txt'>{texte_q}</div>"
                f"</div>",
                unsafe_allow_html=True,
            )

            st.radio(
                f"q{i}", options=labels, index=None,
                key=f"ans_{i}", label_visibility="collapsed",
                disabled=validated,
            )

            if validated:
                raw_ans   = st.session_state.get(f"ans_{i}") or ""
                sel_ltr   = raw_ans[:1]        # "A", "B", "C" ou "D" (ou "" si non répondu)
                bonne_txt = options.get(bonne, "")

                if not sel_ltr:
                    st.markdown(
                        "<div class='fb-skip'>⚠️ Vous n'avez pas répondu à cette question.</div>",
                        unsafe_allow_html=True,
                    )
                elif sel_ltr == bonne:
                    st.markdown(
                        f"<div class='fb-ok'>✅ Correct !</div>"
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

        # ── Boutons action ────────────────────────────────────────────────────
        if not validated:
            c1, c2 = st.columns([3, 1])
            with c1:
                if st.button("✅ Valider mon quiz", use_container_width=True):
                    st.session_state.validated = True
                    st.rerun()
            with c2:
                if st.button("🔄 Nouveau", use_container_width=True):
                    reset_quiz()
                    st.rerun()

        # ── Score final ───────────────────────────────────────────────────────
        if validated:
            score = get_score(questions)
            total = len(questions)
            msg   = SCORE_MSGS.get(score, "")

            st.markdown(
                f"<div class='score-box'>"
                f"<div class='score-num'>{score}/{total}</div>"
                f"<div class='score-label'>Score final</div>"
                f"<div class='score-msg'>{msg}</div>"
                f"</div>",
                unsafe_allow_html=True,
            )
            if st.button("🔄 Générer un nouveau quiz", use_container_width=True):
                reset_quiz()
                st.rerun()

        st.markdown(
            "<div class='foot'>Quiz Master IA · Mistral AI · Gumroad Licensing</div>",
            unsafe_allow_html=True,
        )
