# CARLA 0.9.15 · 源码编译与环境复现

本目录是 **智能驾驶 HIL（Hardware-in-the-Loop，硬件在环）开发** 的 CARLA 仿真端资料归档：记录 Ubuntu 22.04 + Unreal Engine 4.26 + CARLA 0.9.15 源码编译和故障修复，以便在开发机重装、迁移或复现实验环境时使用。

> 这里的文件是 **编译手册与修复脚本**，不是 CARLA 完整源码、地图资源包或现成的 HIL 联调部署程序。

## 文件说明

| 文件 | 用途 | 使用时机 |
| --- | --- | --- |
| [docs/CARLA_0.9.15_UE4.26_源码编译全流程.html](docs/CARLA_0.9.15_UE4.26_%E6%BA%90%E7%A0%81%E7%BC%96%E8%AF%91%E5%85%A8%E6%B5%81%E7%A8%8B.html) | **完整操作手册**：GitHub/Epic Games 鉴权、UE4.26、NVIDIA 驱动、CARLA Assets、Python API/Server 构建、地图与 Python API 联通验证；归档这次遇到的错误及解决路径。可下载后离线用浏览器打开。 | 重新搭建 CARLA 仿真开发环境时**从这里开始**。 |
| [scripts/Setup_CARLA_0915_final.sh](scripts/Setup_CARLA_0915_final.sh) | **第三方依赖修复脚本**：CARLA 0.9.15 原 `Util/BuildTools/Setup.sh` 的修改版，针对 Boost 1.80.0 下载、本地缓存优先、Boost B2 的 GCC bootstrap、libpng 1.6.37 下载文件名等问题。 | 克隆 CARLA 0.9.15 源码后、`make PythonAPI` 之前，备份原脚本并替换。 |

## 目录结构

```text
carla_0.9.15/
├── README.md
├── docs/
│   └── CARLA_0.9.15_UE4.26_源码编译全流程.html
└── scripts/
    └── Setup_CARLA_0915_final.sh
```

## 推荐复现流程

1. 阅读 HTML 手册，确认 Ubuntu、GPU 驱动、CARLA-patched UE4.26、CARLA 0.9.15 源码和 Assets 均已准备。
2. 将本目录的修复脚本复制到 CARLA 源码原位置；不要直接运行仓库里的脚本来期望完成所有编译。
3. 按手册构建 Python API，启动编辑器/Server，并分别验证地图加载与 Python API 连接。

假设本仓库克隆在 `~/Du_work`，CARLA 源码在 `~/carla`：

```bash
cd ~/carla
cp Util/BuildTools/Setup.sh Util/BuildTools/Setup.sh.original
cp ~/Du_work/carla_0.9.15/scripts/Setup_CARLA_0915_final.sh Util/BuildTools/Setup.sh
chmod +x Util/BuildTools/Setup.sh
bash -n Util/BuildTools/Setup.sh

export UE4_ROOT="$HOME/UnrealEngine_4.26"
make PythonAPI
make launch
```

## 验收与适用范围

- `make PythonAPI` 成功以及 wheel/egg 生成，**不等于** Server、地图、传感器与 HIL 数据链路已经联通。
- `make launch` 能启动 UE 编辑器后，还应启动仿真，使用 Python API 连接 CARLA Server，检查当前地图、车辆与传感器等。
- `LogExit: Exiting.` 和 `cannot parse georeference` 警告，**不能单独证明自定义地图已导入成功**；涉及 GNSS/地图坐标时还需要核对 georeference。
- 修复脚本只处理这次归档的第三方依赖问题，不负责 GitHub 权限、GPU 驱动、UE4 编译、自定义地图导入或 Autoware 运行问题。跨版本使用前应重新审核。

返回 [Du_work：智能驾驶 HIL 开发与系统部署总览](../README.md)。
