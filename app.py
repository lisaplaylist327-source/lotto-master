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
st.set_page_config(layout="wide", page_title="Lotto Master V.GodFix")

ALL_PAGES = [
    "🏠 หน้าแรก (4 สูตรมหาประลัย)", 
    "🔍 นักสืบตัวเลข", 
    "🧬 สูตรลับ 5 ชั้น (AI Spin)", 
    "💖 รวมสูตรน้องพารวย", 
    "🎣 สูตรฟันปลา & สามเหลี่ยม", 
    "💀 โซนเลขดับ (Killer Zone)"
]

if 'current_page' not in st.session_state:
    st.session_state.current_page = ALL_PAGES[0]

def navigate_to(page_name):
    st.session_state.current_page = page_name
    st.rerun()

# ---------------------------------------------------------
# 2. CSS Style (แก้ไขเรื่องตัวหนังสือทับกันเรียบร้อย!)
# ---------------------------------------------------------
custom_css = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Kanit:wght@300;400;600;900&display=swap');

/* Global Font - แก้ไขไม่ให้กระทบโครงสร้างภายใน */
html, body, [class*="css"] {
    font-family: 'Kanit', sans-serif;
}

/* ปรับแต่งหัวข้อ Expander ให้ชัดเจน ไม่ทับกัน */
.streamlit-expanderHeader {
    font-family: 'Kanit', sans-serif !important;
    font-weight: bold !important;
    font-size: 16px !important;
    background-color: #2e2e2e;
    border-radius: 8px;
    color: #FFD700 !important;
}

