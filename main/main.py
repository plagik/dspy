from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
import random
from ursina import application
bulles = []
pausa = False
textyr=["res/4","res/5","res/7","res/9","res/21","res/23","res/42","res/wq"]
tryps=[]
time_tick_flag=True
def reset_time_tick_flag():
    global time_tick_flag 
    time_tick_flag=True
class Surface(Entity):
    def __init__(self,rom, **par):
        super().__init__(**par)
        self.ot = True
        self.rom = rom
        self.hashole = False
  
        if rom == "armor":
            self.n=Surface(parent=self,rom="norm" ,name='n', position=(0,0,4), model="cube", scale=(8,8,1), collider="box", color=color.gray,texture=random.choice(textyr))
            self.n.texture_offset = (random.uniform(0, 0.9), random.uniform(0, 0.9))
            self.s=Surface(parent=self,rom="norm" , name='s', position=(0,0,-4), model="cube", scale=(8,8,2), collider="box", color=color.gray,texture=random.choice(textyr))
            self.s.texture_offset = (random.uniform(0, 0.9), random.uniform(0, 0.9))
            self.e=Surface(parent=self,rom="norm" , name='e', position=(4,0,0), model="cube", scale=(2,8,8), collider="box", color=color.gray,texture=random.choice(textyr))
            self.e.texture_offset = (random.uniform(0, 0.9), random.uniform(0, 0.9))
            self.w=Surface(parent=self,rom="norm" , name='w', position=(-4,0,0), model="cube", scale=(1,8,8), collider="box", color=color.gray,texture=random.choice(textyr))
            self.w.texture_offset = (random.uniform(0, 0.9), random.uniform(0, 0.9))
            
    def onot(self):
        self.ot = True

    def riko(self, bules, point, normal):
        if bules.ot > 0 and self.ot:
            self.ot = False
            new_dir = bules.dir - 2 * (bules.dir.dot(normal)) * normal
            bules.dir = new_dir.normalized()
            bules.position = point + normal * 0.1
            bules.look_at(bules.position + bules.dir)
            bules.ot -= 1
            invoke(self.onot, delay=0.1)
        elif bules.ot <= 0:
            if bules in bulles:
                bulles.remove(bules)
            destroy(bules)

