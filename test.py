import streamlit as st
import sympy as sp
import numpy as np
import plotly.graph_objects as go
from streamlit_plotly_events import plotly_events

st.title("☆**")

x, y = sp.symbols('x y')
mode = st.radio("모드 선택", ["함수 vs 함수", "방정식 vs 방정식", "함수 vs 방정식"])

def get_points(solutions, f=None):
    points = []
    for sol in solutions:
        if isinstance(sol, dict):
            px = float(sol[x].evalf())
            py = float(sol[y].evalf())
        else:
            px = float(sol.evalf())
            py = float(f.subs(x, sol).evalf()) if f else None
        points.append((px, py))
    return points

def plot_interactive(points, x_vals=None, y_vals=None, f_vals=None, g_vals=None, eq1_vals=None, eq2_vals=None, mode='function'):
    fig = go.Figure()
    
    if mode == 'function':
        fig.add_trace(go.Scatter(x=x_vals, y=f_vals, mode='lines', name='f(x)', line=dict(color='blue')))
        fig.add_trace(go.Scatter(x=x_vals, y=g_vals, mode='lines', name='g(x)', line=dict(color='green')))
    else:  # equation
        fig.add_trace(go.Contour(z=eq1_vals, x=x_vals, y=y_vals, contours=dict(showlines=True, coloring='lines'),
                                 line=dict(color='blue'), name='eq1'))
        fig.add_trace(go.Contour(z=eq2_vals, x=x_vals, y=y_vals, contours=dict(showlines=True, coloring='lines'),
                                 line=dict(color='green'), name='eq2'))
        
    for px, py in points:
        fig.add_trace(go.Scatter(x=[px], y=[py], mode='markers+text',
                                 text=[f"({px:.2f},{py:.2f})"], textposition="top right",
                                 marker=dict(color='red', size=10), name='교점'))
    clicked_points = plotly_events(fig)
    if clicked_points:
        for pt in clicked_points:
            st.info(f"클릭 좌표: ({pt['x']:.3f}, {pt['y']:.3f})")
    st.plotly_chart(fig, use_container_width=True)


# ---------------------------- 함수 vs 함수 ----------------------------
if mode == "함수 vs 함수":
    f_input = st.text_input("첫 번째 함수 f(x)")
    g_input = st.text_input("두 번째 함수 g(x)")

    if f_input and g_input:
        try:
            f = sp.sympify(f_input)
            g = sp.sympify(g_input)
            solutions = sp.solve(sp.Eq(f, g), x)
            points = get_points(solutions, f)
            if points:
                st.write("교점 좌표:", points)
            x_min = min(p[0] for p in points)-2 if points else -10
            x_max = max(p[0] for p in points)+2 if points else 10
            x_vals = np.linspace(x_min, x_max, 400)
            f_vals = [float(f.subs(x, val).evalf()) for val in x_vals]
            g_vals = [float(g.subs(x, val).evalf()) for val in x_vals]
            plot_interactive(points, x_vals=x_vals, f_vals=f_vals, g_vals=g_vals, mode='function')
        except Exception as e:
            st.error(f"입력 오류: {e}")

# ---------------------------- 방정식 vs 방정식 ----------------------------
elif mode == "방정식 vs 방정식":
    eq1_input = st.text_input("첫 번째 방정식 F1(x,y)=0")
    eq2_input = st.text_input("두 번째 방정식 F2(x,y)=0")

    if eq1_input and eq2_input:
        try:
            eq1 = sp.sympify(eq1_input)
            eq2 = sp.sympify(eq2_input)
            solutions = sp.solve([eq1, eq2], (x, y))
            points = get_points(solutions)
            if points:
                st.write("교점 좌표:", points)
            x_min = min(p[0] for p in points)-2 if points else -10
            x_max = max(p[0] for p in points)+2 if points else 10
            y_min = min(p[1] for p in points)-2 if points else -10
            y_max = max(p[1] for p in points)+2 if points else 10
            x_vals = np.linspace(x_min, x_max, 200)
            y_vals = np.linspace(y_min, y_max, 200)
            X, Y = np.meshgrid(x_vals, y_vals)
            F1 = sp.lambdify((x, y), eq1, 'numpy')
            F2 = sp.lambdify((x, y), eq2, 'numpy')
            Z1 = F1(X, Y)
            Z2 = F2(X, Y)
            plot_interactive(points, x_vals=x_vals, y_vals=y_vals, eq1_vals=Z1, eq2_vals=Z2, mode='equation')
        except Exception as e:
            st.error(f"입력 오류: {e}")

# ---------------------------- 함수 vs 방정식 ----------------------------
else:
    f_input = st.text_input("함수 f(x)")
    eq_input = st.text_input("방정식 F(x,y)=0")

    if f_input and eq_input:
        try:
            f = sp.sympify(f_input)
            eq = sp.sympify(eq_input)
            eq_sub = eq.subs(y, f)
            x_solutions = sp.solve(eq_sub, x)
            points = get_points(x_solutions, f)
            if points:
                st.write("교점 좌표:", points)
            x_min = min(p[0] for p in points)-2 if points else -10
            x_max = max(p[0] for p in points)+2 if points else 10
            y_min = min(p[1] for p in points)-2 if points else -10
            y_max = max(p[1] for p in points)+2 if points else 10
            x_vals = np.linspace(x_min, x_max, 200)
            f_vals = [float(f.subs(x, val).evalf()) for val in x_vals]
            y_vals = np.linspace(y_min, y_max, 200)
            X, Y = np.meshgrid(x_vals, y_vals)
            F = sp.lambdify((x, y), eq, 'numpy')
            Z = F(X, Y)
            plot_interactive(points, x_vals=x_vals, y_vals=y_vals, f_vals=f_vals, eq1_vals=Z, mode='equation')
        except Exception as e:
            st.error(f"입력 오류: {e}")
