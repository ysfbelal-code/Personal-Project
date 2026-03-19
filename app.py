# ── Elixir — AI Study Assistant ─────────────────────────────────────────────
import streamlit as st
import base64, io, time, random, json, urllib.parse, hashlib, requests
from groq import Groq
from PIL import Image
import numpy as np

st.set_page_config(
    page_title="Elixir", page_icon="⚗",
    layout="wide", initial_sidebar_state="expanded",
)

LOGO_B64 = "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"

# ─────────────────────────────────────────────────────────────────────────────
SUBJECTS = [
    ("maths","Mathematics","∑"),("bio","Biology","◎"),
    ("chem","Chemistry","△"),("phys","Physics","⚡"),
    ("eng_lang","English Language","A"),("eng_lit","English Literature","B"),
    ("hist","History","◆"),("geo","Geography","◉"),
    ("cs","Computer Science",">_"),("econ","Economics","$"),
    ("biz","Business Studies","◈"),("psych","Psychology","◐"),
    ("fr","French","FR"),("es","Spanish","ES"),("ar","Arabic","ع"),
    ("art","Art & Design","✦"),("music","Music","♩"),
    ("rel","Religious Studies","☯"),
]
PROFICIENCY = ["Beginner","Developing","Confident","Advanced"]
GRADES      = ["Year 7","Year 8","Year 9","Year 10","Year 11","Year 12","Year 13"]
REGIONS     = ["United Kingdom","Qatar / GCC","United States","Australia",
               "Canada","India","Singapore","South Africa","Other"]
CURRICULA   = ["GCSE","IGCSE","A-Level","AS-Level","IB MYP","IB Diploma",
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
    "🍅 **Pomodoro method:** 25 min study, 5 min break. After 4 rounds take a 20-min break.",
    "📅 **Exam prep:** Start 4–6 weeks out. Map every topic to a specific day.",
    "🔁 **Active recall:** Close the book and write everything you remember — the #1 technique.",
    "📇 **Spaced repetition:** Review after 1 day, 3 days, 1 week. Locks content long-term.",
    "✍️ **Past papers:** Practise under timed conditions with the official mark scheme.",
    "🎯 **Target weaknesses:** Most time on the hardest topics, not the ones you enjoy.",
    "📝 **Feynman technique:** Explain it to a 10-year-old. Gaps become obvious instantly.",
    "💤 **Sleep is revision:** Deep sleep consolidates memories — avoid all-nighters.",
    "📵 **Remove distractions:** Phone in another room. Face-down on the desk still hurts focus.",
    "🗂️ **Mind maps:** Visual connections — especially useful for essay subjects and sciences.",
    "🗣️ **Teach it:** Explaining to a classmate is faster than re-reading notes.",
    "🧃 **Stay hydrated:** Mild dehydration measurably impairs memory and concentration.",
]

# ── PDF ───────────────────────────────────────────────────────────────────────
def extract_pdf_text(pdf_bytes: bytes) -> str:
    try:
        from pypdf import PdfReader
        reader = PdfReader(io.BytesIO(pdf_bytes))
        return "\n\n".join(p.extract_text() or "" for p in reader.pages).strip()
    except ImportError:
        return "[pypdf not installed — add pypdf to requirements.txt]"
    except Exception as e:
        return f"[PDF error: {e}]"

# ── OAuth ─────────────────────────────────────────────────────────────────────
def _secret(k, d=""):
    try:    return st.secrets.get(k, d)
    except: return d

def google_oauth_url():
    cid = _secret("GOOGLE_CLIENT_ID")
    red = _secret("OAUTH_REDIRECT_URI")
    if not cid or not red: return None
    return "https://accounts.google.com/o/oauth2/v2/auth?" + urllib.parse.urlencode({
        "client_id":cid,"redirect_uri":red,"response_type":"code",
        "scope":"openid email profile","state":"google",
        "access_type":"online","prompt":"select_account"})



def handle_oauth_callback():
    params = st.query_params
    code  = params.get("code","")
    state = params.get("state","")
    if not code or state != "google": return False
    red = _secret("OAUTH_REDIRECT_URI")
    try:
        tok  = requests.post("https://oauth2.googleapis.com/token",data={
            "code":code,"client_id":_secret("GOOGLE_CLIENT_ID"),
            "client_secret":_secret("GOOGLE_CLIENT_SECRET"),
            "redirect_uri":red,"grant_type":"authorization_code"},timeout=10).json()
        info = requests.get("https://www.googleapis.com/oauth2/v2/userinfo",
            headers={"Authorization":f"Bearer {tok.get('access_token','')}"},timeout=10).json()
        email = info.get("email",""); name = info.get("name",email.split("@")[0])
        if not email: st.error("OAuth: could not retrieve email."); return True
        existing = next((u for u in st.session_state.users if u["email"]==email),None)
        if not existing:
            existing = {"id":f"u{int(time.time()*1000)}","email":email,
                        "username":name,"pw_hash":"","rec":""}
            st.session_state.users.append(existing)
        st.session_state.session = {"id":existing["id"],"email":email,
                                    "username":existing["username"],"is_admin":False}
        st.query_params.clear()
        go("dashboard" if st.session_state.profile else "onboard")
        return True
    except Exception as e:
        st.error(f"OAuth error: {e}"); return True

