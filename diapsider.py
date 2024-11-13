import random
import math
import pygame
from pygame.locals import *
import sys
def main():
    pygame.init();
    clock = pygame.time.Clock()
    scw=550;
    sch=700;
    score=0;
    speed=6;
    time=0;
    combo=[0,0];
    press=0;
    bgmTime=0;
    screen = pygame.display.set_mode((scw+450, sch));
    pygame.display.set_caption("Diapsider");
    clickedTimes=1;
    class player:
        x=scw/2;
        y=(sch/2)+100;
        v=0;
        a=0;
        anime=[60,0];
        rad=0;
        min=1;
        max=8;
        fireInterval=0;
        gun=3;
        bulletSpeed=10;
        fireDuration=10;
    fire=False;
    bullets=[];
    def abs(x):
        if x<0:
            return -x;
        return x;
    def index(seed):
        for i in range(len(bullets)):
            if seed==bullets[i].seed:
                return i;
        return -1;
    def indexPop(seed):
        for i in range(len(popTexts)):
            if seed==popTexts[i].seed:
                return i;
        return -1;
    def indexEnemy(seed):
        for i in range(len(enemies)):
            if seed==enemies[i].seed:
                return i;
        return -1;
    def collisionToEnemy(x,y):
        for e in enemies:
            if abs(x-e.x)<=33 and abs(y-e.y)<=18+player.bulletSpeed/2:
                return indexEnemy(e.seed);
        return -1;
    class bullet:
        def __init__(self,x,y):
            self.x=x;
            self.y=y;
            self.seed=random.random();
            self.damage=7;
    enemies=[];
    popTexts=[];
    class pops:
        def __init__(self,label,x,y,fontsize,duration,r,g,b):
            self.label=label;
            self.size=fontsize;
            self.duration=duration;
            self.x=x;
            self.y=y;
            self.seed=random.random();
            self.color=[r,g,b];
    class enemy:
        #コンストラクタ
        def __init__(self,name):
            self.x=random.random()*scw;
            if name=="evilFish":
                self.direction=math.floor(random.random()*2);
            self.y=0;
            self.hp=100;
            self.pt=random.random()*math.pi;
            self.seed=random.random();
            self.type=math.floor(random.random()*5);
    font = pygame.font.Font("../font/DotGothic16-Regular.ttf",50)
    font1 = pygame.font.Font("../font/DotGothic16-Regular.ttf",20)
    bcg_c = pygame.image.load("images/background_cave.png")
    pygame.mixer.music.load("sounds/coldocean.mp3");
    killSound = pygame.mixer.Sound("sounds/killSound.mp3");
    hitSound = pygame.mixer.Sound("sounds/hitSound.mp3");
    fireSound = pygame.mixer.Sound("sounds/fireSound.mp3");
    player1 = pygame.image.load("images/jelly1.png")
    player2 = pygame.image.load("images/jelly2.png")
    player3 = pygame.image.load("images/jelly3.png");
    player4 = pygame.image.load("images/jelly4.png")
    lazer=pygame.image.load("images/lazer.png");
    evilFish = pygame.image.load("images/evilFish.png")
    evilFish = pygame.transform.rotate(evilFish, 270)
    player1 = pygame.transform.scale(player1, (51,63))
    player2 = pygame.transform.scale(player2, (51,63))
    player3 = pygame.transform.scale(player3, (51,63))
    player4 = pygame.transform.scale(player4, (51,63))
    lazer = pygame.transform.scale(lazer, (9,45))
    evilFish = pygame.transform.scale(evilFish, (66,36))
    evilFish2 =pygame.transform.flip(evilFish,True,False);
    bcg_c = pygame.transform.scale(bcg_c, (scw, sch*1.5))
    pygame.mixer.music.play(-1);
    #canvasでいうtranslateのようなもの
    while True:
        time+=1/60;
        if bgmTime>0:
            bgmTime-=1/60;
        if bgmTime<=0:
            bgmTime=87;
        if combo[0]>0:
            combo[0]-=1;
            if combo[0]<=0:
                combo=[0,0];
        if player.rad>math.pi:
            player.rad-=2*math.pi;
        if player.rad<-math.pi:
            player.rad+=2*math.pi;
        screen.fill((255,255,255))
        #描画はこの下へ
        backgroundy=(30*time)-3*sch*math.floor((30*time)/(sch*3));
        screen.blit(bcg_c, (0,backgroundy-sch/2));
        if(sch/2<backgroundy):
            screen.blit(bcg_c, (0, backgroundy-(sch*2)));
        if(sch*1.5<backgroundy):
            screen.blit(bcg_c, (0, backgroundy-(sch*3.5)));
        if random.random()<(0.01+math.sqrt(time)/100):
            enemies.append(enemy("evilFish"));
        for e in enemies:
            e.pt+=math.pi/180;
            if e.type==4:
                pygame.draw.circle(screen,(170,10,10),(e.x,e.y),15)
            else:
                if e.direction==0:
                    screen.blit(evilFish, (e.x-33,e.y-18));
                else:
                    screen.blit(evilFish2, (e.x-33,e.y-18));
            pygame.draw.rect(screen,(200,0,0),(e.x-20,e.y-20,40,4))
            pygame.draw.rect(screen,(200,200,200),(e.x-20,e.y-20,math.pow(e.hp,2)/250,4))
            e.y+=(2+math.sin(e.pt)/5);
            if e.direction==0:
                e.x-=1;
            else:
                e.x+=1;
            if e.x+33<0 or e.y-18>sch or e.x-33>scw:
                i=indexEnemy(e.seed);
                dh=enemies[0:i];
                hd=enemies[i+1:len(enemies)];
                enemies=dh+hd;
        #bulletsに関する処理
        if fire:
            if player.fireInterval==0:
                    fireSound.play();
                    for i in range(player.gun):
                        bx=player.x+(20*i)-10*(player.gun-1);
                        by=player.y-40;
                        bullets.append(bullet(bx,by));
                    player.fireInterval=player.fireDuration;
        for b in bullets:
            screen.blit(lazer, (b.x-4.5,b.y-22.5));
            #pygame.draw.circle(screen,(10,10,10),(b.x,b.y),5)
            b.y-=player.bulletSpeed;
            if b.y<0:
                i=index(b.seed);
                dh=bullets[0:i];
                hd=bullets[i+1:len(bullets)];
                bullets=dh+hd;
            if collisionToEnemy(b.x,b.y)!=-1:
                score+=math.floor(random.random()*2+2);
                ind=collisionToEnemy(b.x,b.y);
                i=index(b.seed);
                damage=b.damage+3*random.random()-3*random.random();
                enemies[ind].hp-=b.damage;
                if enemies[ind].hp<=0:
                    combo[1]+=1;
                    combo[0]=60;
                    scoreSum=100;
                    if combo[1]>10:
                        scoreSum+=250;
                    else:
                        if combo[1]>1:
                            scoreSum+=25*(combo[1]-1);
                    score+=scoreSum;
                    popTexts.append(pops("+%i" % scoreSum,enemies[ind].x,enemies[ind].y,20,60,255,255,255))
                    if combo[1]>1:
                        popTexts.append(pops("%i連鎖！" % combo[1],enemies[ind].x,enemies[ind].y-20,20,60,255,255,255))
                    if enemies[ind].type==4:
                        seed=math.ceil(random.random()*2);
                        if seed==1:
                            player.fireDuration=19*player.fireDuration/20;
                            player.bulletSpeed+=1;
                        #if seed==2:
                        #    player.gun+=1;
                    dh=enemies[0:ind];
                    hd=enemies[ind+1:len(enemies)];
                    enemies=dh+hd;
                    killSound.play();
                    hitSound.stop();
                    fireSound.stop();
                else:
                    popTexts.append(pops("-%i" % damage,enemies[ind].x,enemies[ind].y,20,30,255,0,0))
                    hitSound.play();
                    fireSound.stop();
                dh=bullets[0:i];
                hd=bullets[i+1:len(bullets)];
                bullets=dh+hd;
        #十八番,popText
        for p in popTexts:
            screen.blit(font1.render(p.label, True, (p.color[0],p.color[1],p.color[2])),(p.x,p.y));
            p.y-=0.5;
            p.duration-=1;
            if p.duration<=0:
                i=indexPop(p.seed);
                dh=popTexts[0:i];
                hd=popTexts[i+1:len(popTexts)];
                popTexts=dh+hd;
        #playerに関する処理
        if player.anime[0]>0:
            player.anime[0]-=1;
            if player.anime[0]<=0:
                player.anime[0]=60;
                player.anime[1]+=1;
                if player.anime[1]==2:
                    player.anime[1]=0;
        if player.fireInterval>0:
            player.fireInterval-=1;
            if player.fireInterval<0:
                player.fireInterval=0;
        #加速
        if player.v<player.max or player.a<0:
            if player.a<0:
                player.v+=player.a/30;
            else:
                player.v+=player.a/60;
        if player.v<0:
            player.a=0;
            player.v=0;
        #移動
        if (math.sin(player.rad)*player.v<0 and player.y+31.5<sch) or (math.sin(player.rad)*player.v>0 and player.y-31.5>0):
            player.y-=math.sin(player.rad)*player.v;
        if (math.cos(player.rad)*player.v>0 and player.x+25.5<scw) or (math.cos(player.rad)*player.v<0 and player.x-25.5>0):
            player.x+=math.cos(player.rad)*player.v;
        if player.anime[1]==0:
            if player.fireInterval>player.fireDuration/2:
                screen.blit(player3, (player.x-25.5,player.y-31.5));
            else:screen.blit(player1, (player.x-25.5,player.y-31.5));
        else:
            if player.fireInterval>player.fireDuration/2:
                screen.blit(player4, (player.x-25.5,player.y-31.5));
            else:
                screen.blit(player2, (player.x-25.5,player.y-31.5));
        #UI
        pygame.draw.rect(screen, (23,28,43), Rect(scw,0,450,sch))
        screen.blit(font.render("Diapsider", True, (255,255,255)),(scw+10,10));
        screen.blit(font.render("スコア%i" % score, True, (255,255,255)),(scw+10,100));
        clock.tick(60);
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_a or event.key==K_LEFT:
                    player.a=speed;
                    press+=1;
                    if player.rad<=0:
                        player.rad=(player.rad*(press-1)-math.pi)/press;
                    else:
                        player.rad=(player.rad*(press-1)+math.pi)/press;
                if event.key == K_w or event.key==K_UP:
                    player.a=speed;
                    press+=1;
                    if player.rad<0:
                        player.rad=2*math.pi+player.rad;
                    player.rad=(player.rad*(press-1)+(math.pi/2))/press;
                if event.key == K_s or event.key==K_DOWN:
                    player.a=speed;
                    press+=1;
                    if player.rad>0:
                        player.rad=player.rad-2*math.pi;
                    player.rad=(player.rad*(press-1)-(math.pi/2))/press;
                if event.key == K_d or event.key==K_RIGHT:
                    player.a=speed;
                    press+=1;
                    player.rad=(player.rad*(press-1))/press;
                if event.key == K_z or event.key==K_RETURN:
                    fire=True;
                if event.key == K_k:
                    player.gun+=1;
                if player.v<player.min and press>0:
                    player.v=player.min;
            if event.type == KEYUP:
                if event.key == K_a or event.key==K_LEFT:
                    pressA=False;
                    if press>1:
                        if player.rad<=0:
                            player.rad=((press*player.rad)+math.pi)/(press-1);
                        else:
                            player.rad=((press*player.rad)-math.pi)/(press-1);
                    press-=1;
                    if press==0:
                        player.a=-speed;
                if event.key == K_w or event.key==K_UP:
                    if press>1:
                        #if player.rad<=0:
                        player.rad=((press*player.rad)-(math.pi/2))/(press-1);
                        #else:
                        #    player.rad=((press*player.rad)+(3*math.pi/2))/(press-1);
                    press-=1;
                    if press==0:
                        player.a=-speed;
                if event.key == K_s or event.key==K_DOWN:
                    if press>1:
                        player.rad=((press*player.rad)+(math.pi/2))/(press-1);
                    press-=1;
                    if press==0:
                        player.a=-speed;
                if event.key == K_d or event.key==K_RIGHT:
                    if press>1:
                        player.rad=(press*player.rad)/(press-1);
                    press-=1;
                    if press==0:
                        player.a=-speed;
                if event.key == K_z or event.key==K_RETURN:
                    fire=False;
if __name__ == "__main__":
    main()

