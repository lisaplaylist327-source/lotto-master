import streamlit as st
import pandas as pd
import datetime
import time
import random
import itertools
from collections import Counter, defaultdict
import numpy as np
import altair as alt

# ---------------------------------------------------------
# 1. ตั้งค่าหน้าเว็บ & ระบบนำทาง
# ---------------------------------------------------------
st.set_page_config(layout="wide", page_title="Lotto Master V.Final")

# ย้าย "ห้องแห่งความลับ" ไปไว้ล่างสุดตามคำขอ
ALL_PAGES = [
    "🏠 หน้าแรก (6 สูตรมหาประลัย)", 
    "🧪 ห้องวิจัยสูตร (Formula Lab)",
    "🔍 นักสืบตัวเลข", 
    "🧬 สูตรลับ 5 ชั้น (AI Spin)", 
    "💖 รวมสูตรน้องพารวย", 
    "🎣 สูตรฟันปลา & สามเหลี่ยม", 
    "💀 โซนเลขดับ (Killer Zone)",
    "🔑 ห้องแห่งความลับ (Secret Chamber)"
]

if 'current_page' not in st.session_state:
    st.session_state.current_page = ALL_PAGES[0]

# ตัวแปรเช็คสถานะการปลดล็อคห้องลับ
if 'secret_unlocked' not in st.session_state:
    st.session_state.secret_unlocked = False

def navigate_to(page_name):
    st.session_state.current_page = page_name
    st.rerun()

# ---------------------------------------------------------
# 2. CSS Style (Ultimate Jeung Edition ✨)
# ---------------------------------------------------------
custom_css = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Kanit:wght@300;400;600;900&display=swap');

html, body, [class*="css"] { font-family: 'Kanit', sans-serif !important; }

