import streamlit as st
import pandas as pd

# 1. 页面设置
st.set_page_config(page_title="全能健身 Pro", page_icon="🔥", layout="wide")

# 2. 核心逻辑
def get_plan_data(goal):
    if goal == "减脂":
        tips = [
            "早餐: 燕麦(40g) + 鸡蛋(1个) + 牛奶",
            "午餐: 杂粮饭 + 鸡胸肉 + 大量蔬菜",
            "晚餐: 玉米 + 鱼肉 + 凉拌菜",
            "加餐: 苹果 或 蓝莓"
        ]
        acts = [
            ["热身", "开合跳", "2组", "30秒"],
            ["力量", "深蹲", "4组", "20次"],
            ["力量", "俯卧撑", "4组", "力竭"],
            ["力量", "划船", "4组", "15次"],
            ["有氧", "爬坡快走", "1次", "35分钟"]
        ]
        advice = "核心策略：制造热量缺口，保持微饿感。"
    elif goal == "增肌":
        tips = [
            "早餐: 全麦面包 + 2个鸡蛋 + 香蕉",
            "午餐: 大份米饭 + 牛肉 + 蔬菜",
            "晚餐: 意面 + 鱼虾 + 沙拉",
            "加餐: 蛋白粉 + 吐司"
        ]
        acts = [
            ["热身", "肩部激活", "2组", "15次"],
            ["胸部", "卧推", "4组", "10次"],
            ["背部", "高位下拉", "4组", "12次"],
            ["腿部", "深蹲", "4组", "10次"],
            ["核心", "卷腹", "3组", "20次"]
        ]
        advice = "核心策略：热量盈余，大重量训练。"
    else:
        tips = [
            "早餐: 正常碳水 + 蛋白质",
            "午餐: 均衡饮食，七分饱",
            "晚餐: 少油少盐，少主食",
            "加餐: 酸奶 + 坚果"
        ]
        acts = [
            ["激活", "动态拉伸", "1组", "5分钟"],
            ["全身", "波比跳", "3组", "10次"],
            ["下肢", "箭步蹲", "3组", "15次"],
            ["上肢", "俯卧撑", "3组", "15次"],
            ["有氧", "慢跑", "1次", "20分钟"]
        ]
        advice = "核心策略：改善体态，关注动作质量。"

    df = pd.DataFrame(acts, columns=["板块", "动作", "组数", "计划"])
    return tips, df, advice

def check_progress(cur_w, last_w, cur_waist, last_waist, goal):
    w_diff = round(cur_w - last_w, 1)
    waist_diff = round(cur_waist - last_waist, 1)
    
    msg = ""
    status = "normal"
    
    # 简单的字符串拼接，防止报错
    val_w = abs(w_diff)
    
    if goal == "减脂":
        if w_diff < 0:
            msg = "🎉 太棒了！体重下降了 " + str(val_w) + " kg"
            status = "success"
        elif w_diff > 0.5:
            msg = "⚠️ 警告：体重反升。请检查饮食！"
            status = "error"
        else:
            msg = "⚖️ 平台期：体重波动不大，建议增加有氧。"
            status = "warning"
    elif goal == "增肌":
        if w_diff > 0:
            msg = "💪 很好！体重增长了 " + str(val_w) + " kg"
            status = "success"
        else:
            msg = "📉 没变化？你需要多吃点碳水！"
            status = "warning"
            
    return w_diff, waist_diff, msg, status

# 3. 界面显示
st.title("🔥 全能健身教练 Pro")

with st.sidebar:
    st.header("📝 本次记录")
    sex = st.radio("性别", ["男", "女"])
    age = st.number_input("年龄", 18, 80, 25)
    h = st.number_input("身高cm", 100, 250, 163)
    
    c1, c2 = st.columns(2)
    with c1: w_now = st.number_input("今日体重", 30.0, 200.0, 55.0)
    with c2: waist_now = st.number_input("今日腰围", 40.0, 150.0, 70.0)
        
    goal = st.selectbox("目标", ["减脂", "增肌", "维持"])
    act = st.selectbox("活动量", ["久坐", "轻度", "中度", "高强度"])
    
    st.markdown("---")
    has_his = st.checkbox("我有上次的数据")
    
    w_last = 0.0
    waist_last = 0.0
    
    if has_his:
        c3, c4 = st.columns(2)
        with c3: w_last = st.number_input("上次体重", 30.0, 200.0, 56.0)
        with c4: waist_last = st.number_input("上次腰围", 40.0, 150.0, 72.0)
            
    st.markdown("---")
    if st.button("🚀 生成报告", type="primary"):
        st.session_state['run'] = True

if st.session_state.get('run'):
    if sex == '男': bmr = (10*w_now)+(6.25*h)-(5*age)+5
    else: bmr = (10*w_now)+(6.25*h)-(5*age)-161
    
    act_map = {"久坐":1.2, "轻度":1.375, "中度":1.55, "高强度":1.725}
    tdee = int(bmr * act_map[act])
    
    if goal=="减脂": target = tdee - 500
    elif goal=="增肌": target = tdee + 300
    else: target = tdee
    
    if has_his:
        st.subheader("📊 变化趋势")
        d_w, d_waist, msg, stt = check_progress(w_now, w_last, waist_now, waist_last, goal)
        
        k1, k2, k3 = st.columns(3)
        k1.metric("体重变化", f"{w_now}kg", f"{d_w}kg", delta_color="inverse")
        k2.metric("腰围变化", f"{waist_now}cm", f"{d_waist}cm", delta_color="inverse")
        k3.metric("BMI指数", f"{round(w_now/((h/100)**2), 1)}")
        
        if stt == "success": st.success(msg)
        elif stt == "error": st.error(msg)
        else: st.warning(msg)
        
        chart_data = pd.DataFrame({
            "类型": ["上次", "本次"],
            "体重": [w_last, w_now]
        }).set_index("类型")
        st.bar_chart(chart_data)
    else:
        st.info("💡 勾选左侧“我有上次的数据”可查看进度对比图")
        st.metric("今日热量目标", f"{target} kcal")

    st.markdown("---")
    
    tips, df_plan, advice = get_plan_data(goal)
    t1, t2 = st.tabs(["🥗 食谱", "🏋️‍♂️ 训练"])
    
    with t1:
        st.info(advice)
        for t in tips: st.write(f"- {t}")
    with t2:
        st.dataframe(df_plan, use_container_width=True)
else:
    st.info("👈 请点击左侧按钮生成报告")
