# DynamicIP2CF

Dynamically update IP to Cloudflare. 

使用本程序可以实现托管于Cloudflare的DDNS功能。

<link rel="icon" href="res/assets/icon.png">


<div style="margin: auto; text-align: center;">
    <img src="res/assets/icon.png" style="max-width: 50%; max-height: 50%;" alt="DynamicIP2CF Icon.png"/>
</div>

<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" >
<script src="https://code.jquery.com/jquery-3.6.0.min.js" ></script>
<script src="docs/js/go_to_top.js" ></script>
<link rel="stylesheet" href="docs/css/main.css" >

<div class="go-to-top" style="display: none;">
    <i class="fas fa-arrow-up"></i>
</div>

项目地址：[https://github.com/LiuJiewenTT/DynamicIP2CF](https://github.com/LiuJiewenTT/DynamicIP2CF) <br>
项目主页：[https://LiuJiewenTT.github.io/DynamicIP2CF](https://LiuJiewenTT.github.io/DynamicIP2CF) <br>
下载页：[https://github.com/LiuJiewenTT/DynamicIP2CF/releases](https://github.com/LiuJiewenTT/DynamicIP2CF/releases) <br>

<div style="align-items: center; justify-content: center; display: flex; margin: 10px; gap: 10px; flex-wrap: wrap;">
   <img alt="GitHub Downloads (all assets, all releases)" src="https://img.shields.io/github/downloads/LiuJiewenTT/DynamicIP2CF/total">
   <img alt="GitHub Release" src="https://img.shields.io/github/v/release/LiuJiewenTT/DynamicIP2CF">
   <img alt="GitHub Repo stars" src="https://img.shields.io/github/stars/LiuJiewenTT/DynamicIP2CF">
   <img alt="GitHub License" src="https://img.shields.io/github/license/LiuJiewenTT/DynamicIP2CF">
</div>

<div class="quick-navigate">
    <span class="quick-navigate-title">快速访问：<br></span>
    <div class="quick-navigate-item-group">
        &nbsp;&nbsp;&nbsp;&nbsp;
        <span class="quick-navigate-item"><a href="#使用">使用</a></span>
        <span class="quick-navigate-item"><a href="#技术信息">技术信息</a></span>
    </div>
</div>



## 介绍

这是一个管理Cloudflare上DNS记录中的IP地址的程序，可以让用户可视化对DNS中的IP地址进行管理，以达成DDNS功能。

程序包含 **CLI** 和 **GUI** 部分，提供三种运行模式：一种命令行自动化，一种命令行交互，还有一种可视化管理。程序默认进入交互模式，并优先进入可视化管理模式。

> [!NOTE]
>
> 当前程序没有定时执行的功能，因为记录不会过时。



## 使用

本程序共3中使用模式：

1. GUI 可视化模式
2. CLI 命令行交互模式
3. CLI 命令行自动化模式

> [!NOTE]
> 
> 此部分内容为面向用户，默认为使用构建成品的入门情景。

### GUI 可视化模式

双击 EXE 程序，稍等片刻，程序将会弹出图形窗口。

### CLI 命令行交互模式

在命令行终端中输入`DynamicIP2CF.exe --cli-mode`即可进入命令行交互模式。

程序启动后，将会逐一提示用户输入DNS记录信息，并执行更新操作。

> [!NOTE]
> 
> 此模式需要手动输入IP地址等与DNS记录和Cloudflare相关信息，命令行传入的相关参数将被忽略，配置文件中的相关信息也会被忽略。

> [!TIP]
> 
> 网络代理设置仍然可以从命令行参数或配置文件中指定。

### CLI 命令行自动化模式

在命令行终端中输入`DynamicIP2CF.exe --cli-mode --cli-automated [params]`即可进入。

可以使用`DynamicIP2CF.exe --generate-config-ini`来生成初始配置文件`config.ini`。

可以使用`DynamicIP2CF.exe --read-config-ini [file]`来指定要读取的配置文件。

可以使用`DynamicIP2CF.exe --help`来查看命令行参数的详细说明。

> [!TIP]
> 
> 此模式下，可以使用配置文件指定DNS记录与Cloudflare相关信息，也可以使用命令行参数指定。从命令行传入的参数具有更高的优先级，将会覆盖加载自配置文件的相关信息。
> 
> 网络代理信息可以从命令行参数或配置文件中指定。

## 技术信息

- 程序的基础开发环境为 *Python3.8* ，虚拟环境管理使用 *venv* （开发环境和构建环境隔离）。
- 程序使用 *requests* 库来与 *Cloudflare API* 交互，支持通过域名匹配对应的记录而不需要指定记录ID。
- 程序使用 *Windows* 系统的 *netsh* 命令来获取本机IP地址，并使用 *ipaddress* 库进行IP地址的验证和格式化。
- 程序使用 *argparse* 库来解析命令行参数，优先进入可视化管理模式，并使用 *configparser* 库来管理 `.ini` 配置文件。
- 程序使用 **PySide6** 作为 GUI 库，使用 *QWidgets* 传统方式构建界面，分离qss样式表为文件以遵循更好的开发规范。
- 程序复刻了安卓开发实践中常用的 **声明式资源引用系统** ，并对 *字符串* 类资源添加了 *i18n* 多语言能力支持 和 **分级引用机制** ，并应用了PyCharm的文件监视器器来实现 *基于 mypy 库 stubgen* 的 *字符串资源 pyi* 文件的自动更新。
- 程序使用 **PyInstaller 6** 作为构建工具，并使用 **Runtime Hooks** 添加缺省数据以简化普通用户的操作步骤并优化体验，并使用 *全程 Python* 的策略 实现更高的可定制度并避免命令行指令的调用带来的构建系统复杂度过高问题。

## 开发

### 配置和准备

开发环境请参照实际情况自行配置，或在构建环境的基础上进行增减配置。推荐安装的库包括：

1. PySide6
2. requests
3. ipaddress
4. argparse
5. configparser
6. mypy

> [!TIP]
> 
> 推荐使用PyCharm作为开发环境，并启用文件监视器器，以便实时更新字符串资源的pyi文件。

构建环境 *build_env_pyinstaller* 设置：

``` cmd
python -m venv build_env_pyinstaller
build_env_pyinstaller\Scripts\activate
pip install -r venv_requirements\build_venv_pyinstaller_requirements.txt
```

### 构建

切换到构建环境，运行PyCharm任务 *build* （对应文件是`.run/build.run.xml`）。

