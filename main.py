import pygame, random, time
pygame.init()
pygame.mixer.init()
pygame.font.init()
pygame.mixer.music.load("music.mp3")
pygame.mixer.music.play()
ismusicb = True
issoundb = True
w = pygame.display.set_mode((700, 700))
pygame.display.set_caption("Shooter Test")
clock = pygame.time.Clock()
isG = True
cycle = True
ec = (0, 0, 0)
bc = (10, 10, 10)
class Sprite:
    def __init__(self, x, y, w, h, cl=(255, 255, 255), img=None):
        self.color = cl
        self.img = img
        self.rect = pygame.Rect((x, y), (w, h))
    def debug(self):
        pygame.draw.rect(w, self.color, self.rect)
    def checkcol(self, x, y):
        if self.rect.collidepoint(x, y):
            return True
class Player(Sprite):
    def __init__(self, x, y, w, h, cl=(255, 255, 255), img=None, speed=3, damage=1):
        super().__init__(x, y, w, h, cl, img)
        self.sp = speed
        self.dmg = damage
        self.bullets = list()
        self.shootcd = 1
        self.shoottime = time.time()
    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_d]:
            self.rect.x += self.sp
        if keys[pygame.K_a]:
            self.rect.x -= self.sp
        if keys[pygame.K_f] and time.time()-self.shoottime >= self.shootcd:
            self.bullets.append(Sprite(self.rect.centerx, self.rect.y, 6, 6, cl=(200,200,0)))
            self.shoottime = time.time()
            if issoundb:
                shoot.play()
class Enemy(Sprite):
    def __init__(self, x, y, w, h, cl=(255, 255, 255), img=None, hp=1, mr = True):
        super().__init__(x, y, w, h, cl, img)
        self.hp = hp
        self.cd = time.time()
        self.mr = mr
    def update(self):
        self.debug()
        if self.rect.y <= 700 and time.time()-self.cd >= 0.85:
            self.rect.y += 15
            self.cd = time.time()
class TextArea:
    def __init__(self, x=0, y=0, width=10, height=10, color=(0,0,0)):
        self.rect = pygame.Rect(x, y, width, height)
        self.fill_color = color
    def set_text(self, text, fsize=12, text_color=(255, 255, 255)):
        self.text = text
        self.image = pygame.font.Font(None, fsize).render(text, True, text_color)
    def draw(self, shift_x=0, shift_y=0):
        pygame.draw.rect(w, self.fill_color, self.rect)
        w.blit(self.image, (self.rect.x + shift_x, self.rect.y + shift_y))
    def checkcol(self, x, y):
        if self.rect.collidepoint(x, y):
            return True
class Upgrade(Sprite):
    def __init__(self, x, y, w, h, utype, cl=(255, 255, 255), img=None):
        super().__init__(x, y, w, h, cl, img)
        self.utype = utype
    def update(self):
        self.debug()
        self.rect.y += 1
        #
