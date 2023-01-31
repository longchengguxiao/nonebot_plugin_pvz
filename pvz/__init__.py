# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/01/27
# @Author  : longchengguxiao
# @File    : nonebot_plugin_pvz
# @Version : 3.8.9 Python

from nonebot_plugin_apscheduler import scheduler
from PIL import Image, ImageDraw, ImageFont
from typing import List, Tuple, Union
import numpy as np
from nonebot.typing import T_State
from nonebot.adapters.onebot.v11 import Bot, MessageSegment, MessageEvent, GroupMessageEvent, Message
from nonebot.params import CommandArg, ArgStr
from nonebot import on_command
import nonebot
from nonebot import require
from nonebot.permission import SUPERUSER
from pathlib import Path
from collections import Counter
import json
import asyncio
import os
import shutil
from .config import Config
import random
from nonebot.log import logger

# 启动定时器----------------------------------------------------------------------------


require("nonebot_plugin_apscheduler")

# 文档操作----------------------------------------------------------------------------


def write_data(path: Path, data: list) -> bool:
    try:
        if data:
            flag = 0
            for info in data:
                if flag == 0:
                    with open(path, 'w', encoding='utf-8') as f:
                        f.write(' '.join(info))
                    flag = 1
                elif flag == 1:
                    with open(path, 'a', encoding='utf-8') as f:
                        f.write('\n' + (' '.join(info)))
        else:
            with open(path, 'w') as f:
                f.write('')
        return STATE_OK
    except Exception as e:
        logger.error(e)
        return STATE_ERROR


def read_data(path: Path) -> (bool, list):
    try:
        with open(path, 'r', encoding='utf-8') as f:
            data = f.readlines()
        infos = [x.split() for x in data]

        return STATE_OK, infos
    except Exception as e:
        logger.error(e)
        return STATE_ERROR, []

# 配置地址--------------------------------------------------------------------------------


global_config = nonebot.get_driver().config
pvz_config = Config.parse_obj(global_config.dict())
pvz_basic_path = pvz_config.pvz_basic_path

if pvz_basic_path != Path() and not os.path.exists(
        os.path.join(pvz_basic_path, 'font', 'msyh.ttf')):
    shutil.copytree(
        os.path.join(
            os.path.dirname(
                os.path.abspath(__file__)),
            'font'),
        os.path.join(
            pvz_basic_path,
            'font'),
        dirs_exist_ok=True)
    shutil.copytree(
        os.path.join(
            os.path.dirname(
                os.path.abspath(__file__)),
            'images'),
        os.path.join(
            pvz_basic_path,
            'images'),
        dirs_exist_ok=True)
    shutil.copytree(
        os.path.join(
            os.path.dirname(
                os.path.abspath(__file__)),
            'user_data'),
        os.path.join(
            pvz_basic_path,
            'user_data'),
        dirs_exist_ok=True)

if pvz_basic_path == Path():
    pvz_basic_path = pvz_basic_path / \
        os.path.dirname(os.path.abspath(__file__))


bag_path = pvz_basic_path / "user_data" / "bag.txt"
lawn_path = pvz_basic_path / "user_data" / "lawn.txt"

if os.path.exists(lawn_path):
    flag, users = read_data(lawn_path)
    if len(users[0]) == 2:
        logger.warning("检测到lawn.txt未配适1.2.6及以上版本插件，即将自动更新")
        for i in range(len(users)):
            users[i].append("未定级")
        _ = write_data(lawn_path, users)
        logger.warning("自动更新lawn.txt文件完成，可以正常使用")

FONT_PATH = pvz_basic_path / "font" / "msyh.ttf"

PVZ_IMAGE_PATH = pvz_basic_path / 'images' / 'pvz' / 'base'
PVZ_OUTPUT_PATH = pvz_basic_path / 'images' / 'pvz' / 'output'
PVZ_ORI_PATH = pvz_basic_path / 'images' / 'pvz' / 'ori'


STATE_OK = True
STATE_ERROR = False


# 信息操作----------------------------------------------------------


def get_message_at(data: str) -> List[int]:
    """
    获取消息中所有at对象的qq
    :param data: event.json()
    """
    try:
        qq_list = []
        data = json.loads(data)
        for msg in data["message"]:
            if msg["type"] == "at":
                qq_list.append(int(msg["data"]["qq"]))
        return qq_list
    except KeyError:
        return []


# 定义类------------------------------------------------------------------------------


