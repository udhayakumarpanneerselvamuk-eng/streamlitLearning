"""Student Grade Manager - Streamlit version.

Run with:
    pip install streamlit
    streamlit run grade_manager.py
"""

import html

import streamlit as st

st.set_page_config(page_title="Student Grade Manager", page_icon="📝", layout="centered")

# ---------------------------------------------------------------- logic ----


def get_grade(mark):
    if not 0 <= mark <= 100:
        raise ValueError("Mark must be between 0 and 100.")
    if mark >= 90:
        return "A"
    if mark >= 80:
        return "B"
    if mark >= 70:
        return "C"
    if mark >= 60:
        return "D"
    return "F"


# Per-grade presentation: lower bound, colours, and the feedback message.
GRADES = {
    "A": {"low": 90, "color": "#1F7A5C", "tint": "#DCEFE6", "msg": "Excellent work! Keep it up!"},
    "B": {"low": 80, "color": "#2A6F97", "tint": "#DDEBF4", "msg": "Great job! You're doing well."},
    "C": {"low": 70, "color": "#A66A00", "tint": "#F6E8CC", "msg": "Good effort. Keep practicing and you'll improve."},
    "D": {"low": 60, "color": "#BF541A", "tint": "#F7E0D2", "msg": "You're making progress. A little more practice can help."},
    "F": {"low": 0, "color": "#B3261E", "tint": "#F6DAD7", "msg": "Don't give up. Review the material and try again!"},
}
NEXT_UP = {"F": "D", "D": "C", "C": "B", "B": "A"}

# ---------------------------------------------------------------- style ----

CSS = """
@import url('https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,500;12..96,700;12..96,800&family=Figtree:wght@400;500;600&display=swap');
:root {
  --paper: #EDF1F5;
  --card: #FFFFFF;
  --ink: #1B2A41;
  --muted: #5B6B80;
  --line: #CBD5E1;
}

#MainMenu, footer, header[data-testid="stHeader"] { visibility: hidden; height: 0; }

.stApp {
  background-color: var(--paper);
  background-image:
    linear-gradient(var(--line) 1px, transparent 1px),
    linear-gradient(90deg, var(--line) 1px, transparent 1px);
  background-size: 28px 28px;
  background-position: -1px -1px;
}
.stApp, .stApp p, .stApp label, .stApp span, .stApp li { font-family: 'Figtree', sans-serif; color: var(--ink); }
.block-container { max-width: 640px; padding-top: 3rem; padding-bottom: 4rem; }

.title {
  font-family: 'Bricolage Grotesque', sans-serif;
  font-weight: 800;
  font-size: clamp(2.2rem, 7vw, 3.1rem);
  line-height: 1.02;
  letter-spacing: -0.02em;
  margin: 0 0 .6rem;
  color: var(--ink);
}
.lede { color: var(--muted) !important; font-size: 1.05rem; margin: 0 0 1.6rem; max-width: 46ch; }

/* form card */
div[data-testid="stForm"] {
  background: var(--card);
  border: 1.5px solid var(--ink);
  border-radius: 14px;
  padding: 1.4rem 1.4rem 1.2rem;
  box-shadow: 5px 5px 0 var(--ink);
}
div[data-testid="stForm"] label p { font-weight: 600; font-size: .95rem; }
div[data-testid="stForm"] input {
  background: #F7F9FB !important;
  color: var(--ink) !important;
  border-radius: 8px !important;
}
div[data-testid="stNumberInput"] button { color: var(--ink) !important; }

/* buttons */
.stButton > button, div[data-testid="stFormSubmitButton"] > button {
  background: var(--ink);
  color: #fff !important;
  border: 1.5px solid var(--ink);
  border-radius: 10px;
  font-family: 'Figtree', sans-serif;
  font-weight: 600;
  padding: .55rem 1.3rem;
  transition: transform .12s ease, background .12s ease;
}
.stButton > button p, div[data-testid="stFormSubmitButton"] > button p { color: #fff !important; }
.stButton > button:hover, div[data-testid="stFormSubmitButton"] > button:hover {
  background: #2C4163; border-color: #2C4163; transform: translateY(-1px);
}
.stButton > button:focus-visible, div[data-testid="stFormSubmitButton"] > button:focus-visible {
  outline: 3px solid #7FA6D6; outline-offset: 2px;
}
.ghost .stButton > button { background: transparent; color: var(--ink) !important; }
.ghost .stButton > button p { color: var(--ink) !important; }
.ghost .stButton > button:hover { background: #E2E8F0; }

/* result card */
.result {
  margin-top: 2rem;
  background: var(--card);
  border: 1.5px solid var(--ink);
  border-radius: 14px;
  overflow: hidden;
  box-shadow: 5px 5px 0 var(--ink);
  animation: stamp .45s cubic-bezier(.2,.9,.3,1.2) both;
}
@keyframes stamp {
  from { transform: scale(.96) rotate(-.6deg); opacity: 0; }
  to   { transform: none; opacity: 1; }
}
@media (prefers-reduced-motion: reduce) { .result { animation: none; } }

.result-top { display: flex; align-items: center; gap: 1.4rem; padding: 1.4rem 1.5rem; }
.letter {
  font-family: 'Bricolage Grotesque', sans-serif;
  font-weight: 800;
  font-size: 5.6rem;
  line-height: 1;
  width: 7.2rem; height: 7.2rem;
  flex: none;
  display: grid; place-items: center;
  border: 3px solid currentColor;
  border-radius: 50%;
  transform: rotate(-5deg);
}
.result-name { font-family: 'Bricolage Grotesque', sans-serif; font-weight: 700; font-size: 1.45rem; margin: 0 0 .15rem; }
.result-score { margin: 0 0 .5rem; color: var(--muted) !important; }
.result-msg { margin: 0; font-weight: 500; }

.scale { padding: .4rem 1.5rem 1.6rem; border-top: 1.5px dashed var(--line); }
.scale-title { font-size: .9rem; color: var(--muted) !important; margin: 1rem 0 1.1rem; }
.bar { position: relative; display: flex; height: 14px; border-radius: 7px; overflow: visible; }
.bar span { display: block; height: 100%; }
.bar span:first-child { border-radius: 7px 0 0 7px; }
.bar span:last-of-type { border-radius: 0 7px 7px 0; }
.pin {
  position: absolute; top: -7px; width: 4px; height: 28px;
  background: var(--ink); border-radius: 2px; transform: translateX(-2px);
  box-shadow: 0 0 0 2px #fff;
}
.ticks { position: relative; height: 1.4rem; margin-top: .5rem; font-size: .8rem; color: var(--muted); }
.ticks b { position: absolute; transform: translateX(-50%); font-weight: 600; }
.ticks b:first-child { transform: none; }
.ticks b:last-child { transform: translateX(-100%); }

/* class list */
.list-title { font-family: 'Bricolage Grotesque', sans-serif; font-weight: 700; font-size: 1.35rem; margin: 2.6rem 0 .6rem; }
div[data-testid="stDataFrame"] { border: 1.5px solid var(--ink); border-radius: 10px; overflow: hidden; }
div[data-testid="stAlert"] { border-radius: 10px; }
"""

