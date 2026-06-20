#!/usr/bin/env python3
"""制作AI自动化服务演示视频 - 终端风格动画"""

import subprocess
import os
import json
from PIL import Image, ImageDraw, ImageFont

OUTPUT_DIR = "C:/Users/Admin/Learning/IT-PM-Mastery/evolution/path1_demo/video"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# 屏幕参数
W, H = 1280, 720
BG_COLOR = (30, 30, 30)  # 深色背景
TEXT_COLOR = (0, 255, 128)  # 终端绿色
TITLE_COLOR = (255, 200, 50)  # 标题金色
ACCENT_COLOR = (0, 180, 255)  # 蓝色高亮

def create_frame(lines, title="", filename="frame.png"):
    """创建一帧终端风格画面"""
    img = Image.new('RGB', (W, H), BG_COLOR)
    draw = ImageDraw.Draw(img)

    # 尝试加载字体
    try:
        font = ImageFont.truetype("Consolas", 18)
        title_font = ImageFont.truetype("Consolas", 24)
        big_font = ImageFont.truetype("Consolas", 32)
    except:
        try:
            font = ImageFont.truetype("C:/Windows/Fonts/consola.ttf", 18)
            title_font = ImageFont.truetype("C:/Windows/Fonts/consola.ttf", 24)
            big_font = ImageFont.truetype("C:/Windows/Fonts/consola.ttf", 32)
        except:
            font = ImageFont.load_default()
            title_font = font
            big_font = font

    y = 40

    # 标题
    if title:
        draw.text((50, y), title, fill=TITLE_COLOR, font=title_font)
        y += 50
        draw.line([(50, y), (W-50, y)], fill=(80, 80, 80), width=1)
        y += 20

    # 内容行
    for line in lines:
        if isinstance(line, tuple):
            text, color = line
        else:
            text = line
            color = TEXT_COLOR

        if text.startswith("##"):
            draw.text((50, y), text[2:].strip(), fill=TITLE_COLOR, font=title_font)
            y += 35
        elif text.startswith("**"):
            draw.text((50, y), text.replace("**", ""), fill=ACCENT_COLOR, font=font)
            y += 28
        elif text.startswith(">>"):
            draw.text((50, y), text[2:], fill=(255, 100, 100), font=font)
            y += 28
        else:
            draw.text((50, y), text, fill=color, font=font)
            y += 25

    # 底部状态栏
    draw.rectangle([(0, H-35), (W, H)], fill=(20, 20, 20))
    draw.text((50, H-28), "AI Automation Service Demo | Powered by Hermes Agent", fill=(120, 120, 120), font=font)

    path = os.path.join(OUTPUT_DIR, filename)
    img.save(path)
    return path

# ===== 场景定义 =====
scenes = []

# 场景1: 开场
scenes.append({
    "title": "## AI自动化服务 - 产品演示",
    "lines": [
        "**AI-Powered Automation for Business**",
        "",
        "三个真实场景，展示AI如何帮企业提效降本：",
        "",
        ">> 场景1: 电商 - 批量商品上架",
        ">> 场景2: 自媒体 - 批量内容生成",
        ">> 场景3: 企业 - 智能报表分析",
        "",
        "每个场景：输入需求 → AI自动生成 → 一键导出",
        "",
        "**启动演示...**",
    ],
    "duration": 3
})

# 场景2: 电商Demo
scenes.append({
    "title": "## 场景1: 电商自动化 - 批量商品上架",
    "lines": [
        "$ python demo_ecommerce.py",
        "",
        "正在为【无线蓝牙耳机Pro】生成AI上架信息...",
        "  >> AI API调用中... mimo-v2.5",
        "  >> 标题: 🔥 无线蓝牙耳机Pro 旗舰音质 降噪神器",
        "  >> 描述: 40小时续航 | 主动降噪 | Hi-Res认证",
        "  >> 成本: ¥89 → 建议价: ¥268 → 促销价: ¥228",
        "  >> 利润率: 201%",
        "",
        "正在为【智能台灯护眼版】生成AI上架信息...",
        "  >> 护眼认证 | 色温调节 | APP控制",
        "",
        "正在为【有机坚果礼盒】生成...",
        "  >> 健康零食 | 年货送礼 | 自然有机",
        "",
        "**✅ 批量完成！5个商品全部AI生成，平均耗时3秒/个**",
    ],
    "duration": 4
})

