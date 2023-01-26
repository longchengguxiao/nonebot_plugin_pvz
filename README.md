<div align="center">

# nonebot_plugin_pvz

<!-- prettier-ignore-start -->
<!-- markdownlint-disable-next-line MD036 -->
_✨ 跨平台 Python 异步机器人框架 ✨_
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


## 简介

Nonebot2插件，群聊内的植物大战僵尸小游戏，通过签到获得金币，购买植物或僵尸。利用购买的植物填充您的草坪来防守或利用购买的僵尸入侵别人的草坪，吃掉他们的脑子。

## 安装

```buildoutcfg
从 nb_cli 安装
python -m nb_cli plugin install nonebot_plugin_pvz

或从 PyPI 安装
python -m pip install nonebot_plugin_pvz

```

## 使用

```buildoutcfg
在bot.py 中添加nonebot.load_plugin("nonebot_plugin_pvz")

以及配置好nonebot_plugin_apscheduler,否则签到任务无法顺利执行

```
配置部分可以参考[nonebot文档](https://v2.nonebot.dev/docs/advanced/scheduler)

## 详细玩法

```buildoutcfg
您可以通过关键字'pvz帮助'或'pvz使用说明'或'pvz使用方法'在QQ内查看帮助文档

通过使用关键字'查看背包'或'我的背包'来查看您的背包,首次查看背包可以获得初始奖励以及注册成为用户

通过关键字'pvz签到'或'植物大战僵尸签到',来获取（签到会自动在每天0点重置）

通过关键字'查看商店',来查看当前售卖的植物或者僵尸及其价格,例如'查看商店 植物'

通过关键字'购买'+名称来购买植物或者僵尸,例如'购买 豌豆射手'

通过关键字'查看图鉴'+名称来查看某种植物或僵尸的具体属性,例如'查看图鉴 豌豆射手'

通过关键字'放置'来将背包内的植物放在草坪上以抵御僵尸的攻势

通过关键字'植物人机训练'来进行模拟入侵

通过关键字'僵尸人机训练'来进行模拟防御

通过'查看草坪'来查看自己的草坪，或者@一个已经开启草坪的玩家来查看他的草坪,例如'查看草坪 @龙城孤笑'

通过'入侵'来操纵你的僵尸摧毁他人的防御,例如'入侵 @龙城孤笑'

总之，在植物大战僵尸的世界中，祝你玩得开心，享受这个过程！

```

## 命令详解

|  命令  |  格式（逗号分割）  |  命令样例（不需要引号）  |  返回和解释  |
|  ----  |  ----  |  ----  |  ----  |
|  签到  | pvz签到，植物大战僵尸签到 | 'pvz签到' | 签到成功，获取100阳光每天（第二天自动重置） |
|  背包  | 查看背包，我的背包 | '查看背包' | 开启背包，注册插件，开启植物大战僵尸之旅，初次开启时会赠送一个豌豆射手，普通僵尸和100阳光 |
|  草坪  | 查看草坪，我的草坪，查看草坪+@ | '查看草坪'或'查看草坪@龙城孤笑' | 开启草坪，可以放置后续的植物已经解锁更多模式。带上@后可以查看被@的人的草坪，如果此人未开启则无法观看 |
|  商店  | 查看商店+空格+植物/僵尸 | '查看商店 植物' | 返回一张图片包含所有的在商店中植物或僵尸价格，需要足够的阳光才可以购买 |
|  图鉴  | 查看图鉴/查询图鉴/图鉴查询+空格+名称 | '查看图鉴 豌豆射手' | 返回一张对应的图片以及植物或僵尸的详细属性介绍，名称可以通过查看商店来获取 |
|  放置  | 放置+空格+植物名称+空格+数字(1-6从左到右) | '放置 豌豆射手 1' | 返回草坪图片，此时豌豆射手被放置在最左侧，只有放置好植物才可以解锁植物人机训练 |
|  入侵  | 入侵+@ | '入侵@龙城孤笑' | 提示选择僵尸阵容，从背包中已有僵尸来选，最多三个，用空格分割。返回一个合并转发文字，包含战斗细节 |
|  植物人机训练  | 植物人机训练+空格+难度 | '植物人机训练 难' | 在已经摆放好植物的你的草坪上进行模拟入侵，僵尸为预设的四个难度，返回一个合并转发文字，包含战斗细节 |
|  僵尸人机训练  | 僵尸人机训练+空格+难度 | '僵尸人机训练 难' | 使用背包中的僵尸来测试僵尸入侵阵容强度，植物为预设的四个难度，返回一个合并转发文字，包含战斗细节 |

## 人机训练难度详解

### 植物人机

> 易："路障僵尸", "普通僵尸", "小鬼僵尸"
> 
> 中："橄榄球僵尸", "铁栅门僵尸", "路障僵尸"
> 
> 难："橄榄球僵尸", "铁栅门僵尸", "铁桶僵尸", "跳跳僵尸"
> 
> 地狱："伽刚特尔", "橄榄球僵尸", "铁栅门僵尸", "小鬼僵尸"

### 僵尸人机

> 易："寒冰射手", "豌豆射手", "空", "空", "空", "空"
> 
> 中："寒冰射手", "豌豆射手", "豌豆射手", "空", "空", "坚果墙"
> 
> 难："寒冰射手", "玉米投手", "双发射手", "空", "空", "高坚果"
> 
> 地狱："冰瓜", "玉米投手", "机枪射手", "火炬", "高坚果", "地刺王"

## 数据下载以及上传（必看！）

数据下载和上传仅`SUPERUSER`可以使用，**未设置不可使用**，其命令格式如下

> 下载: 'pvz下载数据', 'pvz数据下载', 'pvz保存数据', 'pvz数据保存'

> 上传: 'pvz上传数据', 'pvz数据上传', 'pvz载入数据', 'pvz数据载入'

## 更新

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

## 自定义配置

```buildoutcfg
对Python编程比较熟悉的使用者可以在 .env 文件中设置PVZ_BASIC_PATH来选择图片输出路径（以及其他图片路径，请注意设置此选项之后需要重新下载资源，其位于项目/nonebot_plugin_pvz下的font，image以及user_data）

默认位置为''，即库的安装位置处，可以在环境中的site-packages中找到。

```

## 特别感谢

插件中所有植物僵尸数据以及图片来源于 **植物大战僵尸吧** 提供的全图鉴中v3.6.0，在此由衷感谢数据支持。