class Plants():  # 植物类
    """
    hp:耐久度
    damage:伤害
    damage_interval:造成伤害间隔
    price:购买所需要的阳光
    damage_distance:可造成伤害的范围，即攻击距离
    effect:攻击对僵尸的影响，速度与攻击力
    only_night:只在夜晚有效
    penetrable:攻击是否可穿透
    only_hurt_by_boss:只受到伽刚特尔的攻击
    only_hurt_metal:只能够伤害带金属的僵尸
    """

    def __init__(self, plantname: str):
        self.hp = 0
        self.damage = 0
        self.damage_interval = 0
        self.price = 0
        self.damage_distance = [0, 1]
        self.effect = 1
        self.only_night = 0
        self.penetrable = 0
        self.only_hurt_by_boss = 0
        self.only_hurt_metal = 0
        self.unjumpable = 0

        # 豌豆射手
        if plantname == "pea_shooter":
            self.pea_shooter()
        # 坚果墙
        elif plantname == "wall_nut":
            self.wall_nut()
        # 寒冰射手
        elif plantname == "snow_pea":
            self.snow_pea()
        # 大嘴花
        elif plantname == "chomper":
            self.chomper()
        # 双发豌豆
        elif plantname == "repeater":
            self.repeater()
        # 小喷菇
        elif plantname == "puff_shroom":
            self.puff_shroom()
        # 胆小菇
        elif plantname == "scaredy_shroom":
            self.scaredy_shroom()
        # 大喷菇
        elif plantname == "fume_shroom":
            self.fume_shroom()
        # 地刺
        elif plantname == "spikeweed":
            self.spikeweed()
        # 火炬树桩
        elif plantname == "torchwood":
            self.torchwood()
        # 高坚果
        elif plantname == "tall_nut":
            self.tall_nut()
        # 卷心菜投手
        elif plantname == "cabbage_pult":
            self.cabbage_pult()
        # 玉米投手
        elif plantname == "kernet_pult":
            self.kernet_pult()
        # 西瓜投手
        elif plantname == "melon_pult":
            self.melon_pult()
        # 机枪豌豆
        elif plantname == "gatling_pea":
            self.gatling_pea()
        # 石地刺
        elif plantname == "spikerock":
            self.spikerock()
        # 磁力菇
        elif plantname == "magnet_shroom":
            self.magnet_shroom()
        # "冬"瓜
        elif plantname == "winter_melon":
            self.winter_melon()

    def pea_shooter(self):
        """
        豌豆射手
        :return:
        """
        self.hp = 300
        self.damage = 20
        self.damage_interval = 1.5
        self.price = 100
        self.damage_distance = [0, np.inf]
        self.effect = 1
        self.only_night = 0
        self.penetrable = 0
        self.only_hurt_by_boss = 0
        self.only_hurt_metal = 0

    def wall_nut(self):
        """
        坚果墙
        :return:
        """
        self.hp = 1500
        self.damage = 0
        self.damage_interval = 1.5
        self.price = 50
        self.damage_distance = [0, 0]
        self.effect = 1
        self.only_night = 0
        self.penetrable = 0
        self.only_hurt_by_boss = 0
        self.only_hurt_metal = 0

    def snow_pea(self):
        """
        寒冰射手
        :return:
        """
        self.hp = 300
        self.damage = 20
        self.damage_interval = 1.5
        self.price = 175
        self.damage_distance = [0, np.inf]
        self.effect = 0.5
        self.only_night = 0
        self.penetrable = 0
        self.only_hurt_by_boss = 0
        self.only_hurt_metal = 0

    def chomper(self):
        """
        大嘴花
        :return:
        """
        self.hp = 300
        self.damage = 40
        self.damage_interval = 15
        self.price = 150
        self.damage_distance = [0, 1.5]
        self.effect = 1
        self.only_night = 0
        self.penetrable = 0
        self.only_hurt_by_boss = 0
        self.only_hurt_metal = 0

    def repeater(self):
        """
        双发豌豆
        :return:
        """
        self.hp = 300
        self.damage = 40
        self.damage_interval = 1.5
        self.price = 200
        self.damage_distance = [0, np.inf]
        self.effect = 1
        self.only_night = 0
        self.penetrable = 0
        self.only_hurt_by_boss = 0
        self.only_hurt_metal = 0

    def puff_shroom(self):
        """
        小喷菇
        :return:
        """
        self.hp = 300
        self.damage = 20
        self.damage_interval = 1.5
        self.price = 0
        self.damage_distance = [0, 3]
        self.effect = 1
        self.only_night = 1
        self.penetrable = 0
        self.only_hurt_by_boss = 0
        self.only_hurt_metal = 0

    def scaredy_shroom(self):
        """
        胆小菇
        :return:
        """
        self.hp = 300
        self.damage = 20
        self.damage_interval = 1.5
        self.price = 25
        self.damage_distance = [1, np.inf]
        self.effect = 1
        self.only_night = 1
        self.penetrable = 0
        self.only_hurt_by_boss = 0
        self.only_hurt_metal = 0

    def fume_shroom(self):
        """
        大喷菇
        :return:
        """
        self.hp = 300
        self.damage = 20
        self.damage_interval = 1.5
        self.price = 75
        self.damage_distance = [0, 4]
        self.effect = 1
        self.only_night = 1
        self.penetrable = 1
        self.only_hurt_by_boss = 0
        self.only_hurt_metal = 0

    def spikeweed(self):
        """
        地刺
        :return:
        """
        self.hp = 300
        self.damage = 40
        self.damage_interval = 1.5
        self.price = 100
        self.damage_distance = [-0.5, 0.5]
        self.effect = 1
        self.only_night = 0
        self.penetrable = 1
        self.only_hurt_by_boss = 1
        self.only_hurt_metal = 0

    def torchwood(self):
        """
        火炬树桩
        :return:
        """
        self.hp = 300
        self.damage = 0
        self.damage_interval = 1.5
        self.price = 175
        self.damage_distance = [0, np.inf]
        self.effect = 1
        self.only_night = 0
        self.penetrable = 0
        self.only_hurt_by_boss = 0
        self.only_hurt_metal = 0

    def tall_nut(self):
        """
        高坚果
        :return:
        """
        self.hp = 3000
        self.damage = 0
        self.damage_interval = 1.5
        self.price = 125
        self.damage_distance = [0, 0]
        self.effect = 1
        self.only_night = 0
        self.penetrable = 0
        self.only_hurt_by_boss = 0
        self.only_hurt_metal = 0
        self.unjumpable = 1

    def cabbage_pult(self):
        """
        卷心菜投手
        :return:
        """
        self.hp = 300
        self.damage = 40
        self.damage_interval = 3.0
        self.price = 100
        self.damage_distance = [0, np.inf]
        self.effect = 1
        self.only_night = 0
        self.penetrable = 0
        self.only_hurt_by_boss = 0
        self.only_hurt_metal = 0

    def kernet_pult(self):
        """
        玉米投手
        :return:
        """
        self.hp = 300
        self.damage = 26
        self.damage_interval = 3.0
        self.price = 100
        self.damage_distance = [0, np.inf]
        self.effect = 0.4
        self.only_night = 0
        self.penetrable = 0
        self.only_hurt_by_boss = 0
        self.only_hurt_metal = 0

    def gatling_pea(self):
        """
        机枪豌豆
        :return:
        """
        self.hp = 300
        self.damage = 80
        self.damage_interval = 1.5
        self.price = 450
        self.damage_distance = [0, np.inf]
        self.effect = 1
        self.only_night = 0
        self.penetrable = 0
        self.only_hurt_by_boss = 0
        self.only_hurt_metal = 0

    def spikerock(self):
        """
        石地刺
        :return:
        """
        self.hp = 40000
        self.damage = 20
        self.damage_interval = 1
        self.price = 225
        self.damage_distance = [-0.5, 0.5]
        self.effect = 1
        self.only_night = 0
        self.penetrable = 1
        self.only_hurt_by_boss = 1
        self.only_hurt_metal = 0

    def melon_pult(self):
        """
        西瓜投手
        :return:
        """
        self.hp = 300
        self.damage = 80
        self.damage_interval = 1
        self.price = 300
        self.damage_distance = [0, np.inf]
        self.effect = 1
        self.only_night = 0
        self.penetrable = 0
        self.only_hurt_by_boss = 0
        self.only_hurt_metal = 0

    def magnet_shroom(self):
        """
        磁力菇
        :return:
        """
        self.hp = 300
        self.damage = 1100
        self.damage_interval = 15
        self.price = 100
        self.damage_distance = [-np.inf, np.inf]
        self.effect = 1
        self.only_night = 1
        self.penetrable = 0
        self.only_hurt_by_boss = 0
        self.only_hurt_metal = 1

    def winter_melon(self):
        """
        冬瓜
        :return:
        """
        self.hp = 300
        self.damage = 80
        self.damage_interval = 1
        self.price = 500
        self.damage_distance = [-1, 0]
        self.effect = 0.5
        self.only_night = 0
        self.penetrable = 0
        self.only_hurt_by_boss = 0
        self.only_hurt_metal = 0


class Zombie():
    """
    hp:耐久度
    damage:伤害
    damage_interval:造成伤害间隔
    price:购买所需要的阳光
    v:行走速度
    metal:是否带有金属
    jump:是否可以跳跃
    ignore_effect:是否可以忽略影响
    is_gargantuar:是否是伽刚特尔
    """

    def __init__(self, zombiename: str):
        self.hp = 0
        self.damage = 0
        self.v = 0
        self.price = 0
        self.metal = 0
        self.jump = 0
        self.damage_interval = 0
        self.ignore_effect = 0
        self.is_gargantuar = 0

        # 普通僵尸
        if zombiename == "zombie":
            self.normal_zombie()
        # 路障僵尸
        elif zombiename == "conehead_zombie":
            self.conehead_zombie()
        # 撑杆僵尸
        elif zombiename == "buckethead_zombie":
            self.buckethead_zombie()
        # 铁桶僵尸
        elif zombiename == "pole_vaulting_zombie":
            self.pole_vaulting_zombie()
        # 铁栅门僵尸
        elif zombiename == "screen_door_zombie":
            self.screen_door_zombie()
        # 橄榄球僵尸
        elif zombiename == "football_zombie":
            self.football_zombie()
        # 跳跳僵尸
        elif zombiename == "pogo_zombie":
            self.pogo_zombie()
        # 伽刚特尔
        elif zombiename == "gargantuar":
            self.gargantuar()
        # 小鬼僵尸
        elif zombiename == "imp":
            self.imp()

    def normal_zombie(self):
        """
        普通僵尸
        :return:
        """
        self.hp = 270
        self.v = 0.2
        self.damage = 100
        self.price = 50
        self.damage_interval = 1
        self.jump = 0
        self.metal = 0
        self.ignore_effect = 0
        self.is_gargantuar = 0

    def conehead_zombie(self):
        """
        路障僵尸
        :return:
        """
        self.hp = 270 + 370
        self.v = 0.2
        self.damage = 100
        self.price = 75
        self.damage_interval = 1
        self.jump = 0
        self.metal = 0
        self.ignore_effect = 0
        self.is_gargantuar = 0

    def buckethead_zombie(self):
        """
        撑杆僵尸
        :return:
        """
        self.hp = 500
        self.v = 0.4
        self.damage = 100
        self.price = 75
        self.damage_interval = 1
        self.jump = 1
        self.metal = 0
        self.ignore_effect = 0
        self.is_gargantuar = 0

    def pole_vaulting_zombie(self):
        """
        铁桶僵尸
        :return:
        """
        self.hp = 270 + 1100
        self.v = 0.2
        self.damage = 100
        self.price = 125
        self.damage_interval = 1
        self.jump = 0
        self.metal = 1
        self.ignore_effect = 0
        self.is_gargantuar = 0

    def screen_door_zombie(self):
        """
        铁栅门僵尸
        :return:
        """
        self.hp = 270 + 1100
        self.v = 0.2
        self.damage = 100
        self.price = 100
        self.damage_interval = 1
        self.jump = 0
        self.metal = 1
        self.ignore_effect = 1
        self.is_gargantuar = 0

    def football_zombie(self):
        """
        橄榄球僵尸
        :return:
        """
        self.hp = 270 + 1100
        self.v = 0.4
        self.damage = 100
        self.price = 175
        self.damage_interval = 1
        self.jump = 0
        self.metal = 1
        self.ignore_effect = 0
        self.is_gargantuar = 0

    def pogo_zombie(self):
        """
        跳跳僵尸
        :return:
        """
        self.hp = 270 + 230
        self.v = 0.5
        self.damage = 100
        self.price = 75
        self.damage_interval = 1
        self.jump = 1
        self.metal = 1
        self.ignore_effect = 0
        self.is_gargantuar = 0

    def gargantuar(self):
        """
        伽刚特尔
        :return:
        """
        self.hp = 3000
        self.v = 0.2
        self.damage = 10000
        self.price = 300
        self.damage_interval = 2
        self.jump = 0
        self.metal = 0
        self.ignore_effect = 0
        self.is_gargantuar = 1

    def imp(self):
        """
        小鬼僵尸
        :return:
        """
        self.hp = 270
        self.v = 0.25
        self.damage = 100
        self.price = 50
        self.damage_interval = 0.75
        self.jump = 0
        self.metal = 0
        self.ignore_effect = 0
        self.is_gargantuar = 0