mk = 28
miss = 0
plr = Player(350, 600, 30, 30, (255, 255, 255))
enemies = list()
espawnt = time.time()
espawndel = random.randint(2, 6)
wtext = TextArea(350, 350)
killcount = TextArea(10, 20)
misscount = TextArea(10, 50)
upgrades = list()
upgradetypes = ["dmg", "speed", "cd"]
ts = time.time()
levelup = 15
level = 1
enemyhpmin = 1
enemyhpmax = 1
inmenu = True
insettings = False
#sounds
die = pygame.mixer.Sound("enemydie.mp3")
levelups = pygame.mixer.Sound("levelup.mp3")
shoot = pygame.mixer.Sound("shot.ogg")
upgradesound = pygame.mixer.Sound("upgrade.ogg")
###
#menu
menub = list()
startb = TextArea(20, 60, 200, 90, (100, 100, 100))
startb.set_text("Начать", 80, (10, 10, 10))
settingb = TextArea(20, 200, 200, 90, (100, 100, 100))
settingb.set_text("Настройки", 50, (10, 10, 10))
exitb = TextArea(20, 340, 200, 90, (100, 100, 100))
exitb.set_text("Выход", 80, (10, 10, 10))
menub.append(startb)
menub.append(settingb)
menub.append(exitb)
#settings
settingsb = list()
ismusic = TextArea(20, 60, 200, 90, (0, 100, 0))
ismusic.set_text("Музыка", 80, (10, 10, 10))
issound = TextArea(20, 200, 200, 90, (0, 100, 0))
issound.set_text("Звук", 80, (10, 10, 10))
settingsb.append(ismusic)
settingsb.append(issound)
bosses = list()
lastkillfeed = 0
debugBoss = True
while cycle:
    w.fill(bc)
    if not inmenu:
        if isG:
            if lastkillfeed + 30 == mk:
                print("Появился босс! Убейте его для получения очков урона!")
                bosses.append(Enemy(random.randint(30, 650), 30, 40, 40, (140, 140, 140), None, level + 10))
                lastkillfeed = mk
                debugBoss = False
            for i in bosses:
                i.debug()
                if i.hp <= 0:
                    plr.dmg += 10
                    print(f"Вы победили босса! Игроку добавлено 10 дмг. У игрока {plr.dmg} дмг.")
                    bosses.remove(i)
                if i.rect.y >= 670:
                    bosses.remove(i)
                    print("Вы упустили босса.")
                if time.time() - i.cd >= 0.2:
                    i.rect.y += 1
                    i.cd = time.time()
                if i.mr:
                    i.rect.x += 1
                else:
                    i.rect.x -= 1
                if i.rect.x <= 0:
                    i.mr = True
                if i.rect.x >= 650:
                    i.mr = False
            if time.time()-espawnt >= espawndel:
                espawnt = time.time()
                espawndel = random.randint(2, 6)
                enemies.append(Enemy(random.randint(30, 650), 30, 30, 30, (255, 255, 255), None, random.randint(enemyhpmin, enemyhpmax)))
            for i in enemies:
                if i.hp <= 0:
                    mk += 1
                    if random.randint(1, 10) >= 7:
                        sus = True
                        while sus:
                            random.shuffle(upgradetypes)
                            if upgradetypes[0] == "dmg":
                                upgrades.append(Upgrade(i.rect.x, i.rect.y, 25, 25, upgradetypes[0], (100, 0, 0)))
                            elif upgradetypes[0] == "speed":
                                if plr.sp > 6:
                                    upgradetypes.pop(0)
                                upgrades.append(Upgrade(i.rect.x, i.rect.y, 25, 25, upgradetypes[0], (50, 50, 100)))
                                sus = False
                            elif upgradetypes[0] == "cd":
                                if plr.shootcd < 0.2:
                                    upgradetypes.pop(0)
                                else:
                                    upgrades.append(Upgrade(i.rect.x, i.rect.y, 25, 25, upgradetypes[0], (0, 100, 0)))
                                    sus = False
                    enemies.remove(i)
                    if issoundb:
                        die.play()
                if  i.rect.y >= 700:
                    enemies.remove(i)
                    miss += 1
                i.update()
            for i in plr.bullets:
                if i.rect.y <= 0:
                    plr.bullets.remove(i)
                for enemy in enemies:
                    if pygame.Rect.colliderect(i.rect, enemy.rect):
                        enemy.hp -= plr.dmg
                        plr.bullets.remove(i)
                for enemy in bosses:
                    if pygame.Rect.colliderect(i.rect, enemy.rect):
                        enemy.hp -= plr.dmg
                        plr.bullets.remove(i)
                i.rect.y -= 5
                i.debug()
            for i in upgrades:
                i.update()
                if pygame.Rect.colliderect(i.rect, plr.rect):
                    if i.utype == "dmg":
                        plr.dmg += 1
                        print(f"Урон игрока теперь {plr.dmg}")
                    if i.utype == "cd":
                        plr.shootcd -= 0.05
                        print(f"Кулдаун стрельбы теперь {plr.shootcd}с")
                    if i.utype == "speed":
                        if plr.sp <= 6:
                            plr.sp += 0.3
                            print(f"Скорость игрока теперь {plr.sp}")
                    if issoundb:
                        upgradesound.play()
                    upgrades.remove(i)
            killcount.set_text(f"kills: {mk}", 32)
            misscount.set_text(f"missed: {miss}", 32)
            killcount.draw()
            misscount.draw()
            keys = pygame.key.get_pressed()
            plr.update()
            plr.debug()
            '''
            if miss >= 3:
                isG = False
                bc = (200, 0, 0)
                wtext.set_text("YOU LOST.", 64)
            elif mk >= 3:
                isG = False
                bc = (0, 200, 0)
                wtext.set_text("YOU WIN!", 64)
            '''
            if time.time() - ts >= levelup:
                level += 1
                if random.randint(1, 5) >= 4:
                    enemyhpmin += random.randint(1, 2)
                enemyhpmax += random.randint(1, 2)
                ts = time.time()
                print(f"Переход на {level} уровень. Теперь у врагов от {enemyhpmin} до {enemyhpmax} хп.")
                if issoundb:
                    levelups.play()
        if not isG:
            wtext.draw()
    elif inmenu and not insettings:
        for i in menub:
            i.draw()
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                cycle = False
            if e.type == pygame.MOUSEBUTTONDOWN:
                if e.button == 1:
                    x, y = e.pos
                    if startb.checkcol(x, y):
                        inmenu = False
                    elif exitb.checkcol(x, y):
                        cycle = False
                    elif settingb.checkcol(x, y):
                        insettings = True
    elif inmenu and insettings:
        for i in settingsb:
            i.draw()
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                cycle = False
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_ESCAPE:
                    inmenu = True
                    insettings = False
            if e.type == pygame.MOUSEBUTTONDOWN:
                if e.button == 1:
                    x, y = e.pos
                    if ismusic.checkcol(x, y):
                        if ismusicb:
                            pygame.mixer.music.stop()
                            ismusicb = False
                            ismusic.fill_color = (100, 0, 0)
                        else:
                            pygame.mixer.music.play()
                            ismusicb = True
                            ismusic.fill_color = (0, 100, 0)
                    elif issound.checkcol(x, y):
                        if issoundb:
                            issoundb = False
                            issound.fill_color = (100, 0, 0)
                        else:
                            issoundb = True
                            issound.fill_color = (0, 100, 0)
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            cycle = False
        if e.type == pygame.KEYDOWN:
            if e.key == pygame.K_ESCAPE:
                inmenu = True
                insettings = False
    pygame.display.update()
    clock.tick(60)
