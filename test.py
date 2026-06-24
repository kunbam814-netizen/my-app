import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from PIL import Image
import random
import time
import json
import os

# ==========================================
# 1. 구글 서비스 계정 (절대 안 깨지는 파일 강제 생성 방식)
# ==========================================
SERVICE_ACCOUNT_DICT = {
  "type": "service_account",
  "project_id": "genial-current-500412-h0",
  "private_key_id": "e7e0b521621e3ec062abe8e3aa02241e1cfd8d5f",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQDPEYCa9PslQ7i2\n7gKXMyBVgifbtWrNUBp0CixND2QG9HY+WZTBf6l/MLL4KjuZVpU01VM1uiNJmor4\nsg5QXKNNHVtPmfKpAJeyW9RQd8HeV8IIoOgnfwO+DLF55cvwoDWcsJ7P1m9eJM18\nxftCu9NWMgpALwlbbuwUbSSxY+o2p2HHagFhuR/ElARYaLWWWerL/BqzKlLfZL7c\naUEgDr5KWt+qGkbqhul9bYm75u0hZ1ta98oXIdvge/erJ/nUinwA9/yn5hY+CA95\n/uM0GtRi8bOUB7xZfoVZc0HXYj1LK2P9JWMi9/TQyu+LcuOPMZ7LbHTHzaisows3\n8CEdINSbAgMBAAECggEAQIA8tcgzBTAbtUvdnbiszUX+YXeY/byCiPv0QcrWBz6W\nKKTh7AZ2x2pljV0mdITedHcw9M73GAHeYUqhn9HDgo1u+JRFXPSUzFfDgo9TYg2n\nIOXyev8bLNOqYwS8aseU+6qexbIPvd0r7z6Cno6Abdynice9G/Co9FHtOJ6dgglA\n5hj4qKpsn4N1yEpL5Jl8K4M/p6crXUb49ToN+V+BbnSo+iOl/7RPFU6AZMM5u4gA\nRuRVTHOsbv8oyq6lQHsFtoPB3iwInss5bdI4N1fo73LZ78ZXanmWmWv9GhoQE2FJ\nPF75/a/RsmEYXyxKUMwrQWnN54llEifortUYW1Hi/QKBgQD3C+a12IyU7XiiznA7\nkG3C20UTcXUFXDy1FYkpqpKIHDVv+67FARk7BDVw0k7LaNtSN1ZCo1JoCTdjjGmE\ncIZMfMnALv4QybBOOWOUwE5jtlY5D26F2CHvZg2HgBTGJh4/5+NbBNtE6sC2X7Ou\nzSButNk5/wYdEvXryl3A3ttldQKBgQDWkq8U90GbKXgmJVdvLvr2Zo/GlRIeP9Sj\nI828loQe4ZgQ8xm869A/2xTAIajaoLfHKsI2ZvAz0k6enj8NSZQP5V+B/T/kdq73\n8gqBYH3UOCmfQ+G8eTxRseFnhmhOJt8Sy2Z7M9CqBv95KnwN0EzkAAPETq9sTkqq\niEqQCno/zwKBgQCHJoafowk9jDB7+K3jmB7EBArlGSOovA4mDtML7VnehnghfDHf\nartv0tydjSA4HXQmpUlWiVzSt4AKwM0U/C4sd/QzZEHv0zbVhIXa4d3ApQbEjpGr\nPVNLUaxDHam/wSi5U1XI/H4sVLT60J5PGb8NcXiJRuAEVdQdm4bwtbqW5QKBgQCb\noTyX6laNYeChWkg2fk7MVMtHb2v6wLVLtnZMqKcfduTCtnAelLMw/YfpawB7wkJJ\nlPvUVYk3LPyVE5YL3ygi92z0bWjgHiz97XItMH1TZYDa4XNjLlPPtUMVwWj59jup\n+BlWlthr2jOGAIiFxGVgoZoZ0jBuT8LcOYpLOy48BQKBgGZ402JyLOk8yK4hrmaQ\nhKv0t46kprXD9RLNr0/hKqVAycSK6r74VbFENGiL06w+7t4beR6wfOIVuRmGp2YQ\nxdKbtep1TeTKMI8Ntp4/B7e2tax2wq9kpOrJEbzYmqOsRAXX7TcdjFJXPa4W4c6Z\ni2XkR4YNG+eF47iefr8bOP/y\n-----END PRIVATE KEY-----",
  "client_email": "bot-532@genial-current-500412-h0.iam.gserviceaccount.com",
  "client_id": "114486457354616821244",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/bot-532%40genial-current-500412-h0.iam.gserviceaccount.com",
  "universe_domain": "googleapis.com"
}

# 딕셔너리를 임시 파일로 만들어서 구글 공식 환경변수에 등록 (에러 원천 차단)
with open("google_key.json", "w") as f:
    json.dump(SERVICE_ACCOUNT_DICT, f)
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "google_key.json"