# 获取损失的hp------------------------------------------------------------------------------
def get_hp_down(
        zombie: Zombie,
        plants: List[Plants],
        time: float,
        dist: float,
        plant_pos: List[float]) -> float:
    # 最终返回的损失血量
    ans = 0
    # 对每一个植物都进行判断
    for plant in plants:
        if plant.only_hurt_metal and zombie.metal:
            ans += plant.damage
            zombie.metal = 0
            continue
        if time / plant.damage_interval == int(time / plant.damage_interval) and (
                plant.damage_distance)[0] < dist - plant_pos[plants.index(plant)] < plant.damage_distance[1]:
            ans += plant.damage
    return ans


# 绘制图片---------------------------------------------------------------------------


def lawn_pic(plantname: List[str], cnt: int = 0):
    if not os.path.exists(PVZ_OUTPUT_PATH):
        os.makedirs(PVZ_OUTPUT_PATH)
    if not os.path.exists(PVZ_IMAGE_PATH):
        os.makedirs(PVZ_IMAGE_PATH)
    base_img = Image.open(Path(PVZ_IMAGE_PATH, "lawn.png")).convert("RGBA")
    for i in range(len(plantname)):
        if plantname[i] == "0":
            continue
        box = (0 + 250 * i, 0, 250 + 250 * i, 500)

        tmp_img = Image.open(
            Path(
                PVZ_IMAGE_PATH,
                f"{plantname[i]}.png"))
        region = tmp_img.crop((835, 290, 1085, 790))
        base_img.paste(region, box, region)
    base_img.save(Path(PVZ_OUTPUT_PATH, f"output{cnt}.png"))


def zombie_pic(zombiename: str, dist: float, cnt: int = 0):
    if not os.path.exists(PVZ_OUTPUT_PATH):
        os.makedirs(PVZ_OUTPUT_PATH)

    base_img = Image.open(
        Path(
            PVZ_OUTPUT_PATH,
            f"output{cnt}.png")).convert("RGBA")
    box = (int(0 + 250 * dist), 0, int(250 + 250 * dist), 500)
    tmp_img = Image.open(Path(PVZ_IMAGE_PATH, f"{zombiename}.png"))
    region = tmp_img.crop((835, 290, 1085, 790))
    base_img.paste(region, box, region)
    base_img.save(Path(PVZ_OUTPUT_PATH, f"output_new{cnt}.png"))


def draw_test(text: str, color: Tuple, save_path: Path, fontpath: Path):
    if not os.path.exists(PVZ_OUTPUT_PATH):
        os.makedirs(PVZ_OUTPUT_PATH)
    img = Image.new("RGBA", (1080, 2400), color)
    draw = ImageDraw.Draw(img)

    font = ImageFont.truetype(font=str(fontpath), size=26)

    # 参数：位置、文本、填充、字体
    draw.text(xy=(100, 150), text=text, fill=(0, 0, 0), font=font)
    img.save(save_path)


# 入侵流程-----------------------------------------------------------------


def one_by_one(team: List[str], plants: List[str]
               ) -> (List[MessageSegment], int):
    if not os.path.exists(PVZ_OUTPUT_PATH):
        os.makedirs(PVZ_OUTPUT_PATH)
    # 或去当前全部植物的对象
    lawn_plants = [Plants(all_plants[plant])
                   for plant in plants if plant != "0"]
    # 判断是否胜利
    iswin = 0
    # 生成图片计数
    cnt = 0
    # 僵尸序号
    zcnt = 0
    # 入侵日志
    log = []
    log.append(MessageSegment.text("入！侵！开始！"))
    for zombie in team:
        # 全局时间
        time = 0
        # 僵尸序号+1
        zcnt += 1
        # 初始生成位置不变
        dist = 8
        # 获取现有每个植物的位置
        plant_pos = [
            0.5 +
            i for i in range(
                len(lawn_plants)) if lawn_plants[i].hp > 0]
        # 获取僵尸对象
        zb = Zombie(all_zombie[zombie])
        # 战斗是否开始，即僵尸是否会攻击植物
        fight_cond = 0
        # 每次开始到当前的战斗时间
        fight_time = 0
        # 在僵尸的两次攻击间隔内，植物造成的伤害
        all_damage = 0
        # 生成图片，写入日志
        lawn_pic([all_plants[x] for x in plants if x != "0"], cnt)
        zombie_pic(all_zombie[zombie], dist, cnt)
        log.append(
            MessageSegment.text("当前双方阵容") +
            MessageSegment.image(f"file:///{PVZ_OUTPUT_PATH}/output_new{cnt}.png"))
        # 图片计数序号递增
        cnt += 1
        # 当前僵尸循环，当僵尸死亡后退出，每次循环经过0.5秒
        while zb.hp > all_damage:
            # 计算当前僵尸距每个植物的距离
            distance = [dist - pos for pos in plant_pos if pos < dist]
            if not distance:
                iswin = 1
                break
            # 以0.5为僵尸的攻击距离
            if min(distance) > 0.5 or (lawn_plants[distance.index(
                    min(distance))].only_hurt_by_boss == 1 and zb.is_gargantuar == 0):
                # 此时僵尸攻击不到植物，仅植物攻击僵尸
                # 距离递减
                dist -= zb.v * 0.5
                # 计算植物伤害
                damage = get_hp_down(
                    zb, lawn_plants, time, dist, plant_pos)

                # 不扣除僵尸血量，转而比较僵尸的血量与总伤害
                # # 扣除僵尸血量
                # zb.hp -= damage
                # 设置战斗状态
                fight_cond = 0
                # 记录总伤害，便于打印日志
                all_damage += damage
            else:
                # 此时植物和僵尸可以互相攻击
                # 当前目标植物
                tar = distance.index(min(distance))
                # 变成战斗状态
                if fight_cond == 0:
                    fight_time = 0
                    fight_cond = 1
                    # 生成图片，打印日志
                    lawn_pic([all_plants[x] for x in plants if x != "0"], cnt)
                    zombie_pic(all_zombie[zombie], dist, cnt)
                    log.append(MessageSegment.image(
                        f"file:///{PVZ_OUTPUT_PATH}/output_new{cnt}.png"))
                    cnt += 1
                else:
                    fight_time += 0.5
                # 判断僵尸是否可以跳过植物
                if zb.jump:
                    if lawn_plants[tar].unjumpable == 1:
                        zb.jump = 0
                        zb.v = zb.v / 2
                        log.append(
                            MessageSegment.text(f"时间{time},{zombie}被高坚果阻挡后无法起跳，撑杆掉落，速度减半"))
                    else:
                        # 距离递减
                        dist -= 1
                        # 生成图片
                        lawn_pic([all_plants[x]
                                 for x in plants if x != "0"], cnt)
                        zombie_pic(all_zombie[zombie], dist, cnt)
                        # 如果是跳跳僵尸则不会失去下一次跳跃的功能
                        if zb.v == 0.4:
                            zb.jump = 0
                            zb.v = 0.2
                            log.append(
                                MessageSegment.text(f"时间{time},{zombie}被植物阻挡后起跳，撑杆掉落，速度减半") +
                                MessageSegment.image(f"file:///{PVZ_OUTPUT_PATH}/output_new{cnt}.png"))
                        else:
                            # 如果是跳跳僵尸，则可以继续跳过，同时失去攻击机会
                            log.append(
                                MessageSegment.text(f"时间{time},{zombie}被植物阻挡后起跳,同时企图继续跳过其他植物") +
                                MessageSegment.image(f"file:///{PVZ_OUTPUT_PATH}/output_new{cnt}.png"))
                        cnt += 1
                    # 判断当前目标
                    if tar > 0:
                        lawn_plants[tar - 1].hp -= zb.damage
                        log.append(
                            MessageSegment.text(f"时间{time},{zombie}对{plants[tar]}造成{zb.damage}点伤害"))
                        if lawn_plants[tar - 1].hp < 0:
                            log.append(
                                MessageSegment.text(f"时间{time},{plants[tar - 1]}被击败移出"))
                            lawn_plants.pop(tar - 1)
                            plant_pos.pop(tar - 1)
                            plants.pop(tar - 1)
                    # 如果没有植物则判断为胜利
                    else:
                        iswin = 1
                        break
                # 判断伤害
                damage = get_hp_down(
                    zb, lawn_plants, time, dist, plant_pos)
                # zb.hp -= damage
                all_damage += damage
                # 判断当前时间节点僵尸会不会进行攻击
                if fight_time / \
                        zb.damage_interval == int(fight_time / zb.damage_interval):
                    # 对当前目标植物的HP进行削减
                    if lawn_plants[tar].only_hurt_by_boss == 0 or (
                            lawn_plants[tar].only_hurt_by_boss == 1 and zb.is_gargantuar == 1):
                        lawn_plants[tar].hp -= zb.damage
                        log.append(MessageSegment.text(
                            f"时间{time},{zombie}对{plants[tar]}造成{zb.damage if zb.jump == 0 else 0}点伤害。两次攻击间植物合计对{zombie}造成{all_damage}点伤害,{zombie}剩余血量为{zb.hp - all_damage}"))
                        # 如果当前目标植物的耐久度小于0，则移除该植物
                        if lawn_plants[tar].hp < 0:
                            log.append(
                                MessageSegment.text(f"时间{time},{plants[tar]}被击败移出"))
                            # 移除植物
                            lawn_plants.pop(tar)
                            plant_pos.pop(tar)
                            plants.pop(tar)
                            # 判断游戏是否结束
                            if tar == 0:
                                iswin = 1
                                break
                        # all_damage = 0
            # 总体时间递增
            time += 0.5
        # 判断游戏是否结束
        if iswin != 1 and zcnt == len(team):
            iswin = 2
        if iswin == 1:
            log.append(MessageSegment.text(f"入侵成功！成功吃掉对方脑子！") +
                       MessageSegment.image(f"file:///{PVZ_ORI_PATH}/end.jpg"))
            break
        elif iswin == 2:
            log.append(MessageSegment.text(f"僵尸{zombie}被击败，所有僵尸均死去,入侵结束"))
        elif iswin == 0:
            log.append(MessageSegment.text(f"{zombie}终于不堪重负被击败，但入侵仍在继续"))

    return log, iswin


