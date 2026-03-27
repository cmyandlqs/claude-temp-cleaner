# 开发文档（Dev Doc）- Claude Temp Cleaner（PySide6）

## 1. 技术栈
- Python 3.10+
- PySide6（Qt for Python）
- 单文件或小型项目结构（便于打包）

## 2. 模块划分
- UI 模块（界面与交互）
- 扫描模块（遍历与匹配）
- 删除模块（清理与统计）
- 任务线程模块（避免阻塞 UI）
- 数据模型模块（结果列表结构化）

## 3. 界面结构与交互
- 顶部：标题 + “选择文件夹”按钮
- 中部：结果列表（表格）
- 底部：统计信息 + “清理”按钮
- 扫描中状态提示，按钮禁用
- 扫描完成后列表可见，支持选择全部/部分（可选）
- 清理前弹窗确认

## 3.1 mac 风格 UI 与样式说明
目标：简洁、克制、浅色、圆角、轻阴影，强调色统一。

**颜色与主题**
- 背景：#F7F7F8
- 主卡片背景：#FFFFFF
- 主要文本：#1F2328
- 次级文本：#6B7280
- 边框/分割线：#E5E7EB
- 主按钮强调色：#3B82F6（hover：#2563EB）
- 危险操作色（清理按钮）：#EF4444（hover：#DC2626）

**排版与间距**
- 窗口内边距：20px
- 卡片圆角：12px
- 按钮圆角：8px
- 列表行高：28-32px
- 字体：Segoe UI（标题 16px，正文 12-13px）

**阴影与层级**
- 卡片阴影：0 6px 18px rgba(0,0,0,0.08)
- 次级面板阴影：0 2px 6px rgba(0,0,0,0.06)

**控件风格**
- 顶部标题左对齐，右侧操作按钮
- 主按钮填充，次按钮描边
- 列表表头浅灰背景，分割线柔和
- 弹窗确认使用简洁两按钮布局（取消/确认）

**状态与反馈**
- 扫描中：显示进度提示文本 + 旋转指示器
- 扫描完成：显示统计摘要（数量、大小、耗时）
- 删除完成：结果提示 + 失败项列表（可展开）

## 4. 模块接口设计

### 4.1 扫描模块
职责：递归扫描目录，匹配 `tmpclaude-` 前缀并收集信息。

接口：
- `scan(path: str, prefix: str = "tmpclaude-") -> List[Item]`

`Item` 字段：
- `path: str`
- `is_dir: bool`
- `size_bytes: int`
- `mtime: float`

### 4.2 删除模块
职责：删除匹配项并返回统计。

接口：
- `delete(items: List[Item]) -> DeleteResult`

`DeleteResult` 字段：
- `deleted_count: int`
- `failed_count: int`
- `failed_items: List[Item]`
- `total_bytes: int`
- `elapsed_sec: float`

### 4.3 任务线程模块
职责：在后台执行扫描和删除，避免 UI 卡顿。

接口：
- `run_scan_async(path: str, on_progress: Callable, on_finished: Callable)`
- `run_delete_async(items: List[Item], on_progress: Callable, on_finished: Callable)`

### 4.4 UI 模块
职责：响应用户事件、展示列表与统计。

接口（槽函数）：
- `on_choose_folder()`
- `on_scan_started()`
- `on_scan_finished(items: List[Item])`
- `on_delete_clicked()`
- `on_delete_finished(result: DeleteResult)`

### 4.5 数据模型模块
职责：为 Qt 表格提供模型数据。

接口：
- `ResultTableModel(items: List[Item])`

字段映射：
- 路径 / 类型 / 大小 / 修改时间

## 5. 性能与安全策略
- 遍历使用 `os.scandir` 递归以降低系统调用成本。
- 仅对匹配项取大小与修改时间。
- 默认 dry-run（只展示），删除需确认。
- 删除失败不阻断整体流程，失败项记录并提示。

## 6. 错误处理
- 路径不存在：提示后返回
- 无权限：记录为失败项
- 无匹配项：显示“未找到临时文件”

## 7. 输出与统计
- 扫描完成：显示数量、总大小、耗时
- 删除完成：显示删除数量、失败数量、总大小、耗时

## 8. 后续可选扩展
- 过滤条件可配置（自定义前缀）
- 导出扫描结果（CSV/JSON）
- 最近路径历史