class Player(FirstPersonController):
    def __init__(self, hp, **par):
        super().__init__(camera_offset=(0, 1.2, 0), **par)
        self.patron=[1]
        self.levpain=10
        self.hp = hp
        health_bar_bg = Entity(parent=camera.ui,model='quad',color=color.black66,origin=(-0.5, 0.5),scale=(0.4, 0.04),position=(-0.85, 0.45) )
        self.health_bar = Entity(parent=health_bar_bg,  model='quad',color=color.red,origin=(-0.5, 0.5),scale=(1, 1),z=-0.01)
        self.armor = 0
        self.armo_bar_bg = Entity(parent=camera.ui,model='quad',color=color.black66,origin=(-0.5, 0.5),scale=(0.2, 0.04),position=(-0.85, 0.40) ,enabled=True)
        self.armo_bar = Entity(parent=self.armo_bar_bg,  model='quad',color=color.green,origin=(-0.5, 0.5),scale=(1, 1),z=-0.01,enabled=False)        
        self.time = 0
        self.shot = True
        self.invent = [Entity(model="Pistol", rotation=[0,180,0],parent=camera, position=(0.8, -0.7, 1.5),texture="res/textura 2 modificada", color=color.black, scale=(0.001, 0.001,0.001), name="1",patr=15)]
        self.damage = 10
        self.shp = Entity(parent=camera.ui, model='cube', scale=(1.8, 1, 0.1), position=(0, 0, 0), color=color.red,alpha=0,collider=None)
        self.gun=self.invent[0]
        self.patrsh=Text(text=f"{self.invent[0].patr}/∞", position=(-0.8, -0.4))
        self.menu = Entity(parent=camera.ui, model='quad', scale=(0.5, 0.6),color=color.black66, enabled=False)
        self.btn_resume = Button(text='Continue', parent=self.menu, y=0.2, scale=(0.6, 0.1),on_click=lambda:self.imp("escape"))
        self.txt=Text(position=[-0.15,0.1],text="Difficulty level 5-20",parent=self.menu,scale=[1.5,1.5,1.5])
        self.painlev=InputField(y=0,limit_content_to="1234567890",color=color.gray ,default_value="10", enabled=False,scale=[0.05,0.05],text_origin=(0, 0),on_click=self.clear_painlev)
        self.btn_restart =Button(text='Restart', parent=self.menu, y=-0.2, scale=(0.6, 0.1))
        self.reloading_anim = False
        self.jump_height = 0 

    def open_shot(self):
        self.shot = True

    def clear_painlev(self):
        self.painlev.text = ""
    def imp(self, key):
        if key == 'left mouse down'and not self.menu.enabled:
            if self.shot and pausa == False and not self.reloading_anim:
                if hasattr(self.gun ,"patr"):
                    if self.gun.patr==0:
                        self.gun.enabled=False
                        self.gun=self.invent[0]
                        self.gun.enabled=True
                        player.patrsh.text=f"{player.invent[0].patr}/∞"
                        return
                    self.gun.patr-=1
                fire(self.gun)
                self.shot = False
                invoke(self.open_shot, delay=0.4)
                if self.gun.name == "drobo":
                    self.gun.animate_rotation([0,270,-10], duration=0.2,curve=curve.linear)
                    invoke(self.gun.animate_rotation, [0,270,0], duration=0.1, delay=0.2, curve=curve.linear)
                elif self.gun.name == "1":
                    self.gun.animate_rotation([10,180,0], duration=0.2,curve=curve.linear)
                    invoke(self.gun.animate_rotation, [0,180,0], duration=0.1, delay=0.2, curve=curve.linear)
        if key=="r" and not self.menu.enabled and not self.reloading_anim:
            self.reloading_anim = True
            original_pos = self.gun.position
            if self.gun.name == "drobo":
                self.gun.animate_rotation([0,270,30], duration=0.5,curve=curve.linear)
                self.gun.animate_position((original_pos[0], original_pos[1]-0.5, original_pos[2]), duration=0.4, curve=curve.linear)
                invoke(self.gun.animate_position, original_pos, duration=0.1, delay=1, curve=curve.linear)
                invoke(self.gun.animate_rotation, [0,270,0], duration=0.1, delay=1, curve=curve.linear)
                invoke(setattr, self, 'reloading_anim', False, delay=1.2)
                while self.gun.patr < 3 and self.patron[0] > 0:
                    self.gun.patr += 1
                    self.patron[0] -= 1
                self.patrsh.text=f"{self.invent[1].patr}/{self.patron[0]}"
            if self.gun.name == "1":
                self.gun.animate_rotation([-40,180,0], duration=0.5,curve=curve.linear)
                self.gun.animate_position((original_pos[0], original_pos[1]-0.5, original_pos[2]), duration=0.4, curve=curve.linear)
                invoke(self.gun.animate_position, original_pos, duration=0.1, delay=1, curve=curve.linear)
                invoke(self.gun.animate_rotation, [0,180,0], duration=0.1, delay=1, curve=curve.linear)
                invoke(setattr, self, 'reloading_anim', False, delay=1)
                self.gun.patr = 15
                self.patrsh.text="15/∞"
        if key=="/"and not self.menu.enabled:
            self.position+=[0,15,0]
        if key=="1"and not self.menu.enabled:
            self.gun.enabled=False
            self.gun=self.invent[0]
            self.gun.enabled=True
            player.patrsh.text=f"{player.invent[0].patr}/∞"
        if key=="2"and not self.menu.enabled:
            if len(self.invent)>1:
                self.gun.enabled=False
                self.gun=self.invent[1]
                self.gun.enabled=True
                player.patrsh.text=f"{player.invent[1].patr}/{player.patron[0]}"
        if key=="escape":
            if player.menu.enabled:
                player.mouse_sensitivity = (40, 40)
                self.painlev.enabled=False
            else:
                player.mouse_sensitivity = (0, 0)
                self.btn_restart.on_click=reset
                self.painlev.enabled=True
            self.menu.enabled=not self.menu.enabled
            mouse.locked = not self.menu.enabled
            mouse.visible = self.menu.enabled
            player.cursor.enabled = not self.menu.enabled

        
            

    def onhit(self, damage,a):
        self.shp.alpha += damage / 300
        if self.armor==0:
            self.hp -= damage
            self.health_bar.scale_x -= damage*0.01
        else:
            player.armo_bar.scale_x-=damage*0.02
            self.armor-=damage
        if self.shp.color!=color.red and self.armor>0:
            self.shp.color=color.red
            self.shp.alpha=0
        print(self.hp)
        if self.hp <= 0:
            self.shp.alpha += 0.3
            global pausa
            pausa = True
            player.enabled = False
            self.deadtext=Text(text='Конец игры', origin=(0, 0), scale=2, enabled=True)


