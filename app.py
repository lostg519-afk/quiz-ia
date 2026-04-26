"""
Quiz Master IA — main.py
requirements.txt:
    streamlit>=1.35.0
    requests>=2.31.0
"""

import json
import re
import requests
import streamlit as st

# ─────────────────────────────────────────────────────────────────────────────
# 1. CONFIG PAGE
# ─────────────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Quiz Master IA",
    page_icon="⚡",
    layout="centered",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────────────────────────────────────
# 2. CSS
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Mono:wght@400;500&display=swap');

html, body, [class*="css"] { font-family: 'Syne', sans-serif; }

.stApp {
    background: #06070c;
    background-image:
        radial-gradient(ellipse 65% 40% at 10% 0%,   rgba(120,60,255,.18) 0%, transparent 60%),
        radial-gradient(ellipse 50% 35% at 90% 100%, rgba(0,210,175,.12)  0%, transparent 60%);
    color: #d8e0f0;
}

/* Sidebar — styles purs, aucune condition de visibilité */
[data-testid="stSidebar"] {
    background: #09090f !important;
    border-right: 1px solid #1e2235 !important;
}
[data-testid="stSidebar"] > div { padding: 1.4rem 1.2rem !important; }

#MainMenu, footer, header { visibility: hidden; }
.block-container { padding-top: 1.75rem !important; max-width: 820px; }