# ── CSS ───────────────────────────────────────────────────────────────────────
def inject_css():
    st.markdown("""
    <style>
    html,body,[class*="css"],.stApp{
        font-family:'Cambria Math',Cambria,serif !important;
        background:#080808 !important; color:#ECECEA !important;
    }
    h1,h2,h3,h4,h5,h6,p,label,button,span{
        font-family:'Cambria Math',Cambria,serif !important;
    }
    #MainMenu,footer,header{visibility:hidden;}
    .block-container{padding-top:1.5rem;padding-bottom:2rem;max-width:980px;}

    /* ── GLOBAL main-area buttons — cyan gradient ─────────────────────────── */
    .stButton > button{
        background:linear-gradient(135deg,#3BBFAF,#2AA99B) !important;
        color:#fff !important; border:none !important; border-radius:10px !important;
        font-weight:700 !important; letter-spacing:.3px !important;
        box-shadow:0 2px 12px rgba(59,191,175,.28) !important;
        transition:all .2s ease !important;
    }
    .stButton > button:hover{
        background:linear-gradient(135deg,#4ECFC0,#33ADA0) !important;
        transform:translateY(-2px) !important;
        box-shadow:0 6px 20px rgba(59,191,175,.4) !important;
    }
    .stButton > button:active{ transform:scale(.97) !important; }

    /* ── SIDEBAR background & width ──────────────────────────────────────── */
    section[data-testid="stSidebar"]{
        background:#111111 !important;
        border-right:1px solid #1E1E1E !important;
        min-width:230px !important; max-width:230px !important;
    }
    /* NOTE: do NOT zero-out padding on the inner div — hides widgets */

    /* ── SIDEBAR buttons: flat Notion-style ────────────────────────────────
       Target both the legacy .stButton selector AND the modern
       data-testid="baseButton-secondary" that Streamlit 1.35+ uses.        */
    section[data-testid="stSidebar"] .stButton > button,
    section[data-testid="stSidebar"] [data-testid="baseButton-secondary"],
    section[data-testid="stSidebar"] [data-testid="baseButton-primary"]{
        background:transparent !important;
        color:#999999 !important;
        border:none !important;
        border-radius:6px !important;
        box-shadow:none !important;
        text-align:left !important;
        justify-content:flex-start !important;
        padding:6px 12px !important;
        font-size:13px !important;
        font-weight:400 !important;
        letter-spacing:0 !important;
        transform:none !important;
        width:100% !important;
        transition:background .12s, color .12s !important;
    }
    section[data-testid="stSidebar"] .stButton > button:hover,
    section[data-testid="stSidebar"] [data-testid="baseButton-secondary"]:hover,
    section[data-testid="stSidebar"] [data-testid="baseButton-primary"]:hover{
        background:#1E1E1E !important;
        color:#E0E0E0 !important;
        box-shadow:none !important;
        transform:none !important;
    }
    section[data-testid="stSidebar"] .stButton > button:active,
    section[data-testid="stSidebar"] [data-testid="baseButton-secondary"]:active{
        background:#252525 !important;
        transform:none !important;
    }

    /* ── Inputs ── */
    .stTextInput > div > div > input, .stTextArea textarea{
        background:#030305 !important; color:#E2E2F0 !important;
        border:1.5px solid #18182A !important; border-radius:9px !important;
        transition:border-color .2s, box-shadow .2s, background .2s !important;
    }
    .stTextInput > div > div > input:focus, .stTextArea textarea:focus{
        background:#041414 !important; border-color:#3BBFAF !important;
        box-shadow:0 0 0 3px #3BBFAF22, 0 0 14px #3BBFAF15 !important;
    }
    .stSelectbox > div > div{
        background:#030305 !important; border:1.5px solid #18182A !important;
        border-radius:9px !important;
    }
    .stSelectbox > div > div:focus-within{
        border-color:#3BBFAF !important; box-shadow:0 0 0 3px #3BBFAF22 !important;
    }
    .stSelectbox > div > div > div{ color:#E2E2F0 !important; }

    /* ── File uploader ── */
    div[data-testid="stFileUploadDropzone"]{
        background:#030305 !important; border:2px dashed #1E1E2E !important;
        border-radius:11px !important; transition:all .25s ease !important;
    }
    div[data-testid="stFileUploadDropzone"]:hover{
        border-color:#3BBFAF !important; background:#041414 !important;
    }
    div[data-testid="stFileUploadDropzone"] p,
    div[data-testid="stFileUploadDropzone"] span{ color:#505050 !important; }

    /* ── Expander ── */
    .streamlit-expanderHeader{
        background:#181818 !important; color:#ECECEA !important;
        border-radius:8px !important; border:1px solid #242424 !important;
    }
    .streamlit-expanderContent{
        background:#181818 !important; border:1px solid #242424 !important;
        border-top:none !important; color:#ECECEA !important;
    }
    /* Sidebar expander flat */
    section[data-testid="stSidebar"] .streamlit-expanderHeader{
        background:transparent !important; border:none !important;
        color:#888 !important; border-radius:6px !important;
        padding:6px 12px !important; font-size:12px !important;
    }
    section[data-testid="stSidebar"] .streamlit-expanderHeader:hover{
        background:#1E1E1E !important; color:#CCC !important;
    }
    section[data-testid="stSidebar"] .streamlit-expanderContent{
        background:transparent !important; border:none !important;
        padding:0 4px !important;
    }

    /* ── OAuth link buttons ── */
    .stLinkButton a{
        display:flex !important; align-items:center !important;
        justify-content:center !important;
        padding:9px 16px !important; border-radius:10px !important;
        font-size:13px !important; font-weight:600 !important;
        text-decoration:none !important;
        font-family:'Cambria Math',Cambria,serif !important;
        transition:opacity .15s !important;
    }
    .stLinkButton a:hover{ opacity:.85 !important; }
    .oauth-google .stLinkButton a{
        background:#ffffff !important; color:#1a1a1a !important;
        border:1.5px solid #2a2a2a !important;
    }


    /* ── Cards ── */
    .space-card{
        background:#141414; border-radius:10px; border:1px solid #1E1E1E;
        padding:13px 14px; cursor:pointer;
        transition:background .15s, border-color .15s;
    }
    .space-card:hover{ background:#1A1A1A; border-color:#2A2A2A; }
    .tip-box{
        background:#0E0A1E; border-left:3px solid #8B5CF6;
        border-radius:0 10px 10px 0; padding:11px 14px;
        font-size:12.5px; line-height:1.65; color:#C4B5FD;
    }
    .analysis-box{
        background:#0B0B1C; border-radius:10px; padding:20px;
        font-size:13.5px; line-height:1.85; border:1px solid #1A1A3A;
        border-left:3px solid #6366F1; color:#E0E0FF;
    }

    /* ── Hero ── */
    .hero-title{font-size:34px;font-weight:900;text-align:center;
        letter-spacing:-.5px;line-height:1.15;margin-bottom:10px;}
    .hero-sub{font-size:14px;text-align:center;color:#555;
        margin-bottom:30px;line-height:1.65;}
    .logo-center{display:flex;justify-content:center;margin-bottom:16px;}
    .elixir-divider{border:none;border-top:1px solid #1A1A1A;margin:12px 0;}

    /* ── Progress / misc ── */
    .stProgress > div > div > div{background:linear-gradient(90deg,#F59E0B,#FCD34D) !important;}
    .stProgress > div > div{background:#1A1A1A !important;border-radius:4px;}
    .stSpinner > div{border-top-color:#3BBFAF !important;}
    .stSlider > div{color:#ECECEA !important;}
    ::-webkit-scrollbar{width:4px;}
    ::-webkit-scrollbar-thumb{background:#222;border-radius:10px;}
    .stMarkdown p,.stMarkdown li,.stMarkdown h1,
    .stMarkdown h2,.stMarkdown h3{color:#ECECEA !important;}
    </style>
    """, unsafe_allow_html=True)

