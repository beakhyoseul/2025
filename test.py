import streamlit as st
import sympy as sp
import numpy as np
import plotly.graph_objects as go

st.title("☆**")

# -------------------------------
# Sidebar inputs
# -------------------------------
st.sidebar.header("⚙️ 입력 설정")
expr1_str = st.sidebar.text_input("첫 번째 식 f(x) =", "x**2 - 2")
expr2_str = st.sidebar.text_input("두 번째 식 g(x) =", "0")

x_min, x_max = st.sidebar.slider("x 범위", -10, 10, (-5, 5))
x = sp.symbols("x")

# -------------------------------
# Preprocess & Parse
# -------------------------------
def preprocess(expr_str):
    expr_str = expr_str.replace("^", "**")
    expr_str = expr_str.replace(")(", ")*(")
    expr_str = expr_str.replace("x(", "x*(")
    return expr_str

def parse_equation(expr_str):
    try:
        if "=" in expr_str:
            left, right = expr_str.split("=")
            return sp.sympify(preprocess(left)) - sp.sympify(preprocess(right))
        else:
            return sp.sympify(preprocess(expr_str))
    except Exception as e:
        st.error(f"수식 파싱 오류: {e}")
        st.stop()

expr1 = parse_equation(expr1_str)
expr2 = parse_equation(expr2_str)

# -------------------------------
# Solve intersection (Exact)
# -------------------------------
solutions_exact = []
eq = sp.Eq(expr1, expr2)

try:
    sols = sp.solve(eq, x)
    for s in sols:
        if s.is_real:
            y_exact = expr1.subs(x, s)
            solutions_exact.append((s, y_exact))
except Exception as e:
    st.warning(f"교점 계산 오류: {e}")

# -------------------------------
# Output results (LaTeX for root display)
# -------------------------------
st.subheader("🎯 교점 결과")

if solutions_exact:
    for px, py in solutions_exact:
        # 반드시 evalf 하지 않고 sympy 객체 그대로 전달
        st.latex(sp.Eq(sp.Symbol('x'), px))   # x = -√2 형태
        st.latex(sp.Eq(sp.Symbol('y'), py))   # y = 값
else:
    st.info("실수 해가 없습니다.")
# -------------------------------
# Safe evaluation for plotting
# -------------------------------
def safe_eval(f, X):
    Y = []
    for xi in X:
        try:
            yi = f(xi)
            if isinstance(yi, sp.Expr):
                yi = float(yi.evalf())
            if np.isfinite(yi):
                Y.append(yi)
            else:
                Y.append(np.nan)
        except Exception:
            Y.append(np.nan)
    return np.array(Y)

# -------------------------------
# Graph
# -------------------------------
st.subheader("📈 그래프")

try:
    f1 = sp.lambdify(x, expr1, modules=["numpy"])
    f2 = sp.lambdify(x, expr2, modules=["numpy"])
except Exception as e:
    st.error(f"그래프 변환 오류: {e}")
    st.stop()

X = np.linspace(x_min, x_max, 500)
Y1 = safe_eval(f1, X)
Y2 = safe_eval(f2, X)

fig = go.Figure()
fig.add_trace(go.Scatter(x=X, y=Y1, mode="lines", name="f(x) / 식1"))
fig.add_trace(go.Scatter(x=X, y=Y2, mode="lines", name="g(x) / 식2"))

# -------------------------------
# Plot intersection points with numeric labels
# -------------------------------
if solutions_exact:
    Xp = [float(px.evalf()) for px, _ in solutions_exact]
    Yp = [float(py.evalf()) for _, py in solutions_exact]
    fig.add_trace(go.Scatter(
        x=Xp, y=Yp,
        mode="markers+text",
        marker=dict(size=10, color="red"),
        text=[f"({px:.4f},{py:.4f})" for px, py in zip(Xp, Yp)],
        textposition="top right",
        name="교점"
    ))

fig.update_layout(
    xaxis_title="x",
    yaxis_title="y",
    width=750,
    height=500,
    template="plotly_white"
)

st.plotly_chart(fig, use_container_width=True)
