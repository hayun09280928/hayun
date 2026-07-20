import matplotlib.pyplot as plt
import streamlit as st

# --- 1. 사이드바 (기본 설정) ---
with st.sidebar:
    st.header("🧪 실험실 프로필")
    user_name = st.text_input("실험자 이름", value="학생", key="user_name")
    exp_temp = st.selectbox(
        "실험실 온도는 몇 도인가요?",
        ["20°C (기본)", "25°C (표준)", "30°C (고온)"],
        key="exp_temp",
    )
    st.markdown("---")
    st.info(f"반가워요, {user_name}님! 현재 실험실 환경은 '{exp_temp}'입니다.")

# --- 2. 메인 타이틀 ---
st.title("🧪 AI 화학 중화반응 시뮬레이터")
st.write(
    "사이드바에서 실험자 이름을 확인하고 용액을 조합하여 중화반응을 관찰해보세요!"
)

# --- 3. 용액 조합하기 (컬럼 활용) ---
st.header("🧪 용액 조합하기")
col1, col2 = st.columns(2)

with col1:
    st.subheader("🔴 산성 용액 (Acid)")
    acid_type = st.radio(
        "산 종류",
        ["HCl (염산)", "H2SO4 (황산)"],
        key="acid_type",
    )
    acid_conc = st.select_slider(
        "농도 (M)",
        options=["0.5M", "1.0M", "2.0M"],
        value="1.0M",
        key="acid_conc",
    )
    acid_vol = st.slider("산 부피 (mL)", 10, 50, 20, key="acid_vol")

with col2:
    st.subheader("🔵 염기성 용액 (Base)")
    base_type = st.radio("염기 종류", ["NaOH (수산화 나트륨)"], key="base_type")
    base_conc = st.select_slider(
        "농도 (M)",
        options=["0.5M", "1.0M", "2.0M"],
        value="1.0M",
        key="base_conc",
    )
    base_vol = st.slider("추가할 염기 부피 (mL)", 0, 50, 10, key="base_vol")

# --- 4. 디테일 설정 (탭 활용) ---
st.header("🔍 상세 반응 조건 설정")
tab1, tab2 = st.tabs(["지시약 선택", "이온 수 분석 관찰"])

with tab1:
    st.write("용액의 색 변화를 확인할 지시약을 선택하세요:")
    indicator = st.selectbox(
        "지시약 선택",
        ["BTB 용액", "페놀프탈레인 용액", "메틸 오렌지"],
        key="indicator",
    )
    with st.expander("💡 지시약 선택 팁 보기"):
        st.info(
            "BTB 용액은 산성(노란색), 중성(초록색), 염기성(파란색)으로 변화가 가장 명확해요!"
        )

with tab2:
    st.write("중화열 및 이온 수 변화 관찰 옵션:")
    show_graph = st.checkbox("중화반응 그래프 표시하기", value=True)
    with st.expander("💡 중화점 팁 보기"):
        st.warning("H+와 OH-가 1:1로 정확히 반응하는 지점이 바로 중화점입니다.")
        st.markdown("---")

# --- 5. 반응 실행 및 결과 출력 ---
if st.button("🧪 중화반응 실행하기"):
    with st.container(border=True):
        st.subheader(f"🧪 {user_name}님의 중화반응 실험 결과")

        # 몰 농도 계산을 위한 단순 수치 변환
        c_a = float(acid_conc.replace("M", ""))
        c_b = float(base_conc.replace("M", ""))

        # 가수 적용 (H2SO4는 2가 산)
        n_a = 2 if "H2SO4" in acid_type else 1
        n_b = 1  # NaOH는 1가 염기

        # H+ 및 OH- 몰 수 계산 (가수 * 농도 * 부피)
        h_moles = n_a * c_a * acid_vol
        oh_moles = n_b * c_b * base_vol

        # 액성 판정
        if h_moles > oh_moles:
            acidity = "산성 🔴"
            color_btb = "노란색 💛"
        elif oh_moles > h_moles:
            acidity = "염기성 🔵"
            color_btb = "파란색 💙"
        else:
            acidity = "중성 🟢 (중화점 달성!)"
            color_btb = "초록색 💚"

        st.write(
            f"선택한 조건: **{acid_type} ({acid_vol}mL)** + **{base_type} ({base_vol}mL)**"
        )
        st.write(f"* **현재 용액의 액성:** {acidity}")
        st.write(f"* **{indicator} 색상:** {color_btb}")

        # 그래프 출력
        if show_graph:
            # 이온 수 계산
            rem_h = max(0, h_moles - oh_moles)
            rem_oh = max(0, oh_moles - h_moles)
            cl_ion = h_moles
            na_ion = oh_moles

            fig, ax = plt.subplots()
            ions = ["H+", "OH-", "Cl-/SO42-", "Na+"]
            counts = [rem_h, rem_oh, cl_ion, na_ion]
            colors = ["crimson", "dodgerblue", "gray", "skyblue"]

            ax.bar(ions, counts, color=colors)
            ax.set_ylabel("이온의 상대적 양")
            ax.set_title("혼합 용액 내 이온 수 변화")
            st.pyplot(fig)

        st.success(
            "중화반응 관찰이 완료되었습니다! 반응 전후의 이온 수 변화를 비교해보세요."
        )

    with st.expander("📹 중화반응 개념 이해 영상 보기"):
        st.video("https://www.youtube.com/watch?v=S86FmRW7SHc")
        st.write("통합과학 2 산·염기 중화반응 핵심 개념을 다시 복습해보세요.")

# --- 6. 리셋 함수 정의 ---
def reset_all():
    st.session_state.user_name = "학생"
    st.session_state.exp_temp = "20°C (기본)"
    st.session_state.acid_type = "HCl (염산)"
    st.session_state.acid_conc = "1.0M"
    st.session_state.acid_vol = 20
    st.session_state.base_type = "NaOH (수산화 나트륨)"
    st.session_state.base_conc = "1.0M"
    st.session_state.base_vol = 10
    st.session_state.indicator = "BTB 용액"


st.button("🔄 전체 실험 조건 초기화", on_click=reset_all)
