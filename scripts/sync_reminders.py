#!/usr/bin/env python3
"""
每日提醒自动化 - 双向同步
从 Apple 提醒事项同步完成状态到 Obsidian
"""

import sys
import json
import re
from datetime import datetime
from pathlib import Path
from Foundation import NSDate
from EventKit import EKEventStore


class ReminderSync:
    def __init__(self, vault_path: str):
        self.store = EKEventStore.alloc().init()
        self.vault_path = Path(vault_path)
        self.daily_path = self.vault_path / "Daily"

    def get_completed_reminders(self, list_name: str):
        """获取已完成提醒"""
        completed = []
        
        # 获取提醒列表
        for cal in self.store.calendarsForEntityType_(1):
            if cal.title() == list_name:
                # 获取已完成的提醒
                predicates = self.store.predicateForRemindersInCalendars_([cal])
                reminders = self.store.remindersMatchingPredicate_(predicates)
                
                for reminder in reminders:
                    if reminder.isCompleted():
                        completed.append({
                            'title': reminder.title(),
                            'completed_date': reminder.completionDate() if hasattr(reminder, 'completionDate') else None
                        })
        
        return completed

    def update_obsidian_note(self, date_str: str, completed_titles: list):
        """更新 Obsidian 笔记中的勾选状态"""
        note_path = self.daily_path / f"{date_str}.md"
        
        if not note_path.exists():
            print(f"❌ 笔记不存在: {note_path}")
            return False
        
        content = note_path.read_text(encoding='utf-8')
        updated = False
        
        for title in completed_titles:
            # 简化标题匹配（去除 emoji）
            clean_title = re.sub(r'^[\U0001F300-\U0001F9FF]\s*', '', title)
            
            # 匹配未勾选的任务行
            pattern = rf'(- \[ \] [^\n]*{re.escape(clean_title)}[^\n]*)'
            
            def replace_func(match):
                nonlocal updated
                updated = True
                return match.group(1).replace('- [ ]', '- [x]', 1)
            
            content = re.sub(pattern, replace_func, content)
        
        if updated:
            note_path.write_text(content, encoding='utf-8')
            print(f"✅ 已更新: {note_path}")
        
        return updated

    def sync(self, list_name: str, date_str: str = None):
        """执行同步"""
        if date_str is None:
            date_str = datetime.now().strftime("%Y-%m-%d")
        
        print(f"🔄 同步 {list_name} → {date_str}")
        
        # 获取已完成提醒
        completed = self.get_completed_reminders(list_name)
        
        if not completed:
            print("  没有已完成的提醒")
            return
        
        print(f"  找到 {len(completed)} 个已完成提醒:")
        for r in completed:
            print(f"    - {r['title']}")
        
        # 更新 Obsidian
        titles = [r['title'] for r in completed]
        self.update_obsidian_note(date_str, titles)


def main():
    # 默认配置
    vault_path = "/Users/zhang/Documents/Obsidian Vault"
    
    # 读取参数
    import sys
    config_json = sys.argv[1] if len(sys.argv) > 1 else sys.stdin.read()
    
    try:
        config = json.loads(config_json)
    except json.JSONDecodeError:
        config = {"list_name": "生化重构执行", "date": None}
    
    sync = ReminderSync(vault_path)
    sync.sync(
        list_name=config.get("list_name", "生化重构执行"),
        date_str=config.get("date")
    )


if __name__ == "__main__":
    main()
