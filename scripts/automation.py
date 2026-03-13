#!/usr/bin/env python3
"""
每日提醒自动化 - 完整流程
整合：创建提醒 + 更新 Obsidian
"""

import sys
import json
import subprocess
from pathlib import Path

SCRIPTS_DIR = Path(__file__).parent


def run_create_reminder(config: dict) -> bool:
    """运行提醒创建脚本"""
    script_path = SCRIPTS_DIR / "create_reminder.py"
    config_json = json.dumps(config, ensure_ascii=False)

    result = subprocess.run(
        ["python3", str(script_path), config_json],
        capture_output=True,
        text=True
    )

    return result.returncode == 0


def run_obsidian_updater(config: dict) -> bool:
    """运行 Obsidian 更新脚本"""
    script_path = SCRIPTS_DIR / "obsidian_updater.py"
    config_json = json.dumps(config, ensure_ascii=False)

    result = subprocess.run(
        ["python3", str(script_path), config_json],
        capture_output=True,
        text=True
    )

    return result.returncode == 0


def main():
    """主函数"""
    config_json = sys.argv[1] if len(sys.argv) > 1 else sys.stdin.read()

    try:
        config = json.loads(config_json)
    except json.JSONDecodeError as e:
        print(f"❌ 配置格式错误: {e}")
        sys.exit(1)

    print("=" * 50)
    print("  每日提醒自动化 - 完整流程")
    print("=" * 50)

    # Step 1: 创建提醒
    print("\n📍 Step 1: 创建 Apple 提醒事项...")
    if not run_create_reminder(config):
        print("❌ 创建提醒失败")
        sys.exit(1)

    # Step 2: 更新 Obsidian
    print("\n📍 Step 2: 更新 Obsidian...")
    if not run_obsidian_updater(config):
        print("❌ 更新 Obsidian 失败")
        sys.exit(1)

    print("\n" + "=" * 50)
    print("  ✅ 全部完成！")
    print("=" * 50)
    print(f"""
📱 提醒已创建，将在以下时间推送：
   {', '.join(f"{r['time']} {r['title']}" for r in config.get('reminders', []))}

📝 Obsidian 已更新：
   - 每日笔记：Daily/{config.get('date', 'today')}.md
   - 仪表盘：Daily/{config.get('calendar', '每日提醒')}追踪仪表盘.md

🔔 请确保：
   1. iPhone「提醒事项」App 已登录同一 Apple ID
   2. 系统通知已开启
""")


if __name__ == "__main__":
    main()
