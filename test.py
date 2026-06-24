
  import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from PIL import Image
import random
import time

# ==========================================
# 1. 웹페이지 기본 설정
# ==========================================
st.set_page_config(page_title="초정밀 와꾸 스캐너", page_icon="🧬", layout="centered")

st.title("🧬 [유전자 검사 대용] 내 얼굴 황금비율 & 와꾸 정밀 스캐너 🧬")
st.caption("울산대 의예과 초정밀 알고리즘 탑재 | 관리자 보안 세션 적용")
st.warning("⚠️ **[스캔 전 필독]** 정확한 팩트 폭격을 위해, 얼굴이 기울어지지 않고 **'정면'**에서 **'화면 중앙'**에 꽉 차게 나온 사진을 업로드해 주세요!")
st.markdown("---")

# ==========================================
# 2. 구글 스프레드시트 DB 연결 (Secrets 설정 자동 매핑)
# ==========================================
try:
    # Secrets의 [connections.gsheets] 프로토콜 구조를 지 알아서 연동합니다.
    conn = st.connection("gsheets", type=GSheetsConnection)
    
    # 평소 화면 표시용 로딩 (3초 캐시를 주어 난타로 인한 구글 트래픽 마비 방지)
    display_data = conn.read(worksheet="ranking", ttl="3s")
    if display_data.empty:
        display_data = pd.DataFrame(columns=["name", "score", "gender", "age"])
        
    display_feedback = conn.read(worksheet="feedback", ttl="3s")
    if display_feedback.empty:
        display_feedback = pd.DataFrame(columns=["name", "stars", "text"])
except Exception as e:
    st.error(f"🚨 DB 연결 초기화 실패! Secrets 설정을 확인하세요. 에러: {e}")
    display_data = pd.DataFrame(columns=["name", "score", "gender", "age"])
    display_feedback = pd.DataFrame(columns=["name", "stars", "text"])

# ==========================================
# 3. 사용자 인적사항 입력 구역
# ==========================================
st.subheader("📝 스캔 대상자 인적사항 (명예의 전당 등록용)")
col1, col2, col3 = st.columns(3)

with col1:
    user_name = st.text_input("이름 또는 닉네임", value="홍길동")
with col2:
    gender = st.selectbox("성별 선택", ["남성(Male)", "여성(Female)"])
with col3:
    age = st.number_input("나이 입력", min_value=1, max_value=120, value=20, step=1)

male_db = {"10세 미만": {"얼굴형": "서우진", "눈": "정현준", "코": "문우진", "입": "박다온"}, "10대": {"얼굴형": "라이즈 원빈", "눈": "투어스 신유", "코": "보이넥스트도어 명재현", "입": "앤팀 하루아"}, "20대": {"얼굴형": "차은우", "눈": "서강준", "코": "박보검", "입": "진(BTS)"}, "30대": {"얼굴형": "송중기", "눈": "박서준", "코": "지창욱", "입": "이종석"}, "40대": {"얼굴형": "공유", "눈": "현빈", "코": "조인성", "입": "조정석"}, "50대 이상": {"얼굴형": "이병헌", "눈": "정우성", "코": "장동건", "입": "차승원"}}
female_db = {"10세 미만": {"얼굴형": "오지율", "눈": "구사랑", "코": "박소이", "입": "안소명"}, "10대": {"얼굴형": "뉴진스 해린", "눈": "장원영", "코": "엔믹스 설윤", "입": "베이비몬스터 아현"}, "20대": {"얼굴형": "카리나", "눈": "에스파 윈터", "코": "수지", "입": "아이유"}, "30대": {"얼굴형": "태연", "눈": "한소희", "코": "신세경", "입": "임윤아"}, "40대": {"얼굴형": "송혜교", "눈": "김태희", "코": "한가인", "입": "전지현"}, "50대 이상": {"얼굴형": "김희애", "눈": "이영애", "코": "고소영", "입": "김성령"}}

# ==========================================
# 4. 이미지 업로드 및 초정밀 얼평 알고리즘 가동
# ==========================================
st.subheader("📷 스캔용 낯짝 사진 투척")
uploaded_file = st.file_uploader("얼굴 사진 파일 (PNG, JPG, JPEG)", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption=f"스캔 대기 중인 {user_name}님의 안면 데이터", use_container_width=True)
    
    if st.button("🔥 와꾸 스캔 및 의학적 팩폭 솔루션 시작"):
        with st.spinner("슈퍼컴퓨터가 당신의 이목구비를 소수점 단위로 뜯어내고 있습니다..."):
            time.sleep(1.2)
        
        if age < 10: age_group, bonus = "10세 미만", 3.5
        elif age < 20: age_group, bonus = "10대", 2.0
        elif age < 30: age_group, bonus = "20대", 1.0
        elif age < 40: age_group, bonus = "30대", 0.0
        elif age < 50: age_group, bonus = "40대", -1.0
        else: age_group, bonus = "50대 이상", -2.5

        is_male = "남성" in gender
        
        random.seed(len(user_name) + age + int(uploaded_file.size % 500))
        base_score = random.uniform(80.0, 96.0)
        final_score = round(base_score + bonus, 1)
        final_score = max(55.0, min(99.9, final_score))
        
        # 🚨 [리셋 방지 실시간 검증 트랩] 업로드 클릭 시 순간적으로 라이브 데이터를 직접 동기화
        try:
            realtime_data = conn.read(worksheet="ranking", ttl="0s")
        except Exception as e:
            st.error("🚨 구글 서버 트래픽 초과로 순간 연결이 유실되었습니다. 기존 데이터 보존을 위해 처리가 차단되었으니 1~2초 후 다시 눌러주세요!")
            st.stop()
            
        new_record = pd.DataFrame([{"name": user_name, "score": final_score, "gender": gender, "age": age}])
        updated_df = pd.concat([realtime_data, new_record], ignore_index=True)
        
        try:
            conn.update(worksheet="ranking", data=updated_df)
            display_data = updated_df  # 화면에 실시간으로 반영
        except Exception as e:
            st.error(f"🚨 구글 시트 랭킹 저장 실패! 에러: {e}")

        all_records = display_data.sort_values(by="score", ascending=False).reset_index(drop=True)
        my_rank = all_records[all_records["name"] == user_name].index[0] + 1 if not all_records.empty else 1
        total_players = len(all_records)
        top_percent = round((my_rank / total_players) * 100, 1) if total_players > 0 else 100.0
        if top_percent == 0: top_percent = 0.1

        db = male_db if is_male else female_db

        st.success(f"🎯 {user_name}님의 와꾸 스캔 완료!")
        col_res1, col_res2 = st.columns(2)
        with col_res1:
            st.metric(label="✨ 종합 안면 황금비 스코어", value=f"{final_score} / 100점")
        with col_res2:
            st.metric(label="🏆 실제 참여자 중 당신의 위치", value=f"상위 {top_percent}%", delta=f"{total_players}명 중 {my_rank}등")

        st.markdown("### 📊 부위별 정밀 분석 결과 및 닮은꼴")
        st.info(f"**👤 얼굴형:** `{db[age_group]['얼굴형']}`과 윤곽 흡사. 턱 보톡스 및 인모드 리프팅 추천.")
        st.info(f"**👁️ 눈( 
