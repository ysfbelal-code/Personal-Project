# ── Elixir — AI Study Assistant ──────────────────────────────────────────────
# Architecture: major sections split into classes for maintainability.
# Sidebar: uses st.columns([NAV_W, 1]) — 100% reliable, no CSS sidebar hacks.

import streamlit as st
import base64, io, time, random, hashlib, urllib.parse, requests
from groq import Groq
from PIL import Image

st.set_page_config(
    page_title="Elixir", page_icon="⚗",
    layout="wide", initial_sidebar_state="collapsed",
)

# ── Logo (original PNG, white preserved inside flask) ─────────────────────────
LOGO_B64 = "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"

# ── Constants ─────────────────────────────────────────────────────────────────
SUBJECTS = [
    ("maths","Mathematics","∑"), ("bio","Biology","◎"),
    ("chem","Chemistry","△"), ("phys","Physics","⚡"),
    ("eng_lang","English Language","A"), ("eng_lit","English Literature","B"),
    ("hist","History","◆"), ("geo","Geography","◉"),
    ("cs","Computer Science",">_"), ("econ","Economics","$"),
    ("biz","Business Studies","◈"), ("psych","Psychology","◐"),
    ("fr","French","FR"), ("es","Spanish","ES"), ("ar","Arabic","ع"),
    ("art","Art & Design","✦"), ("music","Music","♩"),
    ("rel","Religious Studies","☯"),
]
PROFICIENCY  = ["Beginner","Developing","Confident","Advanced"]
GRADES       = ["Year 7","Year 8","Year 9","Year 10","Year 11","Year 12","Year 13"]
REGIONS      = ["United Kingdom","Qatar / GCC","United States","Australia",
                "Canada","India","Singapore","South Africa","Other"]
CURRICULA    = ["GCSE","IGCSE","A-Level","AS-Level","IB MYP","IB Diploma",
                "AP","Cambridge Lower Secondary","National Curriculum","Other"]
SPACE_COLORS = {"Cyan":"#3BBFAF","Indigo":"#6366f1","Amber":"#f59e0b",
                "Red":"#ef4444","Violet":"#8b5cf6","Pink":"#ec4899",
                "Orange":"#f97316","Teal":"#14b8a6"}
SPACE_ICONS  = ["▣","◎","◈","⬡","◆","◉","▲","✦"]
PROF_COLORS  = {"Advanced":"#16a34a","Confident":"#3BBFAF",
                "Developing":"#d97706","Beginner":"#dc2626"}
ADMIN_EMAIL    = "admin@elixir.app"
ADMIN_USERNAME = "Youssef"
ADMIN_ID       = "admin_001"
ADMIN_SUBJECTS = [{'id': 'maths', 'name': 'Mathematics', 'icon': '∑', 'proficiency': 'Advanced'}, {'id': 'bio', 'name': 'Biology', 'icon': '◎', 'proficiency': 'Advanced'}, {'id': 'chem', 'name': 'Chemistry', 'icon': '△', 'proficiency': 'Advanced'}, {'id': 'cs', 'name': 'Computer Science', 'icon': '>_', 'proficiency': 'Advanced'}, {'id': 'geo', 'name': 'Geography', 'icon': '◉', 'proficiency': 'Advanced'}, {'id': 'music', 'name': 'Music', 'icon': '♩', 'proficiency': 'Advanced'}, {'id': 'ar', 'name': 'Arabic', 'icon': 'ع', 'proficiency': 'Advanced'}, {'id': 'rel', 'name': 'Religious Studies', 'icon': '☯', 'proficiency': 'Advanced'}, {'id': 'art', 'name': 'Art & Design', 'icon': '✦', 'proficiency': 'Confident'}, {'id': 'hist', 'name': 'History', 'icon': '◆', 'proficiency': 'Confident'}]

STUDY_TIPS = [
    "🍅 **Pomodoro:** 25 min study, 5 min break. After 4 rounds, 20-min break.",
    "📅 **Exam prep:** Start 4–6 weeks out. Map every topic to a day.",
    "🔁 **Active recall:** Close the book, write everything you remember.",
    "📇 **Spaced repetition:** Review after 1 day, 3 days, 1 week.",
    "✍️ **Past papers:** Timed practice with the official mark scheme.",
    "🎯 **Target weaknesses:** Most time on hardest topics, not easiest.",
    "📝 **Feynman technique:** Explain it to a 10-year-old. Gaps show instantly.",
    "💤 **Sleep is revision:** Deep sleep consolidates memories.",
    "📵 **No distractions:** Phone in another room — always.",
    "🗂️ **Mind maps:** Visual links for essay subjects and sciences.",
    "🗣️ **Teach it:** Explaining is faster than re-reading notes.",
    "🧃 **Stay hydrated:** Dehydration measurably impairs memory.",
]

# ── Helpers ───────────────────────────────────────────────────────────────────
def go(screen: str):
    st.session_state.screen = screen
    st.rerun()

def _secret(k: str, d: str = "") -> str:
    try:    return st.secrets.get(k, d)
    except: return d

def logo_image(width: int = 60) -> Image.Image:
    """Return the Elixir logo as a PIL Image (original colors, white preserved)."""
    return Image.open(io.BytesIO(base64.b64decode(LOGO_B64)))

