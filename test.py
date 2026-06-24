import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from PIL import Image
import random
import time

# ==========================================
# 0. 구글 시트 연결 (가장 확실한 방법)
# ==========================================
try:
    # Secrets에서 시트 주소만 가져오기
    sheet_url = st.secrets["spreadsheet_url"]
    
    # [핵심] connection만 선언하면 스트림릿이 자동으로 
    # 환경변수(gcp_service_account)를 찾아서 연결합니다!
    conn = st.connection("gsheets", type=GSheetsConnection)
    
    existing_data = conn.read(spreadsheet=sheet_url, worksheet="ranking", ttl="0s")
    existing_feedback = conn.read(spreadsheet=sheet_url, worksheet="feedback", ttl="0s")

except Exception as e:
    st.error(f"🚨 DB 연결 실패! Secrets 설정을 확인하세요. 에러: {e}")
    existing_data = pd.DataFrame(columns=["name", "score", "gender", "age"])
    existing_feedback = pd.DataFrame(columns=["name", "stars", "text"])

# ... (아래 1~5번 구역 코드는 그대로 유지) ...
 
      
