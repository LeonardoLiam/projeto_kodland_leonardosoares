import pgzrun
import random
import math

WIDTH = 800
HEIGHT = 600

class Blow:
    def __init__(self, center, attack=0.25):
        self.center = center
        self.radius = 0
        self.max_radius = 150
        self.growth_rate = 2
        self.alpha = 255
        self.fade_rate = 5
        self.active = False
        self.interval = 200
        self.timer = 0
        self.attack = attack
        self.level = 1
    
    def update(self):
        self.timer += 1
        if self.timer >= self.interval:
            self.timer = 0
            self.activate()
        
        if self.active:
            self.radius += self.growth_rate
            self.alpha -= self.fade_rate
            if self.alpha <= 0:
                self.active = False
                self.radius = 0

    def activate(self):
        self.active = True
        self.radius = 0
        self.alpha = 255

    def draw(self):
        if self.active:
            for i in range(5):
                alpha_factor = (1 - i/5)
                radius = self.radius - i * 10
                if radius > 0:
                    color = (0, int(150 * alpha_factor), int(255 * alpha_factor))
                    screen.draw.circle(self.center, radius, color)

class Enemy:
    def __init__(self, hp, speed):
        x = random.randint(0, WIDTH)
        y = random.randint(0, HEIGHT)
        self.actor = Actor("flyfly1", (x, y))
        self.hp = hp
        self.speed = speed
        self.attack = 1
        self.position = ''
        self.animation = False
        self.actual_image = 'flyfly2'
    
    def change_image(self):
        
        if self.actual_image == "flyfly1" + self.position:
            self.actual_image = "flyfly2" + self.position
        else:
            self.actual_image = "flyfly1" + self.position
        self.actor.image = self.actual_image

    def move(self, target):
        dx = target.x - self.actor.x
        dy = target.y - self.actor.y
        angle = math.atan2(dy, dx)
        
        if math.cos(angle) > 0:
            self.position = '_flip'
        else:
            self.position = ''
        

        self.actor.x += self.speed * math.cos(angle)
        self.actor.y += self.speed * math.sin(angle)

        if not self.animation:
            self.animation = True
            clock.schedule_interval(self.change_image, 0.5)

    def take_damage(self, center, radius, blow):
        
        enemy_rect = (
            self.actor.x - self.actor.width // 2,
            self.actor.y - self.actor.height // 2,
            self.actor.width,
            self.actor.height
        )

        if circle_rect_collide(center, radius, enemy_rect) and radius != 0:
            self.hp -= blow.attack
            sounds.attack.play()

    def draw(self):
        self.actor.draw()

class Enemy2:
    def __init__(self, hp, speed):
        x = random.randint(WIDTH, WIDTH + 200)
        y = random.randint(HEIGHT, HEIGHT + 200)
        self.actor = Actor("alien1", (x, y))
        self.hp = hp
        self.speed = speed
        self.attack = 1
        self.position = ''
        self.animation = False
        self.actual_image = 'alien2'
    
    def change_image(self):
        
        if self.actual_image == "alien1" + self.position:
            self.actual_image = "alien2" + self.position
        else:
            self.actual_image = "alien1" + self.position
        self.actor.image = self.actual_image

    def move(self, target):
        dx = target.x - self.actor.x
        dy = target.y - self.actor.y
        angle = math.atan2(dy, dx)
        
        if math.cos(angle) < 0:
            self.position = '_flip'
        else:
            self.position = ''
        

        self.actor.x += self.speed * math.cos(angle)
        self.actor.y += self.speed * math.sin(angle)

        if not self.animation:
            self.animation = True
            clock.schedule_interval(self.change_image, 0.5)

    def take_damage(self, center, radius, blow):
        
        enemy_rect = (
            self.actor.x - self.actor.width // 2,
            self.actor.y - self.actor.height // 2,
            self.actor.width,
            self.actor.height
        )

        if circle_rect_collide(center, radius, enemy_rect) and radius != 0:
            self.hp -= blow.attack
            sounds.attack.play()

    def draw(self):
        self.actor.draw()

