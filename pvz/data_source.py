import numpy as np

class Plants():

    def __init__(self,plantname:str):
        self.hp = 0
        self.damage = 0
        self.damage_interval = 0
        self.price = 0
        self.damage_distance = 0
        self.effect = 1
        self.only_night = 0
        self.penetrable = 0
        self.only_hurt_by_boss = 0
        self.only_hurt_metal = 0

        if plantname == "豌豆射手":
            self.pea_shooter()
        elif plantname == "坚果墙":
            self.wall_nut()
        elif plantname == "寒冰射手":
            self.snow_pea()
        elif plantname == "食人花":
            self.chomper()
        elif plantname == "双发射手":
            self.repeater()
        elif plantname == "小喷菇":
            self.puff_shroom()
        elif plantname == "胆小菇":
            self.scaredy_shroom()
        elif plantname == "大喷菇":
            self.fume_shroom()
        elif plantname == "地刺":
            self.spikeweed()
        elif plantname == "火炬树桩":
            self.torchwood()
        elif plantname == "高坚果":
            self.tall_nut()
        elif plantname == "卷心菜投手":
            self.cabbage_pult()
        elif plantname == "玉米投手":
            self.kernet_pult()
        elif plantname == "西瓜投手":
            self.melon_pult()
        elif plantname == "机枪豌豆":
            self.gatling_pea()
        elif plantname == "地刺王":
            self.spikerock()
        elif plantname == "磁力菇":
            self.magnet_shroom()
        elif plantname == "冰瓜":
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
        self.damage_distance = [0,np.inf]
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
        self.hp = 4000
        self.damage = 0
        self.damage_interval = 0
        self.price = 50
        self.damage_distance = [0,0]
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
        self.damage_distance = [0,np.inf]
        self.effect = 0.5
        self.only_night = 0
        self.penetrable = 0
        self.only_hurt_by_boss = 0
        self.only_hurt_metal = 0

    def chomper(self):
        """
        食人花
        :return:
        """
        self.hp = 300
        self.damage = 40
        self.damage_interval = 15
        self.price = 150
        self.damage_distance = [0,1.5]
        self.effect = 1
        self.only_night = 0
        self.penetrable = 0
        self.only_hurt_by_boss = 0
        self.only_hurt_metal = 0

    def repeater(self):
        """
        双发射手
        :return:
        """
        self.hp = 300
        self.damage = 40
        self.damage_interval = 1.5
        self.price = 200
        self.damage_distance = [0,np.inf]
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
        self.damage_distance = [0,3]
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
        self.damage_distance = [1,np.inf]
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
        self.damage_distance = [0,4]
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
        self.damage_distance = [-0.5,0.5]
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
        self.damage_distance = [0,np.inf]
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
        self.hp = 8000
        self.damage = 0
        self.damage_interval = 0
        self.price = 125
        self.damage_distance = [0,0]
        self.effect = 1
        self.only_night = 0
        self.penetrable = 0
        self.only_hurt_by_boss = 0
        self.only_hurt_metal = 0

    def cabbage_pult(self):
        """
        卷心菜投手
        :return:
        """
        self.hp = 300
        self.damage = 40
        self.damage_interval = 3.0
        self.price = 100
        self.damage_distance = [0,np.inf]
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
        self.damage_distance = [0,np.inf]
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
        self.damage_distance = [0,np.inf]
        self.effect = 1
        self.only_night = 0
        self.penetrable = 0
        self.only_hurt_by_boss = 0
        self.only_hurt_metal = 0

    def spikerock(self):
        """
        地刺王
        :return:
        """
        self.hp = 450
        self.damage = 20
        self.damage_interval = 1
        self.price = 225
        self.damage_distance = [-0.5,0.5]
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
        self.damage_distance = [0,np.inf]
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
        self.damage_distance = [-np.inf,np.inf]
        self.effect = 1
        self.only_night = 1
        self.penetrable = 0
        self.only_hurt_by_boss = 0
        self.only_hurt_metal = 1

    def winter_melon(self):
        """
        冰瓜
        :return:
        """
        self.hp = 300
        self.damage = 80
        self.damage_interval = 1
        self.price = 500
        self.damage_distance = [-1,0]
        self.effect = 0.5
        self.only_night = 0
        self.penetrable = 0
        self.only_hurt_by_boss = 0
        self.only_hurt_metal = 0