/* --- HERO SECTION --- */
.hero-container {
    background: radial-gradient(circle at center, #2b2b2b 0%, #1a1a1a 100%);
    border: 2px solid #FFD700; border-radius: 20px; padding: 20px; text-align: center;
    box-shadow: 0 0 30px rgba(255, 215, 0, 0.2); margin-bottom: 25px;
}
.hero-number {
    font-size: clamp(40px, 8vw, 90px); font-weight: 900; 
    background: linear-gradient(to bottom, #FFF8DC 0%, #FFD700 50%, #DAA520 100%);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    filter: drop-shadow(0 4px 6px rgba(0,0,0,0.8)); margin: 10px 0;
}

/* --- CARDS (Used Everywhere) --- */
.formula-card-home, .lab-card, .fp-card, .secret-card { 
    background: linear-gradient(145deg, #222, #181818); 
    padding: 20px; margin-bottom: 20px; border-radius: 15px; border: 1px solid #444; 
    box-shadow: 0 4px 15px rgba(0,0,0,0.4); transition: all 0.3s;
}
.formula-card-home:hover, .lab-card:hover, .fp-card:hover, .secret-card:hover { 
    transform: translateY(-3px); border-color: #FFD700; 
    box-shadow: 0 10px 25px rgba(255, 215, 0, 0.15); 
}

/* --- TEXT & HEADERS --- */
.f-header, .lab-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px; border-bottom: 1px solid #333; padding-bottom: 10px; }
.f-title, .lab-title { font-weight: 900; font-size: 20px; margin: 0; text-shadow: 0 2px 4px rgba(0,0,0,0.8); }
.f-stats-badge { background: #333; color: #ccc; font-size: 12px; padding: 4px 10px; border-radius: 8px; border: 1px solid #555; }
.lab-result-chk { font-weight: bold; font-size: 14px; background: #333; padding: 4px 10px; border-radius: 20px; border: 1px solid #555; }

/* --- BIG GOLD BOX (The "Jeung" Box) --- */
.f-pair-box {
    margin-top: 15px;
    background: linear-gradient(135deg, #000000 0%, #2c3e50 100%);
    padding: 15px; border-radius: 12px;
    color: #FFD700; font-weight: 900; font-size: 36px; line-height: 1.2;
    text-align: center; border: 1px solid #666; letter-spacing: 2px;
    text-shadow: 3px 3px 0px #000; box-shadow: inset 0 0 40px rgba(0,0,0,0.8);
}

/* --- LAB SPECIFIC --- */
.lab-eq { 
    font-family: 'Courier New', monospace; font-size: 13px; color: #00FF7F; 
    background: #000; padding: 8px 12px; border-radius: 6px; margin-bottom: 8px; 
    border-left: 3px solid #00FF7F; overflow-x: auto; white-space: nowrap; 
}
.lab-res-box { 
    display: flex; gap: 15px; align-items: center; margin: 20px 0; 
    background: #252525; padding: 15px; border-radius: 12px; border: 1px dashed #444; justify-content: center;
}
.lab-digit { 
    font-size: 36px; font-weight: 900; color: #FFD700; 
    background: linear-gradient(135deg, #000, #222); 
    padding: 5px 20px; border-radius: 8px; border: 1px solid #FFD700; 
    text-shadow: 0 0 10px rgba(255, 215, 0, 0.5);
}
.lab-pairs-container { 
    margin-top: 15px; line-height: 2.5; text-align: center; background: #151515; padding: 15px; border-radius: 10px; border: 1px solid #333;
}
.lab-item-normal { font-size: 22px; color: #888; margin: 0 8px; font-weight: bold; display: inline-block; }
.lab-item-hit { 
    font-size: 32px; font-weight: 900; color: #000 !important; 
    background: linear-gradient(135deg, #00FF7F, #00CC66); 
    padding: 5px 15px; border-radius: 8px; box-shadow: 0 0 20px rgba(0, 255, 127, 0.6); 
    margin: 0 8px; display: inline-block; border: 2px solid #fff; 
}

/* --- BADGES --- */
.f-val-badge { background-color: #333; color: #fff; padding: 3px 12px; border-radius: 12px; font-size: 16px; margin-right: 5px; border: 1px solid #555; font-weight: bold; }
.rank-badge { position: absolute; top: -10px; right: -5px; padding: 5px 15px; font-size: 14px; border-radius: 20px; font-weight: 900; z-index: 10; border: 2px solid #222; text-transform: uppercase; box-shadow: 0 4px 10px rgba(0,0,0,0.5); }
.rank-1 { background: linear-gradient(135deg, #FFD700, #FDB931); color: #000; }
.rank-2 { background: linear-gradient(135deg, #E0E0E0, #B0B0B0); color: #000; }
.rank-3 { background: linear-gradient(135deg, #cd7f32, #b87333); color: #FFF; }

/* --- PYRAMID & BALLS --- */
.pyramid-container { 
    display: flex; flex-direction: column; align-items: center; justify-content: center; 
    padding: 30px; background: radial-gradient(circle, #2e2e2e 0%, #1a1a1a 100%); 
    border-radius: 20px; margin-top: 15px; border: 1px solid #444;
}
.pyramid-row { display: flex; justify-content: center; margin-bottom: 8px; }
.pyramid-ball { 
    width: 55px; height: 55px; line-height: 55px; border-radius: 50%; 
    background: radial-gradient(circle at 30% 30%, #ffffff, #d4af37); color: #222; 
    font-size: 26px; font-weight: 900; text-align: center; margin: 0 6px; 
    border: 3px solid #b8860b; box-shadow: 0 5px 15px rgba(0,0,0,0.5);
    text-shadow: 1px 1px 0px rgba(255,255,255,0.5); transition: transform 0.2s;
}
.pyramid-ball:hover { transform: scale(1.1); }
.pyramid-ball.result { 
    width: 90px; height: 90px; line-height: 85px; font-size: 48px; 
    background: radial-gradient(circle at 30% 30%, #00FF7F, #006400); 
    border: 4px solid #fff; box-shadow: 0 0 30px #00FF7F; color: #fff;
    text-shadow: 0 2px 5px rgba(0,0,0,0.5);
}
.connector-line { color: #666; font-size: 14px; margin: -5px 0 5px 0; text-shadow: 0 1px 1px #000; }

/* --- KILLER BOX & CONSENSUS --- */
.consensus-box { 
    background: linear-gradient(135deg, #3b0000 0%, #1a0000 100%); 
    border: 2px solid #FF4444; padding: 20px; border-radius: 15px; 
    text-align: center; margin-bottom: 20px; 
    box-shadow: 0 0 20px rgba(255, 68, 68, 0.3);
}
.consensus-title { color: #FF4444; font-weight: bold; font-size: 18px; margin-bottom: 5px; text-transform: uppercase; letter-spacing: 1px; }
.consensus-number { font-size: 70px; font-weight: 900; color: #FFD700; line-height: 1; text-shadow: 0 0 15px rgba(255, 215, 0, 0.5); margin: 10px 0; }
.consensus-desc { color: #aaa; font-size: 14px; }

.killer-box { background-color: #3b0000; border: 1px solid #ff4444; padding: 15px; border-radius: 12px; text-align: center; margin-bottom: 15px; box-shadow: inset 0 0 20px rgba(255,0,0,0.2); }
.killer-digit { font-size: 40px; font-weight: 900; color: #ff4444; text-shadow: 0 0 10px rgba(255, 68, 68, 0.5); margin: 5px 0; }

/* --- PREDICTION --- */
.prediction-box { text-align: center; padding: 30px; background: linear-gradient(135deg, #1a1a1a, #000); border: 3px solid #FFD700; border-radius: 20px; margin-top: 25px; box-shadow: 0 0 40px rgba(255, 215, 0, 0.2); }
.pred-pairs { font-size: 56px; font-weight: 900; color: #39FF14; line-height: 1.4; text-shadow: 0 0 20px rgba(57, 255, 20, 0.6); }

/* --- OTHER --- */
.stat-card { background-color: #444; padding: 10px; text-align: center; border-radius: 8px; margin-bottom: 10px; color: white; }
.stat-val { font-size: 28px; font-weight: bold; color: #00FF7F; }
.stat-label { font-size: 14px; color: #CCCCCC; }
.sidebar-stat-box { background-color: #262626; padding: 12px; border-radius: 10px; margin-bottom: 10px; text-align: center; border: 1px solid #444; box-shadow: 0 4px 6px rgba(0,0,0,0.2); }
.sidebar-stat-num { font-size: 28px; font-weight: 900; color: #FFD700; line-height: 1.2; }
.sidebar-stat-label { font-size: 12px; color: #aaa; margin-bottom: 2px; }
.f-label { font-size: 15px; color: #999; width: 40px; font-weight: 600; }

/* --- SECRET PAGE --- */
.secret-formula-title { font-size: 22px; font-weight: 900; color: #FFD700; margin-bottom: 12px; border-bottom: 1px solid #444; padding-bottom: 8px; }
.secret-desc { color: #ddd; font-size: 14px; margin-bottom: 10px; line-height: 1.6; }
.secret-eq-box { background: #111; padding: 12px; border-radius: 8px; border: 1px dashed #555; margin-bottom: 10px; }
.secret-hl { color: #00FF7F; font-weight: bold; font-family: monospace; font-size: 14px; }
.secret-step { color: #FF4444; font-weight: bold; margin-left: 5px; }
.secret-layer-box { background: #222; padding: 15px; margin-bottom: 10px; border-radius: 10px; border-left: 4px solid #00BFFF; }
.login-box { background: #222; padding: 30px; border-radius: 15px; border: 2px solid #FF4444; max-width: 400px; margin: 50px auto; text-align: center; box-shadow: 0 0 30px rgba(255,0,0,0.3); }
</style>
"""

# ---------------------------------------------------------
# 3. Logic & Calculation
# ---------------------------------------------------------
def format_thai_date(date_obj):
    thai_months = ["ม.ค.", "ก.พ.", "มี.ค.", "เม.ย.", "พ.ค.", "มิ.ย.", "ก.ค.", "ส.ค.", "ก.ย.", "ต.ค.", "พ.ย.", "ธ.ค."]
    year = date_obj.year + 543
    return f"{date_obj.day} {thai_months[date_obj.month - 1]} {year}"

@st.cache_data
def load_data():
    try:
        df = pd.read_csv('thailotto.csv')
        df['date_obj'] = pd.to_datetime(df['date'])
        df = df.sort_values('date_obj').reset_index(drop=True)
        df['วันที่'] = df['date_obj'].apply(format_thai_date)
        
        df['รางวัลที่ 1'] = df['first_prize'].astype(str).str.zfill(6)
        df['first_prize_str'] = df['รางวัลที่ 1'].copy()
        df['two_digit_str'] = df['two_digit'].astype(str).str.zfill(2)
        df['2 ตัวล่าง'] = df['two_digit'].astype(str).str.zfill(2)
        
        cols_3 = ['three_digit_1', 'three_digit_2', 'three_digit_3', 'three_digit_4']
        new_cols_3 = ['เลขท้าย 3 ตัว (1)', 'เลขท้าย 3 ตัว (2)', 'เลขท้าย 3 ตัว (3)', 'เลขท้าย 3 ตัว (4)']
        for old, new in zip(cols_3, new_cols_3):
            if old in df.columns: df[new] = df[old].astype(str).str.zfill(3)
            else: df[new] = "000"
            
        df['R1_Lakh'] = df['รางวัลที่ 1'].str[0].astype(int); df['R1_Muen'] = df['รางวัลที่ 1'].str[1].astype(int)
        df['R1_Pan'] = df['รางวัลที่ 1'].str[2].astype(int); df['R1_Roi'] = df['รางวัลที่ 1'].str[3].astype(int)
        df['R1_Sib'] = df['รางวัลที่ 1'].str[4].astype(int); df['R1_Nui'] = df['รางวัลที่ 1'].str[5].astype(int)
        df['Bot_Sib'] = df['2 ตัวล่าง'].str[0].astype(int); df['Bot_Nui'] = df['2 ตัวล่าง'].str[1].astype(int)
        
        df['Top_Ten'] = df['R1_Sib']; df['Top_Unit'] = df['R1_Nui']
        df['Bot_Ten'] = df['Bot_Sib']; df['Bot_Unit'] = df['Bot_Nui']
        df['2 ตัวบน'] = df['รางวัลที่ 1'].str[-2:]
        return df
    except Exception as e:
        return pd.DataFrame()

# --- Shared Helper ---
def calculate_hit_streaks(hit_series):
    hits = hit_series.astype(int).tolist()
    current_streak = 0; max_streak = 0
    for hit in reversed(hits):
        if hit == 1: current_streak += 1
        else: break
    temp_streak = 0
    for hit in hits:
        if hit == 1: temp_streak += 1
        else: max_streak = max(max_streak, temp_streak); temp_streak = 0
    max_streak = max(max_streak, temp_streak)
    return current_streak, max_streak

# --- AI Spin Logic ---
def get_distribution(df, factor_col, target_col, current_val):
    filtered = df[df[factor_col] == current_val]
    return filtered[target_col].value_counts().to_dict()

def calculate_formula_rank(df, target_type):
    if df.empty: return []
    df_cal = df.copy()
    if target_type == 'Top_Ten': factors = ['Top_Ten', 'Top_Unit', 'Bot_Ten', 'Bot_Unit', 'Top_Ten']
    elif target_type == 'Top_Unit': factors = ['Top_Unit', 'Top_Ten', 'Bot_Ten', 'Bot_Unit', 'Top_Unit']
    elif target_type == 'Bot_Ten': factors = ['Bot_Ten', 'Bot_Unit', 'Top_Ten', 'Top_Unit', 'Bot_Ten']
    elif target_type == 'Bot_Unit': factors = ['Bot_Unit', 'Bot_Ten', 'Top_Ten', 'Top_Unit', 'Bot_Unit']
    else: return []
    df_cal['F1'] = df_cal[factors[0]].shift(1); df_cal['F2'] = df_cal[factors[1]].shift(1)
    df_cal['F3'] = df_cal[factors[2]].shift(1); df_cal['F4'] = df_cal[factors[3]].shift(1); df_cal['F5'] = df_cal[factors[4]].shift(2)
    df_cal = df_cal.dropna()
    last = df.iloc[-1]; prev = df.iloc[-2]; seeds = [last[factors[0]], last[factors[1]], last[factors[2]], last[factors[3]], prev[factors[4]]]
    total = Counter()
    for i, seed in enumerate(seeds): total.update(get_distribution(df_cal, f'F{i+1}', target_type, seed))
    sorted_scores = sorted(total.items(), key=lambda x: x[1], reverse=True); top = sorted_scores[:5]; final = [x[0] for x in top[:3]]
    if len(top) >= 5:
        r4, r5 = top[3], top[4]; rec = df.tail(20)
        f4 = rec[rec[target_type] == r4[0]].shape[0]; f5 = rec[rec[target_type] == r5[0]].shape[0]
        final.append(r4[0] if f4 >= f5 else r5[0])
    elif len(top) == 4: final.append(top[3][0])
    return final

# --- SVD Logic ---
def calculate_harmonizer_stats(df):
    predicted_set = [4, 3, 2, 8]; target_cols = ['R1_Sib', 'R1_Nui', 'Bot_Sib', 'Bot_Nui']
    hit_mask = pd.Series([False] * len(df), index=df.index)
    for digit in predicted_set: hit_mask = hit_mask | (df[target_cols] == digit).any(axis=1)
    total_draws = len(df); total_hits = hit_mask.sum(); calculated_accuracy = (total_hits / total_draws) * 100
    current_streak, max_streak = calculate_hit_streaks(hit_mask)
    scores_data = {'Digit': [i for i in range(10)], 'Score': [0.15, 0.25, 0.70, 0.68, 0.75, 0.10, 0.30, 0.50, 0.65, 0.05], 'Type': ['Other'] * 10}
    scores_df = pd.DataFrame(scores_data) 
    scores_df['Type'] = scores_df['Digit'].apply(lambda d: 'Dominant' if d in predicted_set else 'Other')
    scores_df = scores_df.sort_values('Digit'); window = 50
    rolling_accuracy = hit_mask.rolling(window=window).mean() * 100
    rolling_df = pd.DataFrame({'งวด': df.index, 'ความแม่นยำ 50 งวด': rolling_accuracy}).dropna()
    backtest_df = df[['วันที่', 'รางวัลที่ 1', '2 ตัวล่าง']].copy()
    backtest_df['เลขที่ออก (2 ตัว)'] = df['R1_Sib'].astype(str) + df['R1_Nui'].astype(str) + '/' + df['Bot_Sib'].astype(str) + df['Bot_Nui'].astype(str)
    backtest_df['Hit_Status'] = hit_mask.apply(lambda x: '✅ เข้า' if x else '❌ หลุด')
    backtest_df = backtest_df[['วันที่', 'เลขที่ออก (2 ตัว)', 'Hit_Status']]
    return predicted_set, calculated_accuracy, total_hits, total_draws, scores_df, rolling_df, backtest_df, current_streak, max_streak

# --- 4 Standing Digits Logic ---
def get_target_digit(row, position_type):
    r1_str = row['first_prize_str']; bottom_str = row['two_digit_str']
    if position_type == 'TT': return int(r1_str[4])
    elif position_type == 'UT': return int(r1_str[5])
    elif position_type == 'TB': return int(bottom_str[0])
    elif position_type == 'UB': return int(bottom_str[1])
    return None

def get_axis_digit(row, axis_type):
    r1_str = row['first_prize_str']; bottom_str = row['two_digit_str']
    if axis_type == 'R1_P1': return int(r1_str[0])
    elif axis_type == 'R1_P6': return int(r1_str[5])
    elif axis_type == '2D_P1': return int(bottom_str[0])
    elif axis_type == '2D_P2': return int(bottom_str[1])
    return None

def select_top_4(scores):
    sorted_scores = sorted([(score, digit) for digit, score in scores.items()], key=lambda x: (x[0], x[1]), reverse=True)
    return [digit for score, digit in sorted_scores][:4]

def calculate_f1_scores_dynamic(df, target_pos, current_draw_idx):
    history_df = df.iloc[2:current_draw_idx].copy()
    digit_counts = history_df.apply(lambda row: get_target_digit(row, target_pos), axis=1).value_counts().to_dict()
    total_scores = defaultdict(float)
    for digit in range(10): total_scores[digit] = digit_counts.get(digit, 0)
    if current_draw_idx < 2: return total_scores
    prev_draw = df.iloc[current_draw_idx - 1]; prev_prev_draw = df.iloc[current_draw_idx - 2]
    target_digit_n_2 = get_target_digit(prev_prev_draw, target_pos)
    axis_digits_dn_1 = {get_axis_digit(prev_draw, 'R1_P1'), get_axis_digit(prev_draw, 'R1_P6'), get_axis_digit(prev_draw, '2D_P1'), get_axis_digit(prev_draw, '2D_P2'), target_digit_n_2}
    for digit in range(10):
        if digit in axis_digits_dn_1: total_scores[digit] += total_scores[digit] * 0.05
    return total_scores

def calculate_four_standing_digits(df):
    if df.empty: return [], 0, 0, 0, pd.DataFrame(), 0, 0 
    total_draws = len(df); target_positions = ['TT', 'UT', 'TB', 'UB']
    all_hits = pd.Series([False] * total_draws, index=df.index)
    for current_draw_idx in range(2, total_draws):
        f1_scores_all = {}; 
        for pos in target_positions: f1_scores_all[pos] = calculate_f1_scores_dynamic(df, pos, current_draw_idx)
        total_combined_scores = defaultdict(float)
        for digit in range(10): combined_score = sum(f1_scores_all[pos].get(digit, 0) for pos in target_positions); total_combined_scores[digit] = combined_score
        standing_digits_for_test = select_top_4(total_combined_scores)
        current_row = df.iloc[current_draw_idx]
        hit_digits = {current_row['R1_Sib'], current_row['R1_Nui'], current_row['Bot_Sib'], current_row['Bot_Nui']}
        is_hit = any(digit in hit_digits for digit in standing_digits_for_test); all_hits.iloc[current_draw_idx] = is_hit
    last_draw_idx = total_draws; f1_scores_all_next = {}
    for pos in target_positions: f1_scores_all_next[pos] = calculate_f1_scores_dynamic(df, pos, last_draw_idx)
    total_combined_scores_next = defaultdict(float)
    for digit in range(10): combined_score = sum(f1_scores_all_next[pos].get(digit, 0) for pos in target_positions); total_combined_scores_next[digit] = combined_score
    next_standing_digits = select_top_4(total_combined_scores_next)
    backtest_data = all_hits.iloc[2:].copy(); total_checks = len(backtest_data); total_hits = backtest_data.sum()
    calculated_accuracy = (total_hits / total_checks) * 100 if total_checks > 0 else 0
    current_streak, max_streak = calculate_hit_streaks(backtest_data)
    backtest_df = df.iloc[2:].copy(); backtest_df['Hit_Status'] = backtest_data.apply(lambda x: '✅ เข้า' if x else '❌ หลุด')
    backtest_df['เลขที่ออก (2 ตัว)'] = backtest_df['R1_Sib'].astype(str) + backtest_df['R1_Nui'].astype(str) + '/' + backtest_df['Bot_Sib'].astype(str) + df['Bot_Nui'].astype(str)
    backtest_df = backtest_df[['วันที่', 'เลขที่ออก (2 ตัว)', 'Hit_Status']]
    return next_standing_digits, calculated_accuracy, total_hits, total_checks, backtest_df, current_streak, max_streak 

def calculate_puck_luk_stats(df):
    positions = [('R1_Sib', 'สิบบน (R1 P5)'), ('R1_Nui', 'หน่วยบน (R1 P6)'), ('Bot_Sib', 'สิบล่าง (2D P1)'), ('Bot_Nui', 'หน่วยล่าง (2D P2)')]
    puck_luk_results = {}
    for col_name, pos_name in positions:
        counts = df[col_name].value_counts(normalize=True).mul(100).round(2).sort_values(ascending=False)
        chart_data = pd.DataFrame({'Digit': counts.index.astype(str), 'Frequency': counts.values})
        puck_luk_results[pos_name] = {'Prediction': int(counts.index[0]) if not counts.empty else 0, 'Top_3_Digits': counts.head(3).index.tolist(), 'Top_3_Percent': counts.head(3).values.tolist(), 'ChartData': chart_data}
    return puck_luk_results

def calculate_next_mover_stats(df, leading_digit):
    target_cols = ['R1_Sib', 'R1_Nui', 'Bot_Sib', 'Bot_Nui']
    df['is_leading'] = (df[target_cols] == leading_digit).any(axis=1)
    next_movers = []
    for i in df[df['is_leading']].index:
        if i + 1 < len(df): next_row = df.iloc[i + 1]; next_movers.append(next_row['2 ตัวบน']); next_movers.append(next_row['2 ตัวล่าง'])
    if not next_movers: return []
    mover_counts = Counter(next_movers); top_5 = mover_counts.most_common(5)
    return top_5

def calculate_hit_streaks(hit_series):
    hits = hit_series.astype(int).tolist(); current_streak = 0; max_streak = 0
    for hit in reversed(hits):
        if hit == 1: current_streak += 1
        else: break
    temp_streak = 0
    for hit in hits:
        if hit == 1: temp_streak += 1
        else: max_streak = max(max_streak, temp_streak); temp_streak = 0
    max_streak = max(max_streak, temp_streak)
    return current_streak, max_streak

def generate_pyramid_html(layers):
    html = "<div class='pyramid-container'>"
    for i, layer in enumerate(layers):
        html += "<div class='pyramid-row'>"
        for j, num in enumerate(layer):
            if i == len(layers) - 1: html += f"<div class='pyramid-ball result'>{num}</div>"
            else: html += f"<div class='pyramid-ball'>{num}</div>"
        html += "</div>"
        if i < len(layers) - 1: html += "<div class='connector-line'>" + ("&nbsp;&nbsp;&nbsp;&nbsp;🔻&nbsp;&nbsp;&nbsp;&nbsp;" * len(layers[i+1])) + "</div>"
    html += "</div>"
    return html

def calculate_grand_pyramid_stats(df):
    prev = df.shift(1)
    current_layer_cols = ['R1_Lakh', 'R1_Muen', 'R1_Pan', 'R1_Roi', 'R1_Sib', 'R1_Nui', 'Bot_Sib', 'Bot_Nui']
    temp_df = prev[current_layer_cols].copy()
    while len(current_layer_cols) > 1:
        next_cols = []
        for i in range(len(current_layer_cols) - 1):
            col_name = f"L{len(current_layer_cols)}_{i}"
            c1 = current_layer_cols[i]; c2 = current_layer_cols[i+1]
            temp_df[col_name] = (temp_df[c1] + temp_df[c2]) % 10
            next_cols.append(col_name)
        current_layer_cols = next_cols
    pred_col = current_layer_cols[0]
    pos_8 = ['R1_Lakh', 'R1_Muen', 'R1_Pan', 'R1_Roi', 'R1_Sib', 'R1_Nui', 'Bot_Sib', 'Bot_Nui']
    pos_3top = ['R1_Roi', 'R1_Sib', 'R1_Nui']
    pos_2top = ['R1_Sib', 'R1_Nui']
    pos_2bot = ['Bot_Sib', 'Bot_Nui']
    def check_hit(cols):
        mask = pd.Series([False]*len(df), index=df.index)
        for col in cols: mask = mask | (df[col] == temp_df[pred_col])
        return mask
    hit_8pos = check_hit(pos_8); hit_3top = check_hit(pos_3top)
    hit_2top = check_hit(pos_2top); hit_2bot = check_hit(pos_2bot)
    valid_mask = ~temp_df[pred_col].isna(); total_checks = valid_mask.sum()
    acc_8pos = (hit_8pos & valid_mask).sum() / total_checks * 100
    acc_3top = (hit_3top & valid_mask).sum() / total_checks * 100
    acc_2top = (hit_2top & valid_mask).sum() / total_checks * 100
    acc_2bot = (hit_2bot & valid_mask).sum() / total_checks * 100
    last = df.iloc[-1]
    lb = [int(last[c]) for c in ['R1_Lakh', 'R1_Muen', 'R1_Pan', 'R1_Roi', 'R1_Sib', 'R1_Nui', 'Bot_Sib', 'Bot_Nui']]
    layers = [lb]; curr = lb
    while len(curr) > 1:
        nxt = []
        for i in range(len(curr)-1): nxt.append(int((curr[i]+curr[i+1])%10))
        layers.append(nxt); curr = nxt
    final_digit = curr[0]
    return {'Digit': final_digit, 'Layers': layers, 'Acc_8Pos': acc_8pos, 'Acc_3Top': acc_3top, 'Acc_2Top': acc_2top, 'Acc_2Bot': acc_2bot, 'Total': int(total_checks)}

# --- สูตร 2: สามเหลี่ยมทองคำ ---
def calculate_pyramid_detailed_stats(df):
    prev = df.shift(1)
    b0, b1, b2 = prev['R1_Roi'], prev['R1_Sib'], prev['R1_Nui']
    b3, b4 = prev['Bot_Sib'], prev['Bot_Nui']
    l1_0, l1_1 = (b0+b1)%10, (b1+b2)%10; l1_2, l1_3 = (b2+b3)%10, (b3+b4)%10
    l2_0, l2_1, l2_2 = (l1_0+l1_1)%10, (l1_1+l1_2)%10, (l1_2+l1_3)%10
    l3_0, l3_1 = (l2_0+l2_1)%10, (l2_1+l2_2)%10
    pred = (l3_0+l3_1)%10
    pos_8 = ['R1_Lakh', 'R1_Muen', 'R1_Pan', 'R1_Roi', 'R1_Sib', 'R1_Nui', 'Bot_Sib', 'Bot_Nui']
    pos_3top = ['R1_Roi', 'R1_Sib', 'R1_Nui']; pos_2top = ['R1_Sib', 'R1_Nui']; pos_2bot = ['Bot_Sib', 'Bot_Nui']
    def check_hit(cols):
        mask = pd.Series([False]*len(df), index=df.index)
        for col in cols: mask = mask | (df[col] == pred)
        return mask
    hit_8pos = check_hit(pos_8); hit_3top = check_hit(pos_3top)
    hit_2top = check_hit(pos_2top); hit_2bot = check_hit(pos_2bot)
    valid_mask = ~np.isnan(pred); total_checks = valid_mask.sum()
    acc_8pos = (hit_8pos & valid_mask).sum() / total_checks * 100
    acc_3top = (hit_3top & valid_mask).sum() / total_checks * 100
    acc_2top = (hit_2top & valid_mask).sum() / total_checks * 100
    acc_2bot = (hit_2bot & valid_mask).sum() / total_checks * 100
    last = df.iloc[-1]
    lb = [int(last['R1_Roi']), int(last['R1_Sib']), int(last['R1_Nui']), int(last['Bot_Sib']), int(last['Bot_Nui'])]
    layers = [lb]; curr = lb
    while len(curr) > 1:
        nxt = []
        for i in range(len(curr)-1): nxt.append(int((curr[i]+curr[i+1])%10))
        layers.append(nxt); curr = nxt
    final_digit = curr[0]
    return {'Digit': final_digit, 'Layers': layers, 'Acc_8Pos': acc_8pos, 'Acc_3Top': acc_3top, 'Acc_2Top': acc_2top, 'Acc_2Bot': acc_2bot, 'Total': int(total_checks)}

# --- สูตรฟันปลา 3 ตัว ---
def calculate_triple_fhan_pla_detailed_stats(df):
    prev = df.shift(1)
    base_calc = (prev['R1_Muen'] + prev['R1_Sib'] + prev['Bot_Nui'] + 7) % 10
    p1 = base_calc; p2 = (base_calc + 1) % 10; p3 = (base_calc + 2) % 10
    pos_8 = ['R1_Lakh', 'R1_Muen', 'R1_Pan', 'R1_Roi', 'R1_Sib', 'R1_Nui', 'Bot_Sib', 'Bot_Nui']
    pos_3top = ['R1_Roi', 'R1_Sib', 'R1_Nui']; pos_2top = ['R1_Sib', 'R1_Nui']; pos_2bot = ['Bot_Sib', 'Bot_Nui']
    def check_hit(cols):
        mask = pd.Series([False] * len(df), index=df.index)
        for col in cols: mask = mask | (df[col] == p1) | (df[col] == p2) | (df[col] == p3)
        return mask
    hit_8pos = check_hit(pos_8); hit_3top = check_hit(pos_3top)
    hit_2top = check_hit(pos_2top); hit_2bot = check_hit(pos_2bot)
    valid_mask = ~np.isnan(base_calc); total_checks = valid_mask.sum()
    acc_8pos = (hit_8pos & valid_mask).sum() / total_checks * 100
    acc_3top = (hit_3top & valid_mask).sum() / total_checks * 100
    acc_2top = (hit_2top & valid_mask).sum() / total_checks * 100
    acc_2bot = (hit_2bot & valid_mask).sum() / total_checks * 100
    last = df.iloc[-1]
    next_base = (last['R1_Muen'] + last['R1_Sib'] + last['Bot_Nui'] + 7) % 10
    next_set = [int(next_base), int((next_base+1)%10), int((next_base+2)%10)]
    return {'Digits': next_set, 'Base': int(next_base), 'Acc_8Pos': acc_8pos, 'Acc_3Top': acc_3top, 'Acc_2Top': acc_2top, 'Acc_2Bot': acc_2bot, 'Hits_8Pos': int((hit_8pos & valid_mask).sum()), 'Total': int(total_checks)}

# ---------------------------------------------------------
# 🆕 LOGIC: 6 สูตรมหาประลัย (God Mode Logic)
# ---------------------------------------------------------
def get_variables_god_mode(row):
    p1 = [int(x) for x in str(row['รางวัลที่ 1'])]
    d2 = [int(x) for x in str(row['2 ตัวล่าง'])]
    f1 = [int(x) for x in str(row['เลขท้าย 3 ตัว (1)'])]
    f2 = [int(x) for x in str(row['เลขท้าย 3 ตัว (2)'])]
    b1 = [int(x) for x in str(row['เลขท้าย 3 ตัว (3)'])]
    b2 = [int(x) for x in str(row['เลขท้าย 3 ตัว (4)'])]
    return p1, d2, f1, f2, b1, b2

def calculate_god_formulas(p1, d2, f1, f2, b1, b2):
    results = {}
    
    # 🟢 F1: Lucky 50/50
    sum_t1 = d2[0] + (f1[0]*3) + (f2[2]*2) + b1[0] + (b2[0]*2) + (b2[1]*3) + 9
    base_t1 = sum_t1 % 10
    tens_1 = [base_t1, (base_t1+1)%10, (base_t1+5)%10]
    sum_u1 = (p1[2]*2) + (p1[3]*2) + p1[4] + (p1[5]*2) + b2[0] + 7
    base_u1 = sum_u1 % 10
    units_1 = [base_u1, (base_u1+2)%10]
    results['F1'] = {'name': 'คู่หูพารวย (Lucky)', 'tens': tens_1, 'units': units_1, 'color': '#00FF7F',
                     'eq_t': f"{d2[0]}+({f1[0]}x3)+({f2[2]}x2)+{b1[0]}+({b2[0]}x2)+({b2[1]}x3)+9",
                     'eq_u': f"({p1[2]}x2)+({p1[3]}x2)+{p1[4]}+({p1[5]}x2)+{b2[0]}+7"}

    # 🟡 F2: Emperor
    sum_t2 = p1[1] + (p1[2]*4) + (d2[0]*3) + (f1[1]*2) + (f2[2]*2) + b1[1] + 6
    base_t2 = sum_t2 % 10
    tens_2 = [(base_t2+1)%10, (base_t2+3)%10, (base_t2+8)%10]
    sum_u2 = (p1[0]*4) + (f2[0]*2) + (f2[1]*2) + (b1[0]*3) + 0
    base_u2 = sum_u2 % 10
    units_2 = [(base_u2+4)%10, (base_u2+8)%10]
    results['F2'] = {'name': 'จักรพรรดิ (Emperor)', 'tens': tens_2, 'units': units_2, 'color': '#FFD700',
                     'eq_t': f"{p1[1]}+({p1[2]}x4)+({d2[0]}x3)+({f1[1]}x2)+({f2[2]}x2)+{b1[1]}+6",
                     'eq_u': f"({p1[0]}x4)+({f2[0]}x2)+({f2[1]}x2)+({b1[0]}x3)+0"}

    # 🔴 F3: God of Wealth
    sum_t3 = (p1[3]*4) + f1[1] + (f2[0]*4) + b1[1] + (b2[0]*3) + 4
    base_t3 = sum_t3 % 10
    tens_3 = [(base_t3+1)%10, (base_t3+7)%10, (base_t3+9)%10]
    sum_u3 = (p1[3]*2) + (p1[4]*5) + (d2[1]*5) + (f1[0]*4) + f1[1] + f1[2] + (f2[0]*2) + 9
    base_u3 = sum_u3 % 10
    units_3 = [base_u3, (base_u3+5)%10]
    results['F3'] = {'name': 'มหาเทพ (God Wealth)', 'tens': tens_3, 'units': units_3, 'color': '#FF4444',
                     'eq_t': f"({p1[3]}x4)+{f1[1]}+({f2[0]}x4)+{b1[1]}+({b2[0]}x3)+4",
                     'eq_u': f"({p1[3]}x2)+({p1[4]}x5)+({d2[1]}x5)+({f1[0]}x4)+{f1[1]}+{f1[2]}+({f2[0]}x2)+9"}

    # ⚫ F4: Brutal Sage
    sum_t4 = (p1[1]*3) + (p1[4]*6) + (p1[5]*6) + (d2[1]*7) + (f1[2]*2) + (f2[2]*6) + (b1[0]*2) + 4
    base_t4 = sum_t4 % 10
    tens_4 = [(base_t4+3)%10, (base_t4+5)%10, (base_t4+6)%10]
    sum_u4 = (p1[0]*4) + (p1[1]*4) + (p1[4]*4) + (p1[5]*2) + (f1[0]*7) + (f2[1]*2) + (f2[2]*3) + 0
    base_u4 = sum_u4 % 10
    units_4 = [base_u4, (base_u4+9)%10]
    results['F4'] = {'name': 'มหาโหด (Brutal Sage)', 'tens': tens_4, 'units': units_4, 'color': '#AAAAAA',
                     'eq_t': f"({p1[1]}x3)+({p1[4]}x6)+({p1[5]}x6)+({d2[1]}x7)+({f1[2]}x2)+({f2[2]}x6)+({b1[0]}x2)+4",
                     'eq_u': f"({p1[0]}x4)+({p1[1]}x4)+({p1[4]}x4)+({p1[5]}x2)+({f1[0]}x7)+({f2[1]}x2)+({f2[2]}x3)+0"}

    # 🔵 F5: Immortal
    sum_t5 = (p1[4]*4) + (d2[1]*8) + (f1[1]*5) + (f2[1]*2) + (b1[1]*5) + (b2[0]*3) + (b2[1]*2) + (b2[2]*6) + 2
    base_t5 = sum_t5 % 10
    tens_5 = [(base_t5+3)%10, (base_t5+7)%10, (base_t5+9)%10]
    sum_u5 = p1[1] + p1[3] + (p1[4]*4) + (d2[0]*9) + f2[0] + (f2[1]*3) + (b2[0]*4) + 9
    base_u5 = sum_u5 % 10
    units_5 = [(base_u5+2)%10, (base_u5+6)%10]
    results['F5'] = {'name': 'อมตะนิรันดร์ (Immortal)', 'tens': tens_5, 'units': units_5, 'color': '#00BFFF',
                     'eq_t': f"({p1[4]}x4)+({d2[1]}x8)+({f1[1]}x5)+({f2[1]}x2)+({b1[1]}x5)+({b2[0]}x3)+({b2[1]}x2)+({b2[2]}x6)+2",
                     'eq_u': f"{p1[1]}+{p1[3]}+({p1[4]}x4)+({d2[0]}x9)+{f2[0]}+({f2[1]}x3)+({b2[0]}x4)+9"}

    # 🟣 F6: Cosmic Power
    sum_t6 = (p1[1]*7) + (p1[5]*2) + (d2[0]*7) + (f1[2]*7) + (b1[0]*7) + (b1[1]*7) + 3
    base_t6 = sum_t6 % 10
    tens_6 = [(base_t6+1)%10, (base_t6+3)%10, (base_t6+7)%10]
    sum_u6 = (d2[0]*6) + (f1[1]*4) + b1[0] + (b1[1]*2) + 8
    base_u6 = sum_u6 % 10
    units_6 = [(base_u6+2)%10, (base_u6+4)%10]
    results['F6'] = {'name': 'พลังจักรวาล (Cosmic)', 'tens': tens_6, 'units': units_6, 'color': '#9932CC',
                     'eq_t': f"({p1[1]}x7)+({p1[5]}x2)+({d2[0]}x7)+({f1[2]}x7)+({b1[0]}x7)+({b1[1]}x7)+3",
                     'eq_u': f"({d2[0]}x6)+({f1[1]}x4)+{b1[0]}+({b1[1]}x2)+8"}
    
    return results

def find_consensus_god_mode(formulas_result):
    all_pairs = []
    for key, val in formulas_result.items():
        for t in val['tens']:
            for u in val['units']:
                all_pairs.append(f"{t}{u}")
    return Counter(all_pairs).most_common()

# --- Stats Helper for 6 Formulas (20 Draws) ---
@st.cache_data
def calculate_formula_history_stats(df, lookback=20):
    if len(df) < lookback + 2: return {}
    stats = {k: {'hits': 0, 'streak': 0, 'hits_list': []} for k in ['F1', 'F2', 'F3', 'F4', 'F5', 'F6']}
    
    start_idx = len(df) - lookback
    for i in range(start_idx, len(df)):
        past_row = df.iloc[i-1]; target_row = df.iloc[i]
        pp1, pd2, pf1, pf2, pb1, pb2 = get_variables_god_mode(past_row)
        res = calculate_god_formulas(pp1, pd2, pf1, pf2, pb1, pb2)
        real_2d = str(target_row['2 ตัวล่าง']).zfill(2)
        real_top = str(target_row['2 ตัวบน']).zfill(2)
        
        for key in stats.keys():
            fval = res[key]
            f_pairs = [f"{t}{u}" for t in fval['tens'] for u in fval['units']]
            is_hit = (real_2d in f_pairs) or (real_top in f_pairs)
            if is_hit:
                stats[key]['hits'] += 1
                stats[key]['hits_list'].append(1)
            else:
                stats[key]['hits_list'].append(0)
    
    for key in stats:
        h_list = stats[key]['hits_list']
        curr_streak = 0
        for h in reversed(h_list):
            if h == 1: curr_streak += 1
            else: break
        stats[key]['streak'] = curr_streak
    return stats

# --- Killer Scan Logic ---
@st.cache_data
def scan_for_killers_v2(df):
    cols_map = {
        'Lakh': df['R1_Lakh'], 'Muen': df['R1_Muen'], 'Pan': df['R1_Pan'], 
        'Roi': df['R1_Roi'], 'Sib': df['R1_Sib'], 'Nui': df['R1_Nui'], 
        'BotSib': df['Bot_Sib'], 'BotNui': df['Bot_Nui']
    }
    input_cols = list(cols_map.keys())
    results = []
    pairs = list(itertools.combinations(input_cols, 2))
    
    for c1, c2 in pairs:
        col1_data = cols_map[c1]; col2_data = cols_map[c2]
        for k in range(10):
            pred = (col1_data + col2_data + k) % 10
            pred_shifted = pred.shift(1)
            mask = ~pred_shifted.isna(); valid_df = df[mask]; p = pred_shifted[mask]; total = len(valid_df)
            
            # Top 3
            hit_top3 = (valid_df['R1_Roi'] == p) | (valid_df['R1_Sib'] == p) | (valid_df['R1_Nui'] == p)
            success_top3 = ~hit_top3
            acc_top3 = success_top3.sum() / total * 100
            
            # Top 2
            hit_top2 = (valid_df['R1_Sib'] == p) | (valid_df['R1_Nui'] == p)
            success_top2 = ~hit_top2
            acc_top2 = success_top2.sum() / total * 100
            
            # Bot 2
            hit_bot2 = (valid_df['Bot_Sib'] == p) | (valid_df['Bot_Nui'] == p)
            success_bot2 = ~hit_bot2
            acc_bot2 = success_bot2.sum() / total * 100
            
            last_val = (cols_map[c1].iloc[-1] + cols_map[c2].iloc[-1] + k) % 10
            
            # Calculate Streaks
            cur_t3, max_t3 = (0, 0)
            cur_t2, max_t2 = (0, 0)
            cur_b2, max_b2 = (0, 0)

            if acc_top3 > 75: cur_t3, max_t3 = calculate_hit_streaks(success_top3)
            if acc_top2 > 80: cur_t2, max_t2 = calculate_hit_streaks(success_top2)
            if acc_bot2 > 80: cur_b2, max_b2 = calculate_hit_streaks(success_bot2)
            
            if acc_top3 > 75 or acc_top2 > 80 or acc_bot2 > 80:
                results.append({
                    'Formula': f"({c1}+{c2}+{k})%10", 
                    'Acc_Top3': acc_top3, 'Cur_T3': cur_t3, 'Max_T3': max_t3,
                    'Acc_Top2': acc_top2, 'Cur_T2': cur_t2, 'Max_T2': max_t2,
                    'Acc_Bot2': acc_bot2, 'Cur_B2': cur_b2, 'Max_B2': max_b2,
                    'Next_Dead': int(last_val)
                })
    return pd.DataFrame(results)

# --- Backtest Generator ---
def get_backtest_dataframe(df, periods=20):
    rows = []
    if len(df) < periods + 1: return pd.DataFrame()
    for i in range(len(df)-1, len(df)-1-periods, -1):
        target_row = df.iloc[i]; input_row = df.iloc[i-1]
        p1, d2, f1, f2, b1, b2 = get_variables_god_mode(input_row)
        formulas = calculate_god_formulas(p1, d2, f1, f2, b1, b2)
        real_2d = str(target_row['2 ตัวล่าง']).zfill(2)
        real_top = str(target_row['2 ตัวบน']).zfill(2)
        row_data = {"งวดวันที่": target_row['วันที่'], "เลขที่ออก (บน/ล่าง)": f"{real_top} / {real_2d}"}
        for key in formulas.keys():
            f_data = formulas[key]
            f_pairs = [f"{t}{u}" for t in f_data['tens'] for u in f_data['units']]
            hits = []
            if real_top in f_pairs: hits.append("บน")
            if real_2d in f_pairs: hits.append("ล่าง")
            row_data[f_data['name']] = "✅ " + ",".join(hits) if hits else "❌"
        rows.append(row_data)
    return pd.DataFrame(rows)

# ---------------------------------------------------------
# 4. ส่วนแสดงผล (UI Logic)
# ---------------------------------------------------------
df = load_data()

st.sidebar.title("🐯 Lotto Master")
if 'current_page' in st.session_state:
    if st.session_state.current_page in ALL_PAGES: idx = ALL_PAGES.index(st.session_state.current_page)
    else: idx = 0
    page = st.sidebar.radio("เลือกเมนู:", ALL_PAGES, index=idx, key="sidebar_nav")
    if page != st.session_state.current_page: st.session_state.current_page = page; st.rerun()
else: page = st.sidebar.radio("เลือกเมนู:", ALL_PAGES, key="sidebar_nav")

if not df.empty:
    st.sidebar.markdown("---"); st.sidebar.subheader("🔥 สถิติฮิตตลอดกาล")
    t2 = df['2 ตัวบน'].value_counts().head(2); b2 = df['2 ตัวล่าง'].value_counts().head(2)
    c1, c2 = st.sidebar.columns(2)
    with c1: st.markdown(f"<div class='sidebar-stat-box'><div class='sidebar-stat-label'>บนฮิต</div><div class='sidebar-stat-num'>{t2.index[0]}</div></div>", unsafe_allow_html=True)
    with c2: st.markdown(f"<div class='sidebar-stat-box'><div class='sidebar-stat-label'>ล่างฮิต</div><div class='sidebar-stat-num'>{b2.index[0]}</div></div>", unsafe_allow_html=True)

st.markdown(custom_css, unsafe_allow_html=True)

# ==========================================
# 🏠 หน้าที่ 0: หน้าแรก (6 สูตรมหาประลัย)
# ==========================================
if page == "🏠 หน้าแรก (6 สูตรมหาประลัย)":
    if df.empty: st.error("No Data"); st.stop()
    last = df.iloc[-1]
    
    # Hero Section
    st.markdown(f"""
    <div class='hero-container'>
        <div style="color:#aaa; font-size:18px;">งวดวันที่ {last['วันที่']}</div>
        <div class='hero-number'>{last['รางวัลที่ 1']}</div>
        <div style="display:flex; justify-content:center; gap:20px; margin-top:10px;">
            <div style="background:#222; padding:5px 15px; border-radius:10px; border:1px solid #444;">
                <span style="color:#888; font-size:12px;">3 ตัวหน้า</span><br>
                <span style="color:#eee; font-weight:bold;">{last['เลขท้าย 3 ตัว (1)']} | {last['เลขท้าย 3 ตัว (2)']}</span>
            </div>
            <div style="background:#222; padding:5px 15px; border-radius:10px; border:1px solid #444;">
                <span style="color:#888; font-size:12px;">3 ตัวท้าย</span><br>
                <span style="color:#eee; font-weight:bold;">{last['เลขท้าย 3 ตัว (3)']} | {last['เลขท้าย 3 ตัว (4)']}</span>
            </div>
            <div style="background:#222; padding:5px 15px; border-radius:10px; border:1px solid #FFD700;">
                <span style="color:#888; font-size:12px;">2 ตัวล่าง</span><br>
                <span style="color:#FFD700; font-weight:bold; font-size:20px;">{last['2 ตัวล่าง']}</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Calculate Logic
    p1, d2, f1, f2, b1, b2 = get_variables_god_mode(last)
    formulas = calculate_god_formulas(p1, d2, f1, f2, b1, b2)
    consensus = find_consensus_god_mode(formulas)
    f_stats = calculate_formula_history_stats(df, lookback=20)
    
    # Determine Ranks
    sorted_stats = sorted(f_stats.items(), key=lambda x: (x[1]['hits'], x[1]['streak']), reverse=True)
    rank_map = {}
    if len(sorted_stats) > 0: rank_map[sorted_stats[0][0]] = ("👑 #1", "rank-1")
    if len(sorted_stats) > 1: rank_map[sorted_stats[1][0]] = ("🥈 #2", "rank-2")
    if len(sorted_stats) > 2: rank_map[sorted_stats[2][0]] = ("🥉 #3", "rank-3")

    # Main Layout
    col_main, col_sidebar = st.columns([3, 1.2])

    with col_main:
        st.markdown("### ✨ 6 สูตรมหาประลัย (ทำนายงวดหน้า)")
        
        # Function to generate card HTML (NO INDENTATION - FIXED!)
        def create_card_html(key_id):
            val = formulas[key_id]
            stats = f_stats.get(key_id, {'hits':0,'streak':0})
            
            rank_html = ""
            if key_id in rank_map:
                label, css_class = rank_map[key_id]
                rank_html = f"<div class='rank-badge {css_class}'>{label}</div>"

            tens_html = "".join([f"<span class='f-val-badge'>{x}</span>" for x in val['tens']])
            units_html = "".join([f"<span class='f-val-badge'>{x}</span>" for x in val['units']])
            pairs_html = ", ".join([f"{t}{u}" for t in val['tens'] for u in val['units']])

            return f"""
<div class="formula-card-home" style="border-left: 5px solid {val['color']};">
{rank_html}
<div class="f-header">
<div class="f-title" style="color:{val['color']};">{val['name']}</div>
<div class="f-stats-badge">เข้า {stats['hits']}/20 | ติดกัน {stats['streak']}</div>
</div>
<div class="f-row"><span class="f-label">สิบ:</span> {tens_html}</div>
<div class="f-row"><span class="f-label">หน่วย:</span> {units_html}</div>
<div class="f-pair-box">{pairs_html}</div>
</div>
"""

        # Grid System for 6 Cards
        row1_1, row1_2 = st.columns(2)
        with row1_1: st.markdown(create_card_html('F1'), unsafe_allow_html=True)
        with row1_2: st.markdown(create_card_html('F2'), unsafe_allow_html=True)

        row2_1, row2_2 = st.columns(2)
        with row2_1: st.markdown(create_card_html('F3'), unsafe_allow_html=True)
        with row2_2: st.markdown(create_card_html('F4'), unsafe_allow_html=True)

        row3_1, row3_2 = st.columns(2)
        with row3_1: st.markdown(create_card_html('F5'), unsafe_allow_html=True)
        with row3_2: st.markdown(create_card_html('F6'), unsafe_allow_html=True)

    with col_sidebar:
        # Consensus Box (Fixed!)
        top_pick = consensus[0] if consensus else ("--", 0)
        st.markdown(f"""
        <div class="consensus-box">
            <div class="consensus-title">🔥 ชนแรงสุด</div>
            <div class="consensus-number">{top_pick[0]}</div>
            <div class="consensus-desc">ชนกัน {top_pick[1]} สูตร</div>
        </div>""", unsafe_allow_html=True)

        # Killer Scan (SideBar - Complete with Bot 2)
        st.markdown("#### 💀 เลขดับ (Auto Scan)")
        k_df = scan_for_killers_v2(df)
        if not k_df.empty:
            # Top 3
            best_kill_3 = k_df.sort_values('Acc_Top3', ascending=False).iloc[0]
            st.markdown(f"""
            <div class="killer-box">
                <div style="font-size:14px; color:#fff;">ดับบน (3 ตัว)</div>
                <div class="killer-digit">{best_kill_3['Next_Dead']}</div>
                <div style="font-size:10px; color:#aaa;">ความแม่นยำ {best_kill_3['Acc_Top3']:.1f}%</div>
            </div>""", unsafe_allow_html=True)
            
            # Top 2
            best_kill_2 = k_df.sort_values('Acc_Top2', ascending=False).iloc[0]
            st.markdown(f"""
            <div class="killer-box" style="border-color:#ff8800;">
                <div style="font-size:14px; color:#fff;">ดับบน (2 ตัว)</div>
                <div class="killer-digit" style="color:#ff8800;">{best_kill_2['Next_Dead']}</div>
                <div style="font-size:10px; color:#aaa;">ความแม่นยำ {best_kill_2['Acc_Top2']:.1f}%</div>
            </div>""", unsafe_allow_html=True)

            # Bot 2
            best_kill_b2 = k_df.sort_values('Acc_Bot2', ascending=False).iloc[0]
            st.markdown(f"""
            <div class="killer-box" style="border-color:#00BFFF;">
                <div style="font-size:14px; color:#fff;">ดับล่าง (2 ตัว)</div>
                <div class="killer-digit" style="color:#00BFFF;">{best_kill_b2['Next_Dead']}</div>
                <div style="font-size:10px; color:#aaa;">ความแม่นยำ {best_kill_b2['Acc_Bot2']:.1f}%</div>
            </div>""", unsafe_allow_html=True)
        else:
            st.info("กำลังประมวลผล...")

    st.divider()
    with st.expander("📊 ตรวจสอบผลงานย้อนหลัง (Backtest)", expanded=False):
        bt_df = get_backtest_dataframe(df)
        st.dataframe(bt_df, use_container_width=True, hide_index=True)

# ==========================================
# 🔑 ห้องแห่งความลับ (Secret Chamber) - LOCKED!
# ==========================================
elif page == "🔑 ห้องแห่งความลับ (Secret Chamber)":
    # --- SECURITY CHECK ---
    if not st.session_state.secret_unlocked:
        st.title("🔒 พื้นที่หวงห้าม (Restricted Area)")
        st.markdown("""
        <div class="login-box">
            <h2 style="color:#FF4444;">⚠️ TOP SECRET ⚠️</h2>
            <p style="color:#ccc;">กรุณายืนยันตัวตนเพื่อเข้าถึงข้อมูลระดับสูง</p>
        </div>
        """, unsafe_allow_html=True)
        
        c1, c2, c3 = st.columns([1, 2, 1])
        with c2:
            with st.form("secret_login"):
                password = st.text_input("🔑 คำถาม: ใครคือผู้คิดสูตร?", type="password")
                submit_btn = st.form_submit_button("ปลดล็อค (Unlock)", use_container_width=True)
                
                if submit_btn:
                    if password == "root":
                        st.session_state.secret_unlocked = True
                        st.success("✅ Access Granted! ยินดีต้อนรับครับนายท่าน")
                        time.sleep(1)
                        st.rerun()
                    else:
                        st.error("❌ Access Denied! รหัสผ่านผิดพลาด")

    else:
        # --- UNLOCKED CONTENT ---
        st.title("🔑 ห้องแห่งความลับ (Secret Chamber)")
        st.caption("เผยความลับเบื้องหลังทุกสูตรคำนวณแบบเจาะลึก (ภาษาชาวบ้าน)")
        
        st.markdown("""
        <div style="background:#222; padding:20px; border-radius:15px; border-left:5px solid #FFD700; margin-bottom:20px;">
            <h3>📜 คัมภีร์สูตรมหาประลัย (6 Gods)</h3>
            <p style="color:#ccc;">
                นี่คือ "ไส้ใน" ของ 6 สูตรหลักที่เราใช้คำนวณครับ หลักการคือการเอา <b>ตำแหน่งต่างๆ ของรางวัลที่ 1 และเลขท้าย 3 ตัว (หน้า/หลัง)</b> 
                ในงวดที่แล้ว มาบวกกันตามสูตรลับเฉพาะ แล้วเดินแต้มเพิ่มเพื่อหาเลขเด่น
            </p>
        </div>
        """, unsafe_allow_html=True)

        c1, c2 = st.columns(2)
        
        with c1:
            st.markdown(f"""
            <div class="secret-card" style="border-left:4px solid #00FF7F;">
                <div class="secret-formula-title">1. คู่หูพารวย (Lucky)</div>
                <div class="secret-eq-box">
                    <div class="secret-hl">หลักสิบ:</div>
                    <span style="color:#aaa;">สิบล่าง + (ร้อยหน้า1 x3) + (หน่วยหน้า2 x2) + ร้อยหลัง1 + (ร้อยหลัง2 x2) + (สิบหลัง2 x3) + 9</span>
                    <br><span class="secret-step">⏩ เดินแต้ม: +0, +1, +5</span>
                </div>
                <div class="secret-eq-box">
                    <div class="secret-hl">หลักหน่วย:</div>
                    <span style="color:#aaa;">(พัน x2) + (ร้อย x2) + สิบ + (หน่วย x2) + ร้อยหลัง2 + 7</span>
                    <br><span class="secret-step">⏩ เดินแต้ม: +0, +2</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown(f"""
            <div class="secret-card" style="border-left:4px solid #FFD700;">
                <div class="secret-formula-title">2. จักรพรรดิ (Emperor)</div>
                <div class="secret-eq-box">
                    <div class="secret-hl">หลักสิบ:</div>
                    <span style="color:#aaa;">หมื่น + (พัน x4) + (สิบล่าง x3) + (สิบหน้า1 x2) + (หน่วยหน้า2 x2) + สิบหลัง1 + 6</span>
                    <br><span class="secret-step">⏩ เดินแต้ม: +1, +3, +8</span>
                </div>
                <div class="secret-eq-box">
                    <div class="secret-hl">หลักหน่วย:</div>
                    <span style="color:#aaa;">(แสน x4) + (ร้อยหน้า2 x2) + (สิบหน้า2 x2) + (ร้อยหลัง1 x3) + 0</span>
                    <br><span class="secret-step">⏩ เดินแต้ม: +4, +8</span>
                </div>
            </div>
            """, unsafe_allow_html=True)

            st.markdown(f"""
            <div class="secret-card" style="border-left:4px solid #FF4444;">
                <div class="secret-formula-title">3. มหาเทพ (God Wealth)</div>
                <div class="secret-eq-box">
                    <div class="secret-hl">หลักสิบ:</div>
                    <span style="color:#aaa;">(ร้อย x4) + สิบหน้า1 + (ร้อยหน้า2 x4) + สิบหลัง1 + (ร้อยหลัง2 x3) + 4</span>
                    <br><span class="secret-step">⏩ เดินแต้ม: +1, +7, +9</span>
                </div>
                <div class="secret-eq-box">
                    <div class="secret-hl">หลักหน่วย:</div>
                    <span style="color:#aaa;">(ร้อย x2) + (สิบ x5) + (หน่วยล่าง x5) + (ร้อยหน้า1 x4) + สิบหน้า1 + หน่วยหน้า1 + (ร้อยหน้า2 x2) + 9</span>
                    <br><span class="secret-step">⏩ เดินแต้ม: +0, +5</span>
                </div>
            </div>
            """, unsafe_allow_html=True)

        with c2:
            st.markdown(f"""
            <div class="secret-card" style="border-left:4px solid #AAAAAA;">
                <div class="secret-formula-title">4. มหาโหด (Brutal Sage)</div>
                <div class="secret-eq-box">
                    <div class="secret-hl">หลักสิบ:</div>
                    <span style="color:#aaa;">(หมื่น x3) + (สิบ x6) + (หน่วย x6) + (หน่วยล่าง x7) + (หน่วยหน้า1 x2) + (หน่วยหน้า2 x6) + (ร้อยหลัง1 x2) + 4</span>
                    <br><span class="secret-step">⏩ เดินแต้ม: +3, +5, +6</span>
                </div>
                <div class="secret-eq-box">
                    <div class="secret-hl">หลักหน่วย:</div>
                    <span style="color:#aaa;">(แสน x4) + (หมื่น x4) + (สิบ x4) + (หน่วย x2) + (ร้อยหน้า1 x7) + (สิบหน้า2 x2) + (หน่วยหน้า2 x3) + 0</span>
                    <br><span class="secret-step">⏩ เดินแต้ม: +0, +9</span>
                </div>
            </div>
            """, unsafe_allow_html=True)

            st.markdown(f"""
            <div class="secret-card" style="border-left:4px solid #00BFFF;">
                <div class="secret-formula-title">5. อมตะนิรันดร์ (Immortal)</div>
                <div class="secret-eq-box">
                    <div class="secret-hl">หลักสิบ:</div>
                    <span style="color:#aaa;">(สิบ x4) + (หน่วยล่าง x8) + (สิบหน้า1 x5) + (สิบหน้า2 x2) + (สิบหลัง1 x5) + (ร้อยหลัง2 x3) + (สิบหลัง2 x2) + (หน่วยหลัง2 x6) + 2</span>
                    <br><span class="secret-step">⏩ เดินแต้ม: +3, +7, +9</span>
                </div>
                <div class="secret-eq-box">
                    <div class="secret-hl">หลักหน่วย:</div>
                    <span style="color:#aaa;">หมื่น + ร้อย + (สิบ x4) + (สิบล่าง x9) + ร้อยหน้า2 + (สิบหน้า2 x3) + (ร้อยหลัง2 x4) + 9</span>
                    <br><span class="secret-step">⏩ เดินแต้ม: +2, +6</span>
                </div>
            </div>
            """, unsafe_allow_html=True)

            st.markdown(f"""
            <div class="secret-card" style="border-left:4px solid #9932CC;">
                <div class="secret-formula-title">6. พลังจักรวาล (Cosmic)</div>
                <div class="secret-eq-box">
                    <div class="secret-hl">หลักสิบ:</div>
                    <span style="color:#aaa;">(หมื่น x7) + (หน่วย x2) + (สิบล่าง x7) + (หน่วยหน้า1 x7) + (ร้อยหลัง1 x7) + (สิบหลัง1 x7) + 3</span>
                    <br><span class="secret-step">⏩ เดินแต้ม: +1, +3, +7</span>
                </div>
                <div class="secret-eq-box">
                    <div class="secret-hl">หลักหน่วย:</div>
                    <span style="color:#aaa;">(สิบล่าง x6) + (สิบหน้า1 x4) + ร้อยหลัง1 + (สิบหลัง1 x2) + 8</span>
                    <br><span class="secret-step">⏩ เดินแต้ม: +2, +4</span>
                </div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("---")
        st.markdown("""
        <div class="secret-layer-box">
            <h3 style="color:#00BFFF; border-bottom:1px solid #444; padding-bottom:10px;">🧬 ความลับ: สูตรลับ 5 ชั้น (AI Spin) หาหลักสิบยังไง?</h3>
            <p style="color:#eee; font-size:16px;">
                สูตรนี้ <b>"ไม่ได้ใช้การบวกเลข"</b> เหมือน 6 สูตรข้างบนครับ แต่มันคือการใช้ AI (Artificial Intelligence) 
                สแกนหา <b>"พฤติกรรมของตัวเลข" (Behavior Pattern)</b> จากสถิติย้อนหลัง โดยเจาะลึก 5 ชั้น (Layers) ดังนี้:
            </p>
            <div style="background:#111; padding:15px; border-radius:10px; margin-top:10px;">
                <p style="color:#FFD700;">🔍 <b>คำถามที่ AI ถามสถิติเก่า:</b> "เมื่องวดที่แล้วออกเลขนี้... งวดต่อไปเลข <b>หลักสิบ</b> อะไรที่ชอบตามมา?"</p>
                <ul style="color:#ccc; line-height:1.8;">
                    <li><b>ชั้นที่ 1 (Top Ten Base):</b> เช็คจาก "หลักสิบบน" งวดที่แล้ว -> หาคู่เหมือนในอดีต -> ดูว่าตอนนั้นหลักสิบออกอะไรบ่อยสุด</li>
                    <li><b>ชั้นที่ 2 (Top Unit Base):</b> เช็คจาก "หลักหน่วยบน" งวดที่แล้ว -> หาคู่เหมือน -> ดูผลลัพธ์หลักสิบ</li>
                    <li><b>ชั้นที่ 3 (Bot Ten Base):</b> เช็คจาก "หลักสิบล่าง" งวดที่แล้ว -> หาคู่เหมือน -> ดูผลลัพธ์หลักสิบ</li>
                    <li><b>ชั้นที่ 4 (Bot Unit Base):</b> เช็คจาก "หลักหน่วยล่าง" งวดที่แล้ว -> หาคู่เหมือน -> ดูผลลัพธ์หลักสิบ</li>
                    <li><b>ชั้นที่ 5 (Lag Move):</b> เช็คจาก "หลักสิบบน ของงวดก่อนหน้า" (ย้อน 2 งวด) -> ดูแรงส่งตกกระทบ</li>
                </ul>
                <p style="color:#00FF7F; margin-top:10px;">
                    ✅ <b>ผลลัพธ์:</b> AI จะเอาคะแนนความถี่จากทั้ง 5 ชั้นมารวมกัน ตัวเลขไหนได้คะแนนสูงสุด 3 อันดับแรก จะถูกคัดมาเป็น <b>"เลขเด่นหลักสิบ"</b> ครับ
                </p>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("🔒 ล็อคห้องความลับ (Logout)"):
            st.session_state.secret_unlocked = False
            st.rerun()

# ==========================================
# 🧪 ห้องวิจัยสูตร (Formula Lab)
# ==========================================
elif page == "🧪 ห้องวิจัยสูตร (Formula Lab)":
    st.title("🧪 ห้องวิจัยสูตร (Formula Lab)")
    st.caption("เจาะลึกที่มาของตัวเลข ดูสมการ และตรวจสอบความแม่นยำย้อนหลัง")
    
    if df.empty: st.error("No Data"); st.stop()
    
    # 1. Select Draw
    draws = df['วันที่'].tolist()[::-1] 
    selected_date = st.selectbox("📅 เลือกงวดที่ต้องการตรวจสอบ:", draws[:20]) 
    idx = df[df['วันที่'] == selected_date].index[0]
    
    if idx == len(df)-1:
        st.info("คุณเลือกงวดล่าสุด (ทำนายอนาคต) - ยังไม่มีผลรางวัลให้ตรวจ")
        target_row = None
    else:
        target_row = df.iloc[idx+1] # Next draw (Result)
        
    curr_row = df.iloc[idx] # Input draw
    
    # 2. Input Data
    st.markdown("### 🔢 ข้อมูลตั้งต้น (Input)")
    c1, c2, c3, c4 = st.columns(4)
    with c1: st.metric("รางวัลที่ 1", curr_row['รางวัลที่ 1'])
    with c2: st.metric("2 ตัวล่าง", curr_row['2 ตัวล่าง'])
    with c3: st.metric("3 ตัวหน้า", f"{curr_row['เลขท้าย 3 ตัว (1)']} - {curr_row['เลขท้าย 3 ตัว (2)']}")
    with c4: st.metric("3 ตัวหลัง", f"{curr_row['เลขท้าย 3 ตัว (3)']} - {curr_row['เลขท้าย 3 ตัว (4)']}")
    
    st.divider()
    
    # 3. Formula Execution
    p1, d2, f1, f2, b1, b2 = get_variables_god_mode(curr_row)
    formulas = calculate_god_formulas(p1, d2, f1, f2, b1, b2)
    
    real_top = str(target_row['2 ตัวบน']).zfill(2) if target_row is not None else "??"
    real_bot = str(target_row['2 ตัวล่าง']).zfill(2) if target_row is not None else "??"
    
    st.markdown("### 🔬 ผลการวิเคราะห์แยกรายสูตร")
    
    c_form1, c_form2 = st.columns(2)
    cols_ref = [c_form1, c_form2]
    
    for i, (key, val) in enumerate(formulas.items()):
        pairs = [f"{t}{u}" for t in val['tens'] for u in val['units']]
        hit_status = "รอผล"; hit_color = "#888"
        pair_html_list = []
        
        # Check Hit Logic
        if target_row is not None:
            is_top = real_top in pairs; is_bot = real_bot in pairs
            if is_top and is_bot: 
                hit_status = "✅ เข้าทั้ง บน/ล่าง"; hit_color = "#00FF7F"
            elif is_top: 
                hit_status = "✅ เข้าบน"; hit_color = "#00FF7F"
            elif is_bot: 
                hit_status = "✅ เข้าล่าง"; hit_color = "#00FF7F"
            else: 
                hit_status = "❌ หลุด"; hit_color = "#FF4444"
            
            # Create HTML for pairs
            for p in pairs:
                if p == real_top or p == real_bot:
                    pair_html_list.append(f"<span class='lab-item-hit'>{p}</span>")
                else:
                    pair_html_list.append(f"<span class='lab-item-normal'>{p}</span>")
        else:
            # Future draw
            pair_html_list = [f"<span class='lab-item-normal'>{p}</span>" for p in pairs]
            
        display_html = "".join(pair_html_list)
            
        with cols_ref[i%2]:
            # HTML BLOCK FIXED (Left Aligned)
            st.markdown(f"""
<div class="lab-card" style="border-left: 5px solid {val['color']}">
<div class="lab-header">
<div class="lab-title" style="color:{val['color']}">{val['name']}</div>
<div class="lab-result-chk" style="color:{hit_color}; border-color:{hit_color};">{hit_status}</div>
</div>
<div style="font-size:12px; color:#aaa; margin-bottom:4px;">สมการหลักสิบ:</div>
<div class="lab-eq">{val['eq_t']}</div>
<div style="font-size:12px; color:#aaa; margin-bottom:4px;">สมการหลักหน่วย:</div>
<div class="lab-eq">{val['eq_u']}</div>
<div class="lab-res-box">
<div class="lab-digit" style="color:{val['color']}">{val['tens']}</div>
<div style="font-size:20px; font-weight:bold; color:#666;">X</div>
<div class="lab-digit" style="color:{val['color']}">{val['units']}</div>
</div>
<div class="lab-pairs-container">{display_html}</div>
</div>
""", unsafe_allow_html=True)
            
    if target_row is not None:
        st.markdown(f"""
        <div class="prediction-box">
            <div class="pred-title">เฉลยงวดถัดไป ({target_row['วันที่']})</div>
            <span style="font-size:24px; margin-right:20px; color:#CCC;">บน: <b style="color:#00FF7F; font-size:40px;">{real_top}</b></span>
            <span style="font-size:24px; color:#CCC;">ล่าง: <b style="color:#00FF7F; font-size:40px;">{real_bot}</b></span>
        </div>""", unsafe_allow_html=True)
    else:
        # Show Big Prediction for Next Draw
        all_p = []
        for k, v in formulas.items():
            all_p.extend([f"{t}{u}" for t in v['tens'] for u in v['units']])
        top_consensus = Counter(all_p).most_common(3)
        cons_html = " ".join([f"<span style='color:#FFD700; margin:0 10px;'>{n[0]}</span>" for n in top_consensus])
        
        st.markdown(f"""
        <div class="prediction-box">
            <div class="pred-title">🔮 รอผลเก็งงวดนี้ (Top 3 มาแรง)</div>
            <div class="pred-pairs">{cons_html}</div>
        </div>""", unsafe_allow_html=True)

# ==========================================
# 🔍 นักสืบตัวเลข
# ==========================================
elif page == "🔍 นักสืบตัวเลข":
    st.title("🕵️‍♂️ นักสืบตัวเลข (Sherlock Mode)")
    st.caption("เจาะลึกสถิติ ทั้งบนและล่าง | ดูพฤติกรรมเลข | ทำนายเลขตามตูด (Next Mover)")
    col_inp1, col_inp2 = st.columns([3, 1])
    with col_inp1: search_num = st.text_input("ใส่เลขที่สงสัย (2 หรือ 3 ตัว):", max_chars=3, placeholder="เช่น 85 หรือ 924")
    with col_inp2: st.write(""); st.write(""); btn_search = st.button("🔍 สืบเลย", type="primary", use_container_width=True, key="search_btn_detective")

    if st.session_state.get('search_btn_detective', 0) > 0 and search_num:
        def show_detective_result(title, data_df, target_col, number):
            st.markdown(f"#### {title}: <span style='color:#FFD700;'>{number}</span>", unsafe_allow_html=True)
            if target_col == '3_bottom_mixed':
                mask = (data_df['เลขท้าย 3 ตัว (1)'] == number) | (data_df['เลขท้าย 3 ตัว (2)'] == number) | (data_df['เลขท้าย 3 ตัว (3)'] == number) | (data_df['เลขท้าย 3 ตัว (4)'] == number)
                found = data_df[mask]
            elif target_col == '3_top': found = data_df[data_df['รางวัลที่ 1'].str.endswith(number)]
            else: found = data_df[data_df[target_col] == number]
            count = len(found)
            if count > 0:
                last_date = found.iloc[-1]['วันที่']; last_index = found.index[-1]; current_index = data_df.index[-1]; gap = current_index - last_index; gap_text = f"{gap}" if gap > 0 else "✨ ออกงวดล่าสุด"
                c1, c2, c3 = st.columns(3)
                with c1: st.markdown(f"<div class='stat-card'><div class='stat-val'>{count}</div><div class='stat-label'>ครั้งที่ออก</div></div>", unsafe_allow_html=True)
                with c2: st.markdown(f"<div class='stat-card'><div class='stat-val'>{last_date}</div><div class='stat-label'>ล่าสุดเมื่อ</div></div>", unsafe_allow_html=True)
                with c3: st.markdown(f"<div class='stat-card'><div class='stat-val'>{gap_text}</div><div class='stat-label'>ห่างหาย (งวด)</div></div>", unsafe_allow_html=True)
                st.write(""); st.write("**📅 พฤติกรรมการออก:**")
                days = found['date_obj'].dt.day; day_1 = len(days[days == 1]); day_16 = len(days[days == 16])
                bar_data = pd.DataFrame({'วัน': ['ต้นเดือน (1)', 'กลางเดือน (16)'], 'จำนวน': [day_1, day_16]})
                st.bar_chart(bar_data.set_index('วัน'), color="#FFD700")
                if target_col != '3_bottom_mixed':
                    st.write("**🔮 เลขตามตูด (Next Mover):** งวดถัดไปมักออกเลขอะไร?")
                    next_draw_numbers = []
                    for idx in found.index:
                        if idx + 1 < len(data_df):
                            val = data_df.iloc[idx + 1]['รางวัลที่ 1' if target_col == '3_top' else target_col]
                            if target_col == '3_top': val = val[-3:]
                            next_draw_numbers.append(val)
                    if next_draw_numbers:
                        common = Counter(next_draw_numbers).most_common(4); cols_f = st.columns(4)
                        for i, (num, cnt) in enumerate(common):
                            with cols_f[i]: st.markdown(f"<div class='follower-box'>{num}<br><span class='follower-desc'>ตาม {cnt} ครั้ง</span></div>", unsafe_allow_html=True)
                with st.expander(f"📜 ประวัติการออกของ {number}"):
                    if target_col == '3_bottom_mixed': st.dataframe(found[['วันที่', 'เลขท้าย 3 ตัว (1)', 'เลขท้าย 3 ตัว (2)', 'เลขท้าย 3 ตัว (3)', 'เลขท้าย 3 ตัว (4)']], use_container_width=True)
                    else: st.dataframe(found[['วันที่', 'รางวัลที่ 1', '2 ตัวล่าง']], use_container_width=True)
            else: st.warning(f"❌ ไม่พบประวัติเลข {number} ในหมวดนี้")

        if len(search_num) == 2:
            st.info(f"🔎 ผลการสืบสวนเลข 2 หลัก: **{search_num}**")
            tab1, tab2 = st.tabs(["☁️ 2 ตัวบน (ท้ายรางวัลที่ 1)", "👇 2 ตัวล่าง"])
            with tab1: show_detective_result("สถิติ 2 ตัวบน", df, '2 ตัวบน', search_num)
            with tab2: show_detective_result("สถิติ 2 ตัวล่าง", df, '2 ตัวล่าง', search_num)
        elif len(search_num) == 3:
            st.info(f"🔎 ผลการสืบสวนเลข 3 หลัก: **{search_num}**")
            tab1, tab2 = st.tabs(["☁️ 3 ตัวบน (ท้ายรางวัลที่ 1)", "🎁 3 ตัวหน้า/ล่าง (รางวัลหมุน)"])
            with tab1: show_detective_result("สถิติ 3 ตัวบน", df, '3_top', search_num)
            with tab2: show_detective_result("สถิติ 3 ตัวหน้า/ล่าง", df, '3_bottom_mixed', search_num)
        else: st.error("กรุณากรอกตัวเลข 2 หรือ 3 หลักเท่านั้นครับ")
    elif st.session_state.get('search_btn_detective', 0) > 0: st.error("กรุณากรอกตัวเลขที่ต้องการสืบ")
    
    st.divider()
    with st.expander("📂 ฐานข้อมูลผลรางวัลย้อนหลัง (Full Database)", expanded=False):
        st.dataframe(df.iloc[::-1][['วันที่', 'รางวัลที่ 1', '2 ตัวล่าง', 'เลขท้าย 3 ตัว (1)', 'เลขท้าย 3 ตัว (2)', 'เลขท้าย 3 ตัว (3)', 'เลขท้าย 3 ตัว (4)']], use_container_width=True)

# ==========================================
# 🧬 สูตรลับ 5 ชั้น (AI Spin)
# ==========================================
elif page == "🧬 สูตรลับ 5 ชั้น (AI Spin)":
    st.title("🧬 สูตรหวย 5 ชั้น (AI Focus Spin)")
    st.caption("คัดเน้น 4 ตัว + สำรอง 4 ตัว | ตัวเลขใหญ่พิเศษ!")
    if 'is_calculated' not in st.session_state: st.session_state.is_calculated = False
    if 'top_main' not in st.session_state: st.session_state.top_main = []
    if 'top_backup' not in st.session_state: st.session_state.top_backup = []
    if 'bot_main' not in st.session_state: st.session_state.bot_main = []
    if 'bot_backup' not in st.session_state: st.session_state.bot_backup = []

    if st.button("🚀 1. เริ่มคำนวณสูตร 16 คู่ (Start)", type="primary", use_container_width=True):
        with st.spinner('กำลังวิเคราะห์ 5 Layers...'):
            time.sleep(1)
            st.session_state.top_ten = calculate_formula_rank(df, 'Top_Ten')
            st.session_state.top_unit = calculate_formula_rank(df, 'Top_Unit')
            st.session_state.bot_ten = calculate_formula_rank(df, 'Bot_Ten')
            st.session_state.bot_unit = calculate_formula_rank(df, 'Bot_Unit')
            st.session_state.is_calculated = True
            st.session_state.top_main = []; st.session_state.top_backup = []
            st.session_state.bot_main = []; st.session_state.bot_backup = []

    if st.session_state.is_calculated:
        st.markdown("<div style='text-align:center; font-size:30px; color:#FFD700;'>✨ เลขเด่นงวดต่อไป ✨</div>", unsafe_allow_html=True)
        tab1, tab2 = st.tabs(["👆 วิเคราะห์ชุดบน", "👇 วิเคราะห์ชุดล่าง"])
        with tab1:
            pairs_top = [f"{t}{u}" for t in st.session_state.top_ten for u in st.session_state.top_unit]
            c_btn1, c_btn2 = st.columns(2)
            with c_btn1:
                if st.button("🎰 2.1 หมุนคัดเน้น (4 ตัว)", key="spin_top_main", use_container_width=True):
                    st.session_state.top_main = []; r = st.empty(); p = pairs_top.copy()
                    for i in range(4):
                        if not p: break
                        target = random.choice(p); p.remove(target)
                        for _ in range(5): r.markdown(f"<div class='rolling-box'>{random.choice(pairs_top)}</div>", unsafe_allow_html=True); time.sleep(0.05)
                        for _ in range(3): r.markdown(f"<div class='rolling-box'>{random.choice(pairs_top)}</div>", unsafe_allow_html=True); time.sleep(0.1)
                        html_res = f"<div class='main-box'>{target}</div>"; r.markdown(html_res, unsafe_allow_html=True); time.sleep(0.3)
                        st.session_state.top_main.append(target)
                    r.empty()
            with c_btn2:
                if st.button("🛡️ 2.2 หมุนเลขสำรอง (4 ตัว)", key="spin_top_backup", use_container_width=True):
                    st.session_state.top_backup = []; pool_backup = [p for p in pairs_top if p not in st.session_state.top_main]
                    roll_area = st.empty()
                    if pool_backup:
                        for i in range(4):
                            if not pool_backup: break
                            target = random.choice(pool_backup); pool_backup.remove(target)
                            for _ in range(5): roll_area.markdown(f"<div class='rolling-box'>{random.choice(pairs_top)}</div>", unsafe_allow_html=True); time.sleep(0.05)
                            html_res = f"<div class='backup-box'>{target}</div>"; roll_area.markdown(html_res, unsafe_allow_html=True); time.sleep(0.2)
                            st.session_state.top_backup.append(target)
                        roll_area.empty()
                    else: st.warning("ไม่มีเลขเหลือให้สำรองแล้ว")
            if st.session_state.top_main:
                st.divider(); st.markdown("### 🔥 ชุดเน้น (Main Focus)"); cols_m = st.columns(4)
                for i, p in enumerate(st.session_state.top_main): 
                    with cols_m[i]: st.markdown(f"<div class='main-box'>{p}</div>", unsafe_allow_html=True)
            if st.session_state.top_backup:
                st.markdown("### 🛡️ ชุดสำรอง (Backup)"); cols_b = st.columns(4)
                for i, p in enumerate(st.session_state.top_backup): 
                    with cols_b[i]: st.markdown(f"<div class='backup-box'>{p}</div>", unsafe_allow_html=True)
            if st.session_state.top_main:
                all_nums = " - ".join(st.session_state.top_main); backup_nums = " - ".join(st.session_state.top_backup) if st.session_state.top_backup else "-"
                st.markdown(f"<div class='summary-box'>📋 <b>สรุปแนวทางบน:</b><br>เน้น: <span style='font-size: 48px; color:#FFD700;'>{all_nums}</span><br>รอง: <span style='color:#C0C0C0;'>{backup_nums}</span></div>", unsafe_allow_html=True)
            with st.expander("🔎 ดูตาราง 16 คู่ทั้งหมด"): st.write(pairs_top)

        with tab2:
            pairs_bot = [f"{t}{u}" for t in st.session_state.bot_ten for u in st.session_state.bot_unit]
            c_btn3, c_btn4 = st.columns(2)
            with c_btn3:
                if st.button("🎰 2.1 หมุนคัดเน้น (4 ตัว)", key="spin_bot_main_b", use_container_width=True):
                    st.session_state.bot_main = []; r = st.empty(); p = pairs_bot.copy()
                    for i in range(4):
                        if not p: break
                        target = random.choice(p); p.remove(target)
                        for _ in range(5): r.markdown(f"<div class='rolling-box'>{random.choice(pairs_bot)}</div>", unsafe_allow_html=True); time.sleep(0.05)
                        for _ in range(3): r.markdown(f"<div class='rolling-box'>{random.choice(pairs_bot)}</div>", unsafe_allow_html=True); time.sleep(0.1)
                        html_res = f"<div class='main-box'>{target}</div>"; r.markdown(html_res, unsafe_allow_html=True); time.sleep(0.3)
                        st.session_state.bot_main.append(target)
                    r.empty()
            with c_btn4:
                if st.button("🛡️ 2.2 หมุนเลขสำรอง (4 ตัว)", key="spin_bot_backup_b", use_container_width=True):
                    st.session_state.bot_backup = []; pool_backup = [p for p in pairs_bot if p not in st.session_state.bot_main]
                    roll_area = st.empty()
                    if pool_backup:
                        for i in range(4):
                            if not pool_backup: break
                            target = random.choice(pool_backup); pool_backup.remove(target)
                            for _ in range(5): roll_area.markdown(f"<div class='rolling-box'>{random.choice(pairs_bot)}</div>", unsafe_allow_html=True); time.sleep(0.05)
                            html_res = f"<div class='backup-box'>{target}</div>"; roll_area.markdown(html_res, unsafe_allow_html=True); time.sleep(0.2)
                            st.session_state.bot_backup.append(target)
                        roll_area.empty()
                    else: st.warning("ไม่มีเลขเหลือให้สำรองแล้ว")
            if st.session_state.bot_main:
                st.divider(); st.markdown("### 🔥 ชุดเน้น (Main Focus)"); cols_m = st.columns(4)
                for i, p in enumerate(st.session_state.bot_main): 
                    with cols_m[i]: st.markdown(f"<div class='main-box'>{p}</div>", unsafe_allow_html=True)
            if st.session_state.bot_backup:
                st.markdown("### 🛡️ ชุดสำรอง (Backup)"); cols_b = st.columns(4)
                for i, p in enumerate(st.session_state.bot_backup): 
                    with cols_b[i]: st.markdown(f"<div class='backup-box'>{p}</div>", unsafe_allow_html=True)
            if st.session_state.bot_main:
                all_nums = " - ".join(st.session_state.bot_main); backup_nums = " - ".join(st.session_state.bot_backup) if st.session_state.bot_backup else "-"
                st.markdown(f"<div class='summary-box'>📋 <b>สรุปแนวทางล่าง:</b><br>เน้น: <span style='font-size: 48px; color:#FFD700;'>{all_nums}</span><br>รอง: <span style='color:#C0C0C0;'>{backup_nums}</span></div>", unsafe_allow_html=True)
            with st.expander("🔎 ดูตาราง 16 คู่ทั้งหมด"): st.write(pairs_bot)
    else: st.info("👈 กดปุ่ม 'เริ่มคำนวณสูตร' ด้านบนเพื่อเริ่มกระบวนการ")

# ==========================================
# 💖 รวมสูตรน้องพารวย
# ==========================================
elif page == "💖 รวมสูตรน้องพารวย":
    if 'R1_Lakh' not in df.columns: st.error("❌ ข้อผิดพลาดในการโหลดข้อมูลหลัก!"); st.stop()
    four_standing_digits, calculated_accuracy_run, total_hits_run, total_draws_run, backtest_df_run, current_streak_run, max_streak_run = calculate_four_standing_digits(df)
    digits_str_run = ", ".join(map(str, four_standing_digits))
    predicted_set, calculated_accuracy_svd, total_hits_svd, total_draws_svd, scores_df, rolling_df, backtest_df_svd, current_streak_svd, max_streak_svd = calculate_harmonizer_stats(df)
    set_str_svd = ", ".join(map(str, predicted_set))
    puck_luk_stats = calculate_puck_luk_stats(df)
    
    st.title("💖 รวมสูตรน้องพารวย 💸✨")
    st.caption("ศูนย์รวมสูตรคำนวณขั้นสูงของ Lotto Master")
    
    st.markdown("## 🥇 สูตร 1: เลขวิ่งตัวยืน (High Accuracy)"); st.markdown("---")
    col_run_1, col_run_2 = st.columns(2)
    with col_run_1:
        st.subheader("ชุดตัวเลขวิ่งยืน (4 ตัว)")
        st.markdown(f"<p style='font-size: 36px; font-weight: bold; color: #FFD700;'>[{digits_str_run}]</p>", unsafe_allow_html=True)
        st.metric("Hit Rate (4 ตำแหน่งหลัก)", f"{calculated_accuracy_run:.2f}%", f"({total_hits_run} Hits จาก {total_draws_run} งวด)")
        st.metric("ความต่อเนื่อง", f"{max_streak_run} งวด", delta=f"ปัจจุบัน {current_streak_run} งวด")
    with col_run_2:
        st.subheader("รายละเอียดเชิงลึก")
        st.info(f"💡 **สูตรวิ่งหลัก:** นี่คือสูตรสี่ตัวยืนที่มีความแม่นยำสูงถึง **{calculated_accuracy_run:.2f}%**")
        with st.expander("📜 ดูประวัติการเข้า/หลุด 30 งวดล่าสุด (Backtest)", expanded=False):
            st.dataframe(backtest_df_run.tail(30).iloc[::-1], use_container_width=True, hide_index=True)
    
    st.markdown("---"); st.markdown("## 🌌 สูตร 2: วงจรประสานจักรวาล (SVD)"); st.markdown("---")
    col_1, col_2, col_3 = st.columns([1.5, 1, 2])
    with col_1:
        st.subheader("🔮 ชุดตัวเลขพลังงานหลัก")
        st.markdown(f"<p style='font-size: 36px; font-weight: bold; color: #00FF7F;'>[{set_str_svd}]</p>", unsafe_allow_html=True)
        st.metric("Hit Rate (4 ตำแหน่งหลัก)", f"{calculated_accuracy_svd:.2f}%", f"({total_hits_svd} Hits จาก {total_draws_svd} งวด)")
        st.metric("ความต่อเนื่อง", f"{max_streak_svd} งวด", delta=f"ปัจจุบัน {current_streak_svd} งวด")
    with col_2:
        st.subheader("💡 คำทำนาย"); st.info("ชุดเลขนี้ควรมีอย่างน้อย 1 ตัว ปรากฏใน 2 ตัวบน หรือ 2 ตัวล่างของงวดถัดไป")
        st.subheader("📜 Backtest"); st.dataframe(backtest_df_svd.tail(15).iloc[::-1], use_container_width=True, hide_index=True)
    with col_3:
        st.subheader("📊 การจัดอันดับพลังงานตัวเลข (SVD Score)")
        chart1 = alt.Chart(scores_df).mark_bar().encode(x=alt.X('Digit:O', title='ตัวเลข (Digit)'), y=alt.Y('Score', title='พลังงานหลัก (Score)'), color=alt.Color('Type', scale=alt.Scale(domain=['Dominant', 'Other'], range=['#FFD700', '#666666'])), tooltip=['Digit', 'Score', 'Type']).properties(title='พลังงาน SVD ของแต่ละตัวเลข').interactive()
        st.altair_chart(chart1, use_container_width=True)
    
    st.markdown("---"); st.markdown("## 🎯 สูตร 3: ปักหลักแม่นยำ (ตำแหน่งที่ออกบ่อยที่สุด)"); st.markdown("---")
    col_tl, col_tu, col_bl, col_bu = st.columns(4)
    positions_map = {col_tl: 'สิบบน (R1 P5)', col_tu: 'หน่วยบน (R1 P6)', col_bl: 'สิบล่าง (2D P1)', col_bu: 'หน่วยล่าง (2D P2)'}
    for col, pos_name in positions_map.items():
        stats = puck_luk_stats[pos_name]; top_digits_str = ", ".join(map(str, stats['Top_3_Digits']))
        with col:
            st.markdown(f"#### {pos_name}")
            st.markdown(f"<div class='puck-luk-box'><small>ตัวเลขที่มาบ่อยสุด:</small><div class='puck-luk-digit'>{stats['Prediction']}</div></div>", unsafe_allow_html=True)
            chart_pl = alt.Chart(stats['ChartData']).mark_bar(color='#00FF7F').encode(x=alt.X('Digit:O', title='เลข'), y=alt.Y('Frequency', title='ความถี่ (%)'), tooltip=['Digit', alt.Tooltip('Frequency', format='.2f')]).properties(height=200, title='ความถี่เลขโดด').interactive()
            st.altair_chart(chart_pl, use_container_width=True)
            st.markdown(f"<small>Top 3: {top_digits_str}</small>", unsafe_allow_html=True)
            
    st.markdown("---"); st.markdown("## 🔮 สูตร 4: ชุดตามตูด (Next Mover Predictor)"); st.markdown("---")
    last_row = df.iloc[-1]; default_leading = str(int(last_row['R1_Sib']))
    col_input, col_btn = st.columns([1, 4])
    with col_input: leading_digit_str = st.text_input("เลขนำ (หลักสิบบนล่าสุด):", max_chars=1, value=default_leading)
    st.write("") 
    if leading_digit_str.isdigit() and len(leading_digit_str) == 1:
        leading_digit = int(leading_digit_str); top_movers = calculate_next_mover_stats(df, leading_digit)
        st.subheader(f"✅ ผลวิเคราะห์ Top 5 ชุดตามตูดของเลข: {leading_digit}")
        if top_movers:
            cols_r = st.columns(5)
            for i, (mover_num, count) in enumerate(top_movers):
                with cols_r[i]: st.markdown(f"<div class='next-mover-result'><div class='mover-num'>{mover_num}</div><div class='mover-count'>ตามมา {count} ครั้ง</div></div>", unsafe_allow_html=True)
        else: st.warning(f"❌ ไม่พบประวัติการตามของเลข {leading_digit} ในผลรางวัล 2 ตัวเลยครับ")
    else: st.warning("กรุณากรอกตัวเลขนำ (0-9) เพียง 1 หลักเท่านั้นครับ")

# ==========================================
# 🎣 สูตรฟันปลา & สามเหลี่ยม
# ==========================================
elif page == "🎣 สูตรฟันปลา & สามเหลี่ยม":
    if df.empty: st.error("โหลดข้อมูลไม่ได้"); st.stop()
    st.title("🎣 สูตรฟันปลา & สามเหลี่ยมทองคำ")
    st.caption("รวมสูตรคำนวณแบบ Visual ที่แสดงที่มาของตัวเลขอย่างชัดเจน")
    
    pyr_stats = calculate_pyramid_detailed_stats(df)
    fp_stats = calculate_triple_fhan_pla_detailed_stats(df)
    grand_stats = calculate_grand_pyramid_stats(df)
    digits_str_fhan_pla = " - ".join(map(str, fp_stats['Digits']))
    
    st.markdown("## 🥇 สูตร 1: ฟันปลา 3 ตัว (Triple Fhan Pla)")
    st.caption(f"เน้น: เลขวิ่ง 3 ตัว | ตรวจสอบทั้งหมด {fp_stats['Total']} งวด")
    
    # Layout Split
    c_viz, c_info = st.columns([1.5, 1])
    
    with c_viz:
        st.markdown(f"""
        <div class="fp-card">
            <div style="text-align:center; color:#aaa; margin-bottom:10px;">แผนภาพการบวก (Pyramid Logic)</div>
            <div class='pyramid-container'>
                <div class='pyramid-row'>
                    <div class='pyramid-ball'>{int(df.iloc[-1]['R1_Muen'])}</div>
                    <div class='pyramid-ball'>{int(df.iloc[-1]['R1_Sib'])}</div>
                    <div class='pyramid-ball'>{int(df.iloc[-1]['Bot_Nui'])}</div>
                    <div class='pyramid-ball' style='background:radial-gradient(circle at 30% 30%, #999, #555); border-color:#777;'>7</div>
                </div>
                <div class='connector-line'>&nbsp;&nbsp;🔻&nbsp;&nbsp;</div>
                <div class='pyramid-row'>
                    <div class='pyramid-ball result' style='background: gold; color:black; border-color:#fff;'>{fp_stats['Base']}</div>
                </div>
                <div class='connector-line'>&nbsp;แตกตัว (+0, +1, +2)&nbsp;</div>
                <div class='pyramid-row'>
                    <div class='pyramid-ball result'>{fp_stats['Digits'][0]}</div>
                    <div class='pyramid-ball result'>{fp_stats['Digits'][1]}</div>
                    <div class='pyramid-ball result'>{fp_stats['Digits'][2]}</div>
                </div>
            </div>
        </div>""", unsafe_allow_html=True)

    with c_info:
        st.markdown(f"""
        <div class="fp-card">
            <div class="f-header"><div class="f-title">สรุปเลขเด่นงวดนี้</div></div>
            <div class="f-pair-box" style="margin-top:0;">{digits_str_fhan_pla}</div>
            <div style="margin-top:20px;">
                <div style="display:flex; justify-content:space-between; margin-bottom:10px;">
                    <span>🎯 เข้า 8 ตำแหน่ง</span>
                    <span style="color:#00FF7F; font-weight:bold;">{fp_stats['Acc_8Pos']:.2f}%</span>
                </div>
                <div style="display:flex; justify-content:space-between; margin-bottom:10px;">
                    <span>☁️ เข้า 3 ตัวบน</span>
                    <span style="color:#FFD700; font-weight:bold;">{fp_stats['Acc_3Top']:.2f}%</span>
                </div>
                <div style="display:flex; justify-content:space-between;">
                    <span>👇 เข้า 2 ตัวล่าง</span>
                    <span style="color:#00BFFF; font-weight:bold;">{fp_stats['Acc_2Bot']:.2f}%</span>
                </div>
            </div>
        </div>""", unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("## 🔺 สูตร 2: สามเหลี่ยมทองคำ (Original Pyramid)")
    
    c_viz2, c_info2 = st.columns([2, 1])
    with c_viz2:
        pyramid_html = generate_pyramid_html(pyr_stats['Layers'])
        st.markdown(pyramid_html, unsafe_allow_html=True)
    with c_info2:
        st.markdown(f"""
        <div class="fp-card">
            <div class="f-header"><div class="f-title">ผลลัพธ์สุดท้าย</div></div>
            <div class="f-pair-box" style="font-size:60px; color:#FFD700;">{pyr_stats['Digit']}</div>
            <div style="margin-top:15px; text-align:center; color:#aaa;">ความแม่นยำ (8 จุด): {pyr_stats['Acc_8Pos']:.2f}%</div>
        </div>""", unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("## 🌋 สูตร 3: มหาพีระมิด (Grand Pyramid)")
    
    c_viz3, c_info3 = st.columns([2, 1])
    with c_viz3:
        grand_html = generate_pyramid_html(grand_stats['Layers'])
        st.markdown(grand_html, unsafe_allow_html=True)
    with c_info3:
        st.markdown(f"""
        <div class="fp-card">
            <div class="f-header"><div class="f-title">ผลลัพธ์สุดท้าย</div></div>
            <div class="f-pair-box" style="font-size:60px; color:#FFD700;">{grand_stats['Digit']}</div>
            <div style="margin-top:15px; text-align:center; color:#aaa;">ความแม่นยำ (8 จุด): {grand_stats['Acc_8Pos']:.2f}%</div>
        </div>""", unsafe_allow_html=True)

# ==========================================
# 💀 โซนเลขดับ (Killer Zone)
# ==========================================
elif page == "💀 โซนเลขดับ (Killer Zone)":
    if df.empty: st.error("โหลดข้อมูลไม่ได้"); st.stop()
    st.title("💀 โซนเลขดับ (Killer Zone)")
    st.caption("สแกนหาสูตรดับที่แม่นยำที่สุดจากสถิติย้อนหลัง (AI Real-time Scan)")
    
    if st.button("🚀 เริ่มสแกนหาเลขดับ (Start Scan)", type="primary"):
        with st.spinner("กำลังสแกนสูตรนับร้อย... (AI Working)"):
            time.sleep(1)
            killer_df = scan_for_killers_v2(df)
            
            top3 = killer_df.sort_values('Acc_Top3', ascending=False).head(3)
            top2 = killer_df.sort_values('Acc_Top2', ascending=False).head(3)
            bot2 = killer_df.sort_values('Acc_Bot2', ascending=False).head(3)
            
            st.success("✅ สแกนเสร็จสิ้น! พบสูตรดับความแม่นยำสูงดังนี้:")
            
            c1, c2, c3 = st.columns(3)
            
            with c1:
                best = top3.iloc[0]
                st.markdown(f"""
                <div class='killer-box'>
                    <div class='killer-title'>💀 ดับบน 3 ตัว (เน้นสุด)</div>
                    <div class='killer-digit'>{best['Next_Dead']}</div>
                    <div class='killer-stat'>ความแม่นยำ: {best['Acc_Top3']:.2f}%</div>
                    <div><span class='streak-badge'>🔥 ดับต่อเนื่อง: {best['Cur_T3']} งวด</span> <br><span class='streak-badge' style='background:#555; margin-top:5px;'>🏆 ดับยาวสุด: {best['Max_T3']} งวด</span></div>
                    <div style='font-size:10px; color:#888; margin-top:5px;'>สูตร: {best['Formula']}</div>
                </div>
                """, unsafe_allow_html=True)
                st.dataframe(top3[['Formula', 'Acc_Top3', 'Next_Dead']], hide_index=True)

            with c2:
                best = top2.iloc[0]
                st.markdown(f"""
                <div class='killer-box'>
                    <div class='killer-title'>💀 ดับบน 2 ตัว</div>
                    <div class='killer-digit'>{best['Next_Dead']}</div>
                    <div class='killer-stat'>ความแม่นยำ: {best['Acc_Top2']:.2f}%</div>
                    <div><span class='streak-badge'>🔥 ดับต่อเนื่อง: {best['Cur_T2']} งวด</span> <br><span class='streak-badge' style='background:#555; margin-top:5px;'>🏆 ดับยาวสุด: {best['Max_T2']} งวด</span></div>
                    <div style='font-size:10px; color:#888; margin-top:5px;'>สูตร: {best['Formula']}</div>
                </div>
                """, unsafe_allow_html=True)
                st.dataframe(top2[['Formula', 'Acc_Top2', 'Next_Dead']], hide_index=True)

            with c3:
                best = bot2.iloc[0]
                st.markdown(f"""
                <div class='killer-box'>
                    <div class='killer-title'>💀 ดับล่าง 2 ตัว</div>
                    <div class='killer-digit'>{best['Next_Dead']}</div>
                    <div class='killer-stat'>ความแม่นยำ: {best['Acc_Bot2']:.2f}%</div>
                    <div><span class='streak-badge'>🔥 ดับต่อเนื่อง: {best['Cur_B2']} งวด</span> <br><span class='streak-badge' style='background:#555; margin-top:5px;'>🏆 ดับยาวสุด: {best['Max_B2']} งวด</span></div>
                    <div style='font-size:10px; color:#888; margin-top:5px;'>สูตร: {best['Formula']}</div>
                </div>
                """, unsafe_allow_html=True)
                st.dataframe(bot2[['Formula', 'Acc_Bot2', 'Next_Dead']], hide_index=True)
            
    else:
        st.info("👈 กดปุ่มเพื่อเริ่มสแกนหาเลขดับประจำงวดนี้")