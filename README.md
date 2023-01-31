<!-- markdownlint-disable MD033 MD041 -->
<p align="center">
  <img src="https://github.com/longchengguxiao/nonebot_plugin_pvz/blob/main/nonebot_plugin_pvz_logo.png" width="200" height="200" alt="nonebot_plugin_pvz">
</p>
<div align="center">

# nonebot_plugin_pvz

<!-- prettier-ignore-start -->
<!-- markdownlint-disable-next-line MD036 -->
_✨ 基于nonebot的植物大战僵尸插件 ✨_
<!-- prettier-ignore-end -->

</div>

<p align="center">
    <a href="https://github.com/longchengguxiao/nonebot_plugin_pvz/blob/main/LICENSE">
    <img src="https://img.shields.io/github/license/longchengguxiao/nonebot_plugin_pvz" alt="license">
    </a>
    <a href="https://pypi.python.org/pypi/nonebot_plugin_pvz">
    <img src="https://img.shields.io/pypi/v/nonebot_plugin_pvz" alt="pypi">
    </a>
    <img src="https://img.shields.io/badge/python-3.8+-blue" alt="python">
</p>

## 说在前面

+ 请插件使用者仔细阅读此文档，尤其是数据的[上传与下载](#数据下载以及上传必看)部分，在更新插件版本之前阅读完成（否则可能会导致数据丢失）

+ 请谨慎利用记事本修改数据保存的文件，这可能会导致插件运行出错

+ 对于插件问题可以提交issue或者pull_requests来进行交流

+ 对于本插件及本人下其他插件感兴趣的朋友可以添加QQ群聊（719392400）来对插件的发展给出建议以及测试

+ **用爱发电，请勿商用**

## 简介

Nonebot2插件，群聊内的植物大战僵尸小游戏，通过签到获得金币，购买植物或僵尸。利用购买的植物填充您的草坪来防守或利用购买的僵尸入侵别人的草坪，吃掉他们的脑子。

## 安装

```buildoutcfg
从 nb_cli 安装
python -m nb_cli plugin install nonebot_plugin_pvz

或从 PyPI 安装
python -m pip install nonebot_plugin_pvz

本地安装

将下载的源文件保存在你环境的\Lib\site-packages目录下使用命令

pip install nonebot_plugin_pvz-1.2.6-py3-none-any.whl 

此处的包名应该替换为你下载的包名
```

## 使用

```buildoutcfg
在bot.py 中添加nonebot.load_plugin("nonebot_plugin_pvz")

以及配置好nonebot_plugin_apscheduler,否则签到任务无法顺利执行
```
配置部分可以参考[nonebot文档](https://v2.nonebot.dev/docs/advanced/scheduler)

## 详细玩法

> 详细用法以及命令信息参见[使用文档](https://longchengguxiao.github.io/plugindoc/#/nonebot_plugin_pvz/README)

## 数据下载以及上传

数据下载和上传仅`SUPERUSER`可以使用，**未设置不可使用**，其命令格式如下

> 下载: 'pvz下载数据', 'pvz数据下载', 'pvz保存数据', 'pvz数据保存'

> 上传: 'pvz上传数据', 'pvz数据上传', 'pvz载入数据', 'pvz数据载入'

## 更新

<details>
<summary>展开/收起</summary>

### v1.2.6

+ 2023/01/31 合并转发优化，优化代码结构

+ 2023/01/31 新增植物阵容评级功能，并且能够在当前所有用户中给出阵容强度排名

+ 2023/01/31 未配适1.2.6以上版本的lawn.txt文件将会自动更新

### v1.2.3

+ 2023/01/28 添加购买限制，每种植物至多购买6个,僵尸至多购买3个

+ 2023/01/28 修复已知反馈问题

### v1.2.2

+ 2023/01/28 修复背包中多个同种植物只能放置一个在草坪上的问题

### v1.2.1

+ 2023/01/27 修改入侵部分的逻辑
  
+ 修复跳跳僵尸的漏洞
    + 修复跳跳僵尸起跳过程中无法受到伤害的问题
    + 修复跳跳僵尸在起跳时无法被高坚果挡下的问题
    + 修复跳跳僵尸起跳过程中生成图片错误的问题
    
+ 2023/01/27 完善配置路径功能，会在插件启动时将文件复制到指定目录

### v1.2.0

+ 2023/01/26 增加数据上传和下载功能，完善帮助

### v1.1.9

+ 2023/01/26 修复同一个植物可以被多次放在草坪上的问题。

### v1.1.6

+ 2023/01/25 解决植物人机训练中keyerror错误，更新文档，添加命令详解

### v1.1.5

+ 2023/01/24 解决由于未在草坪上放置植物而进行植物人机训练时出现的错误

### v1.1.3

+ 2023/01/24 解决由于版本更迭后的state字段类别不是储存数据类别的问题

+ 2023/01/24 解决入侵命令中的log产生WindowPath不能被JSON解析的问题

+ 2023/01/24 优化战斗部分，基于图鉴数据细致战斗。经测试"豌豆射手 vs 铁桶僵尸", "豌豆射手 豌豆射手 vs 铁桶僵尸"，"豌豆射手 豌豆射手 坚果墙 vs 铁桶僵尸"均在游戏战斗结果范围内，优化效果良好。

### v1.1.2 

+ 2023/01/24 字体维护以及event内字段摘取更新

### v1.1.1

+ 2023/01/23 增加签到以及定时器来维护签到

### v1.1.0

+ 2023/01/23 修改错误，补全代码，更换英文，可以正常使用

### v1.0.0

+ 2023/01/22 由nonebot2版本2.0.0a16更新配适到2.0.0rc3，并对代码进行了进一步修饰完善

### v0.9.0

+ 2022/06/14 添加僵尸人机训练和植物人机训练模式

### v0.8.0

+ 2022/06/01 基础代码完成，功能接近完善

</details>

## 自定义配置

```buildoutcfg
对Python编程比较熟悉的使用者可以在 .env 文件中设置PVZ_BASIC_PATH来选择图片输出路径，缓存数据将在第一次搭建运行时复制到指定目录下

默认位置为''，即库的安装位置处，可以在环境中的site-packages中找到。

```

## 特别感谢

插件中所有植物僵尸数据以及图片来源于 **植物大战僵尸吧** 提供的全图鉴中v3.6.0，在此由衷感谢数据支持。