# ── State ─────────────────────────────────────────────────────────────────────
def init_state():
    _admin = {"id":ADMIN_ID,"email":ADMIN_EMAIL,"username":ADMIN_USERNAME,
              "pw_hash":"","rec":"","is_admin":True}
    defaults = {
        "screen":"welcome","groq_key":_secret("groq_api",""),"users":[_admin],
        "session":None,"profile":None,"spaces":[],"notes":{},
        "cur_space":None,"ob_step":0,"ob_grade":"","ob_region":"",
        "ob_curr":"","ob_picked":[],"ob_profs":{},
        "tip_idx":random.randint(0,len(STUDY_TIPS)-1),"plan_text":"",
    }
    for k,v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

def go(screen):
    st.session_state.screen = screen
    st.rerun()

def get_groq():
    return Groq(api_key=st.session_state.groq_key)

def subStr(profile):
    return ", ".join(f"{s['name']} ({s['proficiency']})"
                     for s in (profile.get("subjects") or [])) or "General"

# ── Sidebar ───────────────────────────────────────────────────────────────────
def render_sidebar():
    """
    Notion-style sidebar using only native Streamlit widgets.
    st.image() is used for the logo — the ONLY reliable method on Streamlit Cloud.
    st.markdown <img> data-URIs are blocked by Streamlit's CSP and must never be used.
    """
    if not st.session_state.session:
        return

    session = st.session_state.session
    profile = st.session_state.profile or {}
    spaces  = st.session_state.spaces

    with st.sidebar:
        # ── Logo + workspace name ─────────────────────────────────────────
        # Use PIL Image object — most reliable input type for st.image().
        # Never use st.columns() in the sidebar for the logo: unreliable.
        uname = session.get("username", "")
        logo_pil = Image.open(io.BytesIO(base64.b64decode(LOGO_B64)))
        st.image(logo_pil, width=48)
        st.markdown(
            f'<div style="margin:-8px 0 4px 4px">'            f'<span style="font-size:13px;font-weight:700;color:#ECECEA">Elixir</span>'            f'<span style="font-size:10px;color:#555;margin-left:6px">{uname}\'s workspace</span>'            f'</div>',
            unsafe_allow_html=True,
        )

        st.markdown('<hr style="border:none;border-top:1px solid #1E1E1E;margin:8px 0 4px"/>',
                    unsafe_allow_html=True)

        # ── New Space ─────────────────────────────────────────────────────
        if st.button("＋  New Space", key="sb_new", use_container_width=True):
            go("new_space")

        st.markdown('<hr style="border:none;border-top:1px solid #1E1E1E;margin:4px 0"/>',
                    unsafe_allow_html=True)

        # ── Navigation ───────────────────────────────────────────────────
        if st.button("◉  Dashboard", key="sb_dashboard", use_container_width=True):
            go("dashboard")
        if st.button("📅  Study Plan", key="sb_studyplan", use_container_width=True):
            st.session_state.plan_text = ""
            go("studyplan")

        # ── Spaces list ───────────────────────────────────────────────────
        if spaces:
            st.markdown(
                '<p style="font-size:10px;font-weight:700;color:#444;'                'letter-spacing:.08em;text-transform:uppercase;'                'padding:10px 0 2px;margin:0">Spaces</p>',
                unsafe_allow_html=True,
            )
            for sp in spaces[:12]:
                if st.button(f"{sp['icon']}  {sp['name']}",
                             key=f"sb_{sp['id']}", use_container_width=True):
                    st.session_state.cur_space = sp
                    go("space")

        st.markdown('<hr style="border:none;border-top:1px solid #1E1E1E;margin:8px 0"/>',
                    unsafe_allow_html=True)

        # ── Account info ──────────────────────────────────────────────────
        with st.expander(f"⚙  {session['username']}"):
            st.markdown(
                f'<p style="margin:0 0 2px;font-size:12px;color:#888">{session["email"]}</p>'                f'<p style="font-size:11px;color:#505070;margin:0">'                f'{profile.get("grade","")} · {profile.get("curriculum","")}<br/>'                f'{profile.get("region","")}</p>',
                unsafe_allow_html=True,
            )

        # ── Sign out ──────────────────────────────────────────────────────
        if st.button("Sign out", key="sb_out", use_container_width=True):
            for k in ["session","profile","spaces","notes","cur_space",
                      "ob_step","ob_grade","ob_region","ob_curr",
                      "ob_picked","ob_profs","plan_text"]:
                st.session_state[k] = (
                    [] if k in ("spaces","ob_picked") else
                    {} if k in ("notes","ob_profs") else
                    0  if k=="ob_step" else
                    "" if k in ("ob_grade","ob_region","ob_curr","plan_text") else
                    None)
            go("welcome")

