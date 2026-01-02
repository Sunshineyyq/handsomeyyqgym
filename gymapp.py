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
    
    # 计算碳水 (剩余热量 / 4)
    # 1g 蛋白 = 4kcal, 1g 脂肪 = 9kcal
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
    # 1. 计算热量
    bmr = calculate_bmr(gender, weight, height, age)
    tdee = get_tdee(bmr, activity)
    target_cal, prot, fat, carb = generate_plan(goal, tdee, weight)
    
    # 2. 展示核心指标
    st.subheader("📊 每日热量与营养目标")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("每日热量目标", f"{target_cal} kcal", f"{target_cal - int(tdee)} vs TDEE")
    c2.metric("蛋白质", f"{prot} g", "肌肉原料")
    c3.metric("脂肪", f"{fat} g", "激素合成")
    c4.metric("碳水化合物", f"{carb} g", "能量来源")
    
    # 3. 进度可视化
    if has_history:
        st.subheader("📉 您的变化趋势")
        col_chart1, col_text = st.columns([2, 1])
        
        with col_chart1:
            # 创建数据框用于绘图
            df_progress = pd.DataFrame({
                '指标': ['体重 (kg)', '体重 (kg)', '腰围 (cm)', '腰围 (cm)'],
                '时间': ['上次', '本次', '上次', '本次'],
                '数值': [last_weight, weight, last_waist, current_waist]
            })
            
            # 使用 Streamlit 原生图表
            # 这里简单展示体重对比
            st.bar_chart(data=pd.DataFrame({
                '上次': [last_weight], 
                '本次': [weight]
            }, index=["体重 (kg)"]))
            
        with col_text:
            weight_diff = round(weight - last_weight, 2)
            if weight_diff < 0:
                st.success(f"🎉 恭喜！体重下降了 {abs(weight_diff)} kg")
            elif weight_diff > 0:
                if goal == "增肌":
                    st.success(f"💪 不错！体重增长了 {weight_diff} kg (希望是肌肉!)")
                else:
                    st.warning(f"⚠️ 体重上升了 {weight_diff} kg，请检查饮食。")
            else:
                st.info("⚖️ 体重持平")

    # 4. 生成具体方案
    st.markdown("---")
    col_diet, col_workout = st.columns(2)
    
    with col_diet:
        st.subheader("🥗 推荐饮食结构")
        st.info(f"""
        **早餐**: {int(target_cal*0.3)} kcal (高蛋白+优质碳水，如燕麦牛奶鸡蛋)
        **午餐**: {int(target_cal*0.4)} kcal (主食+掌心大小肉类+大量蔬菜)
        **晚餐**: {int(target_cal*0.2)} kcal (少油少盐，减少碳水)
        **加餐**: {int(target_cal*0.1)} kcal (如一个苹果或一勺蛋白粉)
        """)
        st.warning("**⚠️ 避坑指南**: 避免含糖饮料、油炸食品；多喝水 (建议每日 {int(weight*40)}ml)")

    with col_workout:
        st.subheader("🏋️‍♂️ 推荐训练方案")
        if goal == "减脂":
            st.write("**重点：力量训练保代谢 + 有氧造缺口**")
            st.markdown("""
            * **频率**: 每周 4-5 练
            * **力量**: 全身复合动作 (深蹲/俯卧撑/划船), 4组 x 12-15次
            * **有氧**: 力量后接 30分钟 (坡度走/慢跑/单车)
            """)
        elif goal == "增肌":
            st.write("**重点：大重量破坏肌纤维 + 盈余热量修复**")
            st.markdown("""
            * **频率**: 每周 4 练 (推/拉/腿/分化)
            * **力量**: 大重量低次数 (深蹲/卧推/硬拉), 4组 x 8-10次
            * **有氧**: 减少有氧，每周 1-2 次，每次 20分钟
            """)
        else:
            st.write("**重点：改善体态 + 维持代谢**")
            st.markdown("""
            * **频率**: 每周 3 练
            * **内容**: 循环训练 (Circuit Training) 或 HIIT
            """)