/* ── Sidebar éléments ── */
.sb-logo  { font-size:1.05rem; font-weight:800; color:#c4b5fd; margin-bottom:.15rem; }
.sb-sep   { border:none; border-top:1px solid #1e2235; margin:.9rem 0; }
.sb-label { font-size:.7rem; color:#2e3a55; text-transform:uppercase;
            letter-spacing:.12em; font-weight:600; margin-bottom:.35rem; }
.sb-price { font-size:.9rem; color:#94a3b8; line-height:1.6; margin-bottom:.85rem; }
.sb-price strong { color:#34d399; font-size:1rem; }

a.buy-btn {
    display:block; padding:.8rem 1rem; margin-bottom:.9rem;
    background:linear-gradient(135deg,#5b3ff8,#9b6dff);
    color:#fff !important; border-radius:11px; text-decoration:none !important;
    font-weight:700; font-size:.9rem; text-align:center;
    box-shadow:0 4px 18px rgba(91,63,248,.38); transition:all .18s;
}
a.buy-btn:hover { box-shadow:0 6px 26px rgba(91,63,248,.58); transform:translateY(-1px); }

.lic-ok  { background:rgba(16,185,129,.1);  border:1px solid rgba(16,185,129,.25);
           border-radius:9px; padding:.5rem .85rem; color:#34d399;  font-size:.82rem; margin-top:.45rem; }
.lic-err { background:rgba(239,68,68,.08);  border:1px solid rgba(239,68,68,.22);
           border-radius:9px; padding:.5rem .85rem; color:#f87171;  font-size:.82rem; margin-top:.45rem; }
.lic-inf { background:rgba(91,63,248,.08);  border:1px solid rgba(91,63,248,.2);
           border-radius:9px; padding:.5rem .85rem; color:#a5b4fc;  font-size:.82rem; margin-top:.45rem; }
.cpt     { text-align:center; font-family:'DM Mono',monospace; font-size:.73rem;
           color:#252d40; margin-top:.85rem; line-height:1.7; }

/* ── Boutons sidebar ── */
[data-testid="stSidebar"] .stButton > button {
    background:linear-gradient(135deg,#1a1d2e,#22263a) !important;
    color:#a5b4fc !important; border:1px solid #2e3a5a !important;
    border-radius:9px !important; padding:.58rem 1rem !important;
    font-size:.85rem !important; font-weight:600 !important; transition:all .18s !important;
}
[data-testid="stSidebar"] .stButton > button:hover {
    border-color:#5b3ff8 !important; color:#c4b5fd !important;
}

/* ── Bouton Générer (page principale) ── */
.main-content .stButton > button,
.stButton > button {
    background:linear-gradient(135deg,#5b3ff8,#9b6dff) !important;
    color:#fff !important; border:none !important; border-radius:13px !important;
    padding:.9rem 2rem !important; font-size:1rem !important; font-weight:700 !important;
    box-shadow:0 4px 22px rgba(91,63,248,.4) !important; transition:all .2s !important;
}
.stButton > button:hover {
    transform:translateY(-2px) !important;
    box-shadow:0 8px 30px rgba(91,63,248,.58) !important;
}

/* ── Textarea ── */
.stTextArea textarea {
    background:#0c0d15 !important; border:1px solid #181c2e !important;
    border-radius:13px !important; color:#d8e0f0 !important;
    font-family:'Syne',sans-serif !important; font-size:.93rem !important;
    padding:1.05rem !important; resize:vertical;
}
.stTextArea textarea:focus {
    border-color:#818cf8 !important;
    box-shadow:0 0 0 3px rgba(129,140,248,.12) !important;
}
.stTextArea textarea::placeholder { color:#252d40 !important; }

/* ── Hero ── */
.hero { text-align:center; padding:1.1rem 0 .5rem; }
.hero h1 {
    font-size:2.8rem; font-weight:800; letter-spacing:-.04em; line-height:1.05; margin:0;
    background:linear-gradient(125deg,#c084fc 0%,#818cf8 40%,#34d399 100%);
    -webkit-background-clip:text; -webkit-text-fill-color:transparent; background-clip:text;
}
.hero .sub { font-size:.8rem; color:#2e3a55; letter-spacing:.15em;
             text-transform:uppercase; margin-top:.55rem; }

/* Badges */
.bdg { display:inline-block; font-size:.6rem; font-weight:700; letter-spacing:.12em;
       text-transform:uppercase; padding:.14rem .58rem; border-radius:999px;
       vertical-align:middle; margin-left:.4rem; font-family:'DM Mono',monospace; }
.bdg-free { background:linear-gradient(135deg,#10b981,#059669); color:#fff; }
.bdg-lock { background:linear-gradient(135deg,#ef4444,#dc2626); color:#fff; }
.bdg-vip  { background:linear-gradient(135deg,#8b5cf6,#6d28d9); color:#fff; }

/* ── Mur de paiement ── */
.paywall {
    background:rgba(239,68,68,.06); border:1.5px solid rgba(239,68,68,.2);
    border-radius:18px; padding:2.25rem 2rem; text-align:center; margin:.5rem 0 1.2rem;
}
.paywall .ico   { font-size:2.5rem; margin-bottom:.55rem; }
.paywall .title { font-size:1.05rem; font-weight:700; color:#f87171; margin-bottom:.4rem; }
.paywall .desc  { font-size:.88rem; color:#4a5a78; line-height:1.7; margin-bottom:1rem; }
.paywall .arrow { font-size:.85rem; color:#5b3ff8; font-weight:700; letter-spacing:.04em;
                  animation:blink 1.8s infinite; }
@keyframes blink { 0%,100%{opacity:1;} 50%{opacity:.3;} }

/* ── Carte question ── */
.q-wrap {
    background:#0c0d15; border:1px solid #14162a; border-radius:17px;
    padding:1.4rem 1.75rem 1.1rem; margin-bottom:.35rem;
    position:relative; overflow:hidden;
}
.q-wrap::before {
    content:''; position:absolute; top:0; left:0; width:4px; height:100%;
    background:linear-gradient(180deg,#5b3ff8,#9b6dff); border-radius:4px 0 0 4px;
}
.q-num { font-family:'DM Mono',monospace; font-size:.64rem; font-weight:500;
         color:#5b3ff8; letter-spacing:.14em; text-transform:uppercase; margin-bottom:.4rem; }
.q-txt { font-size:1rem; font-weight:700; color:#eef2ff; line-height:1.5; margin-bottom:.85rem; }

/* Radio */
.stRadio label {
    background:#0e0f18; border:1px solid #1a1d2e;
    border-radius:10px; padding:.52rem .88rem !important;
    cursor:pointer; transition:all .15s;
    font-size:.91rem !important; color:#b0bcd8 !important;
}
.stRadio label:hover { border-color:#5b3ff8; background:#131424; color:#eef2ff !important; }

/* Feedback */
.fb-ok   { background:rgba(16,185,129,.1);  border:1px solid rgba(16,185,129,.25);
           border-radius:10px; padding:.65rem 1rem; color:#34d399;
           font-size:.88rem; font-weight:600; margin-top:.55rem; }
.fb-ko   { background:rgba(239,68,68,.09);  border:1px solid rgba(239,68,68,.25);
           border-radius:10px; padding:.65rem 1rem; color:#f87171;
           font-size:.88rem; font-weight:600; margin-top:.55rem; }
.fb-skip { background:rgba(251,191,36,.08); border:1px solid rgba(251,191,36,.2);
           border-radius:10px; padding:.6rem 1rem; color:#fbbf24;
           font-size:.84rem; margin-top:.55rem; }
.fb-exp  { color:#3a4a66; font-size:.82rem; font-style:italic; margin-top:.38rem; line-height:1.5; }

/* Score */
.score-box {
    background:linear-gradient(135deg,#0f1020,#13152a);
    border:1px solid #2a2d4a; border-radius:20px;
    padding:2rem; text-align:center; margin:1.5rem 0 .5rem;
}
.score-num {
    font-size:4.5rem; font-weight:800;
    background:linear-gradient(130deg,#c084fc,#818cf8 50%,#34d399);
    -webkit-background-clip:text; -webkit-text-fill-color:transparent; background-clip:text;
    line-height:1; letter-spacing:-.04em;
}
.score-lbl { font-size:.78rem; color:#2e3a55; letter-spacing:.14em;
             text-transform:uppercase; margin-top:.4rem; }
.score-msg { font-size:.98rem; font-weight:600; color:#d8e0f0; margin-top:.75rem; }

.info-bar {
    background:rgba(129,140,248,.07); border:1px solid rgba(129,140,248,.16);
    border-radius:12px; padding:.88rem 1.1rem;
    color:#9aaaff; font-size:.86rem; margin-bottom:1.1rem; line-height:1.5;
}
hr.s { border:none; border-top:1px solid #14162a; margin:1.1rem 0; }
.foot { text-align:center; color:#1a2035; font-size:.76rem; margin-top:.7rem; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# 3. CONSTANTES
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
    "- 1 seule bonne réponse.\n"
    "- Distracteurs plausibles mais incorrects selon le texte.\n"
    "- Explication courte (1-2 phrases) justifiant la bonne réponse.\n\n"
    "Réponds UNIQUEMENT avec un JSON valide, sans texte avant ni après, sans markdown.\n"
    'Format : {"questions":[{"numero":1,"question":"...","options":{"A":"...","B":"...","C":"...","D":"..."},"bonne_reponse":"A","explication":"..."}]}'
)

SCORE_MSGS = {
    5: "🏆 Parfait ! Maîtrise totale.",
    4: "🎯 Excellent ! Très bonne compréhension.",
    3: "👍 Bien ! Quelques points à revoir.",
    2: "📖 Passable. Relisez les explications.",
    1: "💪 Courage ! Repassez le cours.",
    0: "😅 Il faut tout reprendre depuis le début !",
}

# ─────────────────────────────────────────────────────────────────────────────
# 4. SESSION STATE
# ─────────────────────────────────────────────────────────────────────────────
for k, v in {
    "nb_gen":      0,
    "unlocked":    False,
    "quiz_data":   None,
    "validated":   False,
    "lic_status":  None,
    "lic_message": "",
}.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ─────────────────────────────────────────────────────────────────────────────
# 5. HELPERS
# ─────────────────────────────────────────────────────────────────────────────
def verify_gumroad(key: str) -> tuple[bool, str]:
    try:
        r = requests.post(
            GUMROAD_API,
            data={"product_id": GUMROAD_PRODUCT, "license_key": key.strip()},
            timeout=10,
        )
        d = r.json()
        if d.get("success"):
            return True, "✅ Licence valide — Accès illimité activé !"
        return False, "❌ " + d.get("message", "Licence invalide ou déjà utilisée.")
    except requests.exceptions.Timeout:
        return False, "❌ Délai dépassé — vérifiez votre connexion."
    except Exception as e:
        return False, f"❌ Erreur réseau : {e}"


def call_mistral(api_key: str, course: str) -> dict:
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
    st.session_state.quiz_data = None
    st.session_state.validated = False
    for i in range(10):
        st.session_state.pop(f"ans_{i}", None)


def get_score(questions: list) -> int:
    return sum(
        1 for i, q in enumerate(questions)
        if (st.session_state.get(f"ans_{i}") or "")[:1] == q.get("bonne_reponse", "")
    )


# ══════════════════════════════════════════════════════════════════════════════
# 6. ████  SIDEBAR — EN PREMIER, SANS AUCUNE CONDITION  ████
#    Rendu immédiatement, avant toute logique de blocage.
#    JAMAIS de st.stop() dans ce fichier.
# ══════════════════════════════════════════════════════════════════════════════
with st.sidebar:

    # Titre
    st.markdown("<div class='sb-logo'>⚡ Quiz Master IA</div>", unsafe_allow_html=True)
    st.markdown("<hr class='sb-sep'>", unsafe_allow_html=True)

    # Titre section achat
    st.markdown("<div class='sb-label'>🔑 ACCÈS ILLIMITÉ</div>", unsafe_allow_html=True)

    # Prix
    st.markdown(
        "<div class='sb-price'>"
        "Prix : <strong>2€ seulement</strong><br>"
        "<span style='color:#3a4a66;font-size:.78rem;'>"
        "Générations illimitées, activées instantanément.</span>"
        "</div>",
        unsafe_allow_html=True,
    )

    # Bouton achat Gumroad
    st.markdown(
        f"<a href='{GUMROAD_URL}' target='_blank' class='buy-btn'>"
        "🛒 Acheter ma clé ici</a>",
        unsafe_allow_html=True,
    )

    # Champ clé de licence
    st.markdown("<div class='sb-label'>Entrer ma clé de licence</div>", unsafe_allow_html=True)

    lic_key = st.text_input(
        "licence",
        type="password",
        placeholder="XXXX-XXXX-XXXX-XXXX",
        label_visibility="collapsed",
    )

    if st.button("✔ Vérifier ma clé", use_container_width=True):
        if lic_key.strip():
            with st.spinner("Vérification en cours…"):
                ok, msg = verify_gumroad(lic_key)
            st.session_state.unlocked   = ok
            st.session_state.lic_status  = "ok" if ok else "err"
            st.session_state.lic_message = msg
            st.rerun()
        else:
            st.session_state.lic_status  = "inf"
            st.session_state.lic_message = "Collez votre clé ci-dessus."
            st.rerun()

    # Affichage statut licence (persistant entre reruns)
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

    # Séparateur + compteur
    st.markdown("<hr class='sb-sep'>", unsafe_allow_html=True)

    if st.session_state.unlocked:
        cpt = "<span style='color:#a78bfa;'>∞ Accès illimité actif</span>"
    elif st.session_state.nb_gen < FREE_LIMIT:
        cpt = f"<span style='color:#34d399;'>{FREE_LIMIT - st.session_state.nb_gen} essai gratuit restant</span>"
    else:
        cpt = "<span style='color:#ef4444;'>Essai épuisé</span>"

    st.markdown(
        f"<div class='cpt'>{cpt}</div>",
        unsafe_allow_html=True,
    )


# ══════════════════════════════════════════════════════════════════════════════
# 7. ████  PAGE PRINCIPALE — if/else, jamais st.stop()  ████
# ══════════════════════════════════════════════════════════════════════════════

# Calcul de l'état d'accès (après le rendu sidebar)
is_locked = (st.session_state.nb_gen >= FREE_LIMIT and not st.session_state.unlocked)

# ── Badge de statut dans le titre ────────────────────────────────────────────
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
# BRANCHE A : accès verrouillé → message cadenas seulement
# ─────────────────────────────────────────────────────────────────────────────
if is_locked:
    st.markdown(
        "<div class='paywall'>"
        "<div class='ico'>🔒</div>"
        "<div class='title'>Votre essai gratuit est épuisé</div>"
        "<div class='desc'>"
        "Pour continuer, obtenez votre clé d'accès pour <strong style='color:#34d399;'>2€</strong>.<br><br>"
        "① Cliquez sur <em>« Acheter ma clé ici »</em> dans la barre latérale gauche<br>"
        "② Collez la clé reçue dans le champ et cliquez sur Vérifier"
        "</div>"
        "<div class='arrow'>← La barre latérale est disponible à gauche</div>"
        "</div>",
        unsafe_allow_html=True,
    )

# ─────────────────────────────────────────────────────────────────────────────
# BRANCHE B : accès autorisé → interface complète
# ─────────────────────────────────────────────────────────────────────────────
else:

    # ── Génération du quiz ────────────────────────────────────────────────────
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
                "Collez ici votre cours, vos notes ou un résumé de chapitre…\n\n"
                "Exemple : « La photosynthèse est le processus par lequel les plantes "
                "convertissent la lumière solaire en énergie chimique… »"
            ),
            label_visibility="collapsed",
        )

        if st.button("⚡ Générer mon Quiz", use_container_width=True):
            if not course_text or len(course_text.strip()) < 60:
                st.warning("⚠️ Texte trop court — minimum 60 caractères.")
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

    # ── Affichage du quiz interactif ──────────────────────────────────────────
    if st.session_state.quiz_data:

        questions = st.session_state.quiz_data.get("questions", [])
        validated = st.session_state.validated

        st.markdown(
            f"<div style='color:#5b3ff8;font-size:.71rem;font-weight:700;"
            f"letter-spacing:.14em;text-transform:uppercase;margin-bottom:1rem;'>"
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

            # Feedback après validation
            if validated:
                raw_ans   = st.session_state.get(f"ans_{i}") or ""
                sel_ltr   = raw_ans[:1]
                bonne_txt = options.get(bonne, "")

                if not sel_ltr:
                    st.markdown(
                        "<div class='fb-skip'>⚠️ Sans réponse pour cette question.</div>",
                        unsafe_allow_html=True,
                    )
                elif sel_ltr == bonne:
                    st.markdown(
                        f"<div class='fb-ok'>✅ Correct !</div>"
                        f"<div class='fb-exp'>💡 {expl}</div>",
                        unsafe_allow_html=True,
                    )
                else:
                    st.markdown(
                        f"<div class='fb-ko'>❌ Faux — La bonne réponse était "
                        f"<strong>{bonne}. {bonne_txt}</strong></div>"
                        f"<div class='fb-exp'>💡 {expl}</div>",
                        unsafe_allow_html=True,
                    )

            st.markdown("<hr class='s'>", unsafe_allow_html=True)

        # Boutons Valider / Nouveau
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

        # Score final
        if validated:
            score = get_score(questions)
            total = len(questions)

            st.markdown(
                f"<div class='score-box'>"
                f"<div class='score-num'>{score}/{total}</div>"
                f"<div class='score-lbl'>Score final</div>"
                f"<div class='score-msg'>{SCORE_MSGS.get(score, '')}</div>"
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
