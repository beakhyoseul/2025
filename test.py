import streamlit as st
import sympy as sp
import numpy as np
import plotly.graph_objects as go
import pandas as pd

st.title("☆**")

# -------------------------------
# Sidebar inputs
# -------------------------------
st.sidebar.header("⚙️ 입력 설정")
expr1_str = st.sidebar.text_input("첫 번째 식 f(x) =", "x**2 - 1")
expr2_str = st.sidebar.text_input("두 번째 식 g(x) =", "cos(x)")

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
# Solve intersection
# -------------------------------
solutions = []
eq = sp.Eq(expr1, expr2)

try:
    sols = sp.solve(eq, x)
    for s in sols:
        s_eval = s.evalf()
        if s_eval.is_real:
            y_val = expr1.subs(x, s_eval).evalf()
            solutions.append([float(s_eval), float(y_val)])
except Exception:
    pass

# -------------------------------
# Output results
# -------------------------------
st.subheader("🎯 교점 결과")
if solutions:
    df = pd.DataFrame(solutions, columns=["x", "y"])
    st.dataframe(df, use_container_width=True)
else:
    st.info("실수 해가 없습니다.")

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

if solutions:
    Xp, Yp = zip(*solutions)
    fig.add_trace(go.Scatter(
        x=Xp, y=Yp, mode="markers+text",
        text=[f"({x:.2f},{y:.2f})" for x, y in solutions],
        textposition="top center", name="교점"
    ))

fig.update_layout(
    xaxis_title="x", yaxis_title="y",
    width=750, height=500,
    template="plotly_white"
)

st.plotly_chart(fig, use_container_width=True)
