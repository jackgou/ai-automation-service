#!/usr/bin/env python3
"""
AI自媒体自动化Demo - 批量内容生成脚本 (AI-Powered)
场景：自媒体运营批量生成标题、大纲、标签
用法：python demo_media.py
"""

import json
import requests
import re
from datetime import datetime

# OpenAI-compatible API configuration
API_BASE = "http://localhost:8317"
API_KEY = "hermes-local-key"


def ai_call(prompt, system_prompt="你是一个专业的自媒体运营专家。", temperature=0.9, max_tokens=1500):
    """调用本地AI API生成内容"""
    try:
        resp = requests.post(
            f"{API_BASE}/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {API_KEY}",
                "Content-Type": "application/json",
            },
            json={
                "model": "mimo-v2.5",
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": prompt},
                ],
                "temperature": temperature,
                "max_tokens": max_tokens,
            },
            timeout=60,
        )
        resp.raise_for_status()
        data = resp.json()
        return data["choices"][0]["message"]["content"].strip()
    except Exception as e:
        print(f"  ⚠️ AI API调用失败 ({e}), 使用本地模板作为回退")
        return None


def generate_content(topic, platform, style):
    """AI自动生成自媒体内容方案"""
    prompt = f"""请为以下自媒体内容生成完整的创作方案，用JSON格式返回（不要包含markdown代码块标记）：

内容主题: {topic}
发布平台: {platform}
内容风格: {style}

请返回如下JSON格式:
{{
    "title": "爆款标题（吸引眼球，含数字和emoji，20字以内）",
    "hook": "开头hook（3秒抓住注意力，30字以内）",
    "outline": ["要点1（50字）", "要点2（50字）", "要点3（50字）", "要点4（50字）"],
    "hashtags": ["标签1", "标签2", "标签3", "标签4", "标签5"],
    "best_time": "最佳发布时间",
    "engagement_hook": "互动引导语（引导评论/点赞）",
    "content_type": "内容类型（图文/短视频/长文）",
    "estimated_views": "预估浏览量",
    "cta": "行动号召（关注/收藏/转发）"
}}

要求：
- 标题要有冲击力，包含数字和情绪词
- outline要结构清晰，有逻辑递进
- hashtags要覆盖热门+精准标签"""

    ai_result = ai_call(prompt, temperature=0.9)

    if ai_result:
        try:
            cleaned = ai_result.strip()
            if cleaned.startswith("```"):
                cleaned = re.sub(r'^```(?:json)?\s*\n?', '', cleaned)
                cleaned = re.sub(r'\n?```\s*$', '', cleaned)
            parsed = json.loads(cleaned)

            return {
                "topic": topic,
                "platform": platform,
                "title": parsed.get("title", f"【干货分享】{topic}的5个实用技巧"),
                "hook": parsed.get("hook", f"你还在为{topic}发愁吗？"),
                "outline": parsed.get("outline", []),
                "hashtags": parsed.get("hashtags", []),
                "best_time": parsed.get("best_time", "晚上8点"),
                "engagement_hook": parsed.get("engagement_hook", "你觉得哪个最有用？评论区告诉我！"),
                "content_type": parsed.get("content_type", "图文"),
                "estimated_views": parsed.get("estimated_views", "5000-10000"),
                "cta": parsed.get("cta", "关注我，获取更多干货！"),
                "style": style,
                "source": "AI_Generated",
                "generated_at": datetime.now().isoformat()
            }
        except (json.JSONDecodeError, ValueError) as e:
            print(f"  ⚠️ JSON解析失败: {e}")

    # Fallback
    print("  ℹ️ 使用模板回退方案")
    return {
        "topic": topic,
        "platform": platform,
        "title": f"🔥 {topic}｜{style}必备的5个实用技巧",
        "hook": f"90%的人都不知道的{topic}技巧！",
        "outline": [
            f"问题引入：为什么{topic}这么重要",
            "核心观点1：方法论解析",
            "核心观点2：实操步骤",
            "总结：行动指南"
        ],
        "hashtags": [topic, style, "干货分享", "实用技巧", "收藏"],
        "best_time": "晚上8点",
        "engagement_hook": "你觉得哪个最有用？评论区告诉我！",
        "content_type": "图文",
        "estimated_views": "5000-10000",
        "cta": "关注我，获取更多干货！",
        "style": style,
        "source": "Template_Fallback",
        "generated_at": datetime.now().isoformat()
    }


if __name__ == "__main__":
    print("=" * 60)
    print("📱 AI自媒体自动化Demo - 批量内容生成 (AI-Powered)")
    print(f"🤖 AI API: {API_BASE}")
    print("=" * 60)

    topics = [
        ("AI工具提效", "小红书", "职场干货"),
        ("副业赚钱", "抖音", "生活经验"),
        ("技术面试", "公众号", "深度分析"),
        ("健身减脂", "小红书", "健康科普"),
        ("理财入门", "知乎", "知识分享"),
    ]

    results = []
    for topic, platform, style in topics:
        print(f"\n⏳ 正在为【{topic}】生成{platform}内容方案...")
        result = generate_content(topic, platform, style)
        results.append(result)

        source_tag = "🤖" if result.get("source") == "AI_Generated" else "📋"
        print(f"\n{source_tag} 【{topic}】@{platform}")
        print(f"  标题: {result['title']}")
        print(f"  Hook: {result['hook']}")
        print(f"  类型: {result['content_type']}")
        print(f"  发布时间: {result['best_time']}")
        print(f"  预估浏览: {result['estimated_views']}")
        print(f"  标签: {' '.join(result['hashtags'][:4])}")

    with open("media_output.json", "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

    ai_count = sum(1 for r in results if r.get("source") == "AI_Generated")
    print(f"\n✅ 生成 {len(results)} 套内容方案 (AI: {ai_count}, 模板: {len(results) - ai_count})")
    print(f"📁 输出文件: media_output.json")
