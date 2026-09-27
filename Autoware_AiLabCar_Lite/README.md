# Autoware AiLabCar Lite · 裁剪与快速移植资料

> 本目录存档用户提供的 **Autoware AiLabCar Lite** 规划文档、一次实际裁剪快照，以及用于向另一工作区复现裁剪的三件套。原始五份文件保留原名与内容；此 README 负责解释它们的关系、使用顺序、版本边界和修改风险。

## 一、文件总览

| 文件 | 定位 | 主要内容 |
| --- | --- | --- |
| [Autoware_AiLabCar_Lite_Project_Template(1).html](Autoware_AiLabCar_Lite_Project_Template%281%29.html) | **项目级架构规划 / 设计总览** | 面向无人方程式赛车的系统目标、保留/替换/移除边界、官方节点图裁剪标注、源码功能域划分与 Runtime 模块化部署、接口契约、任务看板、验收指标与风险。文件标注 **Autoware tag 1.71.2、ROS 2 Humble**。 |
| [autoware_trim_architecture.html](autoware_trim_architecture.html) | **实际裁剪结果快照 / 包级可视化** | 按 Sensing、Perception、Localization、Map、Planning、Control 等功能域展示保留与 `COLCON_IGNORE` 包，附裁剪批次和包名搜索；文档标注 `/autoware_1.7.1` 的 2026-09-18 快照。 |
| [autoware_lite_trim_playbook.html](autoware_lite_trim_playbook.html) | **快速移植操作手册** | 如何在另一套 **Autoware 1.7.1 + ROS 2 Humble** 工作区复现这份裁剪：HARD_KEEP、执行顺序、launch/preset 修改、依赖剥离、需要手改的 C++/launch 补丁，以及编译验收。 |
| [apply_lite_trim.py](apply_lite_trim.py) | **执行工具** | 根据清单查找 `src/` 中的 `package.xml`，为命中的包写入 `COLCON_IGNORE`，并从仍编译包的 `package.xml` 移除指向被 IGNORE 包的显式依赖；提供 `--dry-run` 和脚本内 `HARD_KEEP` 保护。**不负责自动应用 C++/launch 补丁。** |
| [lite_trim_ignore_packages.txt](lite_trim_ignore_packages.txt) | **执行输入：包名清单** | 逐行列出 200 个拟 IGNORE 的包名，供 `apply_lite_trim.py --list` 使用。不是执行脚本，也不是最终运行二进制清单。 |

**推荐阅读顺序：** 项目模板（理解目标和边界）→ 裁剪架构图（对照原工作区的结果）→ 迁移手册（确认版本、必保留项和补丁）→ 审核包名清单 → dry-run 脚本 → 正式应用、手工补丁与验证。

## 二、目录结构

```text
Du_work/
└── Autoware_AiLabCar_Lite/
    ├── README.md
    ├── Autoware_AiLabCar_Lite_Project_Template(1).html
    ├── autoware_trim_architecture.html
    ├── autoware_lite_trim_playbook.html
    ├── apply_lite_trim.py
    └── lite_trim_ignore_packages.txt
```

## 三、版本和数据边界（移植前必看）

- **总体设计版本 ≠ 已归档的快速迁移基线。** 项目模板写的是 `tag 1.71.2`；快照、迁移手册和脚本写的是 `1.7.1`。请在实际目标工作区检查 tag/commit、`repositories/autoware.repos`、`src/` 和 `colcon list`，不要直接把 1.7.1 的包清单应用到不同版本。
- **快照统计 ≠ 迁移清单数量。** 架构快照显示约 480 个基线包、292 个当前 `colcon list` 包、196 个已 IGNORE 包；本目录提供的迁移清单为 **200 行包名**。二者属于不同记录/用途，不应直接认定为同一次统计结果；目标树缺失某些包时，执行器会报告 missing。
- **硬保留与旧快照可能有差异。** 迁移手册明确要求保留 `autoware_ndt_scan_matcher` 等硬保留包，脚本也设有自己的 `HARD_KEEP` 集合。以准备复现的目标版本、当前迁移手册以及最终依赖闭包核验为准，不应只按架构图的颜色删除包。
- 该方法属于 **可逆构建排除**：写 `COLCON_IGNORE` 而不是删除源码；但是脚本也会**直接改写仍保留包的 `package.xml`**，回滚这部分需要 Git / 备份，并不能仅靠移除 IGNORE 文件恢复。

## 四、快速移植示例（先演练，后执行）

下例假设本仓库克隆在 `~/Du_work`，目标工作区在 `~/autoware_1.7.1`；根据自己的真实路径调整。**先完整阅读迁移手册的 HARD_KEEP、launch/preset、源码补丁章节。**

```bash
# 1. 准备目标工作区；核对版本与原始状态
cd ~/autoware_1.7.1
git status --short
git describe --tags --always
colcon list --names-only | wc -l

# 2. 将快速移植三件套复制到目标工作区
mkdir -p phase_trim
cp ~/Du_work/Autoware_AiLabCar_Lite/apply_lite_trim.py phase_trim/
cp ~/Du_work/Autoware_AiLabCar_Lite/lite_trim_ignore_packages.txt phase_trim/
cp ~/Du_work/Autoware_AiLabCar_Lite/autoware_lite_trim_playbook.html phase_trim/

# 3. Dry-run：只打印会 IGNORE 哪些包、改哪些 package.xml
python3 phase_trim/apply_lite_trim.py \
  --src src \
  --list phase_trim/lite_trim_ignore_packages.txt \
  --dry-run

# 4. 核对输出和必保留包；备份/提交原工作区后，才正式执行
python3 phase_trim/apply_lite_trim.py \
  --src src \
  --list phase_trim/lite_trim_ignore_packages.txt

# 5. 按迁移手册另外手工应用 launch / preset / C++ 补丁，
#    再检查 colcon list、Git diff 与编译结果
git diff --stat
colcon list --names-only | wc -l
colcon build --symlink-install --cmake-args -DCMAKE_BUILD_TYPE=Release -DBUILD_TESTING=OFF
```

> `--dry-run` 不写入 IGNORE 和 package.xml；正式执行会写入/修改文件。请先创建可回滚的 Git 提交或完整工作区备份，尤其不要对已经承载实车运行的唯一工作区直接操作。

## 五、功能、安全与验收提醒

文档里的裁剪目标涉及定位、感知、实时地图、规划、控制、车辆接口及安全链路。迁移手册中还描述了部分 obstacle stop / cruise / slow-down 等模块被 IGNORE 的方案；这只是原裁剪配置的记录，**不能把“可以编译”视为“可在实车安全运行”**。移植后须依据目标车辆的实际功能需求，复核定位/TF、感知、轨迹、控制门控、紧急停止、故障降级及硬件安全机制，再进行 HIL 和实车验证。

HTML 可以直接下载后在浏览器中打开；三件套按迁移手册的相对路径一起放入同一个 `phase_trim/` 目录即可使用。仓库保留的是流程、源码脚本和清单，**不包含完整 Autoware 源码树、已编译 install/ 或已经验证的实车部署包**。
