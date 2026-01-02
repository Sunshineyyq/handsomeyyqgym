import streamlit as st
import pandas as pd

# 页面设置
st.set_page_config(page_title="健身助手", page_icon="💪")

# 核心计算函数
def get_bmr(gender, w, h, age):
    if gender == '男':
        return (10*w) + (6.25*h) - (5*age) + 5
    else:
        return (10*w) + (6.25*h) - (5*age) - 161

def get_plan(goal):
    if goal == "减脂":
        focus = "全身循环 + 有氧"
        # 动作表：动作 / 组数
        data = [
            ["开合跳", "2组x30秒"],
            ["徒手深蹲", "4组x20次"],
            ["跪姿俯卧撑", "4组力竭"],
            ["平板支撑", "3组x45秒"],
            ["爬坡快走", "30分钟"]
        ]
    elif goal == "增肌":
        focus = "大重量分化"
        data = [
            ["肩部热身", "2组x15次"],
            ["哑铃卧推", "4组x10次"],
            ["高位下拉", "4组x12次"],
            ["负重深蹲", "4组x10次"],
            ["卷腹", "3组x20次"]
        ]
    else:
        focus = "体态改善"
        data = [
            ["动态拉伸", "5分钟"],
            ["臀桥", "3组x15次"],
            ["箭步蹲", "3组x12次"],
            ["俯卧撑", "3组x15次"],
            ["慢跑", "20分钟"]
        ]
    return focus, pd.DataFrame(data, columns=["动作", "计划"])

# 界面显示
st.title("💪 健身计划助手")

# 侧边栏输入
with st.sidebar:
    st.header("输入数据")
    sex = st.radio("性别", ["男", "女"])
    age = st.number_input("年龄", 18, 80, 25)
    h = st.number_input("身高cm", 100, 250, 165)
    w = st.number_input("体重kg", 30.0, 200.0, 55.0)
    goal = st.selectbox("目标", ["减脂", "增肌", "维持"])
    
    if st.button("生成计划"):
        st.session_state['run'] = True

# 结果生成
if st.session_state.get('run'):
    # 计算热量
    bmr = get_bmr(sex, w, h, age)
    if goal == "减脂": target = bmr * 1.2
    elif goal == "增肌": target = bmr * 1.6
    else: target = bmr * 1.4
    
    # 显示结果
    st.subheader("📊 分析结果")
    st.metric("🎯 每日推荐热量", f"{int(target)} kcal")
    
    focus, df = get_plan(goal)
    st.success(f"训练重点：{focus}")
    st.table(df)
    
    st.info("💡 饮食建议：少油少盐，多吃瘦肉蔬菜。")
