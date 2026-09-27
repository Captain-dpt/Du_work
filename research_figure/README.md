# 科研绘图 / Research Figure

本目录为 **Du_work 智能驾驶 HIL 开发与系统部署** 配套的科研绘图学习资料：用于参考如何把仿真架构、算法流程、实验方案、结果对比等技术内容表达为论文和技术报告中的专业插图。

## 来源与收录方式

| 项目 | 信息 |
| --- | --- |
| 教程名称 | **Happy Figure：AI 科研绘图实战教程** |
| 原仓库 | [datawhalechina/happy-figure](https://github.com/datawhalechina/happy-figure) |
| 原作者/社区 | Datawhale 社区；项目 README 列出张鼎伦（BAIKEMARK）为项目负责人 |
| 上游版本 | 固定到 commit [`71f68ae684be97ddb222f8e84c89fa1368bc1377`](https://github.com/datawhalechina/happy-figure/commit/71f68ae684be97ddb222f8e84c89fa1368bc1377) |
| 原项目协议 | **CC BY-NC-SA 4.0**（署名、非商业性使用、相同方式共享）；参见子模块中的 [LICENSE](happy-figure/LICENSE) |
| 项目状态 | 原 README 标明 Alpha 内测版；章节建设状态以原文为准 |

**重要：这里采用 Git 子模块（submodule），不是声称复制或原创上游的全部内容。** 子模块的项目文件、图片素材、网站源码和许可证仍由上游仓库管理；Du_work 固定其版本并提供清晰的入口。此声明不意味着整个 Du_work 仓库自动改为 CC BY-NC-SA 4.0，原协议适用于所引用的 Happy Figure 内容。

## 目录与文件

```text
research_figure/
├── README.md                # 本项目的索引、用途、来源与下载说明
└── happy-figure/            # 完整上游项目：Git submodule
    ├── README.md            # 原版项目说明与章节目录
    ├── LICENSE              # 原版 CC BY-NC-SA 4.0
    ├── docs/                # VitePress 教程、章节、媒体素材
    │   ├── chapter1/ ... chapter7/
    │   ├── appendix/
    │   ├── media/           # 原项目科研插图示例、截图等
    │   └── .vitepress/      # 网站配置与样式
    ├── package.json
    └── package-lock.json
```

## 如何下载全部教程与图片

**首次克隆**（自动拉取子模块）：

```bash
git clone --recurse-submodules https://github.com/Captain-dpt/Du_work.git
cd Du_work/research_figure/happy-figure
```

**之前已克隆 Du_work**（普通 `git pull` 不等于拉取子模块文件）：

```bash
cd ~/Du_work
git pull
git submodule update --init --recursive
```

在线阅读原作者维护的正式教程：[https://datawhalechina.github.io/happy-figure/](https://datawhalechina.github.io/happy-figure/)

## 学习与使用路线

1. **认知与工具**：`docs/chapter1/`、`docs/chapter2/`；了解科学插图设计原则及 AI 绘图工具。
2. **提示词与跨学科实战**：`docs/chapter3/`、`docs/chapter4/`；将研究对象、方法、输入输出关系转译为可复用绘图提示。
3. **高阶控图与合规**：`docs/chapter5/`、`docs/chapter6/`；学习多步骤编辑、矢量化与科研诚信边界。
4. **速查与参考图**：`docs/appendix/quick-reference.md`、`docs/media/`；理解范例构图与配色，制作自己的 HIL 系统架构图和论文方法图时独立核查技术内容。

上面是**本仓库的使用建议**，不是声称原项目专门面向智能驾驶或已为本项目生成任何论文插图。

## 本地预览原项目网站

上游提供了 VitePress 脚本；请在已安装 Node.js/npm 且已拉取子模块后运行：

```bash
cd ~/Du_work/research_figure/happy-figure
npm ci
npm run docs:dev
```

本目录未修改上游代码，也未在本仓库中验证网站构建。

## 如何同步未来的上游更新

本仓库锁定上述提交，以保证教程与素材可复现。需要更新时，先阅读上游变更、核对许可与文档，然后由维护者显式更新 submodule 指针并提交；不要假设它自动跟随 `main` 分支。

返回 [Du_work 项目总览](../README.md)。