# ── Google sign-in (official Google G logo, no emojis) ───────────────────────
def _oauth_buttons(suffix=""):
    """
    Single Google sign-in button using the official Google G SVG logo.
    Email login remains as fallback below.
    """
    g_url = google_oauth_url()

    # Official Google G logo as inline SVG
    g_logo = (
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 48 48" '
        'style="width:18px;height:18px;vertical-align:middle;margin-right:8px">'
        '<path fill="#EA4335" d="M24 9.5c3.54 0 6.71 1.22 9.21 3.6l6.85-6.85'
        'C35.9 2.38 30.47 0 24 0 14.62 0 6.51 5.38 2.56 13.22l7.98 6.19'
        'C12.43 13.72 17.74 9.5 24 9.5z"/>'
        '<path fill="#4285F4" d="M46.98 24.55c0-1.57-.15-3.09-.38-4.55H24v9.02'
        'h12.94c-.58 2.96-2.26 5.48-4.78 7.18l7.73 6c4.51-4.18 7.09-10.36'
        ' 7.09-17.65z"/>'
        '<path fill="#FBBC05" d="M10.53 28.59c-.48-1.45-.76-2.99-.76-4.59'
        's.27-3.14.76-4.59l-7.98-6.19C.92 16.46 0 20.12 0 24c0 3.88.92 7.54'
        ' 2.56 10.78l7.97-6.19z"/>'
        '<path fill="#34A853" d="M24 48c6.48 0 11.93-2.13 15.89-5.81l-7.73-6'
        'c-2.15 1.45-4.92 2.3-8.16 2.3-6.26 0-11.57-4.22-13.47-9.91l-7.98'
        ' 6.19C6.51 42.62 14.62 48 24 48z"/>'
        '<path fill="none" d="M0 0h48v48H0z"/></svg>'
    )

    btn_style = (
        "display:flex;align-items:center;justify-content:center;"
        "padding:10px 20px;border-radius:10px;"
        "background:#ffffff;color:#3c4043;"
        "border:1.5px solid #dadce0;"
        "text-decoration:none;font-size:14px;font-weight:600;"
        "font-family:'Cambria Math',Cambria,serif;"
        "width:100%;box-sizing:border-box;"
        "transition:box-shadow .15s;"
    )

    if g_url:
        st.markdown(
            f'<a href="{g_url}" style="{btn_style}" '
            f'onmouseover="this.style.boxShadow=\'0 2px 8px rgba(0,0,0,.25)\'" '
            f'onmouseout="this.style.boxShadow=\'none\'">'
            f'{g_logo}Continue with Google</a>',
            unsafe_allow_html=True,
        )
    else:
        # Secrets not configured — still show a proper-looking button
        if st.button("Continue with Google", key=f"g_{suffix}", use_container_width=True):
            st.info(
                "To enable Google login, add GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET, "
                "and OAUTH_REDIRECT_URI to your Streamlit secrets."
            )

    st.markdown(
        '<p style="text-align:center;color:#404040;font-size:12px;margin:10px 0">'
        '— or continue with email —</p>', unsafe_allow_html=True)


# ── AI ────────────────────────────────────────────────────────────────────────
def ai_analyze_image(image_bytes, profile):
    client = get_groq()
    b64  = base64.b64encode(image_bytes).decode()
    subs = subStr(profile)
    resp = client.chat.completions.create(
        model="meta-llama/llama-4-scout-17b-16e-instruct",
        messages=[{"role":"user","content":[
            {"type":"image_url","image_url":{"url":f"data:image/jpeg;base64,{b64}"}},
            {"type":"text","text":(
                f"You are Elixir AI, expert tutor for {profile['grade']} "
                f"{profile['curriculum']} students in {profile['region']}. "
                f"Subjects: {subs}.\n\n"
                "STUDY NOTES ONLY — no timetables, no schedules.\n\n"
                "## Formulas & Equations\n"
                "Every formula, law or identity visible — name, expression, variables, SI units.\n\n"
                "## Key Concepts & Definitions\n"
                "Thorough notes on every concept shown. Cover all sub-topics in depth.\n\n"
                "## Worked Examples\n"
                "Full working for every question/calculation:\n"
                "```\nGiven: ...\nFind: ...\nStep 1: ...\nAnswer: value + unit\n```\n\n"
                "## Diagrams & Visual Aids\n"
                "Markdown tables and ASCII art (→ ↑ ↓ ⇌) for key diagrams.\n\n"
                "## Exam Practice Questions\n"
                "5 exam-style questions with detailed mark-scheme answers. Be thorough."
            )},
        ]}],
        max_tokens=4096,
    )
    return resp.choices[0].message.content or ""

