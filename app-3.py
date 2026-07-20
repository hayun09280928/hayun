import streamlit as st
import time

def reset_game():
    # 게임 상태 초기화
    st.session_state.start_time = 0
    st.session_state.end_time = 0
    st.session_state.result = 0

# session_state 초기화
if 'start_time' not in st.session_state:
    reset_game()

st.title("10초 맞추기 게임! ⏱️")
st.write("시작 버튼을 누르고, 마음속으로 10초를 센 뒤 종료 버튼을 누르세요.")

col1, col2 = st.columns(2)
with col1:
    if st.button("시작", use_container_width=True):
        st.session_state.start_time = time.time() # 현재 시각 기록
        st.session_state.end_time = 0             # 종료 시간 초기화
        st.success("시간이 가고 있습니다... 마음속으로 10초를 세세요!")

with col2:
    if st.button("종료", use_container_width=True):
        # 시작 버튼을 누른 상태일 때만 작동 (0이 아닐 때)
        if st.session_state.start_time != 0:
            st.session_state.end_time = time.time()
            # 걸린 시간 계산 (종료 시간 - 시작 시간)
            st.session_state.result = st.session_state.end_time - st.session_state.start_time
                 st.session_state.start_time = 0 
        else:
            st.warning("시작 버튼을 먼저 눌러주세요! (이미 종료되었거나 아직 시작하지 않음)")

# 결과 출력 영역 (종료 시간이 기록되었을 때만 출력)
if st.session_state.end_time != 0:
    diff = st.session_state.result
    st.header(f"결과: {diff:.2f}초")
    
    if 9.7 <= diff <= 10.3:
        st.success("🎉 대단해요! 정확합니다!")
    else:
        st.error(f"❌ 10초와 {abs(10-diff):.2f}초 차이가 납니다. 다시 도전해보세요!")

st.button("다시 하기", on_click=reset_game)