class Enemys(Entity):
    def __init__(self, hp, damage,index, **par):
        self.ismove=False
        self.dead = False
        self.moving = False
        self.obn=True
        self.damage = damage
        self.hp = hp
        self.last_p=None
        self.index=index
        self.inv=[]
        super().__init__(**par)

        # ГОЛОВА
        self.head = Entity(parent=self, model='cube', color=color.white, scale=(0.7, 1.0, 0.7), position=(0, 1, 0),collider="box")
        # РУКИ
        self.left_arm = Entity(parent=self, model='cube', color=color.white, scale=(0.3, 1.3, 0.3),position=(-0.6, 0.5, 0), origin_y=0.5,collider="box")
        self.right_arm = Entity(parent=self,color=color.white, model='cube', scale=(0.3, 1.3, 0.3), position=(0.6, 0.5, 0), origin_y=0.5,collider="box")
        self.gun=Entity(parent=self.right_arm,damage=self.damage,color=color.black,model="cube",scale=(0.5,0.3,0.5),position=(0,-1.1,0),origin_y=0.5)
        # НОГИ
        self.left_leg = Entity(parent=self, model='cube', color=color.white, scale=(0.4, 1, 0.4),position=(-0.35, -0.6, 0), origin_y=0.5,collider="box")
        self.right_leg = Entity(parent=self, model='cube', color=color.white, scale=(0.4, 1, 0.4),position=(0.35, -0.6, 0), origin_y=0.5,collider="box")
    
    def onhit(self, damage,u):
        if self.dead:
            return
        if u==self.head:damage=damage*2
        elif u==self.left_leg or self.right_leg:damage=damage/2
        self.hp -= damage
        u.color = color.red
        u.animate_color(color.white, duration=0.3)
        print(self.hp)
        if self.hp <= 0:
            tryps.append(Entity(name="tryp",model='cube', position=[self.world_position[0], -0.5, self.world_position[2]], color=color.red,collider='box',scale=(1,0.5,1),patr=int(random.randint(0,2))))
            self.dead = True
            self.inv.clear()
            self.animations.clear()
            for child in self.children:
                child.animations.clear()
            for i in self.inv:
                if i:i.kill()
            self.inv.clear()
            if self.collider:self.collider = None
            if self in enemy: 
                enemy.remove(self)
            self.enabled = False
            destroy(self,delay=5)
            return
        if (player.world_position-self.world_position).length()<30:
            self.obnor()
        else:
            self.last_p=player.world_position
            self.haunt()
    def obnor(self):
        if self.dead:
            return
        ignor=[self]+self.children
        ray=raycast(origin=self.world_position,direction=(camera.world_position - self.world_position).normalized(),distance=100,ignore=ignor)
        if ray.entity==player and self.obn:
            self.obn=False
            self.last_p=player.world_position
            rel_x = player.world_x - self.world_x
            rel_z = player.world_z - self.world_z
            angle = math.degrees(math.atan2(rel_x, rel_z))
            self.animate_rotation((0, angle, 0), duration=0.3)
            self.right_arm.animate_rotation((-90, 0, 30), duration=0.3) 
            self.inv.append(invoke(fire,self.gun,delay=1))
            self.inv.append(invoke(self.right_arm.animate_rotation, (0, 0, 0), duration=0.3, delay=1))
            self.inv.append(invoke(setattr,self,'obn',True,delay=1))
            if (player.world_position - self.world_position).length()>7:
                self.animations.clear()
                self.haunt()
    def haunt(self):
        if self.dead:
            return
        if (player.world_position - self.world_position).length() < 10:
            self.moving = False
            self.inv.append(invoke(self.haunt, delay=0.5))
            return

        index = self.index
        curr_room = room[index]
        speed = 4.0  
        
        neighbors = [r for r in room if 7.5 < (r.world_position - curr_room.world_position).length() < 8.5]
        best_kom = curr_room
        min_dist = (self.last_p - best_kom.world_position).length()

        opposite = {'n': 's', 's': 'n', 'e': 'w', 'w': 'e'}

        for neighbor in neighbors:
            diff = neighbor.world_position - curr_room.world_position
            side = ('n' if diff.z > 5 else 's' if diff.z < -5 else 
                    'e' if diff.x > 5 else 'w' if diff.x < -5 else None)
            
            if side:
                has_exit_wall = any(c.name == side for c in curr_room.children)
                has_entry_wall = any(c.name == opposite[side] for c in neighbor.children)
                
                if not has_exit_wall and not has_entry_wall:
                    n_idx = room.index(neighbor)
                    is_occupied = any(en.index == n_idx for en in enemy if en != self and not en.dead)
                    
                    if not is_occupied:
                        d = (self.last_p - neighbor.world_position).length()
                        if d < min_dist:
                            min_dist = d
                            best_kom = neighbor

        if best_kom != curr_room:
            self.moving = True
            for part in [self, self.left_leg, self.right_leg, self.left_arm, self.right_arm]:
                if hasattr(part, 'animations'): part.animations.clear()
            
            dist_to_center = (self.world_position - curr_room.world_position).length()
            time_to_center = dist_to_center / speed
            dist_to_next = (best_kom.world_position - curr_room.world_position).length()
            time_to_next = dist_to_next / speed
            rel_to_center = curr_room.world_position - self.world_position
            if rel_to_center.length() > 0.1:
                center_angle = math.degrees(math.atan2(rel_to_center.x, rel_to_center.z))
                self.animate_rotation((0, center_angle, 0), duration=0.1)
                self.animate_position(curr_room.world_position, duration=time_to_center, curve=curve.linear)
            

            self.index = room.index(best_kom) 
            
            rel_move = best_kom.world_position - curr_room.world_position
            move_angle = math.degrees(math.atan2(rel_move.x, rel_move.z))
            
            move_delay = time_to_center + 0.1
            self.inv.append(invoke(self.animate_rotation, (0, move_angle, 0), duration=0.1, delay=time_to_center))
            self.inv.append(invoke(self.animate_position, best_kom.world_position, duration=time_to_next, delay=move_delay, curve=curve.linear))
            

            step_t = 0.5
            for i in range(int(time_to_next / (step_t * 2))):
                d_step = move_delay + (i * step_t * 2)
                self.inv.append(invoke(self.left_leg.animate_rotation, (50,0,0), duration=step_t, delay=d_step))
                self.inv.append(invoke(self.right_leg.animate_rotation, (-50,0,0), duration=step_t, delay=d_step))
                self.inv.append(invoke(self.left_leg.animate_rotation, (-50,0,0), duration=step_t, delay=d_step + step_t))
                self.inv.append(invoke(self.right_leg.animate_rotation, (50,0,0), duration=step_t, delay=d_step + step_t))

            total_time = move_delay + time_to_next
            self.inv.append(invoke(setattr, self, 'moving', False, delay=total_time))
            self.inv.append(invoke(self.haunt, delay=total_time + 0.5))
        else:
            self.moving = False 
            self.inv.append(invoke(self.haunt, delay=0.5))
        
    def move(self):
        if self.dead or not self.enabled:
            return
        self.ismove=True   
        self.animate_rotation((0,random.uniform(0,180),0),duration=4)
        self.inv.append(invoke(setattr,self,'ismove',False,delay=6))
    