# 初始化全局变量-------------------------------------------------------------------------


now_env = "白天"

all_plants = {
    "豌豆射手": "pea_shooter",
    "坚果墙": "wall_nut",
    "寒冰射手": "snow_pea",
    "食人花": "chomper",
    "双发射手": "repeater",
    "小喷菇": "puff_shroom",
    "胆小菇": "scaredy_shroom",
    "大喷菇": "fume_shroom",
    "地刺": "spikeweed",
    "火炬树桩": "torchwood",
    "高坚果": "tall_nut",
    "卷心菜投手": "cabbage_pult",
    "玉米投手": "kernet_pult",
    "西瓜投手": "melon_pult",
    "机枪豌豆": "gatling_pea",
    "地刺王": "spikerock",
    "磁力菇": "magnet_shroom",
    "冰瓜": "winter_melon"
}
plants_price = [
    100,
    50,
    175,
    150,
    200,
    0,
    25,
    75,
    100,
    175,
    125,
    100,
    100,
    300,
    450,
    225,
    100,
    500]
all_zombie = {
    "普通僵尸": "zombie",
    "路障僵尸": "conehead_zombie",
    "撑杆僵尸": "buckethead_zombie",
    "铁桶僵尸": "pole_vaulting_zombie",
    "铁栅门僵尸": "screen_door_zombie",
    "橄榄球僵尸": "football_zombie",
    "跳跳僵尸": "pogo_zombie",
    "伽刚特尔": "gargantuar",
    "小鬼僵尸": "imp"
}
zombie_price = [50, 75, 75, 125, 100, 175, 150, 300, 50]

# 初始化命令----------------------------------------------------------------------------

pvz_signin = on_command("pvz签到", block=True, priority=5, aliases={"植物大战僵尸签到"})
look_bag = on_command("查看背包", block=True, priority=5, aliases={"我的背包"})
look_lawn = on_command("查看草坪", block=True, priority=5, aliases={"我的草坪"})
look_shop = on_command("查看商店", block=True, priority=5)
look_pvz = on_command("查看图鉴", aliases={"查询图鉴", "图鉴查询"}, block=True, priority=5)
buy = on_command("购买", priority=5, block=True)
put_on_lawn = on_command("放置", block=True, priority=5)
play_with_computer_zombie = on_command("植物人机训练", block=True, priority=5)
play_with_computer_plant = on_command(
    "僵尸人机训练", block=True, priority=5, aliases={"我是僵尸"})
_help = on_command(
    "植物大战僵尸帮助",
    aliases={
        "pvz帮助",
        "pvz使用说明",
        "pvz使用方法"},
    priority=5,
    block=True)
fight = on_command("入侵", priority=5, block=True)

download_data = on_command(
    "pvz下载数据",
    priority=5,
    block=True,
    permission=SUPERUSER,
    aliases={
        "pvz保存数据",
        "pvz数据保存",
        "pvz数据下载"})
upload_data = on_command(
    "pvz载入数据",
    priority=5,
    block=True,
    permission=SUPERUSER,
    aliases={
        "pvz上传数据",
        "pvz数据载入",
        "pvz数据上传"})

lawn_evaluation = on_command("阵容评估",aliases={"植物阵容评估", "战力评估", "阵容评级", "阵容定级", "战力定级"}, priority=5, block=True)

# pvz签到-----------------------------------------------------------------------------


@pvz_signin.handle()
async def _(event: MessageEvent):
    flag, users = read_data(Path(bag_path))
    users_id = [x[0] for x in users]
    user_id = str(event.user_id)
    if user_id in users_id:
        if users[users_id.index(user_id)][4] == "0":
            users[users_id.index(user_id)][3] = str(int(
                users[users_id.index(user_id)][3]) + 100 * (1 + 0.5 * random.randrange(-1, 1)))
            users[users_id.index(user_id)][4] = "1"
            _ = write_data(Path(bag_path), users)
            msg = "今天获得了100阳光，已经放入您的背包"
        else:
            msg = "贪心的人是不会有好运的哦...您今天已经签到过啦！"
    else:
        msg = "您暂未注册植物大战僵尸功能，可以通过“查看背包”或“我的背包”来进行注册"
    await pvz_signin.finish(msg, at_sender=True)


# 查看背包-----------------------------------------------------------------------------


@look_bag.handle()
async def _(event: MessageEvent):
    # 读取现有数据
    flag, users = read_data(Path(bag_path))
    users_id = [x[0] for x in users]
    user_id = str(event.user_id)
    # 判断用户
    if user_id in users_id:
        _, plants, zombies, sunshine, _ = users[users_id.index(user_id)]
        res = ""
        if plants == "0":
            res += "您暂未有任何植物储存，可以去查看商店购买"
        else:
            plants = plants.split(",")
            res += "您目前有植物:\n"
            result = dict(Counter(plants))
            for plant, num in result.items():
                res += f"{plant}*{num}, "
            res += "\n**********\n"
        if zombies == "0":
            res += "您暂未有任何僵尸储存，可以去查看商店购买"
        else:
            zombies = zombies.split(",")
            res += "您目前有僵尸:\n"
            result = dict(Counter(zombies))
            for zombies, num in result.items():
                res += f"{zombies}*{num}, "
            res += "\n**********\n"
        if sunshine == "0":
            res += "目前您没有任何阳光，可以通过签到获得"
        else:
            res += f"目前您有阳光{sunshine},可以查看商店来购买植物或者僵尸哦"
        await asyncio.sleep(1)
        await look_bag.finish(res, at_sender=True)
    else:
        # 储存格式为 user_id 拥有植物 拥有僵尸 拥有阳光 是否签到
        users.append([user_id, "豌豆射手", "普通僵尸", "100", "1"])
        flag = write_data(Path(bag_path), users)
        await asyncio.sleep(1)
        if flag:
            await look_bag.finish("恭喜您第一次开启背包，自动赠送一个豌豆射手和普通僵尸，可以通过签到来获取每天的100阳光哦", at_sender=True)
        else:
            await look_bag.finish("写入文件出错，请联系管理员")