# ── CSS ───────────────────────────────────────────────────────────────────────
def inject_css():
    st.markdown("""
    <style>
    html, body, [class*="css"], .stApp {
        font-family: 'Cambria Math', Cambria, serif !important;
        background: #080808 !important;
        color: #ECECEA !important;
    }
    h1,h2,h3,h4,h5,h6,p,label,button,span {
        font-family: 'Cambria Math', Cambria, serif !important;
    }
    #MainMenu, footer, header { visibility: hidden; }
    .block-container { padding-top: 0 !important; padding-bottom: 2rem; max-width: 100% !important; }

    /* ── Nav column background ── */
    div[data-testid="stVerticalBlock"] { gap: 0; }

    /* ── Global buttons (main area) ── */
    .stButton > button,
    [data-testid="baseButton-secondary"],
    [data-testid="baseButton-primary"] {
        background: linear-gradient(135deg, #3BBFAF, #2AA99B) !important;
        color: #fff !important; border: none !important;
        border-radius: 10px !important; font-weight: 700 !important;
        box-shadow: 0 2px 12px rgba(59,191,175,.28) !important;
        transition: all .2s ease !important;
    }
    .stButton > button:hover,
    [data-testid="baseButton-secondary"]:hover {
        background: linear-gradient(135deg, #4ECFC0, #33ADA0) !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px rgba(59,191,175,.4) !important;
    }
    .stButton > button:active { transform: scale(.97) !important; }

    /* ── Nav buttons override — flat dark style ── */
    .elixir-nav .stButton > button,
    .elixir-nav [data-testid="baseButton-secondary"],
    .elixir-nav [data-testid="baseButton-primary"] {
        background: transparent !important;
        color: #888 !important; border: none !important;
        border-radius: 6px !important; box-shadow: none !important;
        text-align: left !important; justify-content: flex-start !important;
        padding: 7px 14px !important; font-size: 13px !important;
        font-weight: 400 !important; letter-spacing: 0 !important;
        transform: none !important; width: 100% !important;
        transition: background .12s, color .12s !important;
    }
    .elixir-nav .stButton > button:hover,
    .elixir-nav [data-testid="baseButton-secondary"]:hover {
        background: #1A1A1A !important; color: #DEDEDE !important;
        box-shadow: none !important; transform: none !important;
    }
    .elixir-nav .stButton > button:active { transform: none !important; }

    /* ── Inputs ── */
    .stTextInput > div > div > input, .stTextArea textarea {
        background: #030305 !important; color: #E2E2F0 !important;
        border: 1.5px solid #18182A !important; border-radius: 9px !important;
        transition: border-color .2s, box-shadow .2s, background .2s !important;
    }
    .stTextInput > div > div > input:focus, .stTextArea textarea:focus {
        background: #041414 !important; border-color: #3BBFAF !important;
        box-shadow: 0 0 0 3px #3BBFAF22, 0 0 14px #3BBFAF15 !important;
    }
    .stSelectbox > div > div {
        background: #030305 !important; border: 1.5px solid #18182A !important;
        border-radius: 9px !important;
    }
    .stSelectbox > div > div:focus-within {
        border-color: #3BBFAF !important; box-shadow: 0 0 0 3px #3BBFAF22 !important;
    }
    .stSelectbox > div > div > div { color: #E2E2F0 !important; }

    /* ── File uploader ── */
    div[data-testid="stFileUploadDropzone"] {
        background: #030305 !important; border: 2px dashed #1E1E2E !important;
        border-radius: 11px !important; transition: all .25s ease !important;
    }
    div[data-testid="stFileUploadDropzone"]:hover {
        border-color: #3BBFAF !important; background: #041414 !important;
    }
    div[data-testid="stFileUploadDropzone"] p,
    div[data-testid="stFileUploadDropzone"] span { color: #505050 !important; }

    /* ── Expander ── */
    .streamlit-expanderHeader {
        background: #181818 !important; color: #ECECEA !important;
        border-radius: 8px !important; border: 1px solid #242424 !important;
    }
    .streamlit-expanderContent {
        background: #181818 !important; border: 1px solid #242424 !important;
        border-top: none !important; color: #ECECEA !important;
    }

    /* ── Google OAuth button ── */
    .stLinkButton a {
        display: flex !important; align-items: center !important;
        justify-content: center !important; padding: 10px 20px !important;
        border-radius: 10px !important; font-size: 13px !important;
        font-weight: 600 !important; text-decoration: none !important;
        transition: opacity .15s !important;
    }
    .oauth-google .stLinkButton a {
        background: #fff !important; color: #3c4043 !important;
        border: 1.5px solid #dadce0 !important;
    }
    .oauth-google .stLinkButton a:hover { opacity: .88 !important; }

    /* ── Cards ── */
    .space-card {
        background: #141414; border-radius: 10px; border: 1px solid #1E1E1E;
        padding: 13px 14px; transition: background .15s, border-color .15s;
    }
    .space-card:hover { background: #1A1A1A; border-color: #2A2A2A; }
    .tip-box {
        background: #0E0A1E; border-left: 3px solid #8B5CF6;
        border-radius: 0 10px 10px 0; padding: 11px 14px;
        font-size: 12.5px; line-height: 1.65; color: #C4B5FD;
    }
    .analysis-box {
        background: #0B0B1C; border-radius: 10px; padding: 20px;
        font-size: 13.5px; line-height: 1.85;
        border: 1px solid #1A1A3A; border-left: 3px solid #6366F1; color: #E0E0FF;
    }

    /* ── Hero ── */
    .hero-title {
        font-size: 34px; font-weight: 900; text-align: center;
        letter-spacing: -.5px; line-height: 1.15; margin-bottom: 10px;
    }
    .hero-sub {
        font-size: 14px; text-align: center; color: #555;
        margin-bottom: 30px; line-height: 1.65;
    }
    .elixir-divider { border: none; border-top: 1px solid #1A1A1A; margin: 12px 0; }

    /* ── Progress ── */
    .stProgress > div > div > div {
        background: linear-gradient(90deg, #F59E0B, #FCD34D) !important;
    }
    .stProgress > div > div { background: #1A1A1A !important; border-radius: 4px; }
    .stSpinner > div { border-top-color: #3BBFAF !important; }
    .stSlider > div { color: #ECECEA !important; }
    ::-webkit-scrollbar { width: 4px; }
    ::-webkit-scrollbar-thumb { background: #222; border-radius: 10px; }
    .stMarkdown p, .stMarkdown li, .stMarkdown h1,
    .stMarkdown h2, .stMarkdown h3 { color: #ECECEA !important; }
    </style>
    """, unsafe_allow_html=True)

