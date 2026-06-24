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

# ==========================================
# 2. 구글 본사 직통 핫라인 연결 (오류 0% 완전 가동)
# ==========================================
SHEET_ID = "1xcF9FJdZdCFvBArYcFa5vT-iD8Ev03HLfOpbx127UNk"

# 💡 특수문자(\n) 해석 오류를 방지하기 위해 각 줄을 완벽하게 분리하여 정밀 조립합니다.
private_key_parts = [
    "-----BEGIN PRIVATE KEY-----",
    "MIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQDPEYCa9PslQ7i2",
    "7gKXMyBVgifbtWrNUBp0CixND2QG9HY+WZTBf6l/MLL4KjuZVpU01VM1uiNJmor4",
    "sg5QXKNNHVtPmfKpAJeyW9RQd8HeV8IIoOgnfwO+DLF55cvwoDWcsJ7P1m9eJM18",
    "xftCu9NWMgpALwlbbuwUbSSxY+o2p2HHagFhuR/ElARYaLWWWerL/BqzKlLfZL7c",
    "aUEgDr5KWt+qGkbqhul9bYm75u0hZ1ta98oXIdvge/erJ/nUinwA9/yn5hY+CA95",
    "/uM0GtRi8bOU7xZfoVZc0HXYj1LK2P9JWMi9/TQyu+LcuOPMZ7LbHTHzaisows3",
    "8CEdINSbAgMBAAECggEAQIA8tcgzBTAbtUvdnbiszUX+YXeY/byCiPv0QcrWBz6W",
    "KKTh7AZ2x2pljV0mdITedHcw9M73GAHeYUqhn9HDgo1u+JRFXPSUzFfDgo9TYg2n",
    "IOXyev8bLNOqYwS8aseU+6qexbIPvd0r7z6Cno6Abdynice9G/Co9FHtOJ6dgglA",
    "5hj4qKpsn4N1yEpL5Jl8K4M/p6crXUb49ToN+V+BbnSo+iOl/7RPFU6AZMM5u4gA",
    "RuRVTHOsbv8oyq6lQHsFtoPB3iwInss5bdI4N1fo73LZ78ZXanmWmWv9GhoQE2FJ",
    "PF75/a/RsmEYXyxKUMwrQWnN54llEifortUYW1Hi/QKBgQD3C+a12IyU7XiiznA7",
    "kG3C20UTcXUFXDy1FYkpqpKIHDVv+67FARk7BDVw0k7LaNtSN1ZCo1JoCTdjjGmE",
    "cIZMfMnALv4QybBOOWOUwE5jtlY5D26F2CHvZg2HgBTGJh4/5+NbBNtE6sC2X7Ou",
    "zSButNk5/wYdEvXryl3A3ttldQKBgQDWkq8U90GbKXgmJVdvLvr2Zo/GlRIeP9Sj",
    "I828loQe4ZgQ8xm869A/2xTAIajaoLfHKsI2ZvAz0k6enj8NSZQP5V+B/T/kdq73
    "8gqBYH3UOCmfQ+G8eTxRseFnhmhOJt8Sy2Z7M9CqBv95KnwN0EzkAAPETq9sTkqq",
    "iEqQCno/zwKBgQCHJoafowk9jDB7+K3jmB7EBArlGSOovA4mDtML7VnehnghfDHf",
    "artv0tydjSA4HXQmpUlWiVzSt4AKwM0U/C4sd/QzZEHv0zbVhIXa4d3ApQbEjpGr",
    "PVNLUaxDHam/wSi5U1XI/H4sVLT60J5PGb8NcXiJRuAEVdQdm4bwtbqW5QKBgQCb",
    "oTyX6laNYeChWkg2fk7MVMtHb2v6wLVLtnZMqKcfduTCtnAelLMw/YfpawB7wkJJ",
    "lPvUVYk3LPyVE5YL3ygi92z0bWjgHiz97XItMH1TZYDa4XNjLlPPtUMVwWj59jup",
    "+BlWlthr2jOGAIiFxGVgoZoZ0jBuT8LcOYpLOy48BQKBgGZ402JyLOk8yK4hrmaQ",
    "hKv0t46kprXD9RLNr0/hKqVAycSK6r74VbFENGiL06w+7t4beR6wfOIVuRmGp2YQ",
    "xdKbtep1TeTKMI8Ntp4/B7e2tax2wq9kpOrJEbzYmqOsRAXX7TcdjFJXPa4W4c6Z",
    "i2XkR4YNG+eF47ie
  
