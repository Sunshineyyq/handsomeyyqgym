import streamlit as st
import pandas as pd

# --- 1. 页面配置 ---
st.set_page_config(page_title="全能健身教练 Pro", page_icon="🔥", layout="wide")

# --- 2. 核心逻辑：生成计划 ---
def get_detailed_plan(goal):
    # 使用列表格式，防止断行报错
    if goal == "减脂":
        # 饮食
        diet_tips = [
            "早餐: 燕麦(40g) + 鸡蛋(1个) + 牛奶",
            "午餐: 杂粮饭 + 鸡胸肉/虾 + 大量蔬菜",
            "晚餐: 玉米/红薯 + 鱼肉 + 凉拌菜",
            "加餐: 一个苹果 或 少量蓝莓"
        ]
        # 训练
        workout_data = [
            ["热身", "开合跳", "2组", "30秒"],
            ["力量", "深蹲", "4组", "20次"],
            ["力量", "俯卧撑", "4组", "力竭"],
            ["力量", "划船", "4组", "15次"],
            ["有氧", "爬坡快走", "1次", "35分钟"]
        ]
        advice = "核心策略：制造热量缺口。稍微有一点饥饿感是正常的。"
        
    elif goal == "增肌":
        diet_tips = [
            "早餐: 全麦面包 + 2个鸡蛋 + 香蕉",
            "午餐: 米饭(大份) + 牛肉/鸡腿 + 蔬菜",
            "晚餐: 意面 + 鱼/虾 + 橄榄油沙拉",
            "加餐: 蛋白粉 + 吐司 + 花生酱"
        ]
        workout_data = [
            ["热身", "肩部激活", "2组", "15次"],
            ["胸部", "卧推", "4组", "10次"],
            ["背部", "高位下拉", "4组", "12次"],
            ["腿部", "负重深蹲", "4组", "10次"],
            ["核心", "卷腹", "3组", "20次"]
        ]
        advice = "核心策略：盈余热量 + 大重量。不要怕吃碳水，那是力量来源。"
        
    else: # 维持
        diet_tips = [
            "早餐: 正常碳水 + 蛋白质",
            "午餐: 均衡饮食，七分饱",
            "晚餐: 少油少盐，减少主食",
            "加餐: 无糖酸奶 + 坚果"
        ]
        workout_data = [
            ["激活", "动态拉伸", "1组", "5分钟"],
            ["全身", "波比跳", "3组", "10次"],
            ["下肢", "箭步蹲", "3组", "15次"],
            ["上肢", "俯卧撑", "3组", "15次"],
            ["有氧", "慢跑", "1次", "20分钟"]
        ]
        advice = "核心策略：改善体态。关注动作质量而不是重量。"

    return diet_tips, pd.DataFrame(workout_data, columns=["板块", "动作", "组数", "计划"]), advice

# --- 3. 核心逻辑：进度分析 ---
def analyze_progress(cur_w, last_w, cur_waist, last_waist, goal):
    # 计算变化量
    w_change = cur_w - last_w
    waist_change = cur_waist - last_waist
    
    msg = ""
    status = "normal"
    
    # 减脂逻辑判断
    if goal == "减脂":
        if w_change < 0:
            msg = f"🎉 太棒了！体重下降了 {abs(w_change):.1f