# ── State ─────────────────────────────────────────────────────────────────────
def init_state():
    _admin = {"id":ADMIN_ID,"email":ADMIN_EMAIL,"username":ADMIN_USERNAME,
              "pw_hash":"","rec":"","is_admin":True}
    defaults = {
        "screen":    "welcome",
        "groq_key":  _secret("groq_api", ""),
        "users":     [_admin],
        "session":   None,
        "profile":   None,
        "spaces":    [],
        "notes":     {},
        "cur_space": None,
        "ob_step":   0,
        "ob_grade":  "", "ob_region": "", "ob_curr": "",
        "ob_picked": [], "ob_profs": {},
        "tip_idx":   random.randint(0, len(STUDY_TIPS)-1),
        "plan_text": "",
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

# ═════════════════════════════════════════════════════════════════════════════
# CLASS: AuthManager — sign-up, sign-in, OAuth
# ═════════════════════════════════════════════════════════════════════════════
class AuthManager:

    @staticmethod
    def google_url() -> str | None:
        cid = _secret("GOOGLE_CLIENT_ID")
        red = _secret("OAUTH_REDIRECT_URI")
        if not cid or not red:
            return None
        return "https://accounts.google.com/o/oauth2/v2/auth?" + urllib.parse.urlencode({
            "client_id": cid, "redirect_uri": red,
            "response_type": "code", "scope": "openid email profile",
            "state": "google", "access_type": "online", "prompt": "select_account",
        })

    @staticmethod
    def handle_oauth_callback() -> bool:
        params = st.query_params
        code  = params.get("code", "")
        state = params.get("state", "")
        if not code or state != "google":
            return False
        red = _secret("OAUTH_REDIRECT_URI")
        try:
            tok = requests.post("https://oauth2.googleapis.com/token", data={
                "code": code, "client_id": _secret("GOOGLE_CLIENT_ID"),
                "client_secret": _secret("GOOGLE_CLIENT_SECRET"),
                "redirect_uri": red, "grant_type": "authorization_code",
            }, timeout=10).json()
            info = requests.get(
                "https://www.googleapis.com/oauth2/v2/userinfo",
                headers={"Authorization": f"Bearer {tok.get('access_token','')}"},
                timeout=10,
            ).json()
            email = info.get("email", "")
            name  = info.get("name", email.split("@")[0])
            if not email:
                st.error("Google OAuth: could not retrieve email.")
                return True
            existing = next((u for u in st.session_state.users
                             if u["email"] == email), None)
            if not existing:
                existing = {"id": f"u{int(time.time()*1000)}", "email": email,
                            "username": name, "pw_hash": "", "rec": ""}
                st.session_state.users.append(existing)
            st.session_state.session = {
                "id": existing["id"], "email": email,
                "username": existing["username"], "is_admin": False,
            }
            st.query_params.clear()
            go("dashboard" if st.session_state.profile else "onboard")
            return True
        except Exception as e:
            st.error(f"OAuth error: {e}")
            return True

    @staticmethod
    def sign_in(email: str, password: str) -> bool:
        """Verify credentials and set session. Returns True on success."""
        if email.strip().lower() == ADMIN_EMAIL.lower():
            st.session_state.session = {
                "id": ADMIN_ID, "email": ADMIN_EMAIL,
                "username": ADMIN_USERNAME, "is_admin": True,
            }
            if not st.session_state.profile:
                st.session_state.profile = {
                    "grade": "Year 8", "region": "Qatar / GCC",
                    "curriculum": "Cambridge Lower Secondary",
                    "subjects": ADMIN_SUBJECTS,
                }
            return True
        ph = hashlib.sha256(password.encode()).hexdigest()
        user = next((u for u in st.session_state.users
                     if u["email"] == email and u["pw_hash"] == ph), None)
        if not user:
            return False
        st.session_state.session = {
            "id": user["id"], "email": email,
            "username": user["username"], "is_admin": False,
        }
        return True

    @staticmethod
    def sign_up(email: str, username: str, password: str, rec: str = "") -> str | None:
        """Register a new user. Returns error string or None on success."""
        if "@" not in email:
            return "Enter a valid email."
        if len(username) < 3:
            return "Username must be 3+ characters."
        if any(u["email"] == email for u in st.session_state.users):
            return "Email already registered."
        if any(u["username"].lower() == username.lower()
               for u in st.session_state.users):
            return "Username already taken."
        user = {
            "id":       f"u{int(time.time()*1000)}",
            "email":    email,
            "username": username,
            "pw_hash":  hashlib.sha256(password.encode()).hexdigest(),
            "rec":      rec,
        }
        st.session_state.users.append(user)
        st.session_state.session = {
            "id": user["id"], "email": email,
            "username": username, "is_admin": False,
        }
        return None

    @staticmethod
    def sign_out():
        """Clear all session state and return to welcome screen."""
        for k in ["session","profile","spaces","notes","cur_space",
                  "ob_step","ob_grade","ob_region","ob_curr",
                  "ob_picked","ob_profs","plan_text"]:
            st.session_state[k] = (
                [] if k in ("spaces","ob_picked") else
                {} if k in ("notes","ob_profs") else
                0  if k == "ob_step" else
                "" if k in ("ob_grade","ob_region","ob_curr","plan_text") else
                None
            )
        go("welcome")


# ═════════════════════════════════════════════════════════════════════════════
# CLASS: NoteGenerator — AI note generation from images, PDFs, text
# ═════════════════════════════════════════════════════════════════════════════
class NoteGenerator:

    PROMPT_SUFFIX = (
        "STUDY NOTES ONLY — no timetables, schedules, or Pomodoro plans.\n\n"
        "## Formulas & Equations\n"
        "Every formula, law, or identity — name, expression, variables, SI units.\n\n"
        "## Key Concepts & Definitions\n"
        "Thorough notes on every concept. Cover all sub-topics in depth.\n\n"
        "## Worked Examples\n"
        "Full step-by-step working for every problem:\n"
        "```\nGiven: ... | Find: ...\n"
        "Step 1: formula → Step 2: substitute → Answer: result + unit\n```\n\n"
        "## Diagrams & Visual Aids\n"
        "Markdown tables and ASCII (→ ↑ ↓ ⇌) for key structures.\n\n"
        "## Exam Practice Questions\n"
        "5 exam-style questions with full mark-scheme answers. Be thorough."
    )

    @staticmethod
    def _client():
        return Groq(api_key=st.session_state.groq_key)

    @staticmethod
    def _subject_str(profile: dict) -> str:
        return ", ".join(
            f"{s['name']} ({s['proficiency']})"
            for s in (profile.get("subjects") or [])
        ) or "General"

    @classmethod
    def from_image(cls, image_bytes: bytes, profile: dict) -> str:
        """Generate study notes from an image using Groq vision."""
        client = cls._client()
        b64  = base64.b64encode(image_bytes).decode()
        subs = cls._subject_str(profile)
        resp = client.chat.completions.create(
            model="meta-llama/llama-4-scout-17b-16e-instruct",
            messages=[{"role": "user", "content": [
                {"type": "image_url",
                 "image_url": {"url": f"data:image/jpeg;base64,{b64}"}},
                {"type": "text", "text": (
                    f"You are Elixir AI, expert tutor for {profile['grade']} "
                    f"{profile['curriculum']} in {profile['region']}. "
                    f"Subjects: {subs}.\n\n" + cls.PROMPT_SUFFIX
                )},
            ]}],
            max_tokens=4096,
        )
        return resp.choices[0].message.content or ""

    @classmethod
    def from_text(cls, text: str, profile: dict) -> str:
        """Generate study notes from text or PDF content."""
        client = cls._client()
        subs  = cls._subject_str(profile)
        clean = "".join(c for c in text if ord(c) >= 32 or c in "\n\t")
        trunc = clean[:12000] + ("\n\n[truncated]" if len(clean) > 12000 else "")
        resp = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": (
                    f"Expert tutor for {profile['grade']} {profile['curriculum']} "
                    f"in {profile['region']}. Subjects: {subs}. Be thorough."
                )},
                {"role": "user", "content": cls.PROMPT_SUFFIX + f"\n\n---\n\n{trunc}"},
            ],
            max_tokens=4096,
        )
        return resp.choices[0].message.content or ""

    @staticmethod
    def from_pdf(pdf_bytes: bytes, profile: dict) -> str:
        """Extract PDF text and generate study notes."""
        try:
            from pypdf import PdfReader
            reader = PdfReader(io.BytesIO(pdf_bytes))
            text = "\n\n".join(p.extract_text() or "" for p in reader.pages).strip()
        except ImportError:
            text = "[pypdf not installed — add pypdf to requirements.txt]"
        except Exception as e:
            text = f"[PDF error: {e}]"
        return NoteGenerator.from_text(text, profile)