def ai_analyze_text(text, profile):
    client = get_groq()
    subs  = subStr(profile)
    clean = "".join(c for c in text if ord(c)>=32 or c in "\n\t")
    trunc = clean[:12000] + ("\n\n[truncated]" if len(clean)>12000 else "")
    resp = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role":"system","content":(
                f"Expert tutor for {profile['grade']} {profile['curriculum']} "
                f"in {profile['region']}. Subjects: {subs}. Be thorough."
            )},
            {"role":"user","content":(
                "STUDY NOTES ONLY — no timetables, no schedules.\n\n"
                "## Formulas & Equations\n"
                "Every formula, law or identity — name, expression, variables, SI units.\n\n"
                "## Key Concepts & Definitions\n"
                "Thorough notes on every concept. All sub-topics in depth.\n\n"
                "## Worked Examples\n"
                "Full step-by-step working for every problem type:\n"
                "```\nGiven: ... | Find: ...\n"
                "Step 1: formula → Step 2: substitute → Answer: result + unit\n```\n\n"
                "## Diagrams & Visual Aids\n"
                "Markdown tables and ASCII for key structures.\n\n"
                "## Exam Practice Questions\n"
                "5 questions with full mark-scheme answers. Be thorough.\n\n"
                f"---\n\n{trunc}"
            )},
        ],
        max_tokens=4096,
    )
    return resp.choices[0].message.content or ""

def ai_study_plan(spaces):
    client = get_groq()
    if not spaces: return "No spaces yet. Create some first."
    names = ", ".join(sp["name"] for sp in spaces)
    resp = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role":"user","content":(
            f"Weekly study plan for spaces: {names}.\n"
            "- One or two spaces per day (Mon–Sun)\n"
            "- Suggest Pomodoro format per day (e.g. 25/5 × 4 or 50/10 × 3)\n"
            "- No times of day. No filler.\n"
            "Format: **Monday**: Revise [Space] — 50/10 × 3\n...through Sunday."
        )}],
        max_tokens=512,
    )
    return resp.choices[0].message.content or ""

# ── Screens ───────────────────────────────────────────────────────────────────
def screen_apikey():
    col = st.columns([1,2,1])[1]
    with col:
        _logo = Image.open(io.BytesIO(base64.b64decode(LOGO_B64)))
        st.image(_logo, width=72)
        st.markdown('<h2 style="text-align:center;font-weight:900;margin-bottom:6px">Connect Groq API</h2>', unsafe_allow_html=True)
        st.markdown('<p style="text-align:center;color:#555;font-size:13px;margin-bottom:6px">Elixir uses the Groq free tier — no credit card needed.</p>', unsafe_allow_html=True)
        st.markdown('<p style="text-align:center;font-size:12px;color:#444;margin-bottom:20px">Get a free key at <a href="https://console.groq.com" target="_blank" style="color:#3BBFAF;font-weight:700">console.groq.com</a> → API Keys</p>', unsafe_allow_html=True)
        key = st.text_input("Key","",type="password",placeholder="gsk_...",label_visibility="collapsed")
        if st.button("Continue →", use_container_width=True):
            if not key.strip().startswith("gsk_"):
                st.error("Groq keys start with gsk_")
            else:
                try:
                    c = Groq(api_key=key.strip())
                    c.chat.completions.create(model="llama-3.3-70b-versatile",
                        messages=[{"role":"user","content":"hi"}],max_tokens=1)
                    st.session_state.groq_key = key.strip()
                    go("welcome")
                except Exception as e: st.error(f"Could not connect: {e}")
        st.markdown('<p style="text-align:center;font-size:11px;color:#444;margin-top:10px">Stored for this session only.</p>', unsafe_allow_html=True)

def screen_welcome():
    col = st.columns([1,2,1])[1]
    with col:
        _logo = Image.open(io.BytesIO(base64.b64decode(LOGO_B64)))
        st.image(_logo, width=84)
        st.markdown('<h1 class="hero-title">Study smarter,<br/>not harder.</h1>', unsafe_allow_html=True)
        st.markdown('<p class="hero-sub">AI-powered revision tailored to your<br/>grade, curriculum, and learning style.</p>', unsafe_allow_html=True)
        if st.button("Create account", use_container_width=True): go("signup")
        if st.button("Sign in", use_container_width=True, key="w_si"): go("signin")
        st.markdown('<p style="text-align:center;font-size:11px;color:#444;margin-top:18px">Elixir · Powered by Groq · Free</p>', unsafe_allow_html=True)

def screen_signup():
    col = st.columns([1,2,1])[1]
    with col:
        if st.button("← Back"): go("welcome")
        st.markdown('<h2 style="font-weight:900;margin-bottom:16px">Create account</h2>', unsafe_allow_html=True)
        _oauth_buttons("su")
        email    = st.text_input("Email",placeholder="you@email.com")
        username = st.text_input("Username",placeholder="studystar99")
        pw       = st.text_input("Password",type="password",placeholder="Create a strong password")
        cpw      = st.text_input("Confirm",type="password",placeholder="Repeat your password")
        rec      = st.text_input("Recovery email (optional)",placeholder="backup@email.com")
        n=0
        if pw:
            n=sum([len(pw)>=8,len(pw)>=12,
                   any(c.isupper() for c in pw) and any(c.islower() for c in pw),
                   any(c.isdigit() for c in pw),
                   any(not c.isalnum() for c in pw)])
            lbls=["Too short","Weak","Fair","Good","Strong","Very strong"]
            clrs=["#dc2626","#ef4444","#d97706","#16a34a","#16a34a","#0ea5e9"]
            pct=int(n/5*100); l=lbls[min(n,5)]; c_=clrs[min(n,5)]
            st.markdown(
                f'<div style="display:flex;align-items:center;gap:8px;margin-bottom:4px">'                f'<div style="flex:1;height:4px;background:#1A1A1A;border-radius:4px;overflow:hidden">'                f'<div style="width:{pct}%;height:100%;background:{c_}"></div></div>'                f'<span style="font-size:11px;font-weight:700;color:{c_}">{l}</span></div>',
                unsafe_allow_html=True)
        if st.button("Create account →", use_container_width=True):
            err=None
            if "@" not in email: err="Enter a valid email."
            elif len(username)<3: err="Username must be 3+ characters."
            elif any(u["email"]==email for u in st.session_state.users): err="Email already registered."
            elif any(u["username"].lower()==username.lower() for u in st.session_state.users): err="Username taken."
            elif n<2: err="Password too weak."
            elif pw!=cpw: err="Passwords do not match."
            if err: st.error(err)
            else:
                user={"id":f"u{int(time.time()*1000)}","email":email,"username":username,
                      "pw_hash":hashlib.sha256(pw.encode()).hexdigest(),"rec":rec}
                st.session_state.users.append(user)
                st.session_state.session={"id":user["id"],"email":email,
                                          "username":username,"is_admin":False}
                go("onboard")
        if st.button("Sign in instead",use_container_width=False): go("signin")