def fire(obj):
    if obj.parent==camera:
        if player.gun.name=="1":
            player.patrsh.text=f"{player.invent[0].patr}/∞"
        elif player.gun.name=="drobo":
            destroy(player.patrsh)
            player.patrsh=Text(text=f"{player.invent[1].patr}/{player.patron[0]}", position=(-0.8, -0.4))
        start_pos = camera.world_position + camera.forward * 1.5
        napr = camera.forward
    else:
        if obj.parent.parent.dead:
            destroy(obj)
            return
        start_pos = obj.world_position + (player.position - obj.world_position).normalized() * 1.5
        napr = (camera.world_position - obj.world_position).normalized()

    count = 8 if obj.name == "drobo" else 1
    razbros = 0.04

    for i in range(count):

        if count > 1:
            napr = napr + Vec3(
                random.uniform(-razbros, razbros),
                random.uniform(-razbros, razbros),
                random.uniform(-razbros, razbros)
            )
            napr = napr.normalized()
        else:
            napr = napr


        bulet = Entity(
            model="cube", 
            position=start_pos, 
            scale=0.05 if count > 1 else 0.1, 
            color=color.orange, 
            collider='sphere', 
            ot=4, 
            owner=obj, 
            live=180,
            name="dr"if count>1 else ""
        )
        bulet.dir = napr
        bulet.speed = 50
        bulet.look_at(bulet.position + napr)
        bulles.append(bulet)

