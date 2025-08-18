import streamlit as st
import sympy as sp
import numpy as np
import matplotlib.pyplot as plt

# 제목
st.title("📐 함수 그래프 & 미적분 시각화")

# 사용자 입력
func_input = st.text_input("함수를 입력하세요 (변수는 x)", "sin(x)")

# 심볼 정의
x = sp.Symbol('x')

try:
    # 입력한 함수 파싱
    func = sp.sympify(func_input)
    func_diff = sp.diff(func, x)   # 미분
    func_int = sp.integrate(func, x)  # 부정적분

    # 결과 출력
    st.latex(f"f(x) = {sp.latex(func)}")
    st.latex(f"f'(x) = {sp.latex(func_diff)}")
    st.latex(f"∫f(x) dx = {sp.latex(func_int)}")

    # numpy로 변환
    f_lambd = sp.lambdify(x, func, 'numpy')
    f_diff_lambd = sp.lambdify(x, func_diff, 'numpy')

    # 그래프 범위
    X = np.linspace(-10, 10, 400)
    Y = f_lambd(X)
    Y_diff = f_diff_lambd(X)

    # 그래프 그리기
    fig, ax = plt.subplots()
    ax.plot(X, Y, label="f(x)")
    ax.plot(X, Y_diff, label="f'(x)", linestyle="--")
    ax.set_title("함수와 미분 그래프")
    ax.legend()
    st.pyplot(fig)

except Exception as e:
    st.error("함수 입력이 잘못되었습니다. 예: sin(x), x**2 + 3*x + 2")