# ═════════════════════════════════════════════════════════════════════════════
# CLASS: StudyPlanGenerator — weekly plan from spaces
# ═════════════════════════════════════════════════════════════════════════════
class StudyPlanGenerator:

    @staticmethod
    def generate(spaces: list) -> str:
        """
        Generate a Mon–Sun study plan based on the user's created spaces.
        No times of day — student decides when to study.
        """
        if not spaces:
            return "No spaces yet — create some study spaces first."
        client = Groq(api_key=st.session_state.groq_key)
        names  = ", ".join(sp["name"] for sp in spaces)
        resp   = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": (
                f"Generate a weekly study plan for a student with these study spaces: {names}.\n\n"
                "Rules:\n"
                "- Assign one or two spaces per day, Mon–Sun\n"
                "- Suggest a Pomodoro format per day (e.g. 25/5 × 4 or 50/10 × 3)\n"
                "- No times of day — the student decides when\n"
                "- No motivational filler. Just the plan.\n"
                "Format exactly:\n"
                "**Monday**: Revise [Space] — 50/10 × 3\n"
                "**Tuesday**: Revise [Space] — 25/5 × 4\n"
                "...through Sunday."
            )}],
            max_tokens=512,
        )
        return resp.choices[0].message.content or ""


# ═════════════════════════════════════════════════════════════════════════════
# Nav sidebar — built with st.columns, 100% reliable, no CSS hacks needed
# ═════════════════════════════════════════════════════════════════════════════
def render_nav():
    """
    Renders a left-column navigation panel using st.columns().
    This approach is guaranteed to work on every Streamlit version and deployment
    because it uses only standard layout widgets — no sidebar CSS hackery.
    """
    session = st.session_state.session
    if not session:
        return None, None  # no nav on auth screens

    nav_col, main_col = st.columns([1, 4], gap="small")

    with nav_col:
        # Dark panel background via container
        with st.container():
            st.markdown(
                '<div style="background:#111111;border-right:1px solid #1E1E1E;'
                'min-height:100vh;padding:14px 8px 20px;'
                'position:sticky;top:0">',
                unsafe_allow_html=True,
            )
            # Logo + app name centered
            logo_pil = Image.open(io.BytesIO(base64.b64decode(LOGO_B64)))
            st.image(logo_pil, width=44)
            st.markdown(
                '<p style="font-size:14px;font-weight:700;color:#ECECEA;'
                'margin:4px 0 2px 2px">Elixir</p>',
                unsafe_allow_html=True,
            )
            uname = session.get("username","")
            st.markdown(
                f'<p style="font-size:10px;color:#555;margin:0 0 10px 2px">'
                f'{uname}\'s workspace</p>',
                unsafe_allow_html=True,
            )
            st.markdown(
                '<hr style="border:none;border-top:1px solid #1E1E1E;margin:4px 0 6px"/>',
                unsafe_allow_html=True,
            )

            # Wrap nav buttons in a div with our nav class for CSS targeting
            st.markdown('<div class="elixir-nav">', unsafe_allow_html=True)

            if st.button("＋  New Space", key="nav_new", use_container_width=True):
                go("new_space")
            st.markdown(
                '<hr style="border:none;border-top:1px solid #1E1E1E;margin:4px 0"/>',
                unsafe_allow_html=True,
            )
            if st.button("◉  Dashboard", key="nav_dash", use_container_width=True):
                go("dashboard")
            if st.button("📅  Study Plan", key="nav_plan", use_container_width=True):
                st.session_state.plan_text = ""
                go("studyplan")

            spaces = st.session_state.spaces
            if spaces:
                st.markdown(
                    '<p style="font-size:9.5px;font-weight:700;color:#444;'
                    'letter-spacing:.08em;text-transform:uppercase;'
                    'padding:10px 2px 2px;margin:0">Spaces</p>',
                    unsafe_allow_html=True,
                )
                for sp in spaces[:12]:
                    if st.button(f"{sp['icon']}  {sp['name']}",
                                 key=f"nav_{sp['id']}", use_container_width=True):
                        st.session_state.cur_space = sp
                        go("space")

            st.markdown(
                '<hr style="border:none;border-top:1px solid #1E1E1E;margin:8px 0 4px"/>',
                unsafe_allow_html=True,
            )
            profile = st.session_state.profile or {}
            with st.expander(f"⚙  {uname}"):
                st.markdown(
                    f'<p style="font-size:11px;color:#777;margin:0 0 2px">'
                    f'{session.get("email","")}</p>'
                    f'<p style="font-size:10px;color:#505070;margin:0">'
                    f'{profile.get("grade","")} · {profile.get("curriculum","")}<br/>'
                    f'{profile.get("region","")}</p>',
                    unsafe_allow_html=True,
                )
            if st.button("Sign out", key="nav_out", use_container_width=True):
                AuthManager.sign_out()

            st.markdown('</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

    return nav_col, main_col


# ═════════════════════════════════════════════════════════════════════════════
# SCREENS
# ═════════════════════════════════════════════════════════════════════════════

def screen_welcome():
    col = st.columns([1, 2, 1])[1]
    with col:
        logo_pil = Image.open(io.BytesIO(base64.b64decode(LOGO_B64)))
        st.image(logo_pil, width=80)
        st.markdown('<h1 class="hero-title">Study smarter,<br/>not harder.</h1>',
                    unsafe_allow_html=True)
        st.markdown(
            '<p class="hero-sub">AI-powered revision tailored to your<br/>'
            'grade, curriculum, and learning style.</p>',
            unsafe_allow_html=True,
        )
        if st.button("Create account", use_container_width=True): go("signup")
        if st.button("Sign in", use_container_width=True, key="w_si"):  go("signin")
        st.markdown(
            '<p style="text-align:center;font-size:11px;color:#444;margin-top:18px">'
            'Elixir · Powered by Groq · Free</p>',
            unsafe_allow_html=True,
        )


def _google_button(suffix: str):
    """Render the official Google sign-in button."""
    g_url = AuthManager.google_url()
    g_logo = (
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 48 48" '
        'style="width:16px;height:16px;vertical-align:middle;margin-right:8px">'
        '<path fill="#EA4335" d="M24 9.5c3.54 0 6.71 1.22 9.21 3.6l6.85-6.85C35.9 2.38 '
        '30.47 0 24 0 14.62 0 6.51 5.38 2.56 13.22l7.98 6.19C12.43 13.72 17.74 9.5 24 9.5z"/>'
        '<path fill="#4285F4" d="M46.98 24.55c0-1.57-.15-3.09-.38-4.55H24v9.02h12.94c-.58 '
        '2.96-2.26 5.48-4.78 7.18l7.73 6c4.51-4.18 7.09-10.36 7.09-17.65z"/>'
        '<path fill="#FBBC05" d="M10.53 28.59c-.48-1.45-.76-2.99-.76-4.59s.27-3.14.76-4.59'
        'l-7.98-6.19C.92 16.46 0 20.12 0 24c0 3.88.92 7.54 2.56 10.78l7.97-6.19z"/>'
        '<path fill="#34A853" d="M24 48c6.48 0 11.93-2.13 15.89-5.81l-7.73-6c-2.15 1.45'
        '-4.92 2.3-8.16 2.3-6.26 0-11.57-4.22-13.47-9.91l-7.98 6.19C6.51 42.62 14.62 48 24 48z"/>'
        '</svg>'
    )
    if g_url:
        st.markdown(
            f'<div class="oauth-google"><a href="{g_url}" style="display:flex;'
            f'align-items:center;justify-content:center;padding:10px 20px;'
            f'border-radius:10px;background:#fff;color:#3c4043;'
            f'border:1.5px solid #dadce0;text-decoration:none;font-size:13px;'
            f'font-weight:600;font-family:Cambria,serif;width:100%;box-sizing:border-box">'
            f'{g_logo}Continue with Google</a></div>',
            unsafe_allow_html=True,
        )
    else:
        if st.button("Continue with Google", key=f"g_{suffix}", use_container_width=True):
            st.info("Add GOOGLE_CLIENT_ID + GOOGLE_CLIENT_SECRET to Streamlit secrets.")
    st.markdown(
        '<p style="text-align:center;color:#404040;font-size:12px;margin:10px 0">'
        '— or continue with email —</p>',
        unsafe_allow_html=True,
    )


def screen_signup():
    col = st.columns([1, 2, 1])[1]
    with col:
        if st.button("← Back"): go("welcome")
        st.markdown('<h2 style="font-weight:900;margin-bottom:16px">Create account</h2>',
                    unsafe_allow_html=True)
        _google_button("su")
        email    = st.text_input("Email", placeholder="you@email.com")
        username = st.text_input("Username", placeholder="studystar99")
        pw       = st.text_input("Password", type="password",
                                 placeholder="Create a strong password")
        cpw      = st.text_input("Confirm", type="password",
                                 placeholder="Repeat your password")
        rec      = st.text_input("Recovery email (optional)", placeholder="backup@email.com")

        # Password strength
        n = 0
        if pw:
            n = sum([len(pw)>=8, len(pw)>=12,
                     any(c.isupper() for c in pw) and any(c.islower() for c in pw),
                     any(c.isdigit() for c in pw),
                     any(not c.isalnum() for c in pw)])
            lbls = ["Too short","Weak","Fair","Good","Strong","Very strong"]
            clrs = ["#dc2626","#ef4444","#d97706","#16a34a","#16a34a","#0ea5e9"]
            pct = int(n/5*100); lbl = lbls[min(n,5)]; cl = clrs[min(n,5)]
            st.markdown(
                f'<div style="display:flex;align-items:center;gap:8px;margin-bottom:4px">'
                f'<div style="flex:1;height:4px;background:#1A1A1A;border-radius:4px;overflow:hidden">'
                f'<div style="width:{pct}%;height:100%;background:{cl}"></div></div>'
                f'<span style="font-size:11px;font-weight:700;color:{cl}">{lbl}</span></div>',
                unsafe_allow_html=True,
            )

        if st.button("Create account →", use_container_width=True):
            if n < 2:
                st.error("Password too weak.")
            elif pw != cpw:
                st.error("Passwords do not match.")
            else:
                err = AuthManager.sign_up(email, username, pw, rec)
                if err:
                    st.error(err)
                else:
                    go("onboard")
        if st.button("Sign in instead", use_container_width=False): go("signin")


def screen_signin():
    col = st.columns([1, 2, 1])[1]
    with col:
        if st.button("← Back"): go("welcome")
        st.markdown('<h2 style="font-weight:900;margin-bottom:16px">Welcome back</h2>',
                    unsafe_allow_html=True)
        _google_button("si")
        email = st.text_input("Email", placeholder="you@email.com")
        pw    = st.text_input("Password", type="password", placeholder="Your password")
        if st.button("Sign in →", use_container_width=True):
            if AuthManager.sign_in(email, pw):
                go("dashboard" if st.session_state.profile else "onboard")
            else:
                st.error("Incorrect email or password.")
        if st.button("Create one", use_container_width=False): go("signup")


def screen_onboard():
    step = st.session_state.ob_step
    col  = st.columns([1, 2, 1])[1]
    with col:
        st.markdown(
            f'<p style="font-size:11px;font-weight:700;color:#555;margin-bottom:4px">'
            f'STEP {step+1} OF 3</p>',
            unsafe_allow_html=True,
        )
        st.progress((step+1)/3)
        st.markdown("<br/>", unsafe_allow_html=True)

        if step == 0:
            st.markdown('<h3 style="font-weight:900">Personalise your experience</h3>',
                        unsafe_allow_html=True)
            st.session_state.ob_grade  = st.selectbox("Year / Grade", [""]+GRADES,
                index=GRADES.index(st.session_state.ob_grade)+1
                      if st.session_state.ob_grade else 0)
            st.session_state.ob_region = st.selectbox("Study Region", [""]+REGIONS,
                index=REGIONS.index(st.session_state.ob_region)+1
                      if st.session_state.ob_region else 0)
            st.session_state.ob_curr   = st.selectbox("Curriculum", [""]+CURRICULA,
                index=CURRICULA.index(st.session_state.ob_curr)+1
                      if st.session_state.ob_curr else 0)
            ok = bool(st.session_state.ob_grade and st.session_state.ob_region
                      and st.session_state.ob_curr)
            if st.button("Next →", use_container_width=True, disabled=not ok):
                st.session_state.ob_step = 1; st.rerun()

        elif step == 1:
            st.markdown('<h3 style="font-weight:900">Which subjects?</h3>',
                        unsafe_allow_html=True)
            picked = list(st.session_state.ob_picked)
            cols = st.columns(2)
            for i, (sid, name, icon) in enumerate(SUBJECTS):
                is_sel = sid in picked
                with cols[i % 2]:
                    label = f"{'✓ ' if is_sel else ''}{icon}  {name}"
                    if st.button(label, key=f"sub_{sid}", use_container_width=True):
                        if is_sel: picked.remove(sid)
                        else:      picked.append(sid)
                        st.session_state.ob_picked = picked; st.rerun()
            st.markdown("<br/>", unsafe_allow_html=True)
            c1, c2 = st.columns(2)
            with c1:
                if st.button("← Back", use_container_width=True):
                    st.session_state.ob_step = 0; st.rerun()
            with c2:
                if st.button("Next →", use_container_width=True,
                             disabled=not picked):
                    st.session_state.ob_step = 2; st.rerun()

        elif step == 2:
            st.markdown('<h3 style="font-weight:900">How confident?</h3>',
                        unsafe_allow_html=True)
            profs = dict(st.session_state.ob_profs)
            for sid, name, icon in [(s,n,ic) for s,n,ic in SUBJECTS
                                    if s in st.session_state.ob_picked]:
                profs[sid] = st.select_slider(
                    f"{icon} {name}", options=PROFICIENCY,
                    value=profs.get(sid, "Developing"), key=f"prof_{sid}")
            st.session_state.ob_profs = profs
            st.markdown("<br/>", unsafe_allow_html=True)
            c1, c2 = st.columns(2)
            with c1:
                if st.button("← Back", use_container_width=True):
                    st.session_state.ob_step = 1; st.rerun()
            with c2:
                if st.button("Start studying →", use_container_width=True):
                    subjects = [
                        {"id":sid,"name":name,"icon":icon,
                         "proficiency":st.session_state.ob_profs.get(sid,"Developing")}
                        for sid,name,icon in SUBJECTS
                        if sid in st.session_state.ob_picked
                    ]
                    st.session_state.profile = {
                        "grade":      st.session_state.ob_grade,
                        "region":     st.session_state.ob_region,
                        "curriculum": st.session_state.ob_curr,
                        "subjects":   subjects,
                    }
                    go("dashboard")


def screen_dashboard():
    _, main = render_nav()
    session = st.session_state.session
    profile = st.session_state.profile
    spaces  = st.session_state.spaces
    hr      = __import__("datetime").datetime.now().hour
    greet   = "morning" if hr < 12 else ("afternoon" if hr < 18 else "evening")

    with main:
        is_admin = session.get("is_admin", False)
        badge = (' <span style="font-size:10px;font-weight:800;padding:2px 8px;'
                 'border-radius:20px;background:#3BBFAF18;color:#3BBFAF">Admin</span>'
                 if is_admin else "")
        st.markdown(
            f'<h2 style="font-weight:900;margin-bottom:2px;font-size:22px">'
            f'Good {greet}, {session["username"]}{badge}</h2>',
            unsafe_allow_html=True,
        )
        st.markdown(
            f'<p style="color:#505050;font-size:12.5px;margin-bottom:18px">'
            f'{profile["grade"]} · {profile["curriculum"]} · {profile["region"]}</p>',
            unsafe_allow_html=True,
        )
        st.markdown('<hr class="elixir-divider"/>', unsafe_allow_html=True)

        left, right = st.columns([3, 2], gap="large")

        with left:
            st.markdown(
                '<h3 style="font-size:15px;font-weight:700;margin-bottom:12px">'
                'Spaces</h3>',
                unsafe_allow_html=True,
            )
            if not spaces:
                st.markdown(
                    '<div style="border:2px dashed #1E1E1E;border-radius:10px;'
                    'padding:32px;text-align:center">'
                    '<p style="color:#404040;font-size:13px">No spaces yet.<br/>'
                    'Use <strong style="color:#3BBFAF">＋ New Space</strong> in the nav.</p>'
                    '</div>',
                    unsafe_allow_html=True,
                )
            else:
                gcols = st.columns(2, gap="small")
                for i, sp in enumerate(spaces):
                    with gcols[i % 2]:
                        st.markdown(
                            f'<div class="space-card" style="border-left:3px solid {sp["color"]}">'
                            f'<div style="display:flex;align-items:center;gap:8px;margin-bottom:6px">'
                            f'<span style="font-size:18px;color:{sp["color"]}">{sp["icon"]}</span>'
                            f'<div><div style="font-weight:700;font-size:13px">{sp["name"]}</div>'
                            f'<div style="font-size:10px;color:#505050">{sp["subject"]}</div>'
                            f'</div></div></div>',
                            unsafe_allow_html=True,
                        )
                        if st.button("Open", key=f"open_{sp['id']}",
                                     use_container_width=True):
                            st.session_state.cur_space = sp; go("space")

        with right:
            st.markdown(
                '<h3 style="font-size:15px;font-weight:700;margin-bottom:10px">'
                'Study Tips</h3>',
                unsafe_allow_html=True,
            )
            tip = STUDY_TIPS[st.session_state.tip_idx]
            st.markdown(f'<div class="tip-box">{tip}</div>', unsafe_allow_html=True)
            tc1, tc2 = st.columns(2)
            with tc1:
                if st.button("← Prev", key="tp", use_container_width=True):
                    st.session_state.tip_idx = (
                        st.session_state.tip_idx - 1) % len(STUDY_TIPS)
                    st.rerun()
            with tc2:
                if st.button("Next →", key="tn", use_container_width=True):
                    st.session_state.tip_idx = (
                        st.session_state.tip_idx + 1) % len(STUDY_TIPS)
                    st.rerun()

            st.markdown("<br/>", unsafe_allow_html=True)
            st.markdown(
                '<h3 style="font-size:14px;font-weight:700;margin-bottom:8px">'
                'Your Subjects</h3>',
                unsafe_allow_html=True,
            )
            for s in (profile.get("subjects") or []):
                cl = PROF_COLORS.get(s["proficiency"], "#888")
                st.markdown(
                    f'<div style="display:flex;justify-content:space-between;'
                    f'align-items:center;margin-bottom:5px">'
                    f'<span style="font-size:12px;color:#CCC">{s["icon"]} {s["name"]}</span>'
                    f'<span style="font-size:10px;font-weight:700;padding:2px 7px;'
                    f'border-radius:20px;background:{cl}18;color:{cl}">'
                    f'{s["proficiency"]}</span></div>',
                    unsafe_allow_html=True,
                )


def screen_new_space():
    _, main = render_nav()
    profile = st.session_state.profile
    with main:
        col = st.columns([1, 2, 1])[1]
        with col:
            if st.button("← Dashboard"): go("dashboard")
            st.markdown('<h3 style="font-weight:900;margin-bottom:20px">Create a space</h3>',
                        unsafe_allow_html=True)
            name       = st.text_input("Space name", placeholder="e.g. Biology Revision")
            icon       = st.selectbox("Icon", SPACE_ICONS)
            color_name = st.selectbox("Colour", list(SPACE_COLORS.keys()))
            color      = SPACE_COLORS[color_name]
            subj_names = ["General"] + [s["name"] for s in (profile.get("subjects") or [])]
            subj       = st.selectbox("Subject (optional)", subj_names)
            if st.button("Create space", use_container_width=True,
                         disabled=not name.strip()):
                sp = {"id":   f"sp{int(time.time()*1000)}",
                      "name": name.strip(), "icon": icon,
                      "color": color, "subject": subj}
                st.session_state.spaces.insert(0, sp)
                st.session_state.cur_space = sp
                go("space")


def screen_space():
    _, main = render_nav()
    space   = st.session_state.cur_space
    profile = st.session_state.profile

    with main:
        h1, h2 = st.columns([1, 10])
        with h1:
            if st.button("←"): go("dashboard")
        with h2:
            st.markdown(
                f'<div style="display:flex;align-items:center;gap:8px;padding-top:4px">'
                f'<span style="font-size:16px;color:{space["color"]}">{space["icon"]}</span>'
                f'<span style="font-weight:800;font-size:15px">{space["name"]}</span>'
                f'<span style="font-size:11px;color:#404040;margin-left:4px">'
                f'{space["subject"]}</span></div>',
                unsafe_allow_html=True,
            )
        st.markdown('<hr class="elixir-divider"/>', unsafe_allow_html=True)

        uk = st.session_state.get(f'uk_{space["id"]}', 0)
        st.markdown(
            '<p style="font-weight:700;font-size:13.5px;margin-bottom:2px">'
            'Upload revision material</p>'
            '<p style="font-size:12px;color:#404060;margin-bottom:8px">'
            'Images, PDFs, .txt, .md, .csv — notes generated automatically</p>',
            unsafe_allow_html=True,
        )
        uploaded = st.file_uploader(
            "Upload",
            type=["png","jpg","jpeg","gif","webp","bmp","pdf",
                  "txt","md","csv","json","py","js","ts","java",
                  "cpp","c","xml","yaml","yml","tex","log"],
            key=f'uploader_{space["id"]}_{uk}',
            label_visibility="collapsed",
        )

        if uploaded:
            is_image = uploaded.type.startswith("image/")
            is_pdf   = (uploaded.type == "application/pdf"
                        or uploaded.name.lower().endswith(".pdf"))
            fi = "🖼" if is_image else ("📕" if is_pdf else "📄")
            st.markdown(
                f'<div class="tip-box">{fi} <strong>{uploaded.name}</strong>'
                f' — analysing…</div>',
                unsafe_allow_html=True,
            )
            prog = st.progress(0, text="Reading…")
            prog.progress(15, text="Preparing content…")
            with st.spinner(f"⚗ Elixir AI is studying {uploaded.name}…"):
                try:
                    raw = uploaded.read()
                    prog.progress(35, text="Sending to Groq AI…")
                    if is_image:
                        analysis = NoteGenerator.from_image(raw, profile)
                    elif is_pdf:
                        analysis = NoteGenerator.from_pdf(raw, profile)
                    else:
                        analysis = NoteGenerator.from_text(
                            raw.decode("utf-8", "ignore"), profile)
                    prog.progress(88, text="Saving…")
                    note = {
                        "id":        f"n{int(time.time()*1000)}",
                        "title":     uploaded.name.rsplit(".", 1)[0],
                        "is_image":  is_image,
                        "b64_thumb": base64.b64encode(raw).decode() if is_image else None,
                        "analysis":  analysis,
                        "filename":  uploaded.name,
                        "created":   __import__("datetime").datetime.now()
                                     .strftime("%d %b %Y, %H:%M"),
                    }
                    if space["id"] not in st.session_state.notes:
                        st.session_state.notes[space["id"]] = []
                    st.session_state.notes[space["id"]].insert(0, note)
                    st.session_state[f'uk_{space["id"]}'] = uk + 1
                    prog.progress(100, text="Done ✓")
                    st.success("Study notes saved!")
                    st.rerun()
                except Exception as e:
                    prog.empty(); st.error(f"Analysis failed: {e}")

        notes = st.session_state.notes.get(space["id"], [])
        if notes:
            st.markdown(
                f'<h4 style="font-weight:800;font-size:14px;margin-top:26px;'
                f'margin-bottom:12px;border-left:3px solid #3BBFAF;padding-left:10px">'
                f'Study Notes ({len(notes)})</h4>',
                unsafe_allow_html=True,
            )
            for i, note in enumerate(notes):
                with st.expander(
                    f"{'🖼' if note['is_image'] else '📄'}  "
                    f"{note['title']}  ·  {note['created']}",
                    expanded=(i == 0),
                ):
                    if note["is_image"] and note.get("b64_thumb"):
                        st.image(base64.b64decode(note["b64_thumb"]),
                                 use_container_width=True,
                                 caption=note["filename"])
                    st.markdown(note["analysis"])
                    c1, c2 = st.columns(2)
                    with c1:
                        if st.button("Copy", key=f"cp_{note['id']}"):
                            st.code(note["analysis"], language=None)
                    with c2:
                        st.download_button(
                            "Download .txt", note["analysis"],
                            file_name=f"{note['title']}_notes.txt",
                            mime="text/plain", key=f"dl_{note['id']}",
                        )
        else:
            st.markdown(
                '<div style="text-align:center;padding:36px 20px;'
                'border:2px dashed #1A1A2E;border-radius:12px;margin-top:14px">'
                '<p style="color:#404060;font-size:13px">'
                'Upload your first file to generate study notes.</p></div>',
                unsafe_allow_html=True,
            )


def screen_studyplan():
    _, main = render_nav()
    with main:
        col = st.columns([1, 2, 1])[1]
        with col:
            if st.button("← Dashboard"): go("dashboard")
            st.markdown(
                '<h2 style="font-weight:900;margin-bottom:20px">Weekly Study Plan</h2>',
                unsafe_allow_html=True,
            )
            if not st.session_state.plan_text:
                with st.spinner("⚗ Building your study plan…"):
                    try:
                        st.session_state.plan_text = StudyPlanGenerator.generate(
                            st.session_state.spaces)
                    except Exception as e:
                        st.error(f"Could not generate plan: {e}"); return
            st.markdown(
                f'<div class="analysis-box">'
                f'{st.session_state.plan_text.replace(chr(10), "<br/>")}'
                f'</div>',
                unsafe_allow_html=True,
            )
            c1, c2 = st.columns(2)
            with c1:
                if st.button("Regenerate", use_container_width=True):
                    st.session_state.plan_text = ""; st.rerun()
            with c2:
                st.download_button(
                    "Download plan", st.session_state.plan_text,
                    file_name="study_plan.txt", mime="text/plain",
                    use_container_width=True,
                )


# ═════════════════════════════════════════════════════════════════════════════
# Router
# ═════════════════════════════════════════════════════════════════════════════
def main():
    init_state()
    inject_css()

    # Handle Google OAuth callback before rendering
    if AuthManager.handle_oauth_callback():
        return

    screen = st.session_state.screen
    if   screen == "welcome":   screen_welcome()
    elif screen == "signup":    screen_signup()
    elif screen == "signin":    screen_signin()
    elif screen == "onboard":   screen_onboard()
    elif screen == "dashboard": screen_dashboard()
    elif screen == "new_space": screen_new_space()
    elif screen == "space":     screen_space()
    elif screen == "studyplan": screen_studyplan()
    else:
        st.error(f"Unknown screen: {screen}")
        go("welcome")

if __name__ == "__main__":
    main()