def update():
    global pausa
    if pausa:return
    dt = time.dt
    for i in bulles[:]:
        step = i.dir * i.speed * dt
        if hasattr(i.owner, 'parent'):
            i.owner=i.owner.parent
        ignore_list = [i, i.owner]
        ignore_list.extend(bulles)
        if hasattr(i.owner, 'children'):
            ignore_list.extend(i.owner.children)
        ray = raycast(i.world_position, i.dir, distance=step.length() + 0.1, ignore=ignore_list)
        if ray.hit:
            target = None
            if hasattr(ray.entity, "onhit"):
                target = True
                ray.entity.onhit(ray.entity.damage, ray.entity)
            elif ray.entity.parent and hasattr(ray.entity.parent, "onhit"):
                target = True
                ray.entity.parent.onhit(ray.entity.parent.damage, ray.entity)

            if target:
                if i in bulles: bulles.remove(i)
                destroy(i)
            elif hasattr(ray.entity, "riko"):
                if i.name=="dr":
                    bulles.remove(i)
                    destroy(i)
                    continue
                ray.entity.riko(i, ray.world_point, ray.world_normal)
            else:
                if i in bulles: bulles.remove(i)
                destroy(i)
        else:
            i.position += step
            i.live -= 1
            if i.live <= 0:
                if i in bulles: bulles.remove(i)
                destroy(i)
    stolk=player.intersects()
    if str(stolk.entity)=='armor':
        player.armor=50
        player.shp.color=color.green
        player.shp.alpha +=0.2
        if player.armo_bar.enabled==False:
            player.armo_bar.enabled=True
            player.armo_bar_bg.enabled=True
        else:
            player.armo_bar.scale_x=1
        print(1)
        destroy(stolk.entity)
    if str(stolk.entity)=='heal':
        player.hp+=100-player.hp
        player.shp.alpha=0
        player.health_bar.scale_x = 1
        print(1)
        destroy(stolk.entity)
    if str(stolk.entity)=='drobo':
        stolk.entity.enabled=False
        stolk.entity.collider=None
        stolk.entity.rotation=[0,270,0]
        stolk.entity.scale=[0.2,0.2,0.2]
        stolk.entity.parent=camera
        stolk.entity.position=(0.7, -1.2, 1)
        player.invent.append(stolk.entity)
    if str(stolk.entity)=='tryp':
        player.patron[0]+=stolk.entity.patr
        stolk.entity.patr=0
        if player.gun.name=="drobo":
            player.patrsh.text=f"{player.invent[1].patr}/{player.patron[0]}"
    if str(stolk.entity) == 'fin':
        pausa = True
        player.enabled = False          
        mouse.locked = False            
        mouse.visible = True            
        player.fin_menu=Entity(parent=camera.ui, model='quad', scale=(0.9, 0.9),color=color.black90)
        player.stats_text = Text(
        text=f'Победа!\nВремя: {player.time} сек\n Враги: {int(abs((len(enemy) - player.maxvr) / player.maxvr * 100))}%',
        origin=(0, 0),
        scale=2,
        position=(0, 0.2),
        parent=camera.ui,
        color=color.white
        )
        player.rebtn = Button(
        text='Рестарт',
        parent=camera.ui,
        scale=(0.3, 0.1),
        position=(0, -0.3),
        on_click=reset
        )

    for i in enemy[:]:
        if i.hp<=0 or i.dead:
            continue
        if (player.world_position-i.world_position).length()<10 and player.speed >6:
            i.obnor()
        elif (player.world_position-i.world_position).length()<30:
            razn=(player.world_position-i.world_position).normalized()
            dot = Vec3.dot(i.forward, razn)
            if dot > 0.85: 
                i.obnor()
            elif not player.shot :
                i.obnor()
        if not i.moving:
            rel = player.world_position - i.world_position
            target_angle = math.degrees(math.atan2(rel.x, rel.z))
            i.rotation_y = target_angle 
        elif not i.ismove and (player.world_position-i.world_position).length()<60:  
            i.move()
    global time_tick_flag
    if hasattr(player,"text_time")and time_tick_flag and player.text_time != None:
        player.time+=1
        player.text_time.text=str(player.time)
        time_tick_flag=False
        invoke(reset_time_tick_flag,delay=1)
    if held_keys['left shift']:player.speed = 10
    else:player.speed = 6