# 查看草坪-----------------------------------------------------------------------------


@look_lawn.handle()
async def _(event: MessageEvent):
    if not os.path.exists(PVZ_OUTPUT_PATH):
        os.makedirs(PVZ_OUTPUT_PATH)
    # 读取现有数据
    flag, users = read_data(Path(lawn_path))
    users_id = [x[0] for x in users]
    # 是否有@群成员
    at_qid = get_message_at(event.json())
    if at_qid:
        user_id = str(at_qid[0])
        if user_id in users_id:
            _, lawn_plants, level = users[users_id.index(user_id)]
            lawn_plants = lawn_plants.split(",")
            res = "当前他的草坪布置:\n"
            for i in range(len(lawn_plants)):
                if lawn_plants[i] == "0":
                    res += f"位置{i + 1}:空\n"
                else:
                    res += f"位置{i + 1}:{lawn_plants[i]}\n"
            res += "**********\n实际的布置位置的序号从左到右为1,2,3,4,5,6,即僵尸会有限攻击6号位植物\n"
            if level == "未定级":
                res += "当前草坪未定级，可以使用命令'阵容评估'给草坪定级，并且查看当前用户中的排名"
            else:
                res += f"当前草坪被定为{level}级"
            # 生成草坪图片
            lawn_pic([all_plants[x] for x in lawn_plants if x != "0"])
            img = MessageSegment.image(
                "file:///" / PVZ_OUTPUT_PATH / "output0.png")
            res = MessageSegment.text(res) + img
            await asyncio.sleep(1)
            await look_lawn.finish(res, at_sender=True)
        else:
            await asyncio.sleep(1)
            await look_lawn.finish("对方暂未布置草坪", at_sender=True)
    else:
        user_id = str(event.user_id)
        if user_id in users_id:
            _, lawn_plants, level = users[users_id.index(user_id)]
            lawn_plants = lawn_plants.split(",")
            res = "当前您的草坪布置:\n"
            for i in range(len(lawn_plants)):
                if lawn_plants[i] == "0":
                    res += f"位置{i + 1}:空\n"
                else:
                    res += f"位置{i + 1}:{lawn_plants[i]}\n"
            res += "**********\n实际的布置位置的序号从左到右为1,2,3,4,5,6,即僵尸会优先攻击6号位植物\n"
            if level == "未定级":
                res += "您当前草坪未定级，可以使用命令'阵容评估'给草坪顶级，并且查看当前用户中的排名"
            else:
                res += f"当前草坪被定为{level}级"
            # 生成草坪图片
            lawn_pic([all_plants[x] for x in lawn_plants if x != "0"])
            img = MessageSegment.image(
                "file:///" / PVZ_OUTPUT_PATH / "output0.png")
            res = MessageSegment.text(res) + img
            await asyncio.sleep(1)
            await look_lawn.finish(res, at_sender=True)
        else:
            users.append([user_id, "0,0,0,0,0,0", "未定级"])
            flag = write_data(Path(lawn_path), users)
            if flag:
                await asyncio.sleep(1)
                await look_lawn.finish("恭喜您第一次开启草坪，目前您的草坪是空的。您可以通过放置来将背包中的植物放在草坪上", at_sender=True)
            else:
                await asyncio.sleep(1)
                await look_lawn.finish("写入文件出错，请联系管理员")


# 查看商店-----------------------------------------------------------------------------


@look_shop.handle()
async def _(state: T_State, args: Message = CommandArg()):
    msg = args.extract_plain_text().strip()
    if msg and ((msg == "植物") or (msg == "僵尸")):
        state["cate"] = msg


@look_shop.got("cate", prompt="您想要查看植物还是僵尸?")
async def _(state: T_State, cate: str = ArgStr("cate")):
    res = ""
    if cate in ["取消", "算了"]:
        await asyncio.sleep(1)
        await look_shop.finish("已取消操作...")
    if cate == "植物":
        res += "当前在售的植物有：\n"
        for i in range(len(all_plants.items())):
            res += f"{i + 1}.{list(all_plants.keys())[i]}的售价为{plants_price[i]};\n"
        res += "可以通过关键字'购买'+名称来购买植物"
        draw_test(
            res, (255, 255, 153), Path(
                PVZ_OUTPUT_PATH, "plant_store.png"), Path(FONT_PATH))
        await asyncio.sleep(1)
        await look_shop.finish(MessageSegment.image("file:///" / PVZ_OUTPUT_PATH / "plant_store.png"), at_sender=True)
    elif cate == "僵尸":
        res += "当前在售的僵尸为：\n"
        for i in range(len(all_zombie.items())):
            res += f"{i + 1}.{list(all_zombie.keys())[i]}的售价为{zombie_price[i]};\n"
        res += "可以通过关键字'购买'+名称来购买僵尸"
        draw_test(
            res, (255, 255, 153), Path(
                PVZ_OUTPUT_PATH, "zombie_store.png"), Path(FONT_PATH))
        await asyncio.sleep(1)
        await look_shop.finish(MessageSegment.image("file:///" / PVZ_OUTPUT_PATH / "zombie_store.png"), at_sender=True)
    else:
        await asyncio.sleep(1)
        await look_shop.finish("输入无效，请输入植物或僵尸", at_sender=True)


# 查看图鉴-----------------------------------------------------------------------------


@look_pvz.handle()
async def _(state: T_State, args: Message = CommandArg()):
    msg = args.extract_plain_text().strip()
    if msg and (
            (msg in list(
                all_plants.keys())) or (
                    msg in list(
                        all_zombie.keys()))):
        # 如果附加了所要查看的图鉴则不需要询问
        state["cate"] = msg


@look_pvz.got("cate", prompt="您想要查看哪种植物或者僵尸?如果不知道都有那些名字可以通过'查看商店'来查看")
async def _(state: T_State, cate: str = ArgStr("cate")):
    res = ""
    if cate in ["取消", "算了"]:
        await asyncio.sleep(1)
        await look_pvz.finish("已取消操作...")
    if cate in list(all_plants.keys()):
        res += f"{cate}的属性如下:\n"
        plt = Plants(all_plants[cate])
        res += f"生命值为{plt.hp}\n"
        res += f"伤害为{plt.damage}/{plt.damage_interval}s\n"
        res += f"攻击距离为({plt.damage_distance[0]}, {12 if plt.damage_distance[1] == np.inf else plt.damage_distance[1]})\n"
        res += f"攻击使僵尸的属性为先前的{plt.effect}\n"
        if plt.penetrable:
            res += f"此植物的攻击有穿透效果\n"
        if plt.only_night:
            res += f"此为夜间植物，目前环境为{now_env}\n"
        if plt.only_hurt_metal:
            res += f"此植物仅伤害带有金属的僵尸\n"
        if plt.only_hurt_by_boss:
            res += f"此植物仅被伽刚特尔伤害\n"
        res += f"购买需要阳光{plt.price}"
        img = MessageSegment.image(
            "file:///" / PVZ_ORI_PATH / f"{all_plants[cate]}.jpg")
        res = MessageSegment.text(res) + img
    elif cate in list(all_zombie.keys()):
        res += f"{cate}的属性如下:\n"
        zomb = Zombie(all_zombie[cate])
        res += f"生命值为{zomb.hp}\n"
        res += f"伤害为{zomb.damage}/{zomb.damage_interval}s\n"
        res += f"移动速度为{zomb.v}格/s\n"
        if zomb.metal:
            res += f"该僵尸携带金属\n"
        if zomb.jump:
            res += "该僵尸可以越过遇到的第一个植物\n"
        if zomb.ignore_effect:
            res += "该僵尸可以忽视植物攻击带来的效果削弱\n"
        res += f"购买需要阳光{zomb.price}"
        img = MessageSegment.image(
            "file:///" / PVZ_ORI_PATH / f"{all_zombie[cate]}.jpg")
        res = MessageSegment.text(res) + img
    else:
        res += "不合法输入，可以通过'查看商店'来查询支持的植物或僵尸"
    await asyncio.sleep(1)
    await look_pvz.finish(res, at_sender=True)


