#!/usr/bin/env python3
"""
AI电商自动化Demo - 批量商品上架脚本 (AI-Powered)
场景：电商卖家批量生成商品标题、描述、定价建议
用法：python demo_ecommerce.py
"""

import json
import requests
import re
from datetime import datetime

# OpenAI-compatible API configuration
API_BASE = "http://localhost:8317"
API_KEY = "hermes-local-key"


def ai_call(prompt, system_prompt="你是一个专业的电商运营专家。", temperature=0.8, max_tokens=1500):
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


def generate_product_listing(product_name, category, cost_price):
    """AI自动生成商品上架信息"""

    prompt = f"""请为以下商品生成完整的电商上架信息，用JSON格式返回（不要包含markdown代码块标记）：

商品名称: {product_name}
商品类别: {category}
成本价: ¥{cost_price}

请返回如下JSON格式:
{{
    "title": "商品标题（吸引眼球，包含emoji，30字以内）",
    "description": "商品详细描述（包含产品亮点、购买理由、使用场景，200-300字）",
    "selling_points": ["卖点1", "卖点2", "卖点3", "卖点4"],
    "target_audience": "目标受众描述",
    "suggested_price": 建议售价（数字）,
    "promotion_price": 促销价（数字，约为建议价的85%）,
    "marketing_slogan": "一句话营销口号",
    "keywords": ["关键词1", "关键词2", "关键词3", "关键词4", "关键词5"]
}}

要求：
- 标题要有吸引力，包含emoji表情
- 描述要生动具体，突出产品优势
- 价格要合理，考虑成本和市场定位
- 卖点要突出差异化"""

    ai_result = ai_call(prompt, temperature=0.85)

    if ai_result:
        try:
            # Try to extract JSON from the response
            # Remove markdown code block markers if present
            cleaned = ai_result.strip()
            if cleaned.startswith("```"):
                cleaned = re.sub(r'^```(?:json)?\s*\n?', '', cleaned)
                cleaned = re.sub(r'\n?```\s*$', '', cleaned)
            parsed = json.loads(cleaned)

            # Validate required fields
            title = parsed.get("title", f"【品质好物】{product_name} 限时特惠")
            description = parsed.get("description", f"{product_name} - 您的品质之选！")
            suggested_price = float(parsed.get("suggested_price", cost_price * 2.5))
            promotion_price = float(parsed.get("promotion_price", suggested_price * 0.85))

            return {
                "product_name": product_name,
                "title": title,
                "description": description,
                "selling_points": parsed.get("selling_points", []),
                "target_audience": parsed.get("target_audience", "通用消费者"),
                "cost_price": cost_price,
                "suggested_price": round(suggested_price, 2),
                "promotion_price": round(promotion_price, 2),
                "marketing_slogan": parsed.get("marketing_slogan", ""),
                "keywords": parsed.get("keywords", []),
                "category": category,
                "source": "AI_Generated",
                "generated_at": datetime.now().isoformat()
            }
        except (json.JSONDecodeError, ValueError) as e:
            print(f"  ⚠️ JSON解析失败: {e}")

    # Fallback to template-based generation
    print("  ℹ️ 使用模板回退方案")
    title_templates = {
        "数码": f"【新品首发】{product_name} 2026款 超值优惠 限时特惠",
        "服饰": f"【爆款推荐】{product_name} 百搭时尚 品质保证",
        "家居": f"【居家必备】{product_name} 实用美观 提升生活品质",
        "食品": f"【美味推荐】{product_name} 新鲜直达 健康美味",
    }
    title = title_templates.get(category, f"【品质好物】{product_name} 限时特惠")
    suggested_price = round(cost_price * 2.5, 2)
    promotion_price = round(suggested_price * 0.85, 2)

    return {
        "product_name": product_name,
        "title": title,
        "description": f"{product_name} - 您的品质之选！精选优质材料，品质保证。限时优惠，错过不再。",
        "selling_points": ["精选优质材料", "人性化设计", "性价比超高", "售后无忧"],
        "target_audience": "通用消费者",
        "cost_price": cost_price,
        "suggested_price": suggested_price,
        "promotion_price": promotion_price,
        "marketing_slogan": "品质生活，从这里开始",
        "keywords": [product_name, category, "限时优惠"],
        "category": category,
        "source": "Template_Fallback",
        "generated_at": datetime.now().isoformat()
    }


if __name__ == "__main__":
    print("=" * 60)
    print("🛒 AI电商自动化Demo - 批量商品上架 (AI-Powered)")
    print(f"🤖 AI API: {API_BASE}")
    print("=" * 60)

    products = [
        ("无线蓝牙耳机Pro", "数码", 89),
        ("纯棉T恤男款", "服饰", 35),
        ("智能台灯护眼版", "家居", 120),
        ("有机坚果礼盒", "食品", 65),
        ("便携式咖啡机", "数码", 200),
    ]

    results = []
    for name, cat, cost in products:
        print(f"\n⏳ 正在为【{name}】生成AI上架信息...")
        result = generate_product_listing(name, cat, cost)
        results.append(result)

        source_tag = "🤖" if result.get("source") == "AI_Generated" else "📋"
        print(f"\n{source_tag} 【{name}】")
        print(f"  标题: {result['title']}")
        if result.get('marketing_slogan'):
            print(f"  口号: {result['marketing_slogan']}")
        print(f"  成本: ¥{result['cost_price']}")
        print(f"  建议价: ¥{result['suggested_price']}")
        print(f"  促销价: ¥{result['promotion_price']}")
        print(f"  利润率: {round((result['suggested_price'] - result['cost_price']) / result['cost_price'] * 100)}%")
        if result.get('selling_points'):
            print(f"  卖点: {', '.join(result['selling_points'][:3])}")
        if result.get('keywords'):
            print(f"  关键词: {', '.join(result['keywords'][:4])}")

    with open("ecommerce_output.json", "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

    ai_count = sum(1 for r in results if r.get("source") == "AI_Generated")
    print(f"\n✅ 生成 {len(results)} 个商品上架信息 (AI: {ai_count}, 模板: {len(results) - ai_count})")
    print(f"📁 输出文件: ecommerce_output.json")