/* --- HERO SECTION --- */
.hero-container {
    background: radial-gradient(circle at center, #2b2b2b 0%, #1a1a1a 100%);
    border: 2px solid #444;
    border-radius: 20px;
    padding: 30px;
    text-align: center;
    box-shadow: 0 10px 30px rgba(0,0,0,0.5);
    margin-bottom: 25px;
    position: relative;
    overflow: hidden;
}
.hero-container::before {
    content: '';
    position: absolute;
    top: -50%; left: -50%; width: 200%; height: 200%;
    background: radial-gradient(circle, rgba(255,215,0,0.1) 0%, transparent 60%);
    animation: shine 10s infinite linear;
}
@keyframes shine { from {transform: rotate(0deg);} to {transform: rotate(360deg);} }

.hero-title {
    color: #AAA;
    font-size: 18px;
    letter-spacing: 2px;
    margin-bottom: 10px;
    text-transform: uppercase;
}
.hero-number {
    font-size: 90px;
    font-weight: 900;
    line-height: 1;
    background: linear-gradient(to bottom, #FFF8DC 0%, #FFD700 50%, #DAA520 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    filter: drop-shadow(0 4px 6px rgba(0,0,0,0.5));
    margin-bottom: 15px;
}
.hero-sub-grid {
    display: flex;
    justify-content: center;
    gap: 30px;
    margin-top: 10px;
}
.hero-sub-item {
    background: rgba(255,255,255,0.05);
    padding: 10px 20px;
    border-radius: 10px;
    border: 1px solid #333;
}
.hero-sub-label { color: #888; font-size: 14px; }
.hero-sub-val { color: #FFF; font-size: 24px; font-weight: bold; }

/* --- FORMULA CARDS --- */
.formula-card-home { 
    background-color: #222; 
    padding: 15px; 
    margin-bottom: 10px; 
    border-radius: 12px; 
    border: 1px solid #333; 
    text-align: left;
    transition: all 0.3s;
    position: relative;
}
.formula-card-home:hover { transform: translateY(-5px); box-shadow: 0 5px 15px rgba(0,0,0,0.3); border-color: #555; }
.f-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px; border-bottom: 1px solid #333; padding-bottom: 8px; }
.f-title { font-weight: bold; font-size: 18px; }
.f-stats-badge { background: #111; color: #aaa; font-size: 10px; padding: 2px 6px; border-radius: 4px; border: 1px solid #333; }
.f-row { display: flex; align-items: center; margin-bottom: 5px; }
.f-label { font-size: 12px; color: #888; width: 60px; }

.f-val-badge { 
    background-color: #000; 
    color: #ccc; 
    padding: 2px 8px; 
    border-radius: 4px; 
    font-weight: normal; 
    font-size: 12px; 
    border: 1px solid #444;
    margin-right: 4px;
}

.f-pair-box {
    margin-top: 8px;
    background-color: rgba(255, 215, 0, 0.05);
    padding: 10px;
    border-radius: 8px;
    color: #FFD700;
    font-weight: 900;
    font-size: 28px; 
    text-align: center;
    border: 1px dashed #555;
    letter-spacing: 2px;
}

/* --- SIDEBAR STATS --- */
.sidebar-stat-box { background-color: #262626; padding: 12px; border-radius: 10px; margin-bottom: 10px; text-align: center; border: 1px solid #444; box-shadow: 0 4px 6px rgba(0,0,0,0.2); }
.sidebar-stat-num { font-size: 28px; font-weight: 900; color: #FFD700; line-height: 1.2; }
.sidebar-stat-label { font-size: 12px; color: #aaa; margin-bottom: 2px; }

/* --- CONSENSUS & KILLER --- */
.consensus-box { background: linear-gradient(135deg, #3b0000 0%, #1a0000 100%); border: 1px solid #ff4444; padding: 20px; border-radius: 15px; text-align: center; height: 100%; display: flex; flex-direction: column; justify-content: center; box-shadow: 0 0 15px rgba(255, 68, 68, 0.1); }
.consensus-title { color: #ff4444; font-size: 20px; font-weight: bold; margin-bottom: 5px; }
.consensus-number { font-size: 90px; font-weight: 900; color: #FFD700; text-shadow: 0 0 20px rgba(255, 215, 0, 0.3); line-height: 0.9; }

.killer-container { background: #1a0505; border: 1px solid #550000; border-radius: 15px; padding: 15px; text-align: center; height: 100%; display: flex; flex-direction: column; justify-content: space-between; }
.killer-main-title { color: #ff4444; font-weight: bold; font-size: 16px; }
.killer-main-digit { font-size: 56px; font-weight: 900; color: #ff4444; line-height: 1; text-shadow: 0 0 10px rgba(255, 0, 0, 0.3); }
.killer-sub-grid { display: flex; justify-content: space-around; margin-top: 10px; border-top: 1px solid #330000; padding-top: 10px; }
.killer-sub-item { text-align: center; }
.killer-sub-val { font-size: 20px; font-weight: bold; color: #ff8888; }
.killer-sub-lbl { font-size: 10px; color: #884444; }

/* --- OTHER --- */
.stat-grid-box { background-color: #2e2e2e; border: 1px solid #444; border-radius: 10px; padding: 15px; text-align: center; height: 100%; }
.grid-val-big { font-size: 32px; font-weight: bold; color: #00FF7F; }
.ai-pick-item { background: linear-gradient(45deg, #00FF7F, #008080); color: white; font-size: 36px; font-weight: bold; width: 80px; height: 80px; line-height: 80px; text-align: center; border-radius: 50%; margin: 0 auto; }
.main-box, .backup-box, .rolling-box { border: 2px solid #333; padding: 10px; margin-bottom: 10px; text-align: center; border-radius: 8px; font-size: 48px; font-weight: bold; }
.main-box { background-color: #4CAF50; color: white; } .backup-box { background-color: #FF9800; color: white; }
.pyramid-container { display: flex; flex-direction: column; align-items: center; justify-content: center; padding: 20px; background-color: #2e2e2e; border-radius: 15px; margin-top: 10px; }
.pyramid-row { display: flex; justify-content: center; margin-bottom: 5px; }
.pyramid-ball { width: 40px; height: 40px; line-height: 40px; border-radius: 50%; background: radial-gradient(circle at 30% 30%, #FFD700, #DAA520); color: #000; font-size: 20px; font-weight: bold; text-align: center; margin: 0 3px; border: 2px solid #FFF; }
.pyramid-ball.result { background: radial-gradient(circle at 30% 30%, #00FF7F, #006400); color: white; width: 60px; height: 60px; line-height: 60px; font-size: 32px; border: 3px solid #FFF; }
</style>
"""

# ---------------------------------------------------------
# 3. ฟังก์ชันโหลดข้อมูล & คำนวณต่างๆ
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
        
        thai_days = {'Monday': 'วันจันทร์', 'Tuesday': 'วันอังคาร', 'Wednesday': 'วันพุธ', 'Thursday': 'วันพฤหัสบดี', 'Friday': 'วันศุกร์', 'Saturday': 'วันเสาร์', 'Sunday': 'วันอาทิตย์'}
        df['Day_Name'] = df['date_obj'].dt.day_name().map(thai_days)

        df['รางวัลที่ 1'] = df['first_prize'].astype(str).str.zfill(6)
        df['first_prize_str'] = df['รางวัลที่ 1'].copy()
        df['two_digit_str'] = df['two_digit'].astype(str).str.zfill(2)

        df['R1_Lakh'] = df['รางวัลที่ 1'].str[0].astype(int); df['R1_Muen'] = df['รางวัลที่ 1'].str[1].astype(int)
        df['R1_Pan'] = df['รางวัลที่ 1'].str[2].astype(int); df['R1_Roi'] = df['รางวัลที่ 1'].str[3].astype(int)
        df['R1_Sib'] = df['รางวัลที่ 1'].str[4].astype(int); df['R1_Nui'] = df['รางวัลที่ 1'].str[5].astype(int)
        df['2 ตัวล่าง'] = df['two_digit'].astype(str).str.zfill(2)
        df['Bot_Sib'] = df['2 ตัวล่าง'].str[0].astype(int); df['Bot_Nui'] = df['2 ตัวล่าง'].str[1].astype(int)
        
        cols_3 = ['three_digit_1', 'three_digit_2', 'three_digit_3', 'three_digit_4']
        new_cols_3 = ['เลขท้าย 3 ตัว (1)', 'เลขท้าย 3 ตัว (2)', 'เลขท้าย 3 ตัว (3)', 'เลขท้าย 3 ตัว (4)']
        for old, new in zip(cols_3, new_cols_3):
            if old in df.columns: df[new] = df[old].astype(str).str.zfill(3)
            else: df[new] = "000"

        df['Top_Ten'] = df['R1_Sib']; df['Top_Unit'] = df['R1_Nui']
        df['Bot_Ten'] = df['Bot_Sib']; df['Bot_Unit'] = df['Bot_Nui']
        df['2 ตัวบน'] = df['รางวัลที่ 1'].str[-2:]
        return df
    except Exception as e:
        return pd.DataFrame()

# --- HELPER: Streaks ---
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

# --- Puck Luk ---
def calculate_puck_luk_stats(df):
    positions = [('R1_Sib', 'สิบบน (R1 P5)'), ('R1_Nui', 'หน่วยบน (R1 P6)'), ('Bot_Sib', 'สิบล่าง (2D P1)'), ('Bot_Nui', 'หน่วยล่าง (2D P2)')]
    puck_luk_results = {}
    for col_name, pos_name in positions:
        counts = df[col_name].value_counts(normalize=True).mul(100).round(2).sort_values(ascending=False)
        chart_data = pd.DataFrame({'Digit': counts.index.astype(str), 'Frequency': counts.values})
        puck_luk_results[pos_name] = {'Prediction': int(counts.index[0]) if not counts.empty else 0, 'Top_3_Digits': counts.head(3).index.tolist(), 'Top_3_Percent': counts.head(3).values.tolist(), 'ChartData': chart_data}
    return puck_luk_results

# --- Next Mover ---
def calculate_next_mover_stats(df, leading_digit):
    target_cols = ['R1_Sib', 'R1_Nui', 'Bot_Sib', 'Bot_Nui']
    df['is_leading'] = (df[target_cols] == leading_digit).any(axis=1)
    next_movers = []
    for i in df[df['is_leading']].index:
        if i + 1 < len(df): next_row = df.iloc[i + 1]; next_movers.append(next_row['2 ตัวบน']); next_movers.append(next_row['2 ตัวล่าง'])
    if not next_movers: return []
    mover_counts = Counter(next_movers); top_5 = mover_counts.most_common(5)
    return top_5

# --- Pyramid HTML Helper ---
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

# --- สูตร 3: มหาพีระมิด (Grand Pyramid - 8 ตัว) ---
def calculate_grand_pyramid_stats(df):
    prev = df.shift(1)
    
    current_layer_cols = ['R1_Lakh', 'R1_Muen', 'R1_Pan', 'R1_Roi', 'R1_Sib', 'R1_Nui', 'Bot_Sib', 'Bot_Nui']
    temp_df = prev[current_layer_cols].copy()
    
    while len(current_layer_cols) > 1:
        next_cols = []
        for i in range(len(current_layer_cols) - 1):
            col_name = f"L{len(current_layer_cols)}_{i}"
            c1 = current_layer_cols[i]
            c2 = current_layer_cols[i+1]
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
    
    return {
        'Digit': final_digit, 'Layers': layers,
        'Acc_8Pos': acc_8pos, 'Acc_3Top': acc_3top, 
        'Acc_2Top': acc_2top, 'Acc_2Bot': acc_2bot, 'Total': int(total_checks)
    }

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
    pos_3top = ['R1_Roi', 'R1_Sib', 'R1_Nui']
    pos_2top = ['R1_Sib', 'R1_Nui']
    pos_2bot = ['Bot_Sib', 'Bot_Nui']
    
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
    
    return {
        'Digit': final_digit, 'Layers': layers,
        'Acc_8Pos': acc_8pos, 'Acc_3Top': acc_3top, 
        'Acc_2Top': acc_2top, 'Acc_2Bot': acc_2bot, 'Total': int(total_checks)
    }

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
# 🆕 LOGIC: 4 สูตรมหาประลัย (God Mode Logic)
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
    
    # 🟢 Formula 1: Lucky 50/50 -> คู่หูพารวย
    sum_t1 = d2[0] + (f1[0]*3) + (f2[2]*2) + b1[0] + (b2[0]*2) + (b2[1]*3) + 9
    base_t1 = sum_t1 % 10
    tens_1 = [base_t1, (base_t1+1)%10, (base_t1+5)%10]
    sum_u1 = (p1[2]*2) + (p1[3]*2) + p1[4] + (p1[5]*2) + b2[0] + 7
    base_u1 = sum_u1 % 10
    units_1 = [base_u1, (base_u1+2)%10]
    results['F1'] = {'name': 'คู่หูพารวย (Lucky 50/50)', 'tens': tens_1, 'units': units_1, 'color': '#00FF7F'} 

    # 🟡 Formula 2: Emperor's Wealth -> จักรพรรดิพารวย
    sum_t2 = p1[1] + (p1[2]*4) + (d2[0]*3) + (f1[1]*2) + (f2[2]*2) + b1[1] + 6
    base_t2 = sum_t2 % 10
    tens_2 = [(base_t2+1)%10, (base_t2+3)%10, (base_t2+8)%10]
    sum_u2 = (p1[0]*4) + (f2[0]*2) + (f2[1]*2) + (b1[0]*3) + 0
    base_u2 = sum_u2 % 10
    units_2 = [(base_u2+4)%10, (base_u2+8)%10]
    results['F2'] = {'name': 'จักรพรรดิพารวย (Emperor)', 'tens': tens_2, 'units': units_2, 'color': '#FFD700'} 

    # 🔴 Formula 3: God of Wealth -> มหาเทพประทานทรัพย์
    sum_t3 = (p1[3]*4) + f1[1] + (f2[0]*4) + b1[1] + (b2[0]*3) + 4
    base_t3 = sum_t3 % 10
    tens_3 = [(base_t3+1)%10, (base_t3+7)%10, (base_t3+9)%10]
    sum_u3 = (p1[3]*2) + (p1[4]*5) + (d2[1]*5) + (f1[0]*4) + f1[1] + f1[2] + (f2[0]*2) + 9
    base_u3 = sum_u3 % 10
    units_3 = [base_u3, (base_u3+5)%10]
    results['F3'] = {'name': 'มหาเทพประทานทรัพย์ (God of Wealth)', 'tens': tens_3, 'units': units_3, 'color': '#FF4444'} 

    # ⚫ Formula 4: The Brutal Sage -> มหาโหดโคตรเซียน
    sum_t4 = (p1[1]*3) + (p1[4]*6) + (p1[5]*6) + (d2[1]*7) + (f1[2]*2) + (f2[2]*6) + (b1[0]*2) + 4
    base_t4 = sum_t4 % 10
    tens_4 = [(base_t4+3)%10, (base_t4+5)%10, (base_t4+6)%10]
    sum_u4 = (p1[0]*4) + (p1[1]*4) + (p1[4]*4) + (p1[5]*2) + (f1[0]*7) + (f2[1]*2) + (f2[2]*3) + 0
    base_u4 = sum_u4 % 10
    units_4 = [base_u4, (base_u4+9)%10]
    results['F4'] = {'name': 'มหาโหดโคตรเซียน (Brutal Sage)', 'tens': tens_4, 'units': units_4, 'color': '#AAAAAA'} 
    
    return results

def find_consensus_god_mode(formulas_result):
    all_pairs = []
    for key, val in formulas_result.items():
        for t in val['tens']:
            for u in val['units']:
                all_pairs.append(f"{t}{u}")
    return Counter(all_pairs).most_common()

# --- Stats Helper for 4 Formulas (20 Draws) ---
@st.cache_data
def calculate_formula_history_stats(df, lookback=20):
    if len(df) < lookback + 2: return {}
    
    stats = {
        'F1': {'hits': 0, 'streak': 0, 'hits_list': []}, 
        'F2': {'hits': 0, 'streak': 0, 'hits_list': []},
        'F3': {'hits': 0, 'streak': 0, 'hits_list': []}, 
        'F4': {'hits': 0, 'streak': 0, 'hits_list': []}
    }
    
    # Analyze last 'lookback' draws
    start_idx = len(df) - lookback
    
    for i in range(start_idx, len(df)):
        past_row = df.iloc[i-1] # input
        target_row = df.iloc[i] # result
        
        # Calculate
        pp1, pd2, pf1, pf2, pb1, pb2 = get_variables_god_mode(past_row)
        res = calculate_god_formulas(pp1, pd2, pf1, pf2, pb1, pb2)
        
        real_2d = str(target_row['2 ตัวล่าง']).zfill(2)
        real_top = str(target_row['2 ตัวบน']).zfill(2)
        
        for key in ['F1', 'F2', 'F3', 'F4']:
            fval = res[key]
            f_pairs = [f"{t}{u}" for t in fval['tens'] for u in fval['units']]
            
            is_hit = (real_2d in f_pairs) or (real_top in f_pairs)
            if is_hit:
                stats[key]['hits'] += 1
                stats[key]['hits_list'].append(1)
            else:
                stats[key]['hits_list'].append(0)
    
    # Calculate streak
    for key in stats:
        h_list = stats[key]['hits_list']
        curr_streak = 0
        for h in reversed(h_list):
            if h == 1: curr_streak += 1
            else: break
        stats[key]['streak'] = curr_streak
        
    return stats

# --- NEW: Backtest Data Generator ---
def get_backtest_dataframe(df, periods=20):
    rows = []
    if len(df) < periods + 1: return pd.DataFrame()

    # Loop from latest index down
    for i in range(len(df)-1, len(df)-1-periods, -1):
        target_row = df.iloc[i]      
        input_row = df.iloc[i-1]     

        p1, d2, f1, f2, b1, b2 = get_variables_god_mode(input_row)
        formulas = calculate_god_formulas(p1, d2, f1, f2, b1, b2)

        real_2d = str(target_row['2 ตัวล่าง']).zfill(2)
        real_top = str(target_row['2 ตัวบน']).zfill(2)

        row_data = {
            "งวดวันที่": target_row['วันที่'],
            "เลขที่ออก (บน/ล่าง)": f"{real_top} / {real_2d}"
        }

        for key in ['F1', 'F2', 'F3', 'F4']:
            f_data = formulas[key]
            f_pairs = [f"{t}{u}" for t in f_data['tens'] for u in f_data['units']]
            
            hits = []
            if real_top in f_pairs: hits.append("บน")
            if real_2d in f_pairs: hits.append("ล่าง")
            
            if hits:
                row_data[f_data['name']] = "✅ " + ",".join(hits)
            else:
                row_data[f_data['name']] = "❌"
        
        rows.append(row_data)
    
    return pd.DataFrame(rows)

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
        col1_data = cols_map[c1]
        col2_data = cols_map[c2]
        
        for k in range(10):
            pred = (col1_data + col2_data + k) % 10
            pred_shifted = pred.shift(1) # Predict current from previous
            
            mask = ~pred_shifted.isna()
            valid_df = df[mask]
            p = pred_shifted[mask]
            total = len(valid_df)
            
            # Dead Top 3 (Target)
            hit_top3 = (valid_df['R1_Roi'] == p) | (valid_df['R1_Sib'] == p) | (valid_df['R1_Nui'] == p)
            success_top3 = ~hit_top3
            acc_top3 = success_top3.sum() / total * 100
            
            # Dead Top 2
            hit_top2 = (valid_df['R1_Sib'] == p) | (valid_df['R1_Nui'] == p)
            success_top2 = ~hit_top2
            acc_top2 = success_top2.sum() / total * 100
            
            # Dead Bot 2
            hit_bot2 = (valid_df['Bot_Sib'] == p) | (valid_df['Bot_Nui'] == p)
            success_bot2 = ~hit_bot2
            acc_bot2 = success_bot2.sum() / total * 100
            
            last_val = (cols_map[c1].iloc[-1] + cols_map[c2].iloc[-1] + k) % 10
            
            # Streaks Calculation (Calculated only for high accuracy)
            cur_streak_t3, max_streak_t3 = (0,0)
            if acc_top3 > 75: cur_streak_t3, max_streak_t3 = calculate_hit_streaks(success_top3)
                
            cur_streak_t2, max_streak_t2 = (0,0)
            if acc_top2 > 80: cur_streak_t2, max_streak_t2 = calculate_hit_streaks(success_top2)
                
            cur_streak_b2, max_streak_b2 = (0,0)
            if acc_bot2 > 80: cur_streak_b2, max_streak_b2 = calculate_hit_streaks(success_bot2)

            if acc_top3 > 75 or acc_top2 > 80 or acc_bot2 > 80:
                results.append({
                    'Formula': f"({c1} + {c2} + {k}) % 10",
                    'Acc_Top3': acc_top3, 'Cur_T3': cur_streak_t3, 'Max_T3': max_streak_t3,
                    'Acc_Top2': acc_top2, 'Cur_T2': cur_streak_t2, 'Max_T2': max_streak_t2,
                    'Acc_Bot2': acc_bot2, 'Cur_B2': cur_streak_b2, 'Max_B2': max_streak_b2,
                    'Next_Dead': int(last_val)
                })
                
    return pd.DataFrame(results)

# ---------------------------------------------------------
# 4. ส่วนแสดงผล (UI Logic)
# ---------------------------------------------------------
df = load_data()

st.sidebar.title("🐯 Lotto Master")
# Using state to control navigation
if 'current_page' in st.session_state:
    if st.session_state.current_page in ALL_PAGES:
        idx = ALL_PAGES.index(st.session_state.current_page)
    else:
        idx = 0
    page = st.sidebar.radio("เลือกเมนู:", ALL_PAGES, index=idx, key="sidebar_nav")
    
    if page != st.session_state.current_page:
        st.session_state.current_page = page
        st.rerun()
else:
    page = st.sidebar.radio("เลือกเมนู:", ALL_PAGES, key="sidebar_nav")

# ---- SIDEBAR STATS (MOVED HERE) ----
if not df.empty:
    st.sidebar.markdown("---")
    st.sidebar.subheader("🔥 สถิติฮิตตลอดกาล")
    
    top2_counts = df['2 ตัวบน'].value_counts().head(3)
    bot2_counts = df['2 ตัวล่าง'].value_counts().head(3)
    
    c_side1, c_side2 = st.sidebar.columns(2)
    with c_side1:
        st.markdown(f"""
        <div class="sidebar-stat-box">
            <div class="sidebar-stat-label">บนฮิตสุด</div>
            <div class="sidebar-stat-num">{top2_counts.index[0]}</div>
            <div style="font-size:10px; color:#888;">รอง: {top2_counts.index[1]}</div>
        </div>
        """, unsafe_allow_html=True)
    with c_side2:
        st.markdown(f"""
        <div class="sidebar-stat-box">
            <div class="sidebar-stat-label">ล่างฮิตสุด</div>
            <div class="sidebar-stat-num">{bot2_counts.index[0]}</div>
            <div style="font-size:10px; color:#888;">รอง: {bot2_counts.index[1]}</div>
        </div>
        """, unsafe_allow_html=True)
# -----------------------------------

st.markdown(custom_css, unsafe_allow_html=True)

# ==========================================
# 🏠 หน้าที่ 0: หน้าแรก (4 สูตรมหาประลัย)
# ==========================================
if page == "🏠 หน้าแรก (4 สูตรมหาประลัย)":
    if df.empty: st.error("ไม่สามารถโหลดข้อมูลได้"); st.stop()
    
    last_row = df.iloc[-1]
    
    # 1. Hero Section (Premium Gold)
    st.markdown(f"""
    <div class='hero-container'>
        <div class='hero-title'>รางวัลที่ 1 งวดวันที่ {last_row['วันที่']}</div>
        <div class='hero-number'>{last_row['รางวัลที่ 1']}</div>
        <div class='hero-sub-grid'>
            <div class='hero-sub-item'>
                <div class='hero-sub-label'>เลขหน้า 3 ตัว</div>
                <div class='hero-sub-val'>{last_row['เลขท้าย 3 ตัว (1)']} | {last_row['เลขท้าย 3 ตัว (2)']}</div>
            </div>
            <div class='hero-sub-item'>
                <div class='hero-sub-label'>เลขท้าย 3 ตัว</div>
                <div class='hero-sub-val'>{last_row['เลขท้าย 3 ตัว (3)']} | {last_row['เลขท้าย 3 ตัว (4)']}</div>
            </div>
            <div class='hero-sub-item'>
                <div class='hero-sub-label'>2 ตัวล่าง</div>
                <div class='hero-sub-val' style='color:#FFD700;'>{last_row['2 ตัวล่าง']}</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.divider()
    
    # 2. Section A: 4 สูตรมหาประลัย & Killer
    
    # คำนวณสูตร
    p1, d2, f1, f2, b1, b2 = get_variables_god_mode(last_row)
    formulas = calculate_god_formulas(p1, d2, f1, f2, b1, b2)
    consensus = find_consensus_god_mode(formulas)
    
    # คำนวณ Stats ย้อนหลัง 20 งวด
    f_stats = calculate_formula_history_stats(df, lookback=20)
    
    top_pick = consensus[0] if consensus else ("--", 0)
    
    # Killer Logic
    killer_df = scan_for_killers_v2(df)
    dead_top3 = "-"; dead_top2 = "-"; dead_bot2 = "-"
    if not killer_df.empty:
        best_t3 = killer_df.sort_values('Acc_Top3', ascending=False).iloc[0]
        best_t2 = killer_df.sort_values('Acc_Top2', ascending=False).iloc[0]
        best_b2 = killer_df.sort_values('Acc_Bot2', ascending=False).iloc[0]
        dead_top3 = f"{best_t3['Next_Dead']}"
        dead_top2 = f"{best_t2['Next_Dead']}"
        dead_bot2 = f"{best_b2['Next_Dead']}"
    
    # Layout: Left (Consensus), Center (Formulas), Right (Killer)
    col_con, col_form, col_kill = st.columns([1.5, 3, 1.5])
    
    with col_con:
        st.markdown(f"""
        <div class="consensus-box">
            <div class="consensus-title">🔥 เลขชนแรงสุด</div>
            <div class="consensus-number">{top_pick[0]}</div>
            <div style="color:#ccc;">ชนกัน {top_pick[1]} สูตร</div>
            <hr style="border-color:#550000; width:50%; margin: 15px auto;">
            <div style="color:#ff8888; font-size:12px;">คำเตือน: โปรดใช้วิจารณญาณ</div>
        </div>
        """, unsafe_allow_html=True)

    with col_form:
        st.markdown("### ✨ 4 สูตรมหาประลัย (New Gen)")
        c_f1, c_f2 = st.columns(2)
        cols_ref = [c_f1, c_f2]
        
        items = list(formulas.items())
        for i in range(0, 4, 2): # Row loop
            with c_f1:
                key, val = items[i]
                stats = f_stats.get(key, {'hits':0, 'streak':0})
                tens_badges = "".join([f"<span class='f-val-badge'>{x}</span>" for x in val['tens']])
                units_badges = "".join([f"<span class='f-val-badge'>{x}</span>" for x in val['units']])
                st.markdown(f"""
                <div class="formula-card-home" style="border-left: 4px solid {val['color']};">
                    <div class="f-header">
                        <div class="f-title" style="color:{val['color']}; border:none; margin:0;">{val['name']}</div>
                        <div class="f-stats-badge">เข้า {stats['hits']}/20 | ติดกัน {stats['streak']} งวด</div>
                    </div>
                    <div class="f-row"><span class="f-label">หลักสิบ:</span> {tens_badges}</div>
                    <div class="f-row"><span class="f-label">หลักหน่วย:</span> {units_badges}</div>
                    <div class="f-pair-box">{", ".join([f"{t}{u}" for t in val['tens'] for u in val['units']])}</div>
                </div>
                """, unsafe_allow_html=True)
                
            with c_f2:
                key, val = items[i+1]
                stats = f_stats.get(key, {'hits':0, 'streak':0})
                tens_badges = "".join([f"<span class='f-val-badge'>{x}</span>" for x in val['tens']])
                units_badges = "".join([f"<span class='f-val-badge'>{x}</span>" for x in val['units']])
                st.markdown(f"""
                <div class="formula-card-home" style="border-left: 4px solid {val['color']};">
                    <div class="f-header">
                        <div class="f-title" style="color:{val['color']}; border:none; margin:0;">{val['name']}</div>
                        <div class="f-stats-badge">เข้า {stats['hits']}/20 | ติดกัน {stats['streak']} งวด</div>
                    </div>
                    <div class="f-row"><span class="f-label">หลักสิบ:</span> {tens_badges}</div>
                    <div class="f-row"><span class="f-label">หลักหน่วย:</span> {units_badges}</div>
                    <div class="f-pair-box">{", ".join([f"{t}{u}" for t in val['tens'] for u in val['units']])}</div>
                </div>
                """, unsafe_allow_html=True)

    with col_kill:
        st.markdown(f"""
        <div class="killer-container">
            <div>
                <div class="killer-main-title">💀 ดับบน (3 ตัวแม่นๆ)</div>
                <div class="killer-main-digit">{dead_top3}</div>
            </div>
            <div class="killer-sub-grid">
                <div class="killer-sub-item">
                    <div class="killer-sub-lbl">ดับบน (2 ตัว)</div>
                    <div class="killer-sub-val">{dead_top2}</div>
                </div>
                <div class="killer-sub-item">
                    <div class="killer-sub-lbl">ดับล่าง (2 ตัว)</div>
                    <div class="killer-sub-val">{dead_bot2}</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.divider()

    # 3. Section C: New Backtest Table (Moved here)
    with st.expander("📊 เช็คผลงาน 4 สูตรย้อนหลัง (Backtest)", expanded=False):
        bt_df = get_backtest_dataframe(df)
        st.dataframe(bt_df, use_container_width=True, hide_index=True)

# ==========================================
# 🔍 หน้าที่ 2: นักสืบตัวเลข (Sherlock Full)
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
                    next_draw_numbers = []; target_col_real = 'รางวัลที่ 1' if target_col == '3_top' else target_col
                    for idx in found.index:
                        if idx + 1 < len(data_df):
                            val = data_df.iloc[idx + 1][target_col_real]
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
    # --- Moved History Data Here ---
    with st.expander("📂 ฐานข้อมูลผลรางวัลย้อนหลัง (Full Database)", expanded=False):
        st.dataframe(df.iloc[::-1][['วันที่', 'รางวัลที่ 1', '2 ตัวล่าง', 'เลขท้าย 3 ตัว (1)', 'เลขท้าย 3 ตัว (2)', 'เลขท้าย 3 ตัว (3)', 'เลขท้าย 3 ตัว (4)']], use_container_width=True)

# ==========================================
# 🧬 หน้าที่ 3: สูตรลับ 5 ชั้น (AI Spin)
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
# 💖 หน้าที่ 5: รวมสูตรน้องพารวย
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
        # --- ย้ายประวัติมาไว้ตรงนี้ ---
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
    
    # --- New: Default to Latest R1_Sib (สิบบน) ---
    last_row = df.iloc[-1]
    default_leading = str(int(last_row['R1_Sib']))
    
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
# 🎣 หน้าที่ 6: สูตรฟันปลา & สามเหลี่ยม
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
    with st.expander("🔍 กดเพื่อดูวิธีกระทบเลข (Visual Calculation)", expanded=True):
        col_viz, col_desc = st.columns([2, 1])
        with col_viz:
            st.markdown("##### แผนภาพการบวก:")
            html_fhan = f"""
            <div class='pyramid-container'>
                <div style='color:#AAA; margin-bottom:5px;'>หลักหมื่น + สิบ(ร.1) + หน่วยล่าง + 7</div>
                <div class='pyramid-row'>
                    <div class='pyramid-ball'>{int(df.iloc[-1]['R1_Muen'])}</div>
                    <div class='pyramid-ball'>{int(df.iloc[-1]['R1_Sib'])}</div>
                    <div class='pyramid-ball'>{int(df.iloc[-1]['Bot_Nui'])}</div>
                    <div class='pyramid-ball' style='background:grey;'>7</div>
                </div>
                <div class='connector-line'>&nbsp;&nbsp;🔻&nbsp;&nbsp;</div>
                <div class='pyramid-row'>
                    <div class='pyramid-ball result' style='background: gold; color:black;'>{fp_stats['Base']}</div>
                </div>
                <div class='connector-line'>&nbsp;แตกตัว (+0, +1, +2)&nbsp;</div>
                <div class='pyramid-row'>
                    <div class='pyramid-ball result'>{fp_stats['Digits'][0]}</div>
                    <div class='pyramid-ball result'>{fp_stats['Digits'][1]}</div>
                    <div class='pyramid-ball result'>{fp_stats['Digits'][2]}</div>
                </div>
            </div>
            """
            st.markdown(html_fhan, unsafe_allow_html=True)
        with col_desc:
            st.markdown("#### เลขเด่นงวดนี้")
            st.markdown(f"<div style='font-size:48px; font-weight:bold; color:#00FF7F; text-align:center;'>{digits_str_fhan_pla}</div>", unsafe_allow_html=True)
            st.markdown("##### 📊 สถิติความแม่นยำ")
            html_stats = f"""
            <div class='fp-stats-grid'>
                <div class='fp-stat-item'><div class='fp-stat-label'>🎯 8 ตำแหน่ง</div><div class='fp-stat-value'>{fp_stats['Acc_8Pos']:.2f}%</div></div>
                <div class='fp-stat-item'><div class='fp-stat-label'>☁️ 3 ตัวบน</div><div class='fp-stat-value'>{fp_stats['Acc_3Top']:.2f}%</div></div>
                <div class='fp-stat-item'><div class='fp-stat-label'>👆 2 ตัวบน</div><div class='fp-stat-value'>{fp_stats['Acc_2Top']:.2f}%</div></div>
                <div class='fp-stat-item'><div class='fp-stat-label'>👇 2 ตัวล่าง</div><div class='fp-stat-value'>{fp_stats['Acc_2Bot']:.2f}%</div></div>
            </div>
            """
            st.markdown(html_stats, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("## 🔺 สูตร 2: สามเหลี่ยมทองคำ (Original Pyramid)")
    st.caption(f"เน้น: เลขวิ่งตัวเดียว | ตรวจสอบทั้งหมด {pyr_stats['Total']} งวด")
    with st.expander("🔍 กดเพื่อดูภาพสามเหลี่ยมห้อยลงมา (Full Pyramid)", expanded=False):
        col_p_viz, col_p_desc = st.columns([2, 1])
        with col_p_viz:
            pyramid_html = generate_pyramid_html(pyr_stats['Layers'])
            st.markdown(pyramid_html, unsafe_allow_html=True)
        with col_p_desc:
            st.markdown("#### ผลลัพธ์สุดท้าย")
            st.markdown(f"<div style='font-size:48px; font-weight:bold; color:#FFD700; text-align:center;'>{pyr_stats['Digit']}</div>", unsafe_allow_html=True)
            st.markdown("##### 📊 สถิติความแม่นยำ")
            html_stats_pyr = f"""
            <div class='fp-stats-grid'>
                <div class='fp-stat-item'><div class='fp-stat-label'>🎯 8 ตำแหน่ง</div><div class='fp-stat-value'>{pyr_stats['Acc_8Pos']:.2f}%</div></div>
                <div class='fp-stat-item'><div class='fp-stat-label'>☁️ 3 ตัวบน</div><div class='fp-stat-value'>{pyr_stats['Acc_3Top']:.2f}%</div></div>
                <div class='fp-stat-item'><div class='fp-stat-label'>👆 2 ตัวบน</div><div class='fp-stat-value'>{pyr_stats['Acc_2Top']:.2f}%</div></div>
                <div class='fp-stat-item'><div class='fp-stat-label'>👇 2 ตัวล่าง</div><div class='fp-stat-value'>{pyr_stats['Acc_2Bot']:.2f}%</div></div>
            </div>
            """
            st.markdown(html_stats_pyr, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("## 🌋 สูตร 3: มหาพีระมิด (Grand Pyramid)")
    st.caption("เน้น: เลขวิ่งตัวเดียว | ใช้ข้อมูลครบทั้งรางวัลที่ 1 และ 2 ตัวล่าง (8 หลักตั้งต้น)")
    with st.expander("🔍 กดเพื่อดูมหาพีระมิด 8 ชั้น", expanded=False):
        col_g_viz, col_g_desc = st.columns([2, 1])
        with col_g_viz:
            grand_html = generate_pyramid_html(grand_stats['Layers'])
            st.markdown(grand_html, unsafe_allow_html=True)
        with col_g_desc:
            st.markdown("#### ผลลัพธ์สุดท้าย")
            st.markdown(f"<div style='font-size:48px; font-weight:bold; color:#FFD700; text-align:center;'>{grand_stats['Digit']}</div>", unsafe_allow_html=True)
            st.markdown("##### 📊 สถิติความแม่นยำ")
            html_stats_grand = f"""
            <div class='fp-stats-grid'>
                <div class='fp-stat-item'><div class='fp-stat-label'>🎯 8 ตำแหน่ง</div><div class='fp-stat-value'>{grand_stats['Acc_8Pos']:.2f}%</div></div>
                <div class='fp-stat-item'><div class='fp-stat-label'>☁️ 3 ตัวบน</div><div class='fp-stat-value'>{grand_stats['Acc_3Top']:.2f}%</div></div>
                <div class='fp-stat-item'><div class='fp-stat-label'>👆 2 ตัวบน</div><div class='fp-stat-value'>{grand_stats['Acc_2Top']:.2f}%</div></div>
                <div class='fp-stat-item'><div class='fp-stat-label'>👇 2 ตัวล่าง</div><div class='fp-stat-value'>{grand_stats['Acc_2Bot']:.2f}%</div></div>
            </div>
            """
            st.markdown(html_stats_grand, unsafe_allow_html=True)

# ==========================================
# 💀 หน้าที่ 7: Killer Zone (New!)
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