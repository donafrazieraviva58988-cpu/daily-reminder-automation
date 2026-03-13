#!/usr/bin/env python3
"""
每日提醒自动化 - Obsidian 笔记自动生成
根据提醒配置自动创建 Obsidian 每日笔记和仪表盘
"""

import os
import json
from datetime import datetime
from pathlib import Path

class ObsidianUpdater:
    def __init__(self, vault_path: str):
        self.vault_path = Path(vault_path)
        self.daily_path = self.vault_path / "Daily"
        self.tracker_path = self.daily_path / "追踪仪表盘.md"

    def create_daily_note(self, date: datetime, calendar_name: str, reminders: list, tracking: list):
        """创建每日笔记"""

        filename = date.strftime("%Y-%m-%d") + ".md"
        filepath = self.daily_path / filename

        # 生成执行记录
        tracking_items = "\n".join([
            f"- [ ] {t['name']} #{t['tag']}"
            for t in tracking
        ])

        content = f"""---
created: {date.strftime("%Y-%m-%d")}
tags:
  - daily
---

# {date.strftime("%Y-%m-%d")} 执行日

## 🔔 每日提醒

> 已自动创建，到点推送 iPhone/Mac 通知

```apple-reminders
list: {calendar_name}
```

---

## ✅ 执行记录

> 勾选后自动更新仪表盘

{tracking_items}

---

## 📊 查看统计

[[{calendar_name}追踪仪表盘|点击查看仪表盘]]
"""

        # 写入文件
        filepath.parent.mkdir(parents=True, exist_ok=True)
        filepath.write_text(content, encoding="utf-8")
        print(f"✅ 已创建每日笔记: {filepath}")

        return filepath

    def update_dashboard(self, calendar_name: str, tracking: list, date_range: int = 30):
        """更新仪表盘"""

        from datetime import datetime, timedelta

        end_date = datetime.now()
        start_date = end_date - timedelta(days=date_range)

        # 生成追踪代码块
        tracker_blocks = []
        for t in tracking:
            block = f"""### {t['name']}
```tracker
searchType: tag
searchTarget: {t['tag'].replace('#', '')}
folder: Daily
startDate: {start_date.strftime("%Y-%m-%d")}
endDate: {end_date.strftime("%Y-%m-%d")}
bar:
    title: {t['name']}
    barColor: "{t.get('color', '#4CAF50')}"
```"""
            tracker_blocks.append(block)

        content = f"""# 📊 {calendar_name}追踪仪表盘

---

## 📈 本周完成情况

{chr(10).join(tracker_blocks)}

---

## 📝 记录格式

在每日笔记中使用以下格式：

```markdown
- [ ] 任务完成 #标签
```

---

> 自动更新 | 最后更新: {datetime.now().strftime("%Y-%m-%d %H:%M")}
"""

        filepath = self.daily_path / f"{calendar_name}追踪仪表盘.md"
        filepath.write_text(content, encoding="utf-8")
        print(f"✅ 已更新仪表盘: {filepath}")

        return filepath


def main():
    """主函数"""

    # 默认 Vault 路径
    vault_path = "/Users/zhang/Documents/Obsidian Vault"

    # 读取配置
    import sys
    config_json = sys.argv[1] if len(sys.argv) > 1 else sys.stdin.read()

    try:
        config = json.loads(config_json)
    except json.JSONDecodeError as e:
        print(f"❌ 配置格式错误: {e}")
        sys.exit(1)

    calendar_name = config.get("calendar", "每日提醒")
    reminders = config.get("reminders", [])
    tracking = config.get("tracking", [])

    # 创建更新器
    updater = ObsidianUpdater(vault_path)

    # 创建每日笔记
    updater.create_daily_note(
        date=datetime.now(),
        calendar_name=calendar_name,
        reminders=reminders,
        tracking=tracking
    )

    # 更新仪表盘
    if tracking:
        updater.update_dashboard(
            calendar_name=calendar_name,
            tracking=tracking
        )

    print("\n✅ Obsidian 更新完成")


if __name__ == "__main__":
    main()
