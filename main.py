# mbti_job_recommender.py
import streamlit as st

# MBTI별 직업 추천 데이터
mbti_jobs = {
    "INTJ": ["전략 컨설턴트", "데이터 과학자", "정책 분석가"],
    "INTP": ["연구원", "소프트웨어 개발자", "발명가"],
    "ENTJ": ["기업 경영자", "프로젝트 매니저", "변호사"],
    "ENTP": ["기업가", "마케팅 전문가", "기술 혁신가"],
    "INFJ": ["심리학자", "작가", "사회복지사"],
    "INFP": ["예술가", "상담가", "작곡가"],
    "ENFJ": ["교육자", "코치", "비영리 단체 리더"],
    "ENFP": ["광고 기획자", "방송 작가", "여행 기획자"],
    "ISTJ": ["회계사", "행정 공무원", "품질 관리자"],
    "ISFJ": ["간호사", "초등교사", "인사 관리자"],
    "ESTJ": ["군 장교", "운영 관리자", "재무 분석가"],
    "ESFJ": ["호텔 매니저", "영업 관리자", "행사 기획자"],
    "ISTP": ["엔지니어", "정비사", "파일럿"],
    "ISFP": ["그래픽 디자이너", "사진작가", "요리사"],
    "ESTP": ["영업 사원", "이벤트 플래너", "구조 대원"],
    "ESFP": ["배우", "MC", "패션 디자이너"],
}

# 앱 제목
st.title("💼 MBTI별 직업 추천")

# 사용자가 MBTI 선택
mbti = st.selectbox("당신의 MBTI를 선택하세요", list(mbti_jobs.keys()))

# 선택한 MBTI에 맞는 직업 추천
if mbti:
    st.subheader(f"{mbti} 유형 추천 직업")
    for job in mbti_jobs[mbti]:
        st.write(f"- {job}")

# 추가 기능: 랜덤 추천 버튼
if st.button("랜덤 MBTI 추천 받기"):
    import random
    random_mbti = random.choice(list(mbti_jobs.keys()))
    st.success(f"추천 MBTI: {random_mbti}")
    st.write("추천 직업:")
    for job in mbti_jobs[random_mbti]:
        st.write(f"- {job}")