class Zombie():
    all_zombie = ["普通僵尸","路障僵尸","撑杆僵尸","铁桶僵尸","铁栅门僵尸","橄榄球僵尸","跳跳僵尸","伽刚特尔","小鬼僵尸"]
    def __init__(self, zombiename:str):
        self.hp = 0
        self.damage = 0
        self.v = 0
        self.price = 0
        self.metal = 0
        self.jump = 0
        self.damage_interval = 0
        self.ignore_effect = 0
        self.is_gargantuar = 0

        if zombiename == "普通僵尸":
            self.normal_zombie()
        elif zombiename == "路障僵尸":
            self.conehead_zombie()
        elif zombiename == "撑杆僵尸":
            self.buckethead_zombie()
        elif zombiename == "铁桶僵尸":
            self.pole_vaulting_zombie()
        elif zombiename == "铁栅门僵尸":
            self.screen_door_zombie()
        elif zombiename == "橄榄球僵尸":
            self.football_zombie()
        elif zombiename == "跳跳僵尸":
            self.pogo_zombie()
        elif zombiename == "伽刚特尔":
            self.gargantuar()
        elif zombiename == "小鬼僵尸":
            self.imp()




    def normal_zombie(self):
        self.hp = 270
        self.v = 0.2
        self.damage = 100
        self.price=50
        self.damage_interval=1
        self.jump=0
        self.metal=0
        self.ignore_effect = 0
        self.is_gargantuar = 0

    def conehead_zombie(self):
        self.hp = 270+370
        self.v = 0.2
        self.damage = 100
        self.price=75
        self.damage_interval=1
        self.jump=0
        self.metal=0
        self.ignore_effect = 0
        self.is_gargantuar = 0

    def buckethead_zombie(self):
        self.hp = 500
        self.v = 0.4
        self.damage = 100
        self.price=75
        self.damage_interval=1
        self.jump=1
        self.metal=0
        self.ignore_effect = 0
        self.is_gargantuar = 0

    def pole_vaulting_zombie(self):
        self.hp = 270+1100
        self.v = 0.2
        self.damage = 100
        self.price=125
        self.damage_interval=1
        self.jump=0
        self.metal=1
        self.ignore_effect = 0
        self.is_gargantuar = 0

    def screen_door_zombie(self):
        self.hp = 270+1100
        self.v = 0.2
        self.damage = 100
        self.price=100
        self.damage_interval=1
        self.jump=0
        self.metal=1
        self.ignore_effect = 1
        self.is_gargantuar = 0

    def football_zombie(self):
        self.hp = 270+1100
        self.v = 0.4
        self.damage = 100
        self.price=175
        self.damage_interval=1
        self.jump=0
        self.metal=1
        self.ignore_effect = 0
        self.is_gargantuar = 0

    def pogo_zombie(self):
        self.hp = 270+230
        self.v = 0.5
        self.damage = 100
        self.price=75
        self.damage_interval=1
        self.jump=1
        self.metal=1
        self.ignore_effect = 0
        self.is_gargantuar = 0

    def gargantuar(self):
        self.hp = 3000
        self.v = 0.2
        self.damage = 100000
        self.price=300
        self.damage_interval=2
        self.jump=0
        self.metal=0
        self.ignore_effect = 0
        self.is_gargantuar = 1

    def imp(self):
        self.hp = 270
        self.v = 0.25
        self.damage = 100
        self.price=50
        self.damage_interval=0.75
        self.jump=0
        self.metal=0
        self.ignore_effect = 0
        self.is_gargantuar = 0
