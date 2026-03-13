# 每日提醒自动化 Skill

## 功能

**完全自动化**的每日提醒系统，支持从模糊想法到具体执行：

```
┌─────────────────────────────────────────────────────────────┐
│  完整流程                                                    │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  方式一：用户已有计划                                        │
│  用户输入完整计划 → AI 解析 → 确认 → 自动执行                 │
│                                                             │
│  方式二：用户只有一个想法（推荐）                             │
│  用户输入想法 → AI 生成计划 → 用户确认 → 自动执行             │
│                                                             │
└─────────────────────────────────────────────────────────────┘
                                                            ↓
                                                    自动创建提醒 + Obsidian 笔记
                                                            ↓
                                                    到点推送通知
                                                            ↓
                                                    勾选完成 → 自动同步
                                                            ↓
                                                    仪表盘统计追踪
```

---

## 🌟 新功能：从想法到计划

### 输入格式（支持两种方式）

#### 方式一：直接输入计划

```
每天 [主题]：
[时间] [任务] - [说明]
...

监控：[监控项]
```

#### 方式二：只输入想法（AI 自动生成计划）

```
我想 [目标]
```

### 示例：从想法到计划

**用户输入：**
```
我想改善睡眠质量
```

**AI 自动生成计划：**

```yaml
主题：睡眠优化执行

时间节点：
  07:00 晨光曝光 - 拉窗帘直视自然光 10 分钟，重置生物钟
  21:00 蓝光阻断 - 开启夜间模式，减少屏幕使用
  22:00 睡前准备 - 调低室温至 18℃，喝温牛奶
  22:30 放松仪式 - 冥想或深呼吸 10 分钟
  23:00 强制断电 - 手机扔出卧室，闭眼

监控项目：
  - 晨光曝光
  - 蓝光阻断
  - 睡前准备
  - 入睡时间
```

**用户确认后自动执行：**
- ✅ 创建 5 个提醒（每天重复）
- ✅ 生成每日执行笔记
- ✅ 创建追踪仪表盘

---

## 📊 需求匹配度

| 需求 | 状态 | 实现方式 |
|------|------|----------|
| 0. 从想法生成计划 | ✅ 100% | AI 自动生成 |
| 1. 解析方案 | ✅ 100% | AI 自动解析 |
| 2. 生成完整方案 | ✅ 100% | AI 自动生成 |
| 3. 展示确认 | ✅ 100% | AI 展示 + 用户确认 |
| 4. 创建提醒 | ✅ 100% | EventKit 自动（带时间+重复） |
| 5. Obsidian 笔记 | ✅ 100% | 脚本自动创建 |
| 6. 仪表盘配置 | ✅ 100% | 脚本自动更新 |
| 7. 推送通知 | ✅ 100% | iPhone/Mac 系统通知 |
| 8. 同步完成 | ✅ 100% | Apple Reminders 插件 |
| 9. 统计追踪 | ✅ 100% | Tracker 插件 |

---

## 🔧 使用的插件

| 插件 | 版本 | 用途 | 状态 |
|------|------|------|------|
| **Apple Reminders** | 2.0.0 | Obsidian 中显示/勾选提醒 | ✅ 已安装 |
| **Tracker** | 1.19.0 | 统计追踪完成情况 | ✅ 已安装 |
| ~~Reminder~~ | ~~1.1.21~~ | ~~已废弃~~ | ❌ 可禁用 |

---

## 使用方法

### 场景一：用户已有完整计划

**输入格式：**
```
每天 [主题]：
[时间] [任务] - [说明]
...

监控：[监控项]
```

**示例：**
```
每天低碳水：
8点 起床喝海盐水 - 提升胰岛素敏感性
12点 午餐顺序欺骗 - 先肉+菜，碳水拖最后
15点 补剂吞服 - 2000mg苏糖酸镁
21点 睡前断电 - 关手机，立刻闭眼

监控：断食、顺序、补剂、睡眠
```

### 场景二：用户只有一个想法

**输入格式：**
```
我想 [目标]
```

**示例输入：**
- `我想改善睡眠`
- `我想减肥`
- `我想养成运动习惯`
- `我想提高工作效率`
- `我想改善皮肤状态`

**AI 自动生成计划，用户确认后执行。**

---

## 自动化流程

### Step 0: AI 生成计划（如果是想法输入）

```yaml
# AI 根据用户想法自动生成
calendar: 睡眠优化执行
reminders:
  - title: "🌅 晨光曝光"
    time: "07:00"
    notes: "拉窗帘直视自然光 10 分钟"
    priority: 1
    repeat_daily: true
  - title: "🌙 蓝光阻断"
    time: "21:00"
    notes: "开启夜间模式，减少屏幕"
    priority: 1
    repeat_daily: true
  # ...

tracking:
  - name: "晨光曝光完成"
    tag: "睡眠/晨光"
  # ...
```

### Step 1: AI 解析输入

```yaml
calendar: 低碳水执行
reminders:
  - title: "🧂 起床喝海盐水"
    time: "08:00"
    notes: "提升胰岛素敏感性"
    priority: 1
    repeat_daily: true
  # ...

tracking:
  - name: "断食完成"
    tag: "低碳水/断食"
  # ...
```

### Step 2: 用户确认

展示方案，用户可调整后确认。

