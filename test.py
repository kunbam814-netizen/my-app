import streamlit as st
import pandas as pd
from PIL import Image
import random
import time
import gspread
from google.oauth2.service_account import Credentials

# ==========================================
# 1. 웹페이지 기본 설정
# ==========================================
st.set_page_config(page_title="초정밀 와꾸 스캐너", page_icon="🧬", layout="centered")
st.title("🧬 [유전자 검사 대용] 내 얼굴 황금비율 & 와꾸 정밀 스캐너 🧬")
st.caption("울산대 의예과 초정밀 알고리즘 탑재 | 관리자 보안 세션 적용")
st.warning("⚠️ **[스캔 전 필독]** 정확한 팩트 폭격을 위해, 얼굴이 기울어지지 않고 **'정면'**에서 **'화면 중앙'**에 꽉 차게 나온 사진을 업로드해 주세요!")
st.markdown("---")

# 원본 신분증 데이터 (절대 깨지지 않는 순수 딕셔너리 주입)
SERVICE_ACCOUNT_DICT = {
  "type": "service_account",
  "project_id": "genial-current-500412-h0",
  "private_key_id": "e7e0b521621e3ec062abe8e3aa02241e1cfd8d5f",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQDPEYCa9PslQ7i2\n7gKXMyBVgifbtWrNUBp0CixND2QG9HY+WZTBf6l/MLL4KjuZVpU01VM1uiNJmor4\nsg5QXKNNHVtPmfKpAJeyW9RQd8HeV8IIoOgnfwO+DLF55cvwoDWcsJ7P1m9eJM18\nxftCu9NWMgpALwlbbuwUbSSxY+o2p2HHagFhuR/ElARYaLWWWerL/BqzKlLfZL7c\naUEgDr5KWt+qGkbqhul9bYm75u0hZ1ta98oXIdvge/erJ/nUinwA9/yn5hY+CA95\n/uM0GtRi8bOUB7xZfoVZc0HXYj1LK2P9JWMi9/TQyu+LcuOPMZ7LbHTHzaisows3\n8CEdINSbAgMBAAECggEAQIA8tcgzBTAbtUvdnbiszUX+YXeY/byCiPv0QcrWBz6W\nKKTh7AZ2x2pljV0mdITedHcw9M73GAHeYUqhn9HDgo1u+JRFXPSUzFfDgo9TYg2n\nIOXyev8bLNOqYwS8aseU+6qexbIPvd0r7z6Cno6Abdynice9G/Co9FHtOJ6dgglA\n5hj4qKpsn4N1yEpL5Jl8K4M/p6crXUb49ToN+V+BbnSo+iOl/7RPFU6AZMM5u4gA\nRuRVTHOsbv8oyq6lQHsFtoPB3iwInss5bdI4N1fo73LZ78ZXanmWmWv9GhoQE2FJ\nPF75/a/RsmEYXyxKUMwrQWnN54llEifortUYW1Hi/QKBgQD3C+a12IyU7XiiznA7\nkG3C20UTcXUFXDy1FYkpqpKIHDVv+67FARk7BDVw0k7LaNtSN1ZCo1JoCTdjjGmE\ncIZMfMnALv4QybBOOWOUwE5jtlY5D26F2CHvZg2HgBTGJh4/5+NbBNtE6sC2X7Ou\nzSButNk5/wYdEvXryl3A3ttldQKBgQDWkq8U90GbKXgmJVdvLvr2Zo/GlRIeP9Sj\nI828loQe4ZgQ8xm869A/2xTAIajaoLfHKsI2ZvAz0k6enj8NSZQP5V+B/T/kdq73\n8gqBYH3UOCmfQ+G8eTxRseFnhmhOJt8Sy2Z7M9CqBv95KnwN0EzkAAPETq9sTkqq\niEqQCno/zwKBgQCHJoafowk9jDB7+K3jmB7EBArlGSOovA4mDtML7VnehnghfDHf\nartv0tydjSA4HXQmpUlWiVzSt4AKwM0U/C4sd/QzZEHv0zbVhIXa4d3ApQbEjpGr\nPVNLUaxDHam/wSi5U1XI/H4sVLT60J5PGb8NcXiJRuAEVdQdm4bwtbqW5QKBgQCb\noTyX6laNYeChWkg2fk7MVMtHb2v6wLVLtnZMqKcfduTCtnAelLMw/YfpawB7wkJJ\nlPvUVYk3LPyVE5YL3ygi92z0bWjgHiz97XItMH1TZYDa4XNjLlPPtUMVwWj59jup\n+BlWlthr2jOGAIiFxGVgoZoZ0jBuT8LcOYpLOy48BQKBgGZ402JyLOk8yK4hrmaQ\nhKv0t46kprXD9RLNr0/hKqVAycSK6r74VbFENGiL06w+7t4beR6wfOIVuRmGp2YQ\xdKbtep1TeTKMI8Ntp4/B7e2tax2wq9kpOrJEbzYmqOsRAXX7TcdjFJXPa4W4c6Z\ni2XkR4YNG+eF47iefr8bOP/y\n-----END PRIVATE KEY-----\n",
  "client_email": "bot-532@genial-current-500412-h0.iam.gserviceaccount.com",
  "client_id": "114486457354616821244",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/bot-532%40genial-current-500412-h0.iam.gserviceaccount.com",
  "universe_domain": "googleapis.com"
}

ws_ranking = None
ws_feedback = None

# ==========================================
# 2. 순수 gspread 라이브러리로 무적의 연결체 구성
# ==========================================
try:
    sheet_url = st.secrets["spreadsheet_url"]
    scopes = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
    creds = Credentials.from_service_account_info(SERVICE_ACCOUNT_DICT, scopes=scopes)
    gc = gspread.authorize(creds)
    sh = gc.open_by_url(sheet_url)
    
    # ranking 시트 로드
    ws_ranking = sh.worksheet("ranking")
    ranking_records = ws_ranking.get_all_records()
    display_data = pd.DataFrame(ranking_records) if ranking_records else pd.DataFrame(columns=["name", "score", "gender", "age"])
    
    # feedback 시트 로드
    ws_feedback = sh.worksheet("feedback")
    feedback_records = ws_feedback.get_all_records()
    display_feedback = pd.DataFrame(feedback_records) if feedback_records else pd.DataFrame(columns=["name", "stars", "text"])
except Exception as e:
 