# Markdown ends an HTML block at the first blank line, which made the rest of the
# CSS show up as page text. Strip blank lines so the <style> stays a single block.
CSS = "\n".join(line for line in CSS.splitlines() if line.strip())
st.markdown(f"<style>{CSS}</style>", unsafe_allow_html=True)

# ---------------------------------------------------------------- state ----

st.session_state.setdefault("result", None)
st.session_state.setdefault("roster", [])

# ------------------------------------------------------------------- UI ----

st.markdown('<h1 class="title">Student Grade Manager</h1>', unsafe_allow_html=True)
st.markdown(
    '<p class="lede">Enter a name and a mark out of 100 to see the grade it earns and where it sits on the scale.</p>',
    unsafe_allow_html=True,
)

with st.form("grade_form"):
    name_in = st.text_input("Student name", placeholder="e.g. Amara Okafor")
    mark_in = st.number_input(
        "Mark (0 to 100)", min_value=0.0, max_value=100.0, value=75.0, step=0.5, format="%g"
    )
    submitted = st.form_submit_button("Check grade")

if submitted:
    name = name_in.strip() or "Student"
    try:
        grade = get_grade(float(mark_in))
        st.session_state.result = {"name": name, "mark": float(mark_in), "grade": grade}
    except ValueError as error:
        st.session_state.result = None
        st.error(f"That doesn't look like a valid mark. {error}")

result = st.session_state.result

if result:
    name, mark, grade = result["name"], result["mark"], result["grade"]
    info = GRADES[grade]

    # Colour bands on the scale: F 0-60, D 60-70, C 70-80, B 80-90, A 90-100.
    bands = [("F", 60), ("D", 10), ("C", 10), ("B", 10), ("A", 10)]
    segments = "".join(
        f'<span style="width:{w}%;background:{GRADES[g]["color"]};opacity:{1 if g == grade else .28}"></span>'
        for g, w in bands
    )
    ticks = "".join(
        f'<b style="left:{pos}%">{label}</b>'
        for pos, label in [(0, "0"), (60, "60"), (70, "70"), (80, "80"), (90, "90"), (100, "100")]
    )

    if grade in NEXT_UP:
        target = NEXT_UP[grade]
        gap = GRADES[target]["low"] - mark
        progress = f"{gap:g} more {'mark' if gap == 1 else 'marks'} to reach a {target}."
    else:
        progress = "Top grade reached."

    st.markdown(
        f"""
<div class="result">
  <div class="result-top" style="background:{info['tint']}">
    <div class="letter" style="color:{info['color']}">{grade}</div>
    <div>
      <p class="result-name">{html.escape(name)}</p>
      <p class="result-score">Scored {mark:g}/100</p>
      <p class="result-msg">{info['msg']}</p>
    </div>
  </div>
  <div class="scale">
    <p class="scale-title">{progress}</p>
    <div class="bar">{segments}<i class="pin" style="left:{mark}%"></i></div>
    <div class="ticks">{ticks}</div>
  </div>
</div>
""",
        unsafe_allow_html=True,
    )

    st.write("")
    if st.button("Add to class list"):
        st.session_state.roster.append({"Student": name, "Mark": mark, "Grade": grade})
        st.toast(f"Added {name} to the class list")

if st.session_state.roster:
    st.markdown('<p class="list-title">Class list</p>', unsafe_allow_html=True)
    st.dataframe(
        st.session_state.roster,
        hide_index=True,
        use_container_width=True,
        column_config={"Mark": st.column_config.NumberColumn(format="%g")},
    )
    marks = [r["Mark"] for r in st.session_state.roster]
    st.caption(f"{len(marks)} student(s), class average {sum(marks) / len(marks):.1f}")
    st.markdown('<div class="ghost">', unsafe_allow_html=True)
    if st.button("Clear list"):
        st.session_state.roster = []
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)