class SuperHero:
    def __init__(self):
        self.actor = Actor('hero1', (WIDTH / 2, HEIGHT / 2))
        self.hp = 15
        self.max_hp = 15
        self.xp = 0
        self.level = 1
        self.xp_to_next = 5
        self.blow_level = 1
        self.speed = 1
        self.cooldown = 50
        self.cooldown_max = 50
        self.position = ''
        self.animation = False
        self.actual_image = 'hero5'
        self.idle_index = 0
        self.idle_animating = False

    def change_image(self):
        if self.actual_image == "hero5" + self.position:
            self.actual_image = "hero6" + self.position
        else:
            self.actual_image = "hero5" + self.position
        self.actor.image = self.actual_image

    def idle_animation(self):
        if not self.idle_animating:
            return
        self.idle_index = (self.idle_index + 1) % 3
        self.actor.image = f"hero{self.idle_index + 1}{self.position}"

    def move(self):
        self.actor.x = max(0, min(self.actor.x, 1024))
        self.actor.y = max(0, min(self.actor.y, 1024))

        moving = False

        if keyboard.left:
            self.position = '_flip'
            self.actor.x -= self.speed
            
            moving = True

        if keyboard.right:
            self.position = ''
            self.actor.x += self.speed
            
            moving = True

        if keyboard.up:
            self.actor.y -= self.speed
            moving = True

        if keyboard.down:
            self.actor.y += self.speed
            moving = True

        if moving:
            if self.idle_animating:
                self.idle_animating = False
                clock.unschedule(self.idle_animation)
            if not self.animation:
                
                self.actual_image = "hero4" + self.position
                self.actor.image = self.actual_image
                self.animation = True
                clock.schedule_interval(self.change_image, 0.5)

        else:
            if self.animation:
                self.animation = False
                clock.unschedule(self.change_image)
            if not self.idle_animating:
                self.idle_animating = True
                self.idle_index = 0
                clock.schedule_interval(self.idle_animation, 0.5)

    def attack_enemy(self, enemies):
        for enemy in enemies:
            if precise_collision(self.actor, enemy.actor):
                self.hp -= round(enemy.attack / 50, 2)
                sounds.pain.play()

    def gain_xp(self, amount):
        self.xp += amount
        if self.xp >= self.xp_to_next:
            self.level += 1
            self.xp -= self.xp_to_next
            self.xp_to_next += 5
            return True
        return False

    def draw(self):
        self.actor.draw()

