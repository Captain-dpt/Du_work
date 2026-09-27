# Du_work · 智能驾驶 HIL 开发与系统部署

本仓库用于整理和沉淀 **智能驾驶硬件在环（Hardware-in-the-Loop，HIL）开发、自动驾驶软件裁剪与系统部署** 相关的工程资料，包括环境搭建、系统架构、源码编译、轻量化适配、快速移植和验证流程；同时收录支撑论文与技术报告表达的科研绘图学习资源。

项目思路是将 **仿真开发端** 与 **目标运行端** 分开管理：在开发端构建道路场景和传感器输入、调试自动驾驶算法；在目标环境中围绕实际硬件与赛事需求，保留必要的软件模块、配置与车辆接口，逐步完成从仿真验证到目标设备部署的工程闭环。

## 项目方向

| 方向 | 工作内容 |
| --- | --- |
| **仿真与 HIL 开发** | 基于 CARLA/Unreal Engine 搭建仿真环境，提供地图与传感器输入，为感知、定位、规划、控制等模块提供开发和联调条件。 |
| **自动驾驶系统适配** | 对接 ROS 2 / Autoware 软件链路，关注数据接口、坐标与时间一致性、车辆状态和控制指令的衔接。 |
| **轻量化与模块化** | 面向 AiLabCar 无人车需求整理 Autoware 功能边界、保留/替换/裁剪策略、依赖与接口契约。 |
| **系统部署与复现** | 区分开发工作区与 Runtime 运行环境，归档构建、移植、验证和回滚步骤，便于换机和后续迭代。 |
| **科研绘图与学术可视化** | 归档第三方 AI 科研绘图教程，辅助 HIL 系统架构图、方法流程图和论文插图的表达与复现。 |

> 仓库当前主要归档 **文档、脚本和裁剪清单**；不等于已公开完整 CARLA/Autoware 源码、整车部署包或所有 HIL 实验结果。各项验证状态以对应专项文档及后续实际测试为准。

## 当前归档的三个专项

### 1. [CARLA 0.9.15 · 仿真端源码编译](carla_0.9.15/)

Ubuntu 22.04 + Unreal Engine 4.26 + CARLA 0.9.15 的构建复现资料。记录第三方依赖下载、Boost/libpng 修复、Python API 构建、Server 启动及地图联通验收。

- [项目 README：文件职责与复现入口](carla_0.9.15/README.md)
- [交互式 HTML 源码编译手册](carla_0.9.15/docs/CARLA_0.9.15_UE4.26_%E6%BA%90%E7%A0%81%E7%BC%96%E8%AF%91%E5%85%A8%E6%B5%81%E7%A8%8B.html)
- [第三方依赖修复脚本 Setup.sh](carla_0.9.15/scripts/Setup_CARLA_0915_final.sh)

### 2. [Autoware AiLabCar Lite · 裁剪与部署准备](Autoware_AiLabCar_Lite/)

围绕无人车感知 → 地图/定位 → 规划 → 控制 → 车辆接口的运行闭环，保存系统架构规划、包级裁剪快照，以及快速移植三件套（迁移手册、执行脚本、IGNORE 包名清单）。

- [项目 README：五份文件用途、版本边界与迁移流程](Autoware_AiLabCar_Lite/README.md)
- [AiLabCar Lite 系统规划模板](Autoware_AiLabCar_Lite/Autoware_AiLabCar_Lite_Project_Template%281%29.html)
- [裁剪架构与包级保留/移除视图](Autoware_AiLabCar_Lite/autoware_trim_architecture.html)
- [快速迁移手册](Autoware_AiLabCar_Lite/autoware_lite_trim_playbook.html)

**版本提示：** 规划模板标注 Autoware tag `1.71.2`，快速移植资料标注 `1.7.1`。复现前必须检查目标工作区的 tag/commit、依赖和包列表，不应默认跨版本通用。

### 3. [科研绘图 · Happy Figure 学习资源](research_figure/)

以 Git submodule 收录 Datawhale 社区的 [Happy Figure：AI 科研绘图实战教程](https://github.com/datawhalechina/happy-figure)：包含 AI 科研绘图的认知、工具、提示词工程、跨学科绘图实践、矢量化重构与学术合规内容，作为本项目论文和工程文档配图的学习参考。

- [专属 README：文件用途、来源、许可与完整下载方法](research_figure/README.md)
- [上游 Happy Figure 完整项目（子模块）](research_figure/happy-figure)

**归档方式：** 子模块固定到上游提交 `71f68ae684be97ddb222f8e84c89fa1368bc1377`，并非将全部图片二进制复制进 Du_work 自身的 Git 对象库。普通 `git clone` 后需要执行 `git submodule update --init --recursive`，或者首次使用 `git clone --recurse-submodules`。原项目使用 **CC BY-NC-SA 4.0** 许可，版权与署名仍归原作者及其贡献者。

## 仓库结构

```text
Du_work/
├── README.md
├── .gitmodules
├── carla_0.9.15/
│   ├── README.md
│   ├── docs/
│   │   └── CARLA_0.9.15_UE4.26_源码编译全流程.html
│   └── scripts/
│       └── Setup_CARLA_0915_final.sh
├── Autoware_AiLabCar_Lite/
    ├── README.md
    ├── Autoware_AiLabCar_Lite_Project_Template(1).html
    ├── autoware_trim_architecture.html
    ├── autoware_lite_trim_playbook.html
    ├── apply_lite_trim.py
    └── lite_trim_ignore_packages.txt
└── research_figure/
    ├── README.md
    └── happy-figure/          # Git submodule → datawhalechina/happy-figure
```

## 使用原则

1. **先看专项 README，再执行脚本。** 复现路径、环境要求及各文件职责均放在对应子目录。
2. **开发、部署分离。** 仿真/训练/编译工具与控制器 Runtime 依赖分开考虑。
3. **先备份、先验证、再修改。** 自动裁剪前做 dry-run，保留 Git 回滚点；编译通过不代表车辆功能和安全链路完成验收。
4. **明确版本和边界。** 文件中的软件版本、包数和运行验证结论仅适用于对应记录的工作区与阶段。
5. **区分原创与第三方归档。** 研究绘图教程来自 Datawhale，保留上游链接、原始 LICENSE 和 CC BY-NC-SA 4.0 使用边界；子模块需要显式拉取。
