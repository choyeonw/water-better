import streamlit as st
import numpy as np
import pandas as pd

from sklearn.ensemble import IsolationForest, RandomForestRegressor
from sklearn.preprocessing import MinMaxScaler

# =========================
# 1. 가상 수질 데이터 생성
# =========================
def generate_virtual_data(n=300):
    np.random.seed(42)

    temperature = np.random.normal(18, 4, n).clip(0, 35)
    turbidity = np.random.normal(15, 6, n).clip(0, 60)
    pH = np.random.normal(7.2, 0.4, n).clip(5.5, 9.5)

    data = pd.DataFrame({
        "pH": pH,
        "turbidity": turbidity,
        "temperature": temperature
    })

    # 종합 수질 지표 (BOD 유사 개념, 정책 시연용)
    data["water_index"] = (
        0.45 * abs(data["pH"] - 7)
        + 0.035 * data["turbidity"]
        + 0.02 * data["temperature"]
        + np.random.normal(0, 0.25, n)
    )

    return data


# =========================
# 2. AI 모델 클래스
# =========================
class WaterQualityAI:
    def __init__(self):
        self.scaler = MinMaxScaler()

        self.anomaly_model = IsolationForest(
            contamination=0.08,
            random_state=42
        )

        self.predict_model = RandomForestRegressor(
            n_estimators=200,
            random_state=42
        )

        self.is_trained = False

    def train(self, data: pd.DataFrame):
        X = data[["pH", "turbidity", "temperature"]]
        y = data["water_index"]

        X_scaled = self.scaler.fit_transform(X)

        self.anomaly_model.fit(X_scaled)
        self.predict_model.fit(X_scaled, y)

        self.is_trained = True

    def analyze(self, input_vector):
        X_input = np.array(input_vector).reshape(1, -1)
        X_scaled = self.scaler.transform(X_input)

        anomaly_score = self.anomaly_model.decision_function(X_scaled)[0]
        anomaly_label = self.anomaly_model.predict(X_scaled)[0]

        prediction = self.predict_model.predict(X_scaled)[0]

        return {
            "anomaly_score": round(anomaly_score, 3),
            "anomaly_label": "이상" if anomaly_label == -1 else "정상",
            "prediction": round(prediction, 2),
            "feature_importance": dict(
                zip(
                    ["pH", "탁도", "수온"],
                    self.predict_model.feature_importances_.round(3)
                )
            )
        }


# =========================
# 3. Streamlit UI
# =========================
st.set_page_config(
    page_title="AI 기반 갑천 수질 분석 시스템",
    layout="centered"
)

st.title("AI 기반 갑천 수질 분석·예측 시스템")

st.write("""
본 시스템은 **실제 센서가 없더라도 정책 제안 및 기술 검증이 가능하도록 설계된**
AI 기반 수질 분석 모델입니다.
""")

# 세션 상태로 AI 유지
if "ai_model" not in st.session_state:
    ai = WaterQualityAI()
    virtual_data = generate_virtual_data()
    ai.train(virtual_data)
    st.session_state.ai_model = ai
else:
    ai = st.session_state.ai_model


# =========================
# 4. 사용자 입력
# =========================
st.subheader("가상 수질 데이터 입력 (1 시점)")

pH = st.slider("pH", 5.5, 9.5, 7.2)
turbidity = st.slider("탁도 (NTU)", 0.0, 60.0, 15.0)
temperature = st.slider("수온 (℃)", 0.0, 35.0, 18.0)

if st.button("🔍 AI 분석 실행"):
    result = ai.analyze([pH, turbidity, temperature])

    st.subheader("AI 분석 결과")

    st.write(f"**이상 탐지 결과:** {result['anomaly_label']}")
    st.write(f"**이상 점수:** {result['anomaly_score']}")
    st.write(f"**예측 수질 지표:** {result['prediction']}")

    st.subheader("AI 판단 근거 (영향 요인)")
    for k, v in result["feature_importance"].items():
        st.write(f"- {k}: {v}")

    st.subheader("정책적 해석")

    if result["anomaly_label"] == "이상":
        st.error("""
- 단기적 오염원 유입 가능성 존재  
- 상류 지점 집중 모니터링 필요  
- 시민 신고·현장 조사 연계 권장
""")
    else:
        st.success("""
- 현재 수질은 안정 범위  
- 기존 관리 정책 유지 가능  
- 정기적 데이터 축적을 통한 장기 예측 권장
""")