# 购买--------------------------------------------------------------------------------


@buy.handle()
async def _(event: MessageEvent, state: T_State, args: Message = CommandArg()):
    # 获取背包数据
    flag, users = read_data(Path(bag_path))
    users_id = [x[0] for x in users]
    user_id = str(event.user_id)
    if user_id in users_id:
        _, state["plants"], state["zombies"], state["sunshine"], _ = users[users_id.index(
            user_id)]
        state["users"] = users
        state["index"] = users_id.index(user_id)
        msg = args.extract_plain_text().strip()
        if msg and (
                (msg in list(
                    all_plants.keys())) or (
                        msg in list(
                            all_zombie.keys()))):
            # 如果附加了所要购买的植物或者僵尸则不需要询问
            state["cate"] = msg
    else:
        await asyncio.sleep(1)
        await buy.finish("您暂未开启背包，请通过'查看背包'开启", at_sender=True)


@buy.got("cate", prompt="您想要购买哪种植物或者僵尸?如果不知道都有那些名字可以通过'查看商店'来查看")
async def _(state: T_State, cate: str = ArgStr("cate")):
    if cate in ["取消", "算了"]:
        await asyncio.sleep(1)
        await buy.finish("已取消操作...")
    if cate in list(all_plants.keys()):
        if not isinstance(state["plants"], str):
            plants_in_bag = str(state["plants"]).split(",")
        else:
            plants_in_bag = state["plants"].split(",")
        if cate in plants_in_bag and plants_in_bag.count(cate) >= 6:
            await buy.finish(f"您背包中的{cate}个数大于等于6，请不要在购买啦！")
        price = plants_price[list(all_plants.keys()).index(cate)]
        if price > int(state["sunshine"]):
            await asyncio.sleep(1)
            await buy.finish("购买失败，阳光不够")
        else:
            rest_of_sunshine = int(state["sunshine"]) - price
            users = state["users"]
            # 修改数据
            users[state["index"]][1] = state["plants"] + f",{cate}"
            users[state["index"]][3] = str(rest_of_sunshine)
            # 储存
            flag = write_data(Path(bag_path), users)
            if flag:
                await asyncio.sleep(1)
                await buy.finish(f"购买成功，{cate}已经放入背包啦！阳光余额为{rest_of_sunshine}", at_sender=True)
    elif cate in list(all_zombie.keys()):
        if not isinstance(state["zombies"], str):
            zombies_in_bag = str(state["zombies"]).split(",")
        else:
            zombies_in_bag = state["zombies"].split(",")
        if cate in zombies_in_bag and zombies_in_bag.count(cate) >= 3:
            await buy.finish(f"您背包中的{cate}个数大于等于3，请不要在购买啦！")
        price = zombie_price[list(all_zombie.keys()).index(cate)]
        if price > int(state["sunshine"]):
            await asyncio.sleep(1)
            await buy.finish("购买失败，阳光不够")
        else:
            rest_of_sunshine = int(state["sunshine"]) - price
            users = state["users"]
            users[state["index"]][2] = state["zombies"] + f",{cate}"
            users[state["index"]][3] = str(rest_of_sunshine)
            flag = write_data(Path(bag_path), users)
            if flag:
                await asyncio.sleep(1)
                await buy.finish(f"购买成功，{cate}已经放入背包啦！阳光余额为{rest_of_sunshine}", at_sender=True)
    else:
        await asyncio.sleep(1)
        await buy.finish("您输入的名称有误，购买失败", at_sender=True)


# 放置--------------------------------------------------------------------------------


@put_on_lawn.handle()
async def _(event: MessageEvent, state: T_State, args: Message = CommandArg()):
    # 读取数据
    flag, users = read_data(Path(lawn_path))
    users_id = [x[0] for x in users]
    user_id = str(event.user_id)
    if user_id in users_id:
        _, state["lawn_puts"], level = users[users_id.index(user_id)]
        state["users"] = users
        state["index"] = users_id.index(user_id)
        # 读取背包数据，用于后续判断
        flag, users = read_data(Path(bag_path))
        _, state["plants"], _, _, _ = users[users_id.index(user_id)]
        msg = args.extract_plain_text().strip()
        if msg and (
                (msg.split(" ")[0] in list(
                    all_plants.keys())) or (
                        msg.split(" ")[0] in list(
                            all_zombie.keys()))):
            state["cate"] = msg
    else:
        await asyncio.sleep(1)
        await buy.finish("您暂未开启草坪，请通过'查看草坪'开启", at_sender=True)


@put_on_lawn.got("cate", prompt="您想要放置哪种植物?放在几号位置(1-6)?中间用空格分割")
async def _(state: T_State, cate: str = ArgStr("cate")):
    if not os.path.exists(PVZ_OUTPUT_PATH):
        os.makedirs(PVZ_OUTPUT_PATH)
    if cate in ["取消", "算了"]:
        await asyncio.sleep(1)
        await put_on_lawn.finish("已取消操作...")
    temp = cate.split(" ")
    if len(temp) == 2 and temp[1] in ["1", "2", "3", "4", "5", "6"]:
        plant, pos = cate.split(" ")
        pos = int(pos)
        if plant in list(all_plants.keys()):
            now_pos: List = state["lawn_puts"].split(',')
            my_plants: List = (state["plants"]).split(",")
            if plant in my_plants:
                for p in now_pos:
                    if p != "0":
                        my_plants.pop(my_plants.index(p))
                if plant in my_plants:
                    users = state["users"]
                    now_pos[pos - 1] = plant
                    users[state["index"]][1] = ",".join(now_pos)
                    flag = write_data(Path(lawn_path), users)
                    if flag:
                        await asyncio.sleep(1)
                        # 获取图片
                        lawn_pic([all_plants[x] for x in now_pos if x != "0"])
                        img = MessageSegment.image(
                            "file:///" / PVZ_OUTPUT_PATH / "output0.png")
                        now_pos = [x if x!='0' else '空' for x in now_pos]
                        res = MessageSegment.text(
                            f"放置成功，您的草坪现在为：\n{','.join(now_pos)}") + img
                        await put_on_lawn.finish(res, at_sender=True)
                    else:
                        await asyncio.sleep(1)
                        await put_on_lawn.finish("写入文件失败，请联系管理员", at_sender=True)
                else:
                    await asyncio.sleep(1)
                    await put_on_lawn.finish(f"您的背包里没有多余的{plant},请先去购买")
            else:
                await asyncio.sleep(1)
                await put_on_lawn.finish(f"您的背包中没有{plant}哦，请先购买啦", at_sender=True)
        elif cate in list(all_zombie.keys()):
            await asyncio.sleep(1)
            await put_on_lawn.finish("你想脑子被吃掉吗，哼！", at_sender=True)
        else:
            await asyncio.sleep(1)
            await buy.finish("您输入的名称有误，购买失败", at_sender=True)
    else:
        await asyncio.sleep(1)
        await put_on_lawn.finish("输入格式有误，输入样例:'豌豆射手 1'", at_sender=True)


# 入侵--------------------------------------------------------------------------------


@fight.handle()
async def _(event: GroupMessageEvent, state: T_State):
    flag, users = read_data(Path(lawn_path))
    users_id = [x[0] for x in users]
    # 获取@对象
    at_qid = get_message_at(event.json())
    if at_qid:
        user_id = str(at_qid[0])
        if user_id in users_id:
            lawn = users[users_id.index(user_id)][1].split(",")
            if len(set(lawn)) == 1 and set(lawn).pop() == "0":
                await asyncio.sleep(1)
                await fight.finish("您所要入侵的草坪并没有放置植物，请照顾一下这个可怜的家伙换一个草坪入侵吧", at_sender=True)
            else:
                state["lawn"] = lawn
                flag, users_2 = read_data(Path(bag_path))
                if user_id in [x[0] for x in users_2]:
                    state["bag_zombie"] = users_2[users_id.index(
                        str(event.user_id))][2].split(",")
                else:
                    await fight.finish("您暂未开启背包，请先开启背包", at_sender=True)
        else:
            await asyncio.sleep(1)
            await fight.finish("您要入侵的人并没有开启草坪，快去邀请他吧~", at_sender=True)
    else:
        await asyncio.sleep(1)
        await fight.finish("请至少@一个开启草坪的人来进行入侵", at_sender=True)


