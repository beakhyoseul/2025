# mbti_job_recommender_search.py
import streamlit as st
import random

# MBTI별 데이터 (설명 + 이미지 + 직업)
mbti_data = {
    "INTJ": {
        "desc": "전략적 사고와 계획 능력이 뛰어난 마스터마인드형",
        "jobs": ["전략 컨설턴트", "데이터 과학자", "정책 분석가"],
        "img": "https://i.ibb.co/5cPbjvY/intj.png"
    },
    "INFP": {
        "desc": "가치 중심적이고 창의적인 중재자형",
        "jobs": ["예술가", "상담가", "작곡가"],
        "img": "https://i.ibb.co/Dg7TGhM/infp.png"
    },
    "ENTP": {
        "desc": "도전과 변화를 즐기는 발명가형",
        "jobs": ["기업가", "마케팅 전문가", "기술 혁신가"],
        "img": "https://i.ibb.co/F4cPjS3/entp.png"
    },
    "ESFJ": {
        "desc": "친절하고 협력적인 외교관형",
        "jobs": ["호텔 매니저", "영업 관리자", "행사 기획자"],
        "img": "https://i.ibb.co/LnW1nQj/esfj.png"
    },
    # 나머지 MBTI들도 동일하게 추가 가능
}

# 페이지 설정
st.set_page_config(page_title="MBTI 직업 추천", page_icon="💼")

# 제목
st.title("💼 MBTI별 직업 추천")
st.write("MBTI를 입력하거나 선택해서 직업 추천을 받아보세요!")

# 검색 입력
search_input = st.text_input("MBTI를 입력하세요 (예: INFP)").upper()

# 드롭다운 선택
selected_mbti = st.selectbox("또는 MBTI 선택", list(mbti_data.keys()))

# 검색 값이 우선
if search_input in mbti_data:
    mbti = search_input
else:
    mbti = selected_mbti

# MBTI 정보 표시
if mbti in mbti_data:
    info = mbti_data[mbti]
    st.image(info["img"], width=200)
    st.subheader(f"{mbti} - {info['desc']}")
    st.write("**추천 직업:**")
    for job in info["jobs"]:
        st.write(f"- {job}")

# 랜덤 추천 버튼
if st.button("🎲 랜덤 MBTI 추천"):
    random_mbti = random.choice(list(mbti_data.keys()))
    st.success(f"오늘의 랜덤 MBTI: {random_mbti}")
    r_info = mbti_data[random_mbti]
    st.image(r_info["img"], width=200)
    st.subheader(f"{random_mbti} - {r_info['desc']}")
    for job in r_info["jobs"]:
        st.write(f"- {job}")