def unpause():
    global pausa
    pausa = False


ap = Ursina()

def input(key):
    if not pausa:
        check_directions = [
        Vec3(1,0,0), Vec3(-1,0,0), Vec3(0,0,1), Vec3(0,0,-1), 
        Vec3(1,0,1).normalized(), Vec3(1,0,-1).normalized(), 
        Vec3(-1,0,1).normalized(), Vec3(-1,0,-1).normalized()
        ]
        for d in check_directions:
            hit = raycast(player.world_position + [0,1,0], d, distance=0.7, ignore=[player]+room[grid_size*grid_size-1].n.children )
            if hit.hit:
                overlap = 0.7 - hit.distance
                player.position -= d * overlap
        if player.painlev.text.isdigit() and player.painlev.enabled:
            print(1)
            player.levpain = int(player.painlev.text)
            if player.levpain>=25:player.levpain=20
            if player.levpain<=5:player.levpain=5
        player.imp(key)
    else:player.imp("escape")
player = Player(100, name="pel", collider='capsule', height=2, radius=0.5, scale=(1.3, 1.3, 1.3), speed=7, jump_height=3,position=[-8,2,-8],gravity = 0 )
grid_size = player.levpain
start_rom=[]
start=None



Sky()
camera.clip_plane_near = 0.01
window.cog_button.enabled = False
ground=[]
room = []
items_list = []
enemy = []
item_entities = []
grid_size = player.levpain

def reset():
    global pausa, room, enemy, item_entities, bulles, tryps, start_rom, start
    
    pausa = True  

    for s in application.sequences[:]:
        s.kill()


    for e in scene.entities:
        if hasattr(e, 'inv'):
            for i in e.inv:
                if i: i.kill()
            e.inv.clear()

    protected = [player, camera, camera.ui]
    
    for e in scene.entities[:]:
        if e in protected: continue
        if isinstance(e, Sky): continue
        

        is_protected = False
        temp = e
        while temp.parent:
            if temp.parent in protected:
                is_protected = True
                break
            temp = temp.parent
        
        if is_protected: continue


        e.enabled = False
        if hasattr(e, 'collider') and e.collider:
            e.collider = None
        destroy(e)

    room.clear()
    enemy.clear()
    item_entities.clear()
    bulles.clear()
    tryps.clear()
    start_rom.clear()
    start = None

    player.hp = 100
    if hasattr(player, 'health_bar'): player.health_bar.scale_x = 1
    if hasattr(player, 'fin_menu'): destroy(player.fin_menu)
    player.armor = 0
    if str(player.gun)=="drobo":player.gun.enabled=False
    if hasattr(player, 'armo_bar'): player.armo_bar.enabled = False
    player.position = (-8, 3, -8)
    player.shp.color=color.red
    player.shp.alpha = 0
    player.enabled = False

    
    if len(player.invent) > 1:
        player.invent = [player.invent[0]] 
        player.gun = player.invent[0]
        player.gun.enabled = True
    
    invoke(set_map, delay=0.1)
    invoke(unpause, delay=1.1)