@fight.got("team", prompt="请尽快选择您要入侵的阵容，多个僵尸中间用空格分割(最多不超过三个)，默认方式为一个一个出场。\n例如'普通僵尸 普通僵尸 撑杆僵尸'")
async def _(bot: Bot, event: GroupMessageEvent, state: T_State, team: str = ArgStr("team")):
    if team in ["取消", "算了"]:
        await asyncio.sleep(1)
        await fight.finish("已取消操作...")
    # 获取入侵小队
    zombie_team = team.split(" ")
    bag_zombie = state["bag_zombie"]
    # 判断入侵模式
    if zombie_team[-1] == "全上":
        # 暂未写
        pass
    else:
        result1 = dict(Counter(bag_zombie))
        result2 = dict(Counter(zombie_team))
        flag = 1
        if len(result2.items()) > 3:
            # 是否小于三个
            flag = 0
            await fight.finish("僵尸数量太多啦, 请可怜可怜打工的僵尸吧", at_sender=True)
        # 判断背包中僵尸数量是否大于小队中
        for k, v in result2.items():
            if k in list(all_zombie.keys()):
                if result1.get(k, None) and result1.get(k) < v:
                    flag = 0
                    await fight.finish(f"您的背包中没有足够的{k}，请先去商店购买", at_sender=True)
                    break
            else:
                await fight.finish(f"您输入的僵尸名称'{k}'有误，请重新输入", at_sender=True)
                flag = 0
                break
        if flag == 1:
            # 获取当前全部植物的名称
            plants = state["lawn"]
            # 一个一个入侵
            log, iswin = one_by_one(zombie_team, plants)
            # 发送数据
            await send_forward_msg(bot, event, name="疯狂戴夫", uin=str(event.user_id), msgs=log)


# 植物人机训练--------------------------------------------------------------------------


@play_with_computer_zombie.handle()
async def _(event: MessageEvent, state: T_State, args: Message = CommandArg()):
    flag, users = read_data(Path(lawn_path))
    users_id = [x[0] for x in users]
    user_id = str(event.user_id)
    if user_id in users_id:
        msg = args.extract_plain_text().strip()
        if msg and msg in ["易", "中", "难", "地狱"]:
            state["mode"] = msg
        state["lawn"] = (users[users_id.index(user_id)][1]).split(",")
        if len(set(state["lawn"])) == 1 and set(state["lawn"]).pop() == "0":
            await asyncio.sleep(1)
            await play_with_computer_zombie.finish("草坪没有植物，是想要脑子被吃掉嘛喂！可以通过'放置'来向草坪上置放植物哦~")
    else:
        await asyncio.sleep(1)
        await play_with_computer_zombie.finish("您暂未开启草坪,请通过'查看草坪'来开启", at_sender=True)


@play_with_computer_zombie.got("mode", prompt="请选择难度模式，可选择易，中，难，地狱四种不同级别的难度")
async def _(bot: Bot, event: MessageEvent, state: T_State, mode: str = ArgStr("mode")):
    if mode in ["取消", "算了"]:
        await asyncio.sleep(1)
        await play_with_computer_zombie.finish("已取消操作...")
    if mode in ["易", "中", "难", "地狱"]:
        if mode == "易":
            zombie_team = ["路障僵尸", "普通僵尸", "小鬼僵尸"]
        elif mode == "中":
            zombie_team = ["橄榄球僵尸", "铁栅门僵尸", "路障僵尸"]
        elif mode == "难":
            zombie_team = ["橄榄球僵尸", "铁栅门僵尸", "铁桶僵尸", "跳跳僵尸"]
        else:
            zombie_team = ["伽刚特尔", "橄榄球僵尸", "铁栅门僵尸", "小鬼僵尸"]
        lawn_plants = state["lawn"]
        log, iswin = one_by_one(zombie_team, lawn_plants)
        await send_forward_msg(bot, event, name="疯狂戴夫", uin=str(event.user_id), msgs=log)
        await asyncio.sleep(0.5)
        if iswin == 1:
            await play_with_computer_zombie.finish(f"很遗憾您没能通过难度为{mode}的植物人机训练，此次出场的僵尸阵容为{','.join(zombie_team)}",
                                                   at_sender=True)
        else:
            await play_with_computer_zombie.finish(f"恭喜您成功通过难度为{mode}的植物人机训练，此次出场的僵尸阵容为{','.join(zombie_team)}",
                                                   at_sender=True)
    else:
        await asyncio.sleep(1)
        await play_with_computer_zombie.finish("您选择的难度有误，小小垚看不懂，请重新选择", at_sender=True)


# 僵尸人机训练----------------------------------------------------------------------------------------


@play_with_computer_plant.handle()
async def _(event: MessageEvent, state: T_State, args: Message = CommandArg()):
    flag, users = read_data(Path(bag_path))
    users_id = [x[0] for x in users]
    user_id = str(event.user_id)
    if user_id in users_id:
        msg = args.extract_plain_text().strip()
        if msg and msg in ["易", "中", "难", "地狱"]:
            state["mode"] = msg
        state["zombies"] = (users[users_id.index(user_id)][2]).split(",")
    else:
        await asyncio.sleep(1)
        await play_with_computer_plant.finish("您暂未开启背包,请通过'查看背包'来开启", at_sender=True)


@play_with_computer_plant.got("mode", prompt="请选择难度模式，可选择易，中，难，地狱四种不同级别的难度")
async def _(state: T_State, mode: str = ArgStr("mode")):
    if not os.path.exists(PVZ_OUTPUT_PATH):
        os.makedirs(PVZ_OUTPUT_PATH)
    if mode in ["取消", "算了"]:
        await asyncio.sleep(1)
        await play_with_computer_plant.finish("已取消操作...")
    if mode in ["易", "中", "难", "地狱"]:
        if mode == "易":
            plant_team = ["寒冰射手", "豌豆射手", "0", "0", "0", "0"]
        elif mode == "中":
            plant_team = ["寒冰射手", "豌豆射手", "豌豆射手", "0", "0", "坚果墙"]
        elif mode == "难":
            plant_team = ["寒冰射手", "玉米投手", "双发射手", "0", "0", "高坚果"]
        else:
            plant_team = ["冰瓜", "玉米投手", "机枪射手", "火炬", "高坚果", "地刺王"]
        state["plants"] = plant_team
        lawn_pic([all_plants[x] for x in plant_team if x != "0"])
        await asyncio.sleep(0.5)
        state["mode"] = mode
        await play_with_computer_plant.send(
            MessageSegment.text("本次对抗的草坪阵容为") + MessageSegment.image("file:///" / PVZ_OUTPUT_PATH / "output0.png"))
    else:
        await asyncio.sleep(1)
        await play_with_computer_plant.finish("您选择的难度有误，小小垚看不懂，请重新选择", at_sender=True)


@play_with_computer_plant.got("team",
                              prompt="请选择您的僵尸入侵小队，僵尸之间用空格分割，最多选择三个僵尸，例如'普通僵尸 普通僵尸 普通僵尸'")
async def _(bot: Bot, event: MessageEvent, state: T_State, team: str = ArgStr("team")):
    mode = state["mode"]
    if team in ["取消", "算了"]:
        await asyncio.sleep(1)
        await play_with_computer_plant.finish("已取消操作...")
    zombie_team = team.split(" ")
    bag_zombie = state["zombies"]
    result1 = dict(Counter(bag_zombie))
    result2 = dict(Counter(zombie_team))
    flag = 1
    if len(result2.items()) > 3:
        # 是否小于三个
        flag = 0
        await play_with_computer_plant.finish("僵尸数量太多啦, 请可怜可怜打工的僵尸吧", at_sender=True)
    # 判断背包中僵尸数量是否大于小队中
    for k, v in result2.items():
        if k in list(all_zombie.keys()):
            if result1.get(k, None) and result1.get(k) < v:
                flag = 0
                await play_with_computer_plant.finish(f"您的背包中没有足够的{k}，请先去商店购买", at_sender=True)
                break
        else:
            await play_with_computer_plant.finish(f"您输入的僵尸名称'{k}'有误，请重新输入", at_sender=True)
            flag = 0
            break
    if flag == 1:
        # 获取当前全部植物的名称
        plants = state["plants"]
        # 一个一个入侵
        log, iswin = one_by_one(zombie_team, plants)
        # 发送数据
        await send_forward_msg(bot, event, name="疯狂戴夫", uin=str(event.user_id), msgs=log)
        await asyncio.sleep(0.5)
        if iswin == 1:
            await play_with_computer_plant.finish(f"恭喜您成功通过难度为{mode}的僵尸人机训练",
                                                  at_sender=True)
        else:
            await play_with_computer_plant.finish(f"很遗憾您没能通过难度为{mode}的僵尸人机训练",
                                                  at_sender=True)


