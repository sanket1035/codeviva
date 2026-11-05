"""CodeViva Streamlit UI (dark editorial theme)."""
import os

import streamlit as st
import streamlit.components.v1 as components
from dotenv import load_dotenv

load_dotenv()

from codeviva.analyzer import analyze
from codeviva.diagram import call_graph, function_flow
from codeviva.llm import explain_and_quiz, llm_available
from codeviva.verify import check

MERMAID_JS = os.getenv("MERMAID_JS_URL", "https://cdn.jsdelivr.net/npm/mermaid@10.9.1/dist/mermaid.min.js")

st.set_page_config(page_title="CodeViva", layout="wide")

CSS = """
<style>
@font-face{font-family:'Anton';src:url(app/static/fonts/anton.woff2) format('woff2');font-display:swap}
@font-face{font-family:'Manrope';font-weight:500;src:url(app/static/fonts/manrope-500.woff2) format('woff2');font-display:swap}
@font-face{font-family:'Manrope';font-weight:700;src:url(app/static/fonts/manrope-700.woff2) format('woff2');font-display:swap}
html,body,[class*="css"],.stApp{font-family:'Manrope',system-ui,sans-serif}
.block-container{padding-top:1.2rem;max-width:1240px}
header[data-testid="stHeader"]{background:transparent}
iframe{border-radius:20px}

/* hero */
.hero{position:relative;overflow:hidden;border-radius:24px;min-height:360px;padding:22px 26px;margin-bottom:12px;
  background:radial-gradient(1200px 380px at 78% 70%,rgba(232,168,91,.34),transparent 60%),
             linear-gradient(180deg,#17171a 0%,#0b0b0c 100%);}
.hero .code{position:absolute;inset:0;margin:0;padding:96px 34px 0;font:500 13px/1.7 ui-monospace,Menlo,Consolas,monospace;
  color:rgba(232,168,91,.11);overflow:hidden;
  -webkit-mask-image:linear-gradient(180deg,transparent 0,#000 40%,transparent 100%);mask-image:linear-gradient(180deg,transparent 0,#000 40%,transparent 100%)}
.nav{position:relative;z-index:2;display:flex;justify-content:space-between;align-items:center}
.pillnav{display:flex;gap:26px;padding:11px 24px;border-radius:99px;border:1px solid rgba(255,255,255,.14);background:rgba(255,255,255,.04);
  font-size:.82rem;color:#d9d7d2;backdrop-filter:blur(6px)}
.pillbtn{padding:11px 20px;border-radius:99px;border:1px solid rgba(255,255,255,.2);font-size:.82rem;color:#fff;background:rgba(255,255,255,.05)}
.title{position:relative;z-index:2;font-family:'Anton',Impact,'Arial Narrow',sans-serif;font-size:clamp(84px,14.5vw,196px);
  line-height:.92;letter-spacing:.005em;color:#f4f3ef;margin:22px 0 0;text-transform:uppercase;white-space:nowrap}
.tag{position:relative;z-index:2;max-width:470px;font-size:.92rem;line-height:1.55;color:#cfcdc7;margin-top:14px}

/* bento */
.stats{background:#050505;border-radius:20px;padding:26px 28px;min-height:350px;display:flex;flex-direction:column;justify-content:space-between;
  border:1px solid rgba(255,255,255,.06)}
.stats .grid{display:grid;grid-template-columns:1fr 1fr;gap:34px 18px}
.lbl{font-size:.78rem;color:#a8a6a0;letter-spacing:.02em;margin-bottom:6px;display:flex;align-items:center;gap:8px}
.lbl i{width:7px;height:7px;border-radius:50%;background:#e8a85b;display:inline-block}
.num{font-family:'Anton',Impact,sans-serif;font-size:3.6rem;line-height:1;color:#f4f3ef;letter-spacing:.01em}
.foot{display:flex;justify-content:space-between;align-items:center;font-size:.82rem;color:#bdbbb5;border-top:1px solid rgba(255,255,255,.08);padding-top:14px}
.chip{padding:6px 14px;border-radius:99px;border:1px solid rgba(255,255,255,.16);color:#f4f3ef}

/* tabs as pills */
div[data-baseweb="tab-list"]{gap:10px;border:none}
div[data-baseweb="tab-highlight"],div[data-baseweb="tab-border"]{display:none!important}
button[data-baseweb="tab"]{border-radius:99px;border:1px solid rgba(255,255,255,.16);padding:8px 20px;height:auto;background:transparent}
button[data-baseweb="tab"][aria-selected="true"]{background:#f4f3ef!important;border-color:#f4f3ef!important}
button[data-baseweb="tab"][aria-selected="true"] p{color:#0a0a0b!important;font-weight:700}

.card{background:#121214;border-radius:16px;padding:16px 20px;margin-bottom:10px;border:1px solid rgba(255,255,255,.07);color:#e6e4df;line-height:1.55}
.card b{font-family:'Anton',Impact,sans-serif;font-weight:400;letter-spacing:.03em;font-size:1.15rem;color:#f4f3ef}
.pill{display:inline-block;padding:2px 11px;border-radius:99px;font-size:.74rem;margin-left:8px;background:rgba(232,168,91,.14);color:#e8a85b}
.good{background:rgba(74,222,128,.14);color:#86efac}.bad{background:rgba(248,113,113,.16);color:#fca5a5}
section[data-testid="stSidebar"]{background:#0e0e10;border-right:1px solid rgba(255,255,255,.06)}
.stButton>button,.stDownloadButton>button{border-radius:99px!important;border:1px solid #f4f3ef!important;background:#f4f3ef!important;color:#0a0a0b!important;font-weight:700}
.stButton>button p,.stDownloadButton>button p{color:#0a0a0b!important;font-weight:700}
</style>
"""
st.markdown(CSS, unsafe_allow_html=True)

