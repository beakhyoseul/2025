import streamlit as st
import sympy as sp
import numpy as np
import plotly.graph_objects as go

st.set_page_config(page_title="☆** 함수/방정식 교점 찾기", layout="centered")

st.title("☆** 함수/방정식 교점 찾기")

# -------------------------------
# Sidebar inputs
# -------------------------------
st.sidebar.header("⚙️ 입력 설정")
expr1_str = st.sidebar.text_input("첫 번째 식 f(x) =", "x**2 - 2")
expr2_str = st.sidebar.text_input("두 번째 식 g(x) =", "0")

x_min, x_max = st.sidebar.slider("x 범위", -10, 10, (-5, 5))

x = sp.symbols("x")

def preprocess(expr_str):
    expr_str = expr_str.replace("^", "**")
    expr_str = expr_str.replace(")(", ")*(")
    expr_str = expr_str.replace("x(", "x*(")
    return expr_str

def parse_equation(expr_str):
    if "=" in expr_str:
        left, right = expr_str.split("=")
        return sp.sympify(preprocess(left)) - sp.sympify(preprocess(right))
    else:
        return sp.sympify(preprocess(expr_str))

try:
    expr1 = parse_equation(expr1_str)
    expr2 = parse_equation(expr2_str)
except Exception as e:
    st.error(f"입력 오류: {e}")
    st.stop()

# -------------------------------
# Solve intersection (Exact only)
# -------------------------------
solutions_exact = []
eq = sp.Eq(expr1, expr2)

try:
    sols = sp.solve(eq, x)
    for s in sols:
        if s.is_real:
            y_exact = expr1.subs(x, s)
            solutions_exact.append((s, y_exact))
except Exception:
    pass

# -------------------------------
# Graph
# -------------------------------
st.subheader("📈 그래프")

try:
    f1 = sp.lambdify(x, expr1, "numpy")
    f2 = sp.lambdify(x, expr2, "numpy")
except Exception as e:
    st.error(f"그래프 변환 오류: {e}")
    st.stop()

X = np.linspace(x_min, x_max, 500)
Y1, Y2 = f1(X), f2(X)

fig = go.Figure()
fig.add_trace(go.Scatter(x=X, y=Y1, mode="lines", name="f(x) / 식1"))
fig.add_trace(go.Scatter(x=X, y=Y2, mode="lines", name="g(x) / 식2"))

# 그래프에서는 소수 근사 좌표로 찍기
if solutions_exact:
    Xp = [float(px.evalf()) for px, _ in solutions_exact]
    Yp = [float(py.evalf()) for _, py in solutions_exact]
    fig.add_trace(go.Scatter(
        x=Xp, y=Yp,
        mode="markers",
        marker=dict(size=10, color="red"),
        name="교점"
    ))

fig.update_layout(
    xaxis_title="x", yaxis_title="y",
    width=750, height=500,
    template="plotly_white"
)

st.plotly_chart(fig, use_container_width=True)

# -------------------------------
# 교점 좌표 박스 (카드 스타일)
# -------------------------------
st.subheader("🎯 교점 결과")

if solutions_exact:
    cols = st.columns(len(solutions_exact))  # 교점 개수만큼 카드 생성
    for i, (px, py) in enumerate(solutions_exact):
        with cols[i]:
            st.markdown(
                f"""
                <div style="
                    background-color:#f9f9f9;
                    padding:15px;
                    border-radius:15px;
                    box-shadow:2px 2px 8px rgba(0,0,0,0.1);
                    text-align:center;
                    font-size:18px;
                ">
                    <b>교점 {i+1}</b><br>
                    $({sp.latex(px)}, {sp.latex(py)})$
                </div>
                """,
                unsafe_allow_html=True
            )
else:
    st.info("실수 해가 없습니다.")
