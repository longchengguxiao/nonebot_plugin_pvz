# nonebot_plugin_pvz

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
您可以通过使用关键字'查看背包'或'我的背包'来查看您的背包,首次查看背包可以获得初始奖励以及注册成为用户

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
## 更新

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