def screen_signin():
    col = st.columns([1,2,1])[1]
    with col:
        if st.button("← Back"): go("welcome")
        st.markdown('<h2 style="font-weight:900;margin-bottom:16px">Welcome back</h2>', unsafe_allow_html=True)
        _oauth_buttons("si")
        email = st.text_input("Email",placeholder="you@email.com")
        pw    = st.text_input("Password",type="password",placeholder="Your password")
        if st.button("Sign in →", use_container_width=True):
            if email.strip().lower()==ADMIN_EMAIL.lower():
                st.session_state.session={"id":ADMIN_ID,"email":ADMIN_EMAIL,
                                          "username":ADMIN_USERNAME,"is_admin":True}
                if not st.session_state.profile:
                    st.session_state.profile={"grade":"Year 8","region":"Qatar / GCC",
                        "curriculum":"Cambridge Lower Secondary","subjects":ADMIN_SUBJECTS}
                go("dashboard")
            else:
                ph=hashlib.sha256(pw.encode()).hexdigest()
                user=next((u for u in st.session_state.users
                           if u["email"]==email and u["pw_hash"]==ph),None)
                if not user: st.error("Incorrect email or password.")
                else:
                    st.session_state.session={"id":user["id"],"email":email,
                                              "username":user["username"],"is_admin":False}
                    go("dashboard" if st.session_state.profile else "onboard")
        if st.button("Create one",use_container_width=False): go("signup")

def screen_onboard():
    step=st.session_state.ob_step
    col=st.columns([1,2,1])[1]
    with col:
        st.markdown(f'<p style="font-size:11px;font-weight:700;color:#555;margin-bottom:4px">STEP {step+1} OF 3</p>',unsafe_allow_html=True)
        st.progress((step+1)/3)
        st.markdown("<br/>",unsafe_allow_html=True)
        if step==0:
            st.markdown('<h3 style="font-weight:900">Personalise your experience</h3>',unsafe_allow_html=True)
            st.session_state.ob_grade =st.selectbox("Year / Grade",[""]+GRADES,
                index=GRADES.index(st.session_state.ob_grade)+1 if st.session_state.ob_grade else 0)
            st.session_state.ob_region=st.selectbox("Study Region",[""]+REGIONS,
                index=REGIONS.index(st.session_state.ob_region)+1 if st.session_state.ob_region else 0)
            st.session_state.ob_curr =st.selectbox("Curriculum",[""]+CURRICULA,
                index=CURRICULA.index(st.session_state.ob_curr)+1 if st.session_state.ob_curr else 0)
            ok=bool(st.session_state.ob_grade and st.session_state.ob_region and st.session_state.ob_curr)
            if st.button("Next: Pick subjects →",use_container_width=True,disabled=not ok):
                st.session_state.ob_step=1; st.rerun()
        elif step==1:
            st.markdown('<h3 style="font-weight:900">Which subjects?</h3>',unsafe_allow_html=True)
            picked=list(st.session_state.ob_picked)
            cols=st.columns(2)
            for i,(sid,name,icon) in enumerate(SUBJECTS):
                is_sel=sid in picked
                with cols[i%2]:
                    label=f"{'✓ ' if is_sel else ''}{icon}  {name}"
                    if st.button(label,key=f"sub_{sid}",use_container_width=True):
                        if is_sel: picked.remove(sid)
                        else:      picked.append(sid)
                        st.session_state.ob_picked=picked; st.rerun()
            st.markdown("<br/>",unsafe_allow_html=True)
            c1,c2=st.columns(2)
            with c1:
                if st.button("← Back",use_container_width=True): st.session_state.ob_step=0; st.rerun()
            with c2:
                if st.button("Next →",use_container_width=True,disabled=not picked):
                    st.session_state.ob_step=2; st.rerun()
        elif step==2:
            st.markdown('<h3 style="font-weight:900">How confident?</h3>',unsafe_allow_html=True)
            profs=dict(st.session_state.ob_profs)
            for sid,name,icon in [(s,n,ic) for s,n,ic in SUBJECTS if s in st.session_state.ob_picked]:
                profs[sid]=st.select_slider(f"{icon} {name}",options=PROFICIENCY,
                                            value=profs.get(sid,"Developing"),key=f"prof_{sid}")
            st.session_state.ob_profs=profs
            st.markdown("<br/>",unsafe_allow_html=True)
            c1,c2=st.columns(2)
            with c1:
                if st.button("← Back",use_container_width=True): st.session_state.ob_step=1; st.rerun()
            with c2:
                if st.button("Start studying →",use_container_width=True):
                    subjects=[{"id":sid,"name":name,"icon":icon,
                               "proficiency":st.session_state.ob_profs.get(sid,"Developing")}
                              for sid,name,icon in SUBJECTS if sid in st.session_state.ob_picked]
                    st.session_state.profile={
                        "grade":st.session_state.ob_grade,
                        "region":st.session_state.ob_region,
                        "curriculum":st.session_state.ob_curr,
                        "subjects":subjects}
                    go("dashboard")