def set_map():    
    global room, enemy, item_entities,start,start_rom,start,ground,grid_size
    grid_size = player.levpain
    ground = Entity(model='plane', scale=[grid_size*11,0.5,grid_size*11], texture='32', texture_scale=(grid_size*3, grid_size*3), collider='box',position=((grid_size/2)*6,-0.7,(grid_size/2)*6),color=color.gray)

    for i in range(grid_size):
        for j in range(grid_size):
            s = Surface(rom="armor", position=Vec3(i*8, 1, j*8))
            s.gx, s.gz = i, j
            room.append(s)

    curr = room[0]
    curr.hashole = True
    room[grid_size*grid_size-1].n.texture="qw"
    final=Entity(parent=room[grid_size*grid_size-1].n,model='cube',texture='fas',scale=(0.2, 0.4, 0.1),position=(0, 0, -0.51),collider='box',name="fin")

    for _ in range(len(room) * 4):
        x, z = curr.gx, curr.gz
        neighbors = [(0, 1, 'n', 's'), (0, -1, 's', 'n'), (1, 0, 'e', 'w'), (-1, 0, 'w', 'e')]
        
        possible_moves = []
        for dx, dz, my_w, his_w in neighbors:
            nx, nz = x + dx, z + dz
            if 0 <= nx < grid_size and 0 <= nz < grid_size:
                nb = room[nx * grid_size + nz]
                if not nb.hashole:
                    possible_moves.append((nb, my_w, his_w))
        
        if possible_moves:
            next_room, my_w, his_w = random.choice(possible_moves)
            for child in list(curr.children):
                if child.name == my_w: destroy(child)
            for child in list(next_room.children):
                if child.name == his_w: destroy(child)
            next_room.hashole = True
            curr = next_room
        else:
            visited = [r for r in room if r.hashole]
            if visited: curr = random.choice(visited)
    seen_walls = []
    for r in room:
        for child in list(r.children):
            if hasattr(child, 'model') and child.model:
                pos = child.world_position
                if any((pos - p).length() < 1.0 for p in seen_walls):
                    destroy(child)
                else:
                    seen_walls.append(pos)

    items_pool = ([1]*int((grid_size/3))) + ([2]*int((grid_size/3))) + ([3]*int((grid_size))) + ([0]*(grid_size**2 - 25))
    random.shuffle(items_pool)
    drob_chance = random.uniform(0, 10)
    
    for idx, r in enumerate(room):
        if (idx == grid_size-1 and drob_chance >= 5) or (idx == (grid_size*grid_size)-grid_size and drob_chance < 5):
            Entity(patr=3,model="Shotgun", parent=r,scale=0.1,rotation=(90,0,0),texture="res/32", color=color.black,world_position=r.world_position-[0,1,0],name="drobo",collider="box")
        rd = items_pool.pop() if items_pool else 0
        if rd == 1:
            item_entities.append(Entity(scale=0.01,name="armor", collider="box", model="shield.obj", parent=r, position=(random.uniform(0,2), -0.5, random.uniform(0,2)), color=color.green))
        elif rd == 2:  
            item_entities.append(Entity(name="heal", collider="box", model="sphere", parent=r,position=(random.uniform(0,2), 0, random.uniform(0,2)),color=color.red))
        elif rd == 3:  
            vr = Enemys(100, 10, idx, model='cube', color=color.white, collider="box",world_position=(r.world_x + random.uniform(0,2), 1.0, r.world_z + random.uniform(0,2)))
            vr.world_parent = scene
            enemy.append(vr)
    start_rom=[Surface(rom="armor", position=[-8,0,0]),Surface(rom="armor", position=[-8,0,-8])]
    player.enabled=True
    for attr in ['text_time', 'stats_text', 'rebtn', 'deadtext']:
        if hasattr(player, attr) and getattr(player, attr) is not None:
            destroy(getattr(player, attr))
            setattr(player, attr, None)
    player.time=0
    destroy(start_rom[1].n)
    destroy(start_rom[0].s)
    start=Entity(damage=1,collider="box",model="sphere",position=[-8,2,3],color=color.yellow,onhit=lambda *a: (room[0].w.animate_position([room[0].w.position[0],-6,room[0].w.position[2]],duration=5),destroy(start),setattr(player,"text_time",Text(text=str(player.time),position=(-0.83, 0.35)))))
    destroy(start_rom[0].e)
    player.maxvr=len(enemy)
    invoke(setattr,player,"gravity",1,delay=1)
    
set_map()


ap.run()