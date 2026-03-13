#!/usr/bin/env python3
"""每日提醒自动化 - 使用 EventKit 创建带提醒时间的提醒事项"""

import sys
import json
import time
from datetime import datetime, timedelta
from Foundation import NSDate, NSDateComponents, NSCalendar
from EventKit import EKEventStore, EKReminder, EKAlarm, EKRecurrenceRule, EKCalendar

# EKRecurrenceFrequency 常量
EKRecurrenceFrequencyDaily = 0

class ReminderAutomation:
    def __init__(self):
        self.store = EKEventStore.alloc().init()
        self.access_granted = False

    def request_access(self):
        """请求提醒事项访问权限"""
        def handler(granted, error):
            self.access_granted = granted
            if granted:
                print("✅ 权限已授权")
            elif error:
                print(f"❌ 权限被拒绝: {error}")

        self.store.requestAccessToEntityType_completion_(1, handler)

        for _ in range(20):
            if self.access_granted:
                return True
            time.sleep(0.3)
        return self.access_granted

    def get_calendar(self, name):
        """获取提醒列表"""
        for cal in self.store.calendarsForEntityType_(1):
            if cal.title() == name:
                return cal
        return None

    def create_calendar(self, name):
        """创建提醒列表"""
        cal = EKCalendar.calendarForEntityType_eventStore_(1, self.store)
        cal.setTitle_(name)
        cal.setSource_(self.store.defaultCalendarForNewReminders().source())
        ok, err = self.store.saveCalendar_commit_error_(cal, True, None)
        if ok:
            print(f"✅ 已创建列表: {name}")
            return cal
        print(f"❌ 创建列表失败: {err}")
        return None

    def get_or_create_calendar(self, name):
        cal = self.get_calendar(name)
        return cal if cal else self.create_calendar(name)

    def create_reminder(self, title, calendar_name, alarm_time=None, notes="", priority=0, repeat_daily=False):
        """创建提醒"""
        cal = self.get_or_create_calendar(calendar_name)
        if not cal:
            return False

        reminder = EKReminder.reminderWithEventStore_(self.store)
        reminder.setTitle_(title)
        reminder.setCalendar_(cal)
        if notes:
            reminder.setNotes_(notes)
        if priority:
            reminder.setPriority_(priority)

        if alarm_time:
            hour, minute = map(int, alarm_time.split(":"))
            now = datetime.now()
            dt = now.replace(hour=hour, minute=minute, second=0)
            if dt < now:
                dt += timedelta(days=1)

            alarm = EKAlarm.alarmWithAbsoluteDate_(NSDate.dateWithTimeIntervalSince1970_(dt.timestamp()))
            reminder.addAlarm_(alarm)

            comp = NSDateComponents.alloc().init()
            comp.setYear_(dt.year)
            comp.setMonth_(dt.month)
            comp.setDay_(dt.day)
            reminder.setDueDateComponents_(comp)

        if repeat_daily:
            rule = EKRecurrenceRule.alloc().initRecurrenceWithFrequency_interval_end_(
                EKRecurrenceFrequencyDaily, 1, None
            )
            reminder.addRecurrenceRule_(rule)

        ok, err = self.store.saveReminder_commit_error_(reminder, True, None)
        if ok:
            rpt = " (每天)" if repeat_daily else ""
            tm = f" @ {alarm_time}" if alarm_time else ""
            print(f"✅ 已创建: {title}{tm}{rpt}")
            return True
        print(f"❌ 创建失败: {title} - {err}")
        return False


def main():
    automation = ReminderAutomation()

    print("🔐 请求权限...")
    if not automation.request_access():
        print("❌ 请在「系统设置 → 隐私与安全性 → 提醒事项」中授权终端")
        sys.exit(1)

    config_json = sys.argv[1] if len(sys.argv) > 1 else sys.stdin.read()
    try:
        config = json.loads(config_json)
    except json.JSONDecodeError as e:
        print(f"❌ 配置格式错误: {e}")
        sys.exit(1)

    calendar_name = config.get("calendar", "每日提醒")
    reminders = config.get("reminders", [])

    print(f"\n📋 列表: {calendar_name}")
    print("-" * 40)

    ok = sum(1 for r in reminders if automation.create_reminder(
        title=r.get("title", ""),
        calendar_name=calendar_name,
        alarm_time=r.get("time"),
        notes=r.get("notes", ""),
        priority=r.get("priority", 0),
        repeat_daily=r.get("repeat_daily", True)
    ))

    print("-" * 40)
    print(f"✅ 完成: {ok}/{len(reminders)}")


if __name__ == "__main__":
    main()