HERO_CODE = """def explain(code):
    tree = ast.parse(code)
    graph = build_call_graph(tree)
    for fn in graph.functions:
        verify(fn, tree)
        yield viva_question(fn)

def build_call_graph(tree):
    edges = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Call):
            edges.append(resolve(node))
    return edges
"""


HERO_HTML = "<br>".join(
    ("&nbsp;" * (len(l) - len(l.lstrip(" ")))) + l.strip() for l in HERO_CODE.splitlines() if l.strip()
)


def mermaid(code: str, height: int = 420):
    components.html(f"""
    <body style="margin:0;background-color:#efeeec;
      background-image:linear-gradient(rgba(0,0,0,.055) 1px,transparent 1px),linear-gradient(90deg,rgba(0,0,0,.055) 1px,transparent 1px);
      background-size:22px 22px;font-family:ui-monospace,monospace">
    <div class="mermaid" style="display:flex;justify-content:center;padding:18px">{code}</div>
    <script src="{MERMAID_JS}"></script>
    <script>mermaid.initialize({{startOnLoad:true,theme:'base',flowchart:{{curve:'basis',padding:14}},themeVariables:{{
      primaryColor:'#ffffff',primaryBorderColor:'#111',primaryTextColor:'#111',lineColor:'#111',
      fontFamily:'ui-monospace, Menlo, monospace',fontSize:'14px'}}}});</script></body>
    """, height=height, scrolling=True)


with st.sidebar:
    st.subheader("Input")
    up = st.file_uploader("Python file", type=["py"])
    use_sample = st.button("Try sample program")
    lang = st.selectbox("Explain in", ["English", "Hinglish", "Hindi", "Marathi"])
    st.caption("Groq connected" if llm_available() else "Offline mode. Set GROQ_API_KEY for AI explanations.")

source = None
fname = "upload.py"
if up:
    source, fname = up.getvalue().decode("utf-8", "ignore"), up.name
