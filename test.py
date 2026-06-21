import streamlit as st
from PIL import Image
import random
import time

# ==========================================
# 0. 전역 서버 데이터베이스 초기화 (가상 데이터 완전 삭제)
# ==========================================
# 처음 실행 시에는 랭킹 리스트를 텅 빈 공란([])으로 시작합니다.
if "leaderboard" not in st.session_state:
    st.session_state.leaderboard = []

# 피드백 수집함도 마찬가지로 빈 상태로 시작합니다.
if "feedback_db" not in st.session_state:
    st.session_state.feedback_db = []

# ==========================================
# 1. 웹페이지 기본 설정 및 테마
# ==========================================
st.set_page_config(page_title="초정밀 와꾸 스캐너", page_icon="🧬", layout="centered")

st.title("🧬 [유전자 검사 대용] 내 얼굴 황금비율 & 와꾸 정밀 스캐너 🧬")
st.caption("울산대 의예과 초정밀 알고리즘 탑재 | 관리자 보안 세션 적용")

st.warning("⚠️ **[스캔 전 필독]** 정확한 팩트 폭격을 위해, 얼굴이 기울어지지 않고 **'정면'**에서 **'화면 중앙'**에 꽉 차게 나온 사진을 업로드해 주세요!")
st.markdown("---")

# ==========================================
# 2. 사용자 변수 입력 구역
# ==========================================
st.subheader("📝 스캔 대상자 인적사항 (명예의 전당 등록용)")
col1, col2, col3 = st.columns(3)

with col1:
    user_name = st.text_input("이름 또는 닉네임", value="홍길동")
with col2:
    gender = st.selectbox("성별 선택", ["남성(Male)", "여성(Female)"])
with col3:
    age = st.number_input("나이 입력", min_value=1, max_value=120, value=20, step=1)

# 데이터베이스
male_db = {"10세 미만": {"얼굴형": "서우진", "눈": "정현준", "코": "문우진", "입": "박다온"}, "10대": {"얼굴형": "라이즈 원빈", "눈": "투어스 신유", "코": "보이넥스트도어 명재현", "입": "앤팀 하루아"}, "20대": {"얼굴형": "차은우", "눈": "서강준", "코": "박보검", "입": "진(BTS)"}, "30대": {"얼굴형": "송중기", "눈": "박서준", "코": "지창욱", "입": "이종석"}, "40대": {"얼굴형": "공유", "눈": "현빈", "코": "조인성", "입": "조정석"}, "50대 이상": {"얼굴형": "이병헌", "눈": "정우성", "코": "장동건", "입": "차승원"}}
female_db = {"10세 미만": {"얼굴형": "오지율", "눈": "구사랑", "코": "박소이", "입": "안소명"}, "10대": {"얼굴형": "뉴진스 해린", "눈": "장원영", "코": "엔믹스 설윤", "입": "베이비몬스터 아현"}, "20대": {"얼굴형": "카리나", "눈": "에스파 윈터", "코": "수지", "입": "아이유"}, "30대": {"얼굴형": "태연", "눈": "한소희", "코": "신세경", "입": "임윤아"}, "40대": {"얼굴형": "송혜교", "눈": "김태희", "코": "한가인", "입": "전지현"}, "50대 이상": {"얼굴형": "김희애", "눈": "이영애", "코": "고소영", "입": "김성령"}}

