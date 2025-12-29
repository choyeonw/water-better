import streamlit as st

# 앱 기본 설정
st.set_page_config(
    page_title="갑천 AI 수질 분석",
    layout="centered"
)

# -------------------------
# 가상 수질 센서 (AI 역할)
# -------------------------
def virtual_water_sensor(location, population, urban, green, sewage, rain):
    bod = 2.0  # 기본 BOD 값

    if location == "하류":
        bod += 1.5

    bod += population * 0.3
    bod += urban * 0.4
    bod -= green * 0.5
    bod -= sewage * 0.4
    bod += rain * 0.2

    if bod < 3:
        grade = "좋음"
    elif bod < 6:
        grade = "보통"
    else:
        grade = "나쁨"

    return round(bod, 2), grade

# -------------------------
# 수질 문제 원인 분석
# -------------------------
def analyze_problem(population, urban, green, sewage, rain):
    problems = []

    if population >= 3:
        problems.append("생활하수 증가로 인한 유기물 오염")

    if urban >= 3:
        problems.append("도시화로 인한 비점오염원 유입")

    if green <= 2:
        problems.append("강변 녹지 부족으로 정화 능력 저하")

    if sewage <= 2:
        problems.append("하수처리 효율 부족")

    if rain >= 3:
        problems.append("강우 시 오염물 유입 증가")

    return problems

# -------------------------
# 행동 가이드 생성
# -------------------------
def action_guide(problems):
    actions = []

    if "생활하수 증가로 인한 유기물 오염" in problems:
        actions.append("생활하수 절약 및 하수처리 시설 관리 강화")

    if "도시화로 인한 비점오염원 유입" in problems:
        actions.append("빗물 정화 시설 확대 및 도로 오염 관리")

    if "강변 녹지 부족으로 정화 능력 저하" in problems:
        actions.append("강변 녹지 확충 및 생태 복원 활동 추진")

    if "하수처리 효율 부족" in problems:
        actions.append("하수 처리 시스템 개선 및 점검 강화")

    if "강우 시 오염물 유입 증가" in problems:
        actions.append("비점오염 저감 시설 설치 및 관리 강화")

    return actions

# -------------------------
# 앱 화면 구성
# -------------------------
st.title("🌊 AI 기반 갑천 가상 수질 센서")
st.write(
    "환경 요인을 입력하면 갑천의 수질 상태를 예측하고, "
    "오염 원인과 수질 보호를 위한 행동을 안내합니다."
)

st.subheader("① 지역 환경 정보 입력")

location = st.selectbox("측정 위치 선택", ["상류", "하류"])

population = st.slider("인구 밀도 (낮음 → 높음)", 1, 5, 3)
urban = st.slider("도시화 비율", 1, 5, 3)
green = st.slider("강변 녹지 비율", 1, 5, 3)
sewage = st.slider("하수 처리 수준", 1, 5, 3)
rain = st.slider("최근 강수량", 1, 5, 3)

# -------------------------
# 분석 실행
# -------------------------
if st.button("수질 분석하기"):
    bod, grade = virtual_water_sensor(
        location, population, urban, green, sewage, rain
    )

    problems = analyze_problem(
        population, urban, green, sewage, rain
    )

    actions = action_guide(problems)

    st.subheader("② 수질 예측 결과")
    st.write(f"• 예상 BOD 수치: **{bod}**")
    st.write(f"• 종합 수질 등급: **{grade}**")

    st.subheader("③ 현재 수질 문제 분석")
    for p in problems:
        st.write("⚠️ " + p)

    st.subheader("④ 수질 보호를 위한 행동 제안")
    for a in actions:
        st.write("🌱 " + a)
