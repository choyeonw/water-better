import streamlit as st
import numpy as np
import pandas as pd

from sklearn.ensemble import IsolationForest, RandomForestRegressor
from sklearn.linear_model import LinearRegression

# =========================
# 1. 가상 수질 데이터 생성
# =========================
def generate_virtual_data(n=200):
    np.random.seed(42)
    data = pd.DataFrame({
        "pH": np.random.normal(7.2, 0.5, n),
        "turbidity": np.random.normal(15, 5, n),
        "temperature": np.random.normal(18, 4, n),
    })

    # 가상의 수질 지표 (BOD 유사 개념)
    data["water_index"] = (
        0.4 * abs(data["pH"] - 7)
        + 0.03 * data["turbidity"]
        + 0.02 * data["temperature"]
        + np.random.normal(0, 0.3, n)
    )
    return data


# =========================
# 2. AI 모델 클래스 정의
# =========================
class WaterQualityAI:
    def __init__(self):
        # 이상 탐지 모델
        self.anomaly_model = IsolationForest(contamination=0.1, random_state=42)

        # 예측 모델 (해석 가능한 회귀)
        self.predict_model = RandomForestRegressor(random_state=42)

        self.is_trained = False

    def train(self, data: pd.DataFrame):
        X = data[["pH", "turbidity", "temperature"]]
        y = data["water_index"]

        # 모델 학습
        self.anomaly_model.fit(X)
        self.predict_model.fit(X, y)

        self.is_trained = True

    def analyze(self, input_vector):
        """
        input_vector: [pH, turbidity, temperature]
        """
        X_input = np.array(input_vector).reshape(1, -1)

        if not self.is_trained:
            return {
                "status": "모델이 아직 학습되지 않았습니다.",
                "anomaly": "판단 불가",
                "prediction": None
            }

        anomaly_score = self.anomaly_model.predict(X_input)[0]
        prediction = self.predict_model.predict(X_input)[0]

        return {
            "status": "분석 완료",
            "anomaly": "이상" if anomaly_score == -1 else "정상",
            "prediction": round(prediction, 2)
        }


# =========================
# 3. Streamlit UI
# =========================
st.set_page_config(page_title="갑천 AI 수질 분석 시스템", layout="centered")

st.title("🌊 AI 기반 갑천 수질 분석·예측 시스템")
st.write("""
이 시스템은 **실제 센서 없이도 실행 가능한 AI 모델**을 기반으로  
갑천의 수질 상태를 분석하고, 다음 시점의 수질 변화를 예측합니다.
""")

# AI 모델 준비
ai = WaterQualityAI()

# 가상 데이터 생성 & 학습
virtual_data = generate_virtual_data()
ai.train(virtual_data)

# =========================
# 4. 사용자 입력
# =========================
st.subheader("📥 수질 데이터 입력 (1시점)")

pH = st.slider("pH", 4.0, 10.0, 7.0)
turbidity = st.slider("탁도 (NTU)", 0.0, 50.0, 15.0)
temperature = st.slider("수온 (℃)", 0.0, 35.0, 18.0)

if st.button("🔍 AI 분석 실행"):
    result = ai.analyze([pH, turbidity, temperature])

    st.subheader("📊 분석 결과")

    if result["prediction"] is None:
        st.warning(result["status"])
    else:
        st.write(f"**현재 수질 상태:** {result['anomaly']}")
        st.write(f"**다음 시점 수질 예측 지표:** {result['prediction']}")

        # 행동 제안
        st.subheader("🌱 수질 보호 행동 제안")

        if result["anomaly"] == "이상":
            st.error("""
- 생활하수 및 오염원 유입 가능성 증가  
- 상류 쓰레기 관리 및 하수 처리 점검 필요  
- 지역 주민 참여 하천 정화 활동 권장
""")
        else:
            st.success("""
- 현재 수질은 비교적 안정적  
- 정기 모니터링 유지  
- 생태 보전 중심의 하천 이용 필요
""")

# =========================
# 5. 프로젝트 의미
# =========================
st.markdown("---")
st.subheader("📌 프로젝트 의의")
st.write("""
- 실제 센서 없이도 **AI 구조 설계 능력**을 증명  
- 이상 탐지 + 예측 모델 분리 설계  
- 향후 IoT 센서와 바로 연동 가능한 구조  
- 학생·주민 참여형 환경 협력 모델로 확장 가능
""")
