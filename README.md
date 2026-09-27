# Du_work

个人工程文档与复现脚本归档。目前主要记录 **Ubuntu 22.04 + Unreal Engine 4.26 + CARLA 0.9.15** 的源码编译实践，供以后重装系统、迁移设备或复现开发环境时查阅。

## 文件索引

| 文件 | 用途 | 什么时候使用 |
| --- | --- | --- |
| [docs/CARLA_0.9.15_UE4.26_源码编译全流程.html](docs/CARLA_0.9.15_UE4.26_%E6%BA%90%E7%A0%81%E7%BC%96%E8%AF%91%E5%85%A8%E6%B5%81%E7%A8%8B.html) | 可离线阅读的交互式编译手册：从 GitHub / Epic Games 仓库访问、UE4.26 与 NVIDIA 环境，到 CARLA Assets、Python API、Server、地图与 API 联通验证；包括实际故障和排查方法。 | **先读这份**，按步骤复现完整环境；下载 HTML 后用浏览器打开可使用导航、命令复制和进度标记。 |
| [scripts/Setup_CARLA_0915_final.sh](scripts/Setup_CARLA_0915_final.sh) | 基于 CARLA 0.9.15 的 `Util/BuildTools/Setup.sh` 改写的第三方依赖准备脚本；处理 Boost 1.80.0 下载、本地压缩包优先、B2 bootstrap 使用 GCC、libpng 1.6.37 下载文件名等本次遇到的问题。 | CARLA 0.9.15 源码克隆完成后、执行 `make PythonAPI` **之前**，用于替换源码中的同名脚本。 |

## 推荐使用顺序

1. 阅读 [HTML 编译手册](docs/CARLA_0.9.15_UE4.26_%E6%BA%90%E7%A0%81%E7%BC%96%E8%AF%91%E5%85%A8%E6%B5%81%E7%A8%8B.html)，完成 GPU 驱动、UE4.26、CARLA 0.9.15 源码和 Assets 的准备。
2. 在 CARLA 源码目录中备份原脚本，再用本仓库的修复版替换 `Util/BuildTools/Setup.sh`。下例假设本仓库克隆到 `~/Du_work`、CARLA 源码位于 `~/carla`：

   ```bash
   cd ~/carla
   cp Util/BuildTools/Setup.sh Util/BuildTools/Setup.sh.original
   cp ~/Du_work/scripts/Setup_CARLA_0915_final.sh Util/BuildTools/Setup.sh
   chmod +x Util/BuildTools/Setup.sh
   bash -n Util/BuildTools/Setup.sh
   ```

3. 配置实际的 UE4 路径，再按手册执行：

   ```bash
   export UE4_ROOT="$HOME/UnrealEngine_4.26"
   cd ~/carla
   make PythonAPI
   make launch
   ```

4. 通过生成的 wheel/egg、UE4Editor 启动情况，以及 Python API 对运行中的 CARLA Server 的连接结果分别验收；**`make launch` 退出日志并不能单独证明自定义地图已成功导入并运行**。

## 使用边界

- **HTML 是完整流程指南；Setup.sh 只是第三方依赖构建脚本，不是“一条命令修复所有 CARLA 问题”。**
- 这套记录针对上述版本与本次机器环境；其他 UE/CARLA/Python 版本、下载镜像或代理状态可能需要调整。
- 本仓库中的脚本不是 CARLA 官方发行版；使用前请核对源码版本、备份原文件。建议在独立工作区中验证，不要覆盖其他正在使用的 CARLA 项目。