# 场景3: 自媒体Demo
scenes.append({
    "title": "## 场景2: 自媒体自动化 - 批量内容生成",
    "lines": [
        "$ python demo_media.py",
        "",
        "正在为【AI工具提效】生成小红书内容方案...",
        "  >> 标题: 🔥 AI工具提效｜职场人必备的5个神器",
        "  >> Hook: 90%的人还在手动操作！",
        "  >> 类型: 图文 | 发布时间: 晚上8点",
        "  >> 预估浏览: 5000-10000",
        "",
        "正在为【副业赚钱】生成抖音内容方案...",
        "  >> 3秒hook + 干货分享 + 互动引导",
        "",
        "正在为【技术面试】生成公众号内容...",
        "  >> 深度分析 + 案例拆解 + 面试技巧",
        "",
        "**✅ 5套内容方案全部AI生成，含标题/Hook/标签/发布时间**",
    ],
    "duration": 4
})

# 场景4: 企业Demo
scenes.append({
    "title": "## 场景3: 企业自动化 - 智能报表生成",
    "lines": [
        "$ python demo_enterprise.py",
        "",
        "正在为【销售部】生成AI周报...",
        "  >> KPI状态: 达标",
        "  >> 数据洞察: 新客户+45, 收入¥380K, 转化率23%",
        "  >> AI建议: 重点关注老客户复购率",
        "",
        "正在为【技术部】生成AI周报...",
        "  >> Bug修复28个, 新功能5个, 系统99.95%可用",
        "  >> 风险预警: 跨部门协作效率待提升",
        "",
        "正在为【市场部】生成...",
        "  >> 线索230+, ROI 3.2x, 粉丝+1200",
        "",
        "**✅ 3个部门周报AI自动生成，含数据洞察+行动建议**",
    ],
    "duration": 4
})

# 场景5: 定价与交付
scenes.append({
    "title": "## 服务定价与交付",
    "lines": [
        "**套餐一：单个自动化流程**",
        "  价格: ¥500-2,000 | 交付: 1-3天 | 含需求分析+部署+培训",
        "",
        "**套餐二：整套解决方案**",
        "  价格: ¥3,000-10,000 | 交付: 1周 | 含定制开发+文档+30天维护",
        "",
        "**套餐三：长期维护**",
        "  价格: ¥500-2,000/月 | 含持续优化+7x24技术支持",
        "",
        "**为什么选择我们？**",
        "  ✅ 3个真实Demo验证能力",
        "  ✅ 本地部署，数据不出境",
        "  ✅ 按需定制，灵活调整",
        "  ✅ 专业团队，快速响应",
    ],
    "duration": 3
})

# 场景6: 联系方式
scenes.append({
    "title": "## 立即开始",
    "lines": [
        "**联系我们获取免费咨询**",
        "",
        ">> 扫码添加微信，获取免费方案评估",
        "",
        "**交付承诺：**",
        "  ✅ 源码交付，无隐性收费",
        "  ✅ 7天不满意全额退款",
        "  ✅ 终身免费技术咨询",
        "",
        "**AI自动化，让效率飞起来！**",
        "",
        "",
        "感谢观看 | AI Automation Service Demo",
    ],
    "duration": 3
})

# ===== 生成帧 =====
print("正在生成视频帧...")
frame_idx = 0
for i, scene in enumerate(scenes):
    print(f"  场景 {i+1}: {scene['title']}")
    # 每个场景生成多帧（模拟打字效果）
    for j in range(scene["duration"] * 2):  # 2fps
        visible_lines = scene["lines"][:min(len(scene["lines"]), j + 3)]
        frame_path = create_frame(
            visible_lines,
            title=scene["title"],
            filename=f"frame_{frame_idx:04d}.png"
        )
        frame_idx += 1

print(f"共生成 {frame_idx} 帧")

# ===== 用ffmpeg合成视频 =====
print("\n正在合成MP4视频...")
ffmpeg = "/c/ProgramData/chocolatey/bin/ffmpeg"
output_video = os.path.join(OUTPUT_DIR, "demo_video.mp4")

# 创建帧列表文件
frame_list = os.path.join(OUTPUT_DIR, "frames.txt")
with open(frame_list, "w") as f:
    for i in range(frame_idx):
        f.write(f"file 'frame_{i:04d}.png'\n")
        f.write("duration 0.5\n")  # 每帧0.5秒 = 2fps
    # 最后一帧需要再写一次
    f.write(f"file 'frame_{frame_idx-1:04d}.png'\n")

cmd = [
    ffmpeg, "-y",
    "-f", "concat",
    "-safe", "0",
    "-i", frame_list,
    "-c:v", "libx264",
    "-pix_fmt", "yuv420p",
    "-r", "2",
    "-vf", "scale=1280:720",
    output_video
]

result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
if result.returncode == 0:
    size = os.path.getsize(output_video)
    print(f"\n✅ 视频生成成功！")
    print(f"📁 路径: {output_video}")
    print(f"📊 大小: {size/1024:.1f} KB")
    print(f"⏱️ 时长: ~{frame_idx * 0.5:.1f}秒")
else:
    print(f"\n❌ 视频合成失败: {result.stderr[:500]}")
