# DynamicIP2CF

Dynamically update IP to Cloudflare. 

使用本程序可以实现托管于Cloudflare的DDNS功能。

<link rel="icon" href="res/assets/icon.png">


<div style="margin: auto; text-align: center;">
    <img src="res/assets/icon.png" style="max-width: 50%; max-height: 50%;" alt="DynamicIP2CF Icon.png"/>
</div>

<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
<script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
<script src="docs/js/go_to_top.js"></script>
<link rel="stylesheet" href="docs/css/main.css">

<div class="go-to-top" style="display: none;">
    <i class="fas fa-arrow-up"></i>
</div>

项目地址：[https://github.com/LiuJiewenTT/DynamicIP2CF](https://github.com/LiuJiewenTT/DynamicIP2CF) <br>
项目主页：[https://LiuJiewenTT.github.io/DynamicIP2CF](https://LiuJiewenTT.github.io/DynamicIP2CF) <br>
下载页：[https://github.com/LiuJiewenTT/DynamicIP2CF/releases](https://github.com/LiuJiewenTT/DynamicIP2CF/releases) <br>

<div style="align-items: center; justify-content: center; display: flex; margin: 10px; gap: 10px">
   <img alt="GitHub Downloads (all assets, all releases)" src="https://img.shields.io/github/downloads/LiuJiewenTT/DynamicIP2CF/total">
   <img alt="GitHub Release" src="https://img.shields.io/github/v/release/LiuJiewenTT/DynamicIP2CF">
   <img alt="GitHub Actions Workflow Status" src="https://img.shields.io/github/actions/workflow/status/LiuJiewenTT/DynamicIP2CF/jekyll-gh-pages.yml">
   <img alt="GitHub License" src="https://img.shields.io/github/license/LiuJiewenTT/DynamicIP2CF">
</div>

<div class="quick-navigate">
    <span id="quick-navigate-title">快速访问：<br></span>
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
> 当前程序没有定时执行的功能。



## 使用


## 技术信息

- 程序的基础开发环境为 *Python3.8* ，虚拟环境管理使用 *venv* 。
- 程序使用 *requests* 库来与 *Cloudflare API* 交互，支持通过域名匹配对应的记录而不需要记录ID。
- 程序使用 *Windows* 系统的 *netsh* 命令来获取本机IP地址，并使用 *ipaddress* 库进行IP地址的验证和格式化。
- 程序使用 *argparse* 库来解析命令行参数，优先进入可视化管理模式，并使用 *configparser* 库来管理 `.ini` 配置文件。
- 程序使用 **PySide6** 作为 GUI 库，使用 *QWidgets* 传统方式构建界面，分离qss样式表为文件以遵循更好的开发规范。
- 程序复刻了安卓开发实践中常用的 **声明式资源引用系统** ，并对 *字符串* 类资源添加了 *i18n* 多语言能力支持 和 **分级引用机制** ，并应用了PyCharm的文件监视器器来实现 *基于 mypy 库 stubgen* 的 *字符串资源 pyi* 文件的自动更新。
- 程序使用 **PyInstaller 6** 作为构建工具，并使用 **Runtime Hooks** 添加缺省数据以简化普通用户的操作步骤并优化体验，并使用 *全程 Python* 的策略 实现更高的可定制度并避免命令行指令的调用带来的构建系统复杂度过高问题。

