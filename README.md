# 每日提醒自动化 🍎

> **一句话描述**：告诉 AI 你的每日计划，它自动帮你创建 iPhone/Mac 推送提醒、Obsidian 笔记、完成统计。

[![macOS](https://img.shields.io/badge/platform-macOS-lightgrey)](https://www.apple.com/macos)
[![Python](https://img.shields.io/badge/python-3.8+-blue)](https://www.python.org)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)

---

## 🎯 你能用它做什么？

### 场景一：建立每日健康习惯

```
你输入：
每天低碳水：
8点 晨光曝光 - 拉窗帘直视自然光
12点 午餐顺序 - 先肉后碳水
21点 睡前断电 - 关手机闭眼

你获得：
✅ iPhone 到点自动弹窗提醒
✅ Obsidian 自动生成每日执行清单
✅ 长期统计图表，看到自己的进步
```

### 场景二：执行复杂健康方案

```
你输入：
每天生化重构（从医生/书籍/视频学来的方案）：
08:00 视网膜曝光 - 重置生物钟
10:30 电解质防御 - 心慌时盐温水
11:30 午餐顺序欺骗 - 碳水拖最后
23:00 强制断电 - 吞镁+降温

你获得：
✅ 复杂方案一键自动化执行
✅ 不用记时间，手机提醒你
✅ 每天勾选，养成习惯
```

### 场景三：追踪长期习惯养成

```
你输入：
监控：晨光、断食、睡眠

你获得：
✅ 自动生成追踪仪表盘
✅ 图表展示 30 天完成趋势
✅ 看到「连续执行 15 天」的成就感
```

---

## ✨ 核心效果

| 输入 | 自动输出 |
|------|---------|
| 📝 自然语言描述的每日计划 | 📱 iPhone/Mac 到点推送提醒 |
| 📋 复杂的健康执行方案 | 📝 Obsidian 每日执行清单 |
| 🎯 想追踪的习惯 | 📊 30 天完成趋势图表 |

---

## 🚀 快速开始

### 方式一：AI 助手使用（推荐）

将此 Skill 放到 AI 助手的 Skills 目录下：

| AI 助手 | Skills 目录 |
|---------|------------|
| **CodeBuddy** | `Skills/Skill/03-daily-reminder-automation/` |
| **Claude Code** | `~/.claude/skills/daily-reminder-automation/` |

然后在对话中：

```
你：帮我设置每天低碳水提醒
    8点 晨光曝光 - 拉窗帘直视自然光
    12点 午餐顺序 - 先肉后碳水
    21点 睡前断电 - 关手机闭眼

AI：[自动解析 → 创建提醒 → 生成笔记]
    ✅ 已创建 3 个提醒
    ✅ 已生成每日笔记
    ✅ 已创建追踪仪表盘
```

### 方式二：命令行使用

```bash
# 1. 克隆仓库
git clone https://github.com/your-username/daily-reminder-automation.git
cd daily-reminder-automation

# 2. 安装依赖
pip3 install pyobjc-framework-EventKit

# 3. 运行示例
python3 scripts/create_reminder.py '{
  "calendar": "每日健康",
  "reminders": [
    {"title": "🌅 晨光曝光", "time": "08:00", "notes": "拉开窗帘", "priority": 1, "repeat_daily": true}
  ]
}'
```

---

## 📱 效果演示

### 1. 输入你的计划

```
每天运动：
7点 晨跑 - 30分钟有氧
19点 力量训练 - 20分钟核心

监控：运动、睡眠
```

### 2. 自动创建 iPhone 提醒

| 时间 | 提醒内容 | 重复 |
|------|---------|------|
| 07:00 | 🏃 晨跑 | 每天 |
| 19:00 | 💪 力量训练 | 每天 |

### 3. 自动生成 Obsidian 笔记

```markdown
# 2026-03-13 执行日

## 🔔 每日提醒
> 已自动创建，到点推送 iPhone/Mac 通知

## ✅ 执行记录
- [ ] 晨跑完成 #运动/晨跑
- [ ] 力量训练完成 #运动/力量

## 📊 查看统计
[[运动追踪仪表盘|点击查看仪表盘]]
```

### 4. 自动生成追踪仪表盘

```markdown
# 📊 运动追踪仪表盘

## 📈 本周完成情况
[自动生成的趋势图表]
```

---

## 📁 文件结构

```
daily-reminder-automation/
├── README.md                 # 本文件
├── SKILL.md                  # AI 助手 Skill 定义
├── install.sh                # 一键安装脚本
├── scripts/
│   ├── create_reminder.py    # 创建 Apple 提醒
│   ├── obsidian_updater.py   # 更新 Obsidian 笔记
│   └── automation.py         # 完整自动化流程
└── examples/
    └── config.json           # 示例配置
```

---

## ⚙️ 配置说明

### 提醒参数

| 参数 | 类型 | 说明 |
|------|------|------|
| `title` | string | 提醒标题 |
| `time` | string | 提醒时间 (HH:MM) |
| `notes` | string | 备注 |
| `priority` | int | 优先级 (1=高, 5=中, 9=低) |
| `repeat_daily` | bool | 是否每天重复 |

### 追踪参数

| 参数 | 类型 | 说明 |
|------|------|------|
| `name` | string | 追踪项名称 |
| `tag` | string | Obsidian 标签 |

---

## 🔧 依赖

- **macOS** (EventKit 仅限 macOS)
- **Python 3.8+**
- **pyobjc-framework-EventKit**

```bash
pip3 install pyobjc-framework-EventKit
```

---

## 🔐 权限

首次运行时，macOS 会请求以下权限：

- **提醒事项**：创建和管理提醒
- **终端**：执行脚本

请在「系统设置 → 隐私与安全性」中授权。

---

## 📱 同步

提醒创建后会自动同步到：

- **iPhone**：提醒事项 App（需登录同一 Apple ID）
- **Mac**：提醒事项 App
- **Apple Watch**：提醒事项 Complication

---

## 🤝 适配的 AI 助手

| AI 助手 | 支持状态 | 使用方式 |
|---------|---------|---------|
| **CodeBuddy** | ✅ 完全支持 | 放入 Skills 目录 |
| **Claude Code** | ✅ 完全支持 | 放入 skills 目录 |
| **Cursor** | ✅ 完全支持 | 放入 .cursor/skills/ |
| **命令行** | ✅ 完全支持 | 直接运行脚本 |

---

## 🎁 你将获得

1. **不再忘记执行计划** - iPhone 到点自动提醒
2. **不再手动写笔记** - AI 自动生成每日清单
3. **看到长期进步** - 自动统计图表
4. **养成健康习惯** - 追踪+反馈闭环

---

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

---

## 📄 License

MIT License