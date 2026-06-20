#!/usr/bin/env python3
"""
AI企业自动化Demo - 智能报表生成脚本 (AI-Powered)
场景：企业自动生成部门周报、数据洞察、行动建议
用法：python demo_enterprise.py
"""

import json
import requests
import re
from datetime import datetime, timedelta

# OpenAI-compatible API configuration
API_BASE = "http://localhost:8317"
API_KEY = "hermes-local-key"


def ai_call(prompt, system_prompt="你是一个专业的企业数据分析师。", temperature=0.7, max_tokens=2000):
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


def generate_department_report(dept_name, metrics, goals):
    """AI自动生成部门周报"""
    prompt = f"""请为以下部门生成一份专业的周报，用JSON格式返回（不要包含markdown代码块标记）：

部门: {dept_name}
本周核心数据:
{json.dumps(metrics, ensure_ascii=False, indent=2)}
本周目标: {goals}

请返回如下JSON格式:
{{
    "summary": "本周整体概述（100字以内）",
    "highlights": ["亮点1", "亮点2", "亮点3"],
    "data_insights": ["数据洞察1（基于数据发现的问题或机会）", "数据洞察2"],
    "issues": ["问题1", "问题2"],
    "next_week_plan": ["计划1", "计划2", "计划3"],
    "risk_alert": "风险预警（如有）",
    "kpi_status": "KPI完成状态（超额/达标/未达标）",
    "recommendation": "AI建议（50字以内）"
}}

要求：
- 数据洞察要基于实际数据进行分析
- 发现问题要具体可执行
- 下周计划要有明确目标"""

    ai_result = ai_call(prompt, temperature=0.7)

    if ai_result:
        try:
            cleaned = ai_result.strip()
            if cleaned.startswith("```"):
                cleaned = re.sub(r'^```(?:json)?\s*\n?', '', cleaned)
                cleaned = re.sub(r'\n?```\s*$', '', cleaned)
            parsed = json.loads(cleaned)

            return {
                "department": dept_name,
                "metrics": metrics,
                "summary": parsed.get("summary", f"{dept_name}本周工作正常推进"),
                "highlights": parsed.get("highlights", []),
                "data_insights": parsed.get("data_insights", []),
                "issues": parsed.get("issues", []),
                "next_week_plan": parsed.get("next_week_plan", []),
                "risk_alert": parsed.get("risk_alert", "无重大风险"),
                "kpi_status": parsed.get("kpi_status", "达标"),
                "recommendation": parsed.get("recommendation", "继续保持"),
                "source": "AI_Generated",
                "generated_at": datetime.now().isoformat()
            }
        except (json.JSONDecodeError, ValueError) as e:
            print(f"  ⚠️ JSON解析失败: {e}")

    # Fallback
    print("  ℹ️ 使用模板回退方案")
    return {
        "department": dept_name,
        "metrics": metrics,
        "summary": f"{dept_name}本周整体工作推进顺利，核心指标基本达标",
        "highlights": ["完成重点项目交付", "团队协作效率提升", "客户满意度提高"],
        "data_insights": ["核心数据稳步增长", "部分指标需关注"],
        "issues": ["跨部门协作效率待提升", "部分任务延期风险"],
        "next_week_plan": ["推进重点项目", "优化工作流程", "加强团队培训"],
        "risk_alert": "无重大风险",
        "kpi_status": "达标",
        "recommendation": "继续保持当前节奏，关注跨部门协作",
        "source": "Template_Fallback",
        "generated_at": datetime.now().isoformat()
    }


def format_report_text(report):
    """格式化周报为文本"""
    lines = []
    lines.append(f"{'='*60}")
    lines.append(f"📊 {report['department']}周报")
    lines.append(f"{'='*60}")
    lines.append(f"\n📋 整体概述：{report['summary']}")
    lines.append(f"📈 KPI状态：{report['kpi_status']}")
    lines.append(f"⚠️ 风险预警：{report['risk_alert']}")

    lines.append(f"\n🌟 本周亮点：")
    for h in report['highlights']:
        lines.append(f"  • {h}")

    lines.append(f"\n📊 数据洞察：")
    for d in report['data_insights']:
        lines.append(f"  • {d}")

    lines.append(f"\n🔧 待解决问题：")
    for i in report['issues']:
        lines.append(f"  • {i}")

    lines.append(f"\n📅 下周计划：")
    for p in report['next_week_plan']:
        lines.append(f"  • {p}")

    lines.append(f"\n💡 AI建议：{report['recommendation']}")

    return "\n".join(lines)


if __name__ == "__main__":
    print("=" * 60)
    print("🏢 AI企业自动化Demo - 智能报表生成 (AI-Powered)")
    print(f"🤖 AI API: {API_BASE}")
    print("=" * 60)

    departments = [
        {
            "name": "销售部",
            "metrics": {
                "new_customers": 45,
                "revenue": "¥380,000",
                "conversion_rate": "23%",
                "avg_deal_size": "¥8,444",
                "top_product": "企业版套餐",
                "lost_deals": 3
            },
            "goals": "新客户≥40，收入≥¥350,000"
        },
        {
            "name": "技术部",
            "metrics": {
                "bugs_fixed": 28,
                "features_shipped": 5,
                "system_uptime": "99.95%",
                "response_time": "120ms",
                "code_coverage": "87%",
                "deployments": 12
            },
            "goals": "Bug修复≥25，新功能≥4，系统可用性≥99.9%"
        },
        {
            "name": "市场部",
            "metrics": {
                "leads_generated": 230,
                "campaign_roi": "3.2x",
                "social_followers": "+1,200",
                "content_views": "45,000",
                "email_open_rate": "28%",
                "events_hosted": 2
            },
            "goals": "线索≥200，ROI≥2.5x，粉丝增长≥1000"
        }
    ]

    all_reports = []
    full_report_text = []

    for dept in departments:
        print(f"\n⏳ 正在为【{dept['name']}】生成AI周报...")
        report = generate_department_report(dept["name"], dept["metrics"], dept["goals"])
        all_reports.append(report)

        report_text = format_report_text(report)
        full_report_text.append(report_text)

        source_tag = "🤖" if report.get("source") == "AI_Generated" else "📋"
        print(f"\n{source_tag} {report_text}")

    # Save full report
    with open("weekly_report_full.txt", "w", encoding="utf-8") as f:
        f.write(f"{'#'*60}\n")
        f.write(f"# 企业智能周报 - AI生成\n")
        f.write(f"# 生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n")
        f.write(f"{'#'*60}\n\n")
        f.write("\n\n".join(full_report_text))

    # Save JSON
    with open("enterprise_output.json", "w", encoding="utf-8") as f:
        json.dump(all_reports, f, ensure_ascii=False, indent=2)

    ai_count = sum(1 for r in all_reports if r.get("source") == "AI_Generated")
    print(f"\n✅ 生成 {len(all_reports)} 个部门周报 (AI: {ai_count}, 模板: {len(all_reports) - ai_count})")
    print(f"📁 文本报告: weekly_report_full.txt")
    print(f"📁 JSON数据: enterprise_output.json")