# ==========================================
# 2. 웹페이지 기본 설정 및 DB 자동 연결
# ==========================================
st.set_page_config(page_title="초정밀 와꾸 스캐너", page_icon="🧬", layout="centered")
st.title("🧬 [유전자 검사 대용] 내 얼굴 황금비율 & 와꾸 정밀 스캐너 🧬")
st.caption("울산대 의예과 초정밀 알고리즘 탑재 | 관리자 보안 세션 적용")
st.warning("⚠️ **[스캔 전 필독]** 정확한 팩트 폭격을 위해, 얼굴이 기울어지지 않고 **'정면'**에서 **'화면 중앙'**에 꽉 차게 나온 사진을 업로드해 주세요!")
st.markdown("---")

try:
    conn = st.connection("gsheets", type=GSheetsConnection)
    display_data = conn.read(worksheet="ranking", ttl="3s")
    if display_data.empty:
        display_data = pd.DataFrame(columns=["name", "score", "gender", "age"])
        
    display_feedback = conn.read(worksheet="feedback", ttl="3s")
    if display_feedback.empty:
        display_feedback = pd.DataFrame(columns=["name", "stars", "text"])
except Exception as e:
    st.error(f"🚨 DB 연결 초기화 실패! 에러 내용: {e}")
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
        
        try:
            realtime_data = conn.read(worksheet="ranking", ttl="0s")
        except Exception as e:
            st.error("🚨 구글 서버 트래픽 초과! 1~2초 뒤 버튼을 다시 눌러주세요!")
            st.stop()
            
        new_record = pd.DataFrame([{"name": user_name, "score": final_score, "gender": gender, "age": age}])
        updated_df = pd.concat([realtime_data, new_record], ignore_index=True)
        
        try:
            conn.update(worksheet="ranking", data=updated_df)
            display_data = updated_df
        except Exception as e:
            st.error(f"🚨 랭킹 저장 실패! 에러: {e}")

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
        st.info(f"**👁️ 눈(Eye):** `{db[age_group]['눈']}`과 눈매 흡사. 비절개 눈매 교정 고려.")
        st.info(f"**👃 코(Nose):** `{db[age_group]['코']}`와 콧대 라인 일치. 하이코 필러 및 코끝 연골 묶기 시술 추천.")
        st.info(f"**👄 입(Lip):** `{db[age_group]['입']}`과 입술 볼륨 유사. 입술 필러+입꼬리 보톡스 밸런스 추천.")

# ==========================================
# 5. 실시간 피드백 및 설문조사 작성란
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
            try:
                realtime_feedback = conn.read(worksheet="feedback", ttl="0s")
            except Exception as e:
                st.error("🚨 구글 서버 트래픽 초과! 1~2초 후 다시 시도해 주세요!")
                st.stop()
                
            new_fb = pd.DataFrame([{"name": user_name, "stars": accuracy_stars, "text": user_review}])
            updated_fb = pd.concat([realtime_feedback, new_fb], ignore_index=True)
            
            try:
                conn.update(worksheet="feedback", data=updated_fb)
                display_feedback = updated_fb
                st.success("🎉 설문조사가 성공적으로 제출되었습니다!")
            except Exception as e:
                st.error(f"🚨 피드백 저장 실패! 에러: {e}")

# ==========================================
# 6. 하단 레이아웃 (명예의 전당 / 비밀기지)
# ==========================================
st.markdown("---")
col_bottom1, col_bottom2 = st.columns(2)

with col_bottom1:
    st.subheader("🏆 명예의 전당 (TOP 3)")
    if not display_data.empty:
        top_records = display_data.sort_values(by="score", ascending=False).to_dict(orient="records")
    else:
        top_records = []
    
    for rank in range(1, 4):
        medal = "🥇" if rank == 1 else "🥈" if rank == 2 else "🥉"
        if len(top_records) >= rank:
            p = top_records[rank - 1]
            st.markdown(f"> **{medal} {rank}등: {p['name']}** ({p['score']}점)")
        else:
            st.markdown(f"> **{medal} {rank}등:** `아직 등록된 기록이 없습니다.`")

with col_bottom2:
    st.subheader("🔒 개발자 전용 피드백 비밀기지")
    admin_password = st.text_input("마스터 비밀번호를 입력하세요", type="password", placeholder="Password...")
    
    if admin_password == "shutainz1718":
        if display_feedback.empty:
            st.info("🔓 인증 성공! 아직 수집된 피드백 데이터가 없습니다.")
        else:
            st.success("🔓 인증 성공! 구글 시트 실시간 피드백 현황판 오픈.")
            fb_list = display_feedback.to_dict(orient="records")
            for fb in reversed(fb_list):
                st.markdown(f"> **{fb['name']}** (평점: {'⭐' * int(fb['stars'])})\n> *\"{fb['text']}\"*\n> ---")
    elif admin_password != "":
        st.error("❌ 비밀번호가 올바르지 않습니다. 접근 권한이 없습니다.")
  