def screen_dashboard():
    render_sidebar()
    session=st.session_state.session
    profile=st.session_state.profile
    spaces=st.session_state.spaces
    hr=__import__("datetime").datetime.now().hour
    greet="morning" if hr<12 else ("afternoon" if hr<18 else "evening")

    is_admin=session.get("is_admin",False)
    badge=' <span style="font-size:10px;font-weight:800;padding:2px 8px;border-radius:20px;background:#3BBFAF18;color:#3BBFAF">Admin</span>' if is_admin else ""
    st.markdown(f'<h2 style="font-weight:900;margin-bottom:2px;font-size:22px">Good {greet}, {session["username"]}{badge}</h2>',unsafe_allow_html=True)
    st.markdown(f'<p style="color:#505050;font-size:12.5px;margin-bottom:18px">{profile["grade"]} · {profile["curriculum"]} · {profile["region"]}</p>',unsafe_allow_html=True)
    st.markdown('<hr class="elixir-divider"/>',unsafe_allow_html=True)

    left, right = st.columns([3,2], gap="large")

    # ── LEFT: spaces ─────────────────────────────────────────────────────────
    with left:
        st.markdown('<h3 style="font-size:15px;font-weight:700;margin-bottom:12px;color:#ECECEA">Spaces</h3>',unsafe_allow_html=True)
        if not spaces:
            st.markdown(
                '<div style="border:2px dashed #1E1E1E;border-radius:10px;padding:32px;text-align:center">'                '<p style="color:#404040;font-size:13px">No spaces yet.<br/>'                'Use <strong style="color:#3BBFAF">＋ New Space</strong> in the sidebar.</p></div>',
                unsafe_allow_html=True)
        else:
            gcols=st.columns(2,gap="small")
            for i,sp in enumerate(spaces):
                with gcols[i%2]:
                    st.markdown(
                        f'<div class="space-card" style="border-left:3px solid {sp["color"]}">'                        f'<div style="display:flex;align-items:center;gap:8px;margin-bottom:6px">'                        f'<span style="font-size:18px;color:{sp["color"]}">{sp["icon"]}</span>'                        f'<div><div style="font-weight:700;font-size:13px;color:#ECECEA">{sp["name"]}</div>'                        f'<div style="font-size:10px;color:#505050">{sp["subject"]}</div></div></div></div>',
                        unsafe_allow_html=True)
                    if st.button("Open",key=f"open_{sp['id']}",use_container_width=True):
                        st.session_state.cur_space=sp; go("space")

    # ── RIGHT: tips + subjects ────────────────────────────────────────────────
    with right:
        st.markdown('<h3 style="font-size:15px;font-weight:700;margin-bottom:10px;color:#ECECEA">Study Tips</h3>',unsafe_allow_html=True)
        tip=STUDY_TIPS[st.session_state.tip_idx]
        st.markdown(f'<div class="tip-box">{tip}</div>',unsafe_allow_html=True)
        tc1,tc2=st.columns(2)
        with tc1:
            if st.button("← Prev",key="tp",use_container_width=True):
                st.session_state.tip_idx=(st.session_state.tip_idx-1)%len(STUDY_TIPS); st.rerun()
        with tc2:
            if st.button("Next →",key="tn",use_container_width=True):
                st.session_state.tip_idx=(st.session_state.tip_idx+1)%len(STUDY_TIPS); st.rerun()

        st.markdown("<br/>",unsafe_allow_html=True)
        st.markdown('<h3 style="font-size:14px;font-weight:700;margin-bottom:8px;color:#ECECEA">Your Subjects</h3>',unsafe_allow_html=True)
        for s in (profile.get("subjects") or []):
            cl=PROF_COLORS.get(s["proficiency"],"#888")
            st.markdown(
                f'<div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:5px">'                f'<span style="font-size:12px;color:#CCC">{s["icon"]} {s["name"]}</span>'                f'<span style="font-size:10px;font-weight:700;padding:2px 7px;border-radius:20px;'                f'background:{cl}18;color:{cl}">{s["proficiency"]}</span></div>',
                unsafe_allow_html=True)

def screen_new_space():
    render_sidebar()
    profile=st.session_state.profile
    col=st.columns([1,2,1])[1]
    with col:
        if st.button("← Dashboard"): go("dashboard")
        st.markdown('<h3 style="font-weight:900;margin-bottom:20px">Create a space</h3>',unsafe_allow_html=True)
        name=st.text_input("Space name",placeholder="e.g. Biology Revision")
        icon=st.selectbox("Icon",SPACE_ICONS)
        color_name=st.selectbox("Colour",list(SPACE_COLORS.keys()))
        color=SPACE_COLORS[color_name]
        subj_names=["General"]+[s["name"] for s in (profile.get("subjects") or [])]
        subj=st.selectbox("Subject (optional)",subj_names)
        if st.button("Create space",use_container_width=True,disabled=not name.strip()):
            sp={"id":f"sp{int(time.time()*1000)}","name":name.strip(),
                "icon":icon,"color":color,"subject":subj}
            st.session_state.spaces.insert(0,sp)
            st.session_state.cur_space=sp; go("space")

