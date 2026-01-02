import streamlit as st
import pandas as pd

# --- 页面配置 ---
st.set_page_config(page_title="私人健身计划助手", page_icon="💪", layout="wide")

# --- 核心逻辑函数 ---
def calculate_bmr(gender, weight, height, age):
    # Mifflin-St Jeor 公式
    if gender == '男':
        return (10 * weight) + (6.25 * height) - (5 * age) + 5
    else:
        return (10 * weight) + (6.25 * height) - (5 * age) - 161

def get_tdee(bmr, activity_level):
    levels = {
        "久坐 (几乎不运动)": 1.2,
        "轻度活跃 (每周1-3次运动)": 1.375,
        "中度活跃 (每周3-5次运动)": 1.55,
        "非常活跃 (每周6-7次运动)": 1.725,
        "超级活跃 (体力工作+高强度训练)": 1.9
    }
    return bmr * levels[activity_level]

def generate_plan(goal, tdee, weight):
    if goal == "减脂":
        target_calories = tdee - 500
        protein_g = weight * 2.2  # 减脂期高蛋白保肌
        fat_g = weight * 0.8
    elif goal == "增肌":
        target_calories = tdee + 300
        protein_g = weight * 2.0
        fat_g = weight * 1.0
    else:  # 维持
        target_calories = tdee
        protein_g = weight * 1.8
        fat_g = weight * 0.9
    
    # 计算碳水
    remaining_cal = target_calories - (protein_g * 4) - (fat_g * 9)
    carbs_g = remaining_cal / 4
    
    return int(target_calories), int(protein_g), int(fat_g), int(carbs_g)

# --- 界面 UI ---
st.title("💪 AI 健身计划助手")
st.markdown("输入您的身体数据，获取今日的**热量缺口**、**饮食建议**与**训练方案**。")

with st.sidebar:
    st.header("📋 1. 您的档案")
    gender = st.radio("性别", ["男", "女"], horizontal=True)
    col1, col2 = st.columns(2)
    with col1:
        age = st.number_input("年龄", 18, 80, 25)
        height = st.number_input("身高 (cm)", 100, 250, 175)
    with col2:
        weight = st.number_input("当前体重 (kg)", 30.0, 200.0, 70.0)
        goal = st.selectbox("当前目标", ["减脂", "增肌", "维持"])
    
    activity = st.selectbox("日常活动量", [
        "久坐 (几乎不运动)",
        "轻度活跃 (每周1-3次运动)",
        "中度活跃 (每周3-5次运动)",
        "非常活跃 (每周6-7次运动)",
        "超级活跃 (体力工作+高强度训练)"
    ])
    
    st.markdown("---")
    st.header("📉 2. 进度对比 (选填)")
    has_history = st.checkbox("我有上一次的数据")
    if has_history:
        last_weight = st.number_input("上次体重 (kg)", 30.0, 200.0, 71.0)
        last_waist = st.number_input("上次腰围 (cm)", 40.0, 150.0, 85.0)
        current_waist = st.number_input("当前腰围 (cm)", 40.0, 150.0, 84.0)

# --- 主体计算 ---
if st.button("🚀 生成我的计划", type="primary"):
    bmr = calculate_bmr(gender, weight, height, age)
    tdee = get_tdee(bmr, activity)
    target_cal, prot, fat, carb = generate_plan(goal, tdee, weight)
    
    st.subheader("📊 每日热量与营养目标")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("每日热量目标", f"{target_cal} kcal", f"{target_cal - int(tdee)} vs TDEE")
    c2.metric("蛋白质", f"{prot} g", "肌肉原料")
    c3.metric("脂肪", f"{fat} g", "激素合成")
    c4.metric("碳水化合物", f"{carb} g", "能量来源")
    
    if has_history:
        st.subheader("📉 您的变化趋势")
        col_chart1, col_text = st.columns([2, 1])
        with col_chart1:
            st.bar_chart(data=pd.DataFrame({
                '上次': [last_weight], 
                '本次': [weight]
            }, index=["体重 (kg)"]))
        with col_text:
            weight_diff = round(weight - last_weight, 2)
            if weight_diff < 0:
                st.success(f"🎉 恭喜！体重下降了 {abs(weight_diff)} kg")
            elif weight_diff > 0:
                st.warning(f"⚠️ 体重上升了 {weight_diff} kg")
            else:
                st.info("⚖️ 体重持平")

    st.markdown("---")
    col_diet, col_workout = st.columns(2)
    with col_diet:
        st.subheader("🥗 推荐饮食结构")
        st.info(f"""
        **早餐**: {int(target_cal*0.3)} kcal
        **午餐**: {int(target_cal*0.4)} kcal
        **晚餐**: {int(target_cal*0.2)} kcal
        **加餐**: {int(target_cal*0.1)} kcal
        """)
    with col_workout:
        st.subheader("🏋️‍♂️ 推荐训练方案")
        if goal == "减脂":
            st.write("重点：力量训练保代谢 + 有氧造缺口")
        elif goal == "增肌":
            st.write("重点：大重量破坏肌纤维 + 盈余热量修复")
        else:
            st.write("重点：改善体态 + 维持代谢")