elif use_sample or st.session_state.get("sample"):
    st.session_state["sample"] = True
    source, fname = open("samples/bank_account.py", encoding="utf-8").read(), "bank_account.py"

st.markdown(f"""
<div class="hero">
  <div class="code">{HERO_HTML}</div>
  <div class="nav"><div class="pillnav"><span>Flow</span><span>Explain</span><span>Viva</span></div>
  <div class="pillbtn">{'Groq live' if llm_available() else 'Offline mode'}</div></div>
  <div class="title">CodeViva</div>
  <div class="tag">Upload lab code. Get a flow diagram built from the syntax tree, plain-language explanations and a full viva sheet. Nothing in the diagram is guessed.</div>
</div>
""", unsafe_allow_html=True)

if not source:
    st.info("Upload a .py file from the sidebar, or click Try sample program.")
    st.stop()

try:
    a = analyze(source)
except SyntaxError as e:
    st.error(f"Syntax error on line {e.lineno}: {e.msg}")
    st.stop()

if "res" not in st.session_state or st.session_state.get("src") != source or st.session_state.get("lang") != lang:
    with st.spinner("Explaining your code..."):
        st.session_state.update(res=explain_and_quiz(a, lang), src=source, lang=lang)
res = st.session_state["res"]

loops = sum(f.loops for f in a.functions.values())
decs = sum(f.branches for f in a.functions.values())

left, right = st.columns([1.55, 1])
with left:
    mermaid(call_graph(a), 350)
with right:
    st.markdown(f"""
    <div class="stats">
      <div class="grid">
        <div><div class="lbl"><i></i>Lines of code</div><div class="num">{a.loc}</div></div>
        <div><div class="lbl"><i></i>Functions</div><div class="num">{len(a.functions)}</div></div>
        <div><div class="lbl"><i></i>Loops</div><div class="num">{loops}</div></div>
        <div><div class="lbl"><i></i>Decisions</div><div class="num">{decs}</div></div>
      </div>
      <div class="foot"><span>{fname}</span><span class="chip">{len(a.imports)} import(s)</span></div>
    </div>""", unsafe_allow_html=True)

st.write("")
t1, t2, t3, t4 = st.tabs(["Function zoom", "Explanation", "Viva Q&A", "Verification"])

with t1:
    st.caption("Dotted arrow means recursion. Amber box means the function has a loop.")
    pick = st.selectbox("Function", list(a.functions))
    mermaid(function_flow(pick, a), 200)
    with st.expander("Mermaid source"):
        st.code(call_graph(a), language="text")

with t2:
    st.markdown(f'<div class="card">{res.get("summary","")}</div>', unsafe_allow_html=True)
    for name, text in res.get("functions", {}).items():
        f = a.functions.get(name)
        meta = f'<span class="pill">line {f.lineno}</span>' if f else ""
        st.markdown(f'<div class="card"><b>{name}()</b>{meta}<br>{text}</div>', unsafe_allow_html=True)

with t3:
    for i, qa in enumerate(res.get("viva", []), 1):
        with st.expander(f"Q{i}. {qa['q']}"):
            st.write(qa["a"])
    md = "\n\n".join(f"**Q{i}. {x['q']}**\n\n{x['a']}" for i, x in enumerate(res.get("viva", []), 1))
    st.download_button("Download viva sheet (.md)", md, "viva.md")

with t4:
    v = check(res, a)
    cls = "good" if v["grounded"] else "bad"
    msg = "All function names verified against the syntax tree" if v["grounded"] else "Hallucination detected"
    st.markdown(f'<span class="pill {cls}" style="margin-left:0">{msg}</span>', unsafe_allow_html=True)
    st.write(f"Checked **{v['checked']}** function names mentioned in the explanation.")
    if v["hallucinated"]:
        st.error("Not found in your code: " + ", ".join(v["hallucinated"]))