# ==========================================
# 3. 이미지 업로드 및 알고리즘 가동
# ==========================================
st.subheader("📷 스캔용 낯짝 사진 투척")
uploaded_file = st.file_uploader("얼굴 사진 파일 (PNG, JPG, JPEG)", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption=f"스캔 대기 중인 {user_name}님의 안면 데이터", use_container_width=True)
    
    if st.button("🔥 와꾸 스캔 및 의학적 팩폭 솔루션 시작"):
        with st.spinner("슈퍼컴퓨터가 당신의 이목구비를 소수점 단위로 뜯어내고 있습니다..."):
            time.sleep(1.0)
        
        if age < 10: age_group, age_comment, bonus = "10세 미만", "영유아기 특유의 젖살 볼륨감과", 3.5
        elif age < 20: age_group, age_comment, bonus = "10대", "생기 넘치는 피부 톤과 균형 잡힌", 2.0
        elif age < 30: age_group, age_comment, bonus = "20대", "골격 구조가 완성되어 가장 입체적인", 1.0
        elif age < 40: age_group, age_comment, bonus = "30대", "성숙함과 세련미가 공존하며 깊이를 더하는", 0.0
        elif age < 50: age_group, age_comment, bonus = "40대", "기품 있는 중안부의 안정감과", -1.0
        else: age_group, age_comment, bonus = "50대 이상", "세월의 연륜이 묻어나는 중후한 아우라와", -2.5

        is_male = "남성" in gender
        random.seed(len(user_name) + age + int(uploaded_file.size % 500))
        base_score = random.uniform(80.0, 96.0)
        final_score = round(base_score + bonus, 1)
        final_score = max(55.0, min(99.9, final_score))
        
        new_record = {"name": user_name, "score": final_score, "gender": gender, "age": age}
        st.session_state.leaderboard.append(new_record)
        
        all_records = sorted(st.session_state.leaderboard, key=lambda x: x["score"], reverse=True)
        my_rank = all_records.index(new_record) + 1
        total_players = len(all_records)
        top_percent = round((my_rank / total_players) * 100, 1)
        if top_percent == 0: top_percent = 0.1

        db = male_db if is_male else female_db

        # 결과 출력
        st.success(f"🎯 {user_name}님의 와꾸 스캔 완료!")
        col_res1, col_res2 = st.columns(2)
        with col_res1:
            st.metric(label="✨ 종합 안면 황금비 스코어", value=f"{final_score} / 100점")
        with col_res2:
            st.metric(label="🏆 실제 참여자 중 당신의 위치", value=f"상위 {top_percent}%", delta=f"{total_players}명 중 {my_rank}등")

        st.markdown("### 📊 부위별 정밀 분석 결과 및 닮은꼴")
        st.info(f"**👤 얼굴형:** `{db[age_group]['얼굴형']}`과 윤곽 흡사. 턱 보톡스 및 인모드 리프팅 추천.")
        st.info(f"**👁️ 눈(Eye):** `{db[age_group]['눈']}`과 눈매 흡사. 비절개 눈매 교정 고려.")
        st.info(f"**👃 코(Nose):** `{db[age_group]['코']}`와 콧대 라인 일치. 하이코 필러 및 코끝 연골 묶기 시술 추천.")
        st.info(f"**👄 입(Lip):** `{db[age_group]['입']}`과 입술 볼륨 유사. 입술 필러+입꼬리 보톡스 밸런스 추천.")

# ==========================================
# 4. 실시간 피드백 및 설문조사 작성란 (유저용)
# ==========================================
st.markdown("---")
st.subheader("💬 프로그램 피드백 및 후기 남기기")

with st.expander("💌 분석 결과에 대한 정확성 평가 및 후기 작성란 열기"):
    st.write(f"**{user_name}**님, AI의 팩폭 진단이 얼마나 정확했나요?")
    accuracy_stars = st.slider("1) 진단의 정확성 평점 (5점 만점)", min_value=1, max_value=5, value=5, step=1)
    user_review = st.text_area("2) 주관식 한줄평 및 개선점 피드백을 남겨주세요")
    
    if st.button("🚀 설문 데이터 최종 제출하기"):
        if user_review.strip() == "":
            st.error("후기 내용을 입력해 주세요!")
        else:
            fb_record = {"name": user_name, "stars": accuracy_stars, "text": user_review}
            st.session_state.feedback_db.append(fb_record)
            st.success("🎉 설문조사가 성공적으로 제출되었습니다!")

# ==========================================
# 5. 결과 페이지 최하단 2단 레이아웃
# ==========================================
st.markdown("---")
col_bottom1, col_bottom2 = st.columns(2)

# [왼쪽] 명예의 전당 (💥 공란 보정 로직 가동)
with col_bottom1:
    st.subheader("🏆 명예의 전당 (TOP 3)")
    
    # 누적 기록을 정렬
    top_records = sorted(st.session_state.leaderboard, key=lambda x: x["score"], reverse=True)
    
    # 1, 2, 3위에 대해 순회하면서 데이터가 있으면 출력, 없으면 공란 표시
    for rank in range(1, 4):
        medal = "🥇" if rank == 1 else "🥈" if rank == 2 else "🥉"
        
        if len(top_records) >= rank:
            # 실제 데이터가 존재하는 경우
            p = top_records[rank - 1]
            st.markdown(f"> **{medal} {rank}등: {p['name']}** ({p['score']}점)")
        else:
            # 💥 데이터가 아직 채워지지 않은 공란인 경우
            st.markdown(f"> **{medal} {rank}등:** `아직 등록된 기록이 없습니다.`")

# [오른쪽] 잠금형 비밀 피드백 보관함
with col_bottom2:
    st.subheader("🔒 개발자 전용 피드백 비밀기지")
    admin_password = st.text_input("마스터 비밀번호를 입력하세요", type="password", placeholder="Password...")
    
    if admin_password == "shutainz1718":
        if len(st.session_state.feedback_db) == 0:
            st.info("🔓 인증 성공! 아직 수집된 피드백 데이터가 없습니다.")
        else:
            st.success("🔓 인증 성공! 실시간 데이터 수집 현황을 오픈합니다.")
            for fb in reversed(st.session_state.feedback_db):
                st.markdown(f"> **{fb['name']}** (평점: {'⭐' * fb['stars']})\n> *\"{fb['text']}\"*\n> ---")
    elif admin_password != "":
        st.error("❌ 비밀번호가 올바르지 않습니다. 접근 권한이 없습니다.")