### Step 3: 自动执行

```bash
python3 scripts/automation.py '{"calendar":"低碳水执行","reminders":[...],"tracking":[...]}'
```

**自动完成：**
1. ✅ 创建 Apple 提醒事项（带时间 + 每天重复）
2. ✅ 创建 Obsidian 每日笔记
3. ✅ 更新追踪仪表盘

---

## 文件结构

```
03-daily-reminder-automation/
├── README.md                 # 说明文档
├── SKILL.md                  # 本文件（AI 助手 Skill 定义）
├── scripts/
│   ├── create_reminder.py    # 创建提醒（EventKit）
│   ├── obsidian_updater.py   # 更新 Obsidian
│   └── automation.py         # 完整自动化流程
└── examples/
    └── config.json           # 示例配置

Daily/
├── YYYY-MM-DD.md             # 每日笔记（自动创建）
└── [主题]追踪仪表盘.md        # 仪表盘（自动创建）
```

---

## 技术细节

### EventKit 创建提醒

```python
from EventKit import EKEventStore, EKReminder, EKAlarm, EKRecurrenceRule, EKCalendar

# 请求权限
store.requestAccessToEntityType_completion_(1, handler)

# ⚠️ 创建日历的正确方式（不能直接用 calendarForEntityType_）
cal = EKCalendar.calendarForEntityType_eventStore_(1, store)
cal.setTitle_("列表名称")
cal.setSource_(store.defaultCalendarForNewReminders().source())

# 创建提醒
reminder = EKReminder.reminderWithEventStore_(store)
reminder.setTitle_("任务名称")
reminder.setCalendar_(cal)

# 设置提醒时间
alarm = EKAlarm.alarmWithAbsoluteDate_(nsdate)
reminder.addAlarm_(alarm)

# 设置每天重复
rule = EKRecurrenceRule.alloc().initRecurrenceWithFrequency_interval_end_(
    EKRecurrenceFrequencyDaily, 1, None
)
reminder.addRecurrenceRule_(rule)
```

### ⚠️ EventKit API 常见错误

| 错误写法 | 正确写法 |
|---------|---------|
| `store.calendarForEntityType_(1)` | `EKCalendar.calendarForEntityType_eventStore_(1, store)` |
| `cal.setSource_(None)` | `cal.setSource_(store.defaultCalendarForNewReminders().source())` |

### Tracker 插件正确语法

**❌ 错误写法（会报 "Invalid inputs for label"）：**

```tracker
searchType: tag
searchTarget: 标签1, 标签2
pie:
   label: true  # ❌ 错误
```

**✅ 正确写法：**

```tracker
# 方式1：折线图
searchType: tag
searchTarget: 标签名
folder: Daily
startDate: 2026-03-14
line:
   title: "完成趋势"
   yAxisLabel: 完成次数

# 方式2：汇总统计
searchType: tag
searchTarget: 标签1, 标签2
folder: Daily
startDate: 2026-03-14
summary:
   template: "标签1: {{v0}}次 | 标签2: {{v1}}次"
```

### 优先级映射

| 值 | 含义 | 显示 |
|----|------|------|
| 1 | 高优先级 | !!! |
| 5 | 中优先级 | !! |
| 9 | 低优先级 | ! |
| 0 | 无优先级 | - |

---

## 工作流程示例

### 示例一：从想法开始

```
用户: "我想改善睡眠"
        ↓
AI: 生成睡眠优化方案（展示确认）
        ↓
用户: 确认（或调整）
        ↓
脚本: 自动创建 5 个提醒
      自动创建每日笔记
      自动更新仪表盘
        ↓
每天: iPhone/Mac 弹窗提醒
        ↓
用户: 执行后勾选
        ↓
系统: 自动同步到 Obsidian
        ↓
仪表盘: 实时统计完成情况
```

### 示例二：已有计划

```
用户: "每天低碳水：8点海盐水、12点顺序、21点断电，监控断食和睡眠"
        ↓
AI: 解析生成方案（展示确认）
        ↓
用户: 确认
        ↓
脚本: 自动创建 5 个提醒
      自动创建每日笔记
      自动更新仪表盘
        ↓
每天: iPhone/Mac 弹窗提醒
```

---

## 注意事项

### 权限与同步

1. **首次使用需要授权**：终端需要提醒事项权限
2. **同步延迟**：提醒创建后 1-2 分钟同步到 iPhone
3. **通知权限**：确保系统通知已开启
4. **Apple ID**：iPhone 需登录同一 Apple ID

### 文件位置

| 文件 | 位置 | 用途 |
|------|------|------|
| 每日笔记 | `Daily/YYYY-MM-DD.md` | 今日执行清单 |
| 追踪仪表盘 | `Daily/[主题]追踪仪表盘.md` | 长期统计 |

### Tracker 图表不显示？

1. **需要有数据**：必须先勾选完成任务，Tracker 才能统计
2. **检查标签格式**：确保使用 `#标签名` 格式
3. **检查日期范围**：`startDate` 不能是未来日期

### 依赖安装

```bash
# 检查 EventKit 是否可用
python3 -c "from EventKit import EKEventStore; print('✅ EventKit 可用')"

# 如果不可用，安装 pyobjc
pip3 install pyobjc-framework-EventKit
```