# 阵容评估------------------------------------------------------------------------------------

@lawn_evaluation.handle()
async def _(event: MessageEvent):
    flag, users = read_data(Path(lawn_path))
    users_id = [x[0] for x in users]
    user_id = str(event.user_id)
    if user_id in users_id:
        lawn_plants = (users[users_id.index(user_id)][1]).split(",")
        zombie_team = [["跳跳僵尸"], ["铁桶僵尸"], ["橄榄球僵尸"], ["伽刚特尔"]]
        flag = 0
        cnt = 0
        for i in range(len(zombie_team)):
            _, iswin = one_by_one(zombie_team[i], lawn_plants)
            if iswin == 1:
                flag = 1
                cnt = i
                break
        if flag == 0:
            level = "S"
        else:
            if cnt == 0:
                level = "D"
            elif cnt == 1:
                level = "C"
            elif cnt == 2:
                level = "B"
            else:
                level = "A"
        users[users_id.index(user_id)][2] = level
        flag = write_data(Path(lawn_path), users)
        level_all = [x[2] if x != '未定级' else 'D' for x in users]
        level_count = dict(Counter(level_all))
        level_order = ["S", "A", "B", "C", "D"]
        summary_m = 0
        summary_z = 0
        for i in range(len(level_order)):
            if i >= level_order.index(level):
                summary_z += level_count[level_order[i]]
            summary_m += level_count[level_order[i]]
        exceed = round(summary_z/summary_m,4)*100
        await asyncio.sleep(1)
        await lawn_evaluation.finish(f"您当前的阵容定级为{level},超越了{exceed}%的当前用户", at_sender=True)
    else:
        await asyncio.sleep(1)
        await play_with_computer_zombie.finish("您暂未开启草坪,请通过'查看草坪'来开启", at_sender=True)

# 帮助---------------------------------------------------------------------------------


@_help.handle()
async def _():
    if not os.path.exists(PVZ_OUTPUT_PATH):
        os.makedirs(PVZ_OUTPUT_PATH)
    res = "欢迎了解植物大战僵尸v1.2.5\n\n" \
          "**************************************************\n\n" \
          "您可以通过使用关键字'查看背包'来查看您的背包\n\n" \
          "**************************************************\n" \
          "通过关键字'查看商店',来查看当前售卖的植物或者僵尸及其价格（植物最多购买六个,僵尸购买三个）\n例如'查看商店 植物'\n\n" \
          "**************************************************\n\n" \
          "通过关键字'购买'+名称来购买植物或者僵尸\n例如'购买 豌豆射手'\n\n" \
          "**************************************************\n\n" \
          "通过关键字'查看图鉴'+名称来查看某种植物或僵尸的具体属性\n例如'查看图鉴 豌豆射手'\n\n" \
          "**************************************************\n\n" \
          "通过关键字'放置'来将背包内的植物放在草坪上以抵御僵尸的攻势\n\n" \
          "**************************************************\n\n" \
          "通过关键字'植物人机训练'来进行模拟入侵\n\n" \
          "**************************************************\n\n" \
          "通过关键字'僵尸人机训练'来进行模拟防御\n\n" \
          "**************************************************\n" \
          "通过'查看草坪'来查看自己的草坪，或者@一个已经开启草坪的玩家来查看他的草坪\n例如'查看草坪 @龙城孤笑'\n\n" \
          "**************************************************\n\n" \
          "通过'入侵'来操纵你的僵尸摧毁他人的防御\n例如'入侵 @龙城孤笑'\n\n" \
          "**************************************************\n\n" \
          "管理员在使用前请务必仔细看文档，在更新插件之前请下载数据，以免数据丢失\n\n"\
          "**************************************************\n\n" \
          "总之，在植物大战僵尸的世界中，祝你玩得开心，享受这个过程！\n\n\n" \
          "插件中所有数据以及图片来源于 ’植物大战僵尸吧‘ 提供的全图鉴中v3.6.0，\n在此由衷感谢数据支持。\n\n\n" \
          "Create by longchengguxiao"
    await asyncio.sleep(1)
    draw_test(res, (255, 255, 153), Path(
        PVZ_OUTPUT_PATH, "help.png"), Path(FONT_PATH))
    await _help.finish(
        MessageSegment.image("file:///" / PVZ_OUTPUT_PATH / "help.png") + MessageSegment.text("建议使用前阅读更详细的命令https://longchengguxiao.github.io/plugindoc/#/nonebot_plugin_pvz/README"), at_sender=True)

# 数据的上传与下载--------------------------------------------------------------------


@download_data.handle()
async def _():
    await asyncio.sleep(1)
    await download_data.send("收到请求")
    await asyncio.sleep(1)


@download_data.got("for_sure",
                   prompt="本功能常用于更新包前的数据下载，请再次确认下载数据吗，这将会覆盖当前本地储存数据，回复'算了'或'取消'来取消操作")
async def _(for_sure: str = ArgStr("for_sure")):
    if for_sure in ["算了", "取消"]:
        await download_data.finish("取消下载数据")
    target_path = os.path.expanduser(
        os.path.join('~', '.nonebot_plugin_pvz')
    )
    if not os.path.exists(target_path):
        os.makedirs(target_path)
    shutil.copyfile(Path(bag_path), os.path.join(target_path, 'bag.txt'))
    shutil.copyfile(Path(lawn_path), os.path.join(target_path, 'lawn.txt'))
    await download_data.finish("pvz用户数据已经成功保存")


@upload_data.handle()
async def _():
    await asyncio.sleep(1)
    await download_data.send("收到请求")
    await asyncio.sleep(1)


@upload_data.got("for_sure",
                 prompt="本功能常用于更新包后的数据载入，请再次确认上传数据吗，这将会覆盖当前安装包内数据，回复'算了'或'取消'来取消操作")
async def _(for_sure: str = ArgStr("for_sure")):
    if for_sure in ["算了", "取消"]:
        await download_data.finish("取消下载数据")
    src_path = os.path.expanduser(
        os.path.join('~', '.nonebot_plugin_pvz')
    )
    if not os.path.exists(src_path):
        await upload_data.finish("未发现本地缓存的pvz用户数据，请先使用命令'pvz下载数据'后上传")
    shutil.copyfile(os.path.join(src_path, 'bag.txt'), Path(bag_path))
    shutil.copyfile(os.path.join(src_path, 'lawn.txt'), Path(lawn_path))
    await download_data.finish("pvz用户数据已经成功保存")

# 定时操作，更改签到数据----------------------------------------------------------------


@scheduler.scheduled_job("cron", day="*")
async def run_every_day_to_reset_signin_data():
    flag, users = read_data(Path(bag_path))
    for i in range(len(users)):
        users[i][4] = "0"
    flag = write_data(Path(bag_path), users)
    if flag:
        logger.warning("********植物大战僵尸签到数据已重置*********")
    else:
        logger.warning("********植物大战僵尸签到数据重置失败*********")




# 合并转发---------------------------------------------------------------------------------------


async def send_forward_msg(
    bot: Bot,
    event: MessageEvent,
    name: str,
    uin: str,
    msgs: List[Union[MessageSegment, Message]],
) -> dict:
    def to_json(msg: Union[MessageSegment, Message]):
        return {
            "type": "node",
            "data": {
                "name": name,
                "uin": uin,
                "content": msg}}

    messages = [to_json(msg) for msg in msgs]
    if isinstance(event, GroupMessageEvent):
        return await bot.call_api(
            "send_group_forward_msg", group_id=event.group_id, messages=messages
        )
    else:
        return await bot.call_api(
            "send_private_forward_msg", user_id=event.user_id, messages=messages
        )