class PausedGame:

    def __init__(self):
        self.title = "Jogo pausado"
        self.options = ["Continuar", "Sair"]
        self.selected = 0


    def draw(self):
        screen.draw.filled_rect(Rect((100,100), (600, 400)), "#5a6ec0")
        screen.draw.text(self.title, center = (WIDTH//2, 200),  fontname='pixeltype', fontsize=80)

        for i, option in enumerate(self.options):
            self.color = 'yellow' if i == self.selected else 'white'
            screen.draw.text(option, center=(WIDTH//2, 350 + i *50), fontsize=40,  fontname='pixeltype', color = self.color)

    def on_key_down(self, key):
        global game_state, game
        if key == keys.UP:
            self.selected = (self.selected - 1) % len(self.options)
            sounds.menu_select.play()
        elif key == keys.DOWN:
            sounds.menu_select.play()
            self.selected = (self.selected + 1) % len(self.options)
        elif key == keys.RETURN:
            sounds.menu_select.play()
            if self.options[self.selected] == "Continuar":
                return False
            elif self.options[self.selected] == "Sair":
                game_state = 'menu'
                game = None
        return True

class EndGame:

    def __init__(self, title):
        self.title = title
        self.options = ["Sair"]
        self.selected = 0
        self.message = ""


    def draw(self):
        
        screen.draw.filled_rect(Rect((100,100), (600, 400)), "#5a6ec0")
        screen.draw.text(self.title, center = (WIDTH//2, 200),  fontname='pixeltype', fontsize=80)
        screen.draw.text(self.message, center = (WIDTH//2, 250),  fontname='pixeltype', fontsize=40)


        for i, option in enumerate(self.options):
            self.color = 'yellow' if i == self.selected else 'white'
            screen.draw.text(option, center=(WIDTH//2, 350 + i *50), fontsize=40,  fontname='pixeltype', color = self.color)

    def on_key_down(self, key):
        global game_state, game
        if key == keys.UP:
            self.selected = (self.selected - 1) % len(self.options)
        elif key == keys.DOWN:
            self.selected = (self.selected + 1) % len(self.options)
        elif key == keys.RETURN:
            sounds.menu_select.play()
            if self.options[self.selected] == "Sair":
                game_state = 'menu'
                game = None
        return True 

class Game:
    def __init__(self):
        self.hero = SuperHero()
        self.blow = Blow(self.hero.actor.pos)
        self.menu_paused = PausedGame()
        self.camera_x = 0
        self.camera_y = 0
        self.map_width = 1024
        self.map_height = 1024
        self.enemies = []
        self.time_passed = 0
        self.upgrade = False
        self.paused = False
        self.won = False
        self.lost = False
        self.upgrade_options = []
        self.enemies_defeat = 0
        self.endgame = EndGame('')

        clock.schedule_interval(self.atualizar_tempo, 1.0)

    def atualizar_tempo(self):
        if not (self.paused or self.upgrade or self.won or self.lost):
            self.time_passed += 1
            if self.time_passed >= 300:
                sounds.victory.play()
                self.won = True


    def update(self):
        global game_state, game

        if self.upgrade or self.won or self.lost or self.paused:
            return

        clock.schedule_interval(game.spawn_enemy, 1.5)

        self.hero.move()
        self.hero.attack_enemy(self.enemies)
        self.blow.center = self.hero.actor.pos
        self.blow.update()

        self.camera_x = max(0, min(self.hero.actor.x - WIDTH // 2, self.map_width - WIDTH))
        self.camera_y = max(0, min(self.hero.actor.y - HEIGHT // 2, self.map_height - HEIGHT))

        if self.hero.hp < 1:
            sounds.attack.stop()
            sounds.pain.stop()
            sounds.death.play()
            self.hero.actor.image = 'hero_dead'
            self.lost = True

        circle_center = (self.hero.actor.x, self.hero.actor.y)
        circle_radius = self.blow.radius

        for enemy in self.enemies[:]:
            enemy.move(self.hero.actor)
            enemy.take_damage(circle_center, circle_radius, self.blow)
            if enemy.hp <= 0:
                self.enemies_defeat += 1
                self.enemies.remove(enemy)
                if self.hero.gain_xp(1):

                    self.trigger_upgrade()

        


    def draw_blow(self, blow):
        if blow.active:
            for i in range(5):
                alpha_factor = (1 - i / 5)
                radius = blow.radius - i * 10
                if radius > 0:
                    color = (0, int(150 * alpha_factor), int(255 * alpha_factor))
                    draw_x = blow.center[0] - self.camera_x
                    draw_y = blow.center[1] - self.camera_y
                    screen.draw.circle((draw_x, draw_y), radius, color)

    def draw_actor(self, actor):
        screen.blit(actor.image, (actor.x - self.camera_x - actor.width // 2, actor.y - self.camera_y - actor.height // 2))

    def draw(self):
        screen.blit("background_city.png", (-self.camera_x, -self.camera_y))

        self.draw_actor(self.hero.actor)
        self.draw_blow(self.blow)

        for enemy in self.enemies:
            self.draw_actor(enemy.actor)

        self.draw_ui()

        if self.upgrade:
            self.draw_upgrade_menu()

        if self.paused:
            self.menu_paused.draw()


        if self.won:
            sounds.adventure.stop()
            self.endgame.title = "Venceu!"
            self.endgame.message = f"Inimigos derrotados: {self.enemies_defeat}"
            self.endgame.draw()

        if self.lost:
            sounds.adventure.stop()
            self.endgame.title = "Derrota!"
            self.endgame.message = "Pratique um pouco mais que vai conseguir!"
            self.endgame.draw()


    def on_key_down(self, key):
        if not self.paused:
            if key == keys.RETURN:
                self.paused = True
                sounds.pause.play()

        else:
            self.paused = self.menu_paused.on_key_down(key)

        if self.lost:
            self.endgame.on_key_down(key)
        
        if self.won:
            self.endgame.on_key_down(key)

    def spawn_enemy(self):
        elapsed = self.time_passed
        max_enemies = 15 + (elapsed // 120) * 15
        if len(self.enemies) < max_enemies:
            hp = 1 + (elapsed // 60)
            speed = 1.5 + (elapsed // 240)

            if random.randint(0, 1) == 0:
                self.enemies.append(Enemy(hp, speed))
            else:
                self.enemies.append(Enemy2(hp, speed))

    def trigger_upgrade(self):

        self.upgrade = True

        self.bonus = ['+1 HP']

        if self.blow.attack < 0.75:
            self.bonus.append('+1 ATK')

        if self.hero.max_hp < 25:
            self.bonus.append('+2 HP Max')

        if self.hero.speed < 2:
            self.bonus.append('+1 Velocidade')

        if self.blow.interval > 50:
            self.bonus.append('Sopro')

        self.choices = 2 if len(self.bonus) > 1 else 1
        self.upgrade_options = random.sample(self.bonus, self.choices)

    def draw_upgrade_menu(self):

        screen.draw.filled_rect(Rect((100, 100), (600, 400)), "#5a6ec0")
        screen.draw.text("Escolha um upgrade:", center=(WIDTH // 2, HEIGHT // 2 - 100), fontsize=75, fontname='pixeltype', color="white")
        for i, option in enumerate(self.upgrade_options):
            y = HEIGHT // 2 + i * 50
            screen.draw.textbox(option, Rect(WIDTH // 2 - 150, y, 300, 40), color='white', fontname='pixeltype', background="blue")

    def draw_ui(self):
        bar_width = 200
        bar_height = 20
        x, y = 10, 10
        percentage = self.hero.hp / self.hero.max_hp
        screen.draw.filled_rect(Rect((x, y), (bar_width, bar_height)), "gray")
        screen.draw.filled_rect(Rect((x, y), (bar_width * percentage, bar_height)), 'red')
        screen.draw.text(f"HP: {int(self.hero.hp)}", (x + 5, y + 2), fontsize=20, fontname='pixeltype', color="white")
        screen.draw.text(f"XP: {self.hero.xp}", (10, 40), fontsize=24, fontname='pixeltype', color="white")
        screen.draw.text(f"Level: {self.hero.level}", (10, 70), fontsize=24, fontname='pixeltype', color="yellow")

        if self.won or self.lost or self.upgrade or self.paused:
            return
        else:
            t = self.time_passed
        minutes, seconds = t // 60, t % 60
        screen.draw.text(f"Time: {minutes:02}:{seconds:02}", (WIDTH - 150, 10), fontsize=30, fontname="pixeltype", color='lightblue')
        screen.draw.text(f"Inimigos eliminados: {self.enemies_defeat}", (WIDTH - 400, 10), fontsize=30, fontname="pixeltype", color='lightblue')


    def on_mouse_down(self, pos):
        if self.upgrade:
            for i, option in enumerate(self.upgrade_options):
                y = HEIGHT // 2 + i * 50
                rect = Rect(WIDTH // 2 - 150, y, 300, 40)
                if rect.collidepoint(pos):
                    self.apply_upgrade(option)
                    self.upgrade = False

    def apply_upgrade(self, option):
        if option == '+1 ATK':
            self.blow.attack += 1
        elif option == '+2 HP Max':
            self.hero.max_hp += 2
        elif option == '+1 Velocidade':
            self.hero.speed += 0.5
        elif option == 'Sopro':
            self.blow.interval -= 15
        elif option == '+1 HP':
            if self.hero.hp < self.hero.max_hp:
                self.hero.hp += 1

class Menu:

    def __init__(self):

        self.options = ["Iniciar", "Sair", "Som: On"]
        self.selected = 0

    def draw(self):
        screen.clear()
        # screen.draw.text(self.title, center = (WIDTH//2, 100), fontsize=60)
        screen.blit('opening', (0,0))
        
        for i, option in enumerate(self.options):
            self.color = '#5a6ec0' if i == self.selected else 'white'
            screen.draw.text(option, center=(400, 300 + i * 50), fontname='pixeltype', fontsize=50, color = self.color)

    def on_key_down(self, key):
        global status_sound

        if key == keys.UP:
            self.selected = (self.selected - 1) % len(self.options)
            sounds.menu_select.play()
        elif key == keys.DOWN:
            self.selected = (self.selected + 1) % len(self.options)
            sounds.menu_select.play()
        elif key == keys.RETURN:
            sounds.menu_select.play()
            if self.options[self.selected] == "Iniciar":
                return 'play'
            elif self.options[self.selected] == "Sair":
                exit()
            elif self.options[self.selected] == f"Som: On" or self.options[self.selected] == f"Som: Off":
                if status_sound:
                    status_sound = False
                else:
                    status_sound = True
        return "menu"




def precise_collision(actor1, actor2):
    hitbox1 = Rect((actor1.x - 10, actor1.y - 10), (20, 20))
    hitbox2 = Rect((actor2.x - 10, actor2.y - 10), (20, 20))
    return hitbox1.colliderect(hitbox2)

game_state = "menu"
status_sound = True
menu = Menu()
last_stage_option = None
last_status_sound = None
game = None

def play_opening():
    if status_sound:
        sounds.opening.play()
        clock.schedule(play_opening, sounds.opening.get_length())

def play_adventure():
    if status_sound:
        sounds.adventure.play()
        clock.schedule(play_adventure, sounds.adventure.get_length())

def stop_all_songs():
    sounds.opening.stop()
    sounds.adventure.stop()
    clock.unschedule(play_opening)
    clock.unschedule(play_adventure)


def update():
    global last_stage_option, last_status_sound, game

    if game_state != last_stage_option or status_sound != last_status_sound:
        stop_all_songs()

        if game_state == "menu":

            if status_sound:
                play_opening()
                menu.options[2] = "Som: On"
            else:
                menu.options[2] = "Som: Off"

        elif game_state == "play":
            if status_sound:
                play_adventure()
            game = Game()

        last_stage_option = game_state 
        last_status_sound = status_sound
        

    if game_state == "play":
        game.update()


def draw():
    screen.clear()
    if game_state == "menu":
        menu.draw()
    elif game_state == "play":
        game.draw()

def on_mouse_down(pos):
    game.on_mouse_down(pos)

def on_key_down(key):
    global game_state
    if game_state == "menu":
        game_state = menu.on_key_down(key)
    elif game_state == "play":
        game.on_key_down(key)

def circle_rect_collide(circle_center, circle_radius, rect):
        cx, cy = circle_center
        rx, ry, rw, rh = rect

        closest_x = max(rx, min(cx, rx + rw))
        closest_y = max(ry, min(cy, ry + rh))

        dx = cx - closest_x
        dy = cy - closest_y

        return dx * dx + dy * dy <= circle_radius * circle_radius

pgzrun.go()