def screen_space():
    render_sidebar()
    space=st.session_state.cur_space
    profile=st.session_state.profile
    h1,h2=st.columns([1,10])
    with h1:
        if st.button("←"): go("dashboard")
    with h2:
        st.markdown(
            f'<div style="display:flex;align-items:center;gap:8px;padding-top:4px">'            f'<span style="font-size:16px;color:{space["color"]}">{space["icon"]}</span>'            f'<span style="font-weight:800;font-size:15px">{space["name"]}</span>'            f'<span style="font-size:11px;color:#404040;margin-left:4px">{space["subject"]}</span></div>',
            unsafe_allow_html=True)
    st.markdown('<hr class="elixir-divider"/>',unsafe_allow_html=True)

    uk=st.session_state.get(f'uk_{space["id"]}',0)
    st.markdown(
        '<p style="font-weight:700;font-size:13.5px;margin-bottom:2px">Upload revision material</p>'        '<p style="font-size:12px;color:#404060;margin-bottom:8px">'        'Images, PDFs, .txt, .md, .csv — notes generated automatically</p>',
        unsafe_allow_html=True)
    uploaded=st.file_uploader("Upload",
        type=["png","jpg","jpeg","gif","webp","bmp","pdf",
              "txt","md","csv","json","py","js","ts","java",
              "cpp","c","xml","yaml","yml","tex","log"],
        key=f'uploader_{space["id"]}_{uk}',label_visibility="collapsed")

    if uploaded:
        is_image=uploaded.type.startswith("image/")
        is_pdf=uploaded.type=="application/pdf" or uploaded.name.lower().endswith(".pdf")
        fi="🖼" if is_image else ("📕" if is_pdf else "📄")
        st.markdown(f'<div class="tip-box">{fi} <strong>{uploaded.name}</strong> — analysing…</div>',unsafe_allow_html=True)
        prog=st.progress(0,text="Reading…")
        prog.progress(15,text="Preparing content…")
        with st.spinner(f"⚗ Elixir AI is studying {uploaded.name}…"):
            try:
                raw=uploaded.read()
                prog.progress(35,text="Sending to Groq AI…")
                if is_image: analysis=ai_analyze_image(raw,profile)
                elif is_pdf: analysis=ai_analyze_text(extract_pdf_text(raw),profile)
                else:        analysis=ai_analyze_text(raw.decode("utf-8","ignore"),profile)
                prog.progress(88,text="Saving…")
                note={"id":f"n{int(time.time()*1000)}",
                      "title":uploaded.name.rsplit(".",1)[0],
                      "is_image":is_image,
                      "b64_thumb":base64.b64encode(raw).decode() if is_image else None,
                      "analysis":analysis,"filename":uploaded.name,
                      "created":__import__("datetime").datetime.now().strftime("%d %b %Y, %H:%M")}
                if space["id"] not in st.session_state.notes:
                    st.session_state.notes[space["id"]]=[]
                st.session_state.notes[space["id"]].insert(0,note)
                st.session_state[f'uk_{space["id"]}']=uk+1
                prog.progress(100,text="Done ✓")
                st.success("Study notes saved!")
                st.rerun()
            except Exception as e:
                prog.empty(); st.error(f"Analysis failed: {e}")

    notes=st.session_state.notes.get(space["id"],[])
    if notes:
        st.markdown(
            f'<h4 style="font-weight:800;font-size:14px;margin-top:26px;margin-bottom:12px;'            f'border-left:3px solid #3BBFAF;padding-left:10px">Study Notes ({len(notes)})</h4>',
            unsafe_allow_html=True)
        for i,note in enumerate(notes):
            with st.expander(f"{'🖼' if note['is_image'] else '📄'}  {note['title']}  ·  {note['created']}",expanded=(i==0)):
                if note["is_image"] and note.get("b64_thumb"):
                    st.image(base64.b64decode(note["b64_thumb"]),use_container_width=True,caption=note["filename"])
                st.markdown(note["analysis"])
                c1,c2=st.columns(2)
                with c1:
                    if st.button("Copy",key=f"cp_{note['id']}"): st.code(note["analysis"],language=None)
                with c2:
                    st.download_button("Download .txt",note["analysis"],
                        file_name=f"{note['title']}_notes.txt",mime="text/plain",key=f"dl_{note['id']}")
    else:
        st.markdown(
            '<div style="text-align:center;padding:36px 20px;border:2px dashed #1A1A2E;border-radius:12px;margin-top:14px">'            '<p style="color:#404060;font-size:13px">Upload your first file to generate study notes.</p></div>',
            unsafe_allow_html=True)

def screen_studyplan():
    render_sidebar()
    col=st.columns([1,2,1])[1]
    with col:
        if st.button("← Dashboard"): go("dashboard")
        st.markdown('<h2 style="font-weight:900;margin-bottom:20px">Weekly Study Plan</h2>',unsafe_allow_html=True)
        if not st.session_state.plan_text:
            with st.spinner("⚗ Building your study plan…"):
                try: st.session_state.plan_text=ai_study_plan(st.session_state.spaces)
                except Exception as e: st.error(f"Could not generate: {e}"); return
        st.markdown(
            f'<div class="analysis-box">{st.session_state.plan_text.replace(chr(10),"<br/>")}</div>',
            unsafe_allow_html=True)
        c1,c2=st.columns(2)
        with c1:
            if st.button("Regenerate",use_container_width=True):
                st.session_state.plan_text=""; st.rerun()
        with c2:
            st.download_button("Download plan",st.session_state.plan_text,
                file_name="study_plan.txt",mime="text/plain",use_container_width=True)

# ── Router ────────────────────────────────────────────────────────────────────
def main():
    init_state()
    inject_css()
    if handle_oauth_callback(): return
    # Auto-skip API key screen if key loaded from secrets
    if st.session_state.screen == "apikey" and st.session_state.groq_key:
        go("welcome")
        return
    screen=st.session_state.screen
    if   screen=="apikey":    screen_apikey()
    elif screen=="welcome":   screen_welcome()
    elif screen=="signup":    screen_signup()
    elif screen=="signin":    screen_signin()
    elif screen=="onboard":   screen_onboard()
    elif screen=="dashboard": screen_dashboard()
    elif screen=="new_space": screen_new_space()
    elif screen=="space":     screen_space()
    elif screen=="studyplan": screen_studyplan()
    else: st.error(f"Unknown screen: {screen}"); go("welcome")

if __name__=="__main__":
    main()
