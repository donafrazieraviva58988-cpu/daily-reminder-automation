#!/usr/bin/env python3
"""
每日提醒自动化 - 智能双向同步
Apple 提醒事项 ↔ Obsidian 智能同步

同步策略：
1. 如果 Obsidian 有勾选变化 → 以 Obsidian 为准同步到 Apple
2. 如果 Apple 有勾选变化 → 以 Apple 为准同步到 Obsidian
3. 使用时间戳判断哪个是最新变化
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
        self.sync_state_file = self.vault_path / ".reminder_sync_state.json"

    def load_sync_state(self):
        """加载上次同步状态"""
        if self.sync_state_file.exists():
            return json.loads(self.sync_state_file.read_text())
        return {}

    def save_sync_state(self, state):
        """保存同步状态"""
        self.sync_state_file.write_text(json.dumps(state, ensure_ascii=False, indent=2))

    def get_reminder_by_title(self, list_name: str, title: str):
        """根据标题获取提醒"""
        clean_title = re.sub(r'^[\U0001F300-\U0001F9FF]\s*', '', title).strip()
        
        for cal in self.store.calendarsForEntityType_(1):
            if cal.title() == list_name:
                predicates = self.store.predicateForRemindersInCalendars_([cal])
                reminders = self.store.remindersMatchingPredicate_(predicates)
                
                for reminder in reminders:
                    reminder_title = reminder.title()
                    clean_reminder = re.sub(r'^[\U0001F300-\U0001F9FF]\s*', '', reminder_title).strip()
                    
                    if clean_title in clean_reminder or clean_reminder in clean_title:
                        return reminder
        return None

    def get_obsidian_checkboxes(self, date_str: str):
        """获取 Obsidian 中的勾选状态"""
        note_path = self.daily_path / f"{date_str}.md"
        
        if not note_path.exists():
            return {}
        
        content = note_path.read_text(encoding="utf-8")
        pattern = r'- \[([ x])\] ([^\n]+)'
        matches = re.findall(pattern, content)
        
        checkboxes = {}
        for checked, line in matches:
            title_match = re.match(r'([\U0001F300-\U0001F9FF]?\s*[^@→]+)', line)
            if title_match:
                title = title_match.group(1).strip()
                checkboxes[title] = (checked == 'x')
        
        return checkboxes

    def get_apple_reminders_status(self, list_name: str):
        """获取 Apple 提醒的完成状态"""
        status = {}
        
        for cal in self.store.calendarsForEntityType_(1):
            if cal.title() == list_name:
                predicates = self.store.predicateForRemindersInCalendars_([cal])
                reminders = self.store.remindersMatchingPredicate_(predicates)
                
                for reminder in reminders:
                    title = reminder.title()
                    status[title] = reminder.isCompleted()
        
        return status

    def sync_to_apple(self, list_name: str, title: str, completed: bool):
        """同步到 Apple 提醒"""
        reminder = self.get_reminder_by_title(list_name, title)
        
        if not reminder:
            return False
        
        if completed and not reminder.isCompleted():
            reminder.setCompleted_(True)
            reminder.setCompletionDate_(NSDate.date())
            ok, err = self.store.saveReminder_commit_error_(reminder, True, None)
            if ok:
                print(f"  ✅ Apple 已标记完成: {title}")
                return True
        
        elif not completed and reminder.isCompleted():
            reminder.setCompleted_(False)
            reminder.setCompletionDate_(None)
            ok, err = self.store.saveReminder_commit_error_(reminder, True, None)
            if ok:
                print(f"  ✅ Apple 已取消完成: {title}")
                return True
        
        return False

    def sync_to_obsidian(self, date_str: str, title: str, completed: bool):
        """同步到 Obsidian"""
        note_path = self.daily_path / f"{date_str}.md"
        
        if not note_path.exists():
            return False
        
        content = note_path.read_text(encoding="utf-8")
        clean_title = re.sub(r'^[\U0001F300-\U0001F9FF]\s*', '', title).strip()
        
        pattern = rf'(- \[[ x]\] [^\n]*{re.escape(clean_title)}[^\n]*)'
        
        def replace_func(match):
            line = match.group(1)
            if completed:
                return line.replace('- [ ]', '- [x]', 1)
            else:
                return line.replace('- [x]', '- [ ]', 1)
        
        new_content = re.sub(pattern, replace_func, content)
        
        if new_content != content:
            note_path.write_text(new_content, encoding="utf-8")
            print(f"  ✅ Obsidian 已{'勾选' if completed else '取消勾选'}: {title}")
            return True
        return False

    def smart_sync(self, list_name: str, date_str: str = None):
        """智能双向同步"""
        if date_str is None:
            date_str = datetime.now().strftime("%Y-%m-%d")
        
        print(f"🔄 智能双向同步: {list_name} ↔ {date_str}")
        print("=" * 50)
        
        # 获取当前状态
        obsidian_state = self.get_obsidian_checkboxes(date_str)
        apple_state = self.get_apple_reminders_status(list_name)
        
        # 加载上次同步状态
        last_sync = self.load_sync_state()
        list_key = f"{list_name}_{date_str}"
        last_state = last_sync.get(list_key, {})
        
        # 对比变化
        sync_to_apple = []
        sync_to_obsidian = []
        
        all_titles = set(obsidian_state.keys()) | set(apple_state.keys())
        
        for title in all_titles:
            obs_checked = obsidian_state.get(title, False)
            apple_checked = apple_state.get(title, False)
            last_checked = last_state.get(title, None)
            
            # 判断哪个有变化
            obs_changed = (last_checked is not None and obs_checked != last_checked)
            apple_changed = (last_checked is not None and apple_checked != last_checked)
            
            if obs_checked != apple_checked:
                if obs_changed and not apple_changed:
                    # Obsidian 有变化 → 同步到 Apple
                    sync_to_apple.append((title, obs_checked))
                elif apple_changed and not obs_changed:
                    # Apple 有变化 → 同步到 Obsidian
                    sync_to_obsidian.append((title, apple_checked))
                else:
                    # 都有变化或都无变化 → 默认以 Obsidian 为准
                    sync_to_apple.append((title, obs_checked))
        
        # 执行同步
        if sync_to_apple:
            print(f"\n📤 Obsidian → Apple")
            for title, completed in sync_to_apple:
                self.sync_to_apple(list_name, title, completed)
        
        if sync_to_obsidian:
            print(f"\n📥 Apple → Obsidian")
            for title, completed in sync_to_obsidian:
                self.sync_to_obsidian(date_str, title, completed)
        
        if not sync_to_apple and not sync_to_obsidian:
            print("\n✅ 状态一致，无需同步")
        
        # 保存当前状态
        current_state = {}
        for title in all_titles:
            current_state[title] = obsidian_state.get(title, apple_state.get(title, False))
        
        last_sync[list_key] = current_state
        self.save_sync_state(last_sync)
        
        print("=" * 50)
        print(f"✅ 同步完成: {len(sync_to_apple)} → Apple, {len(sync_to_obsidian)} → Obsidian")


def main():
    vault_path = "/Users/zhang/Documents/Obsidian Vault"
    
    config_json = sys.argv[1] if len(sys.argv) > 1 else sys.stdin.read()
    
    try:
        config = json.loads(config_json)
    except json.JSONDecodeError:
        config = {"list_name": "生化重构执行", "date": None}
    
    sync = ReminderSync(vault_path)
    sync.smart_sync(
        list_name=config.get("list_name", "生化重构执行"),
        date_str=config.get("date")
    )


if __name__ == "__main__":
    main()
