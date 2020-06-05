from abc import abstractmethod
import arcade
import random
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

WIN_WIDTH = 800
WIN_HEIGHT = 800

class Problem:

    def __init__(self):
        self.problem_text = ""
        self.points_right = 0
        self.points_wrong = 0

    @abstractmethod
    def solve(self, response):
        pass


class Factors_Problem(Problem):

    def __init__(self):
        super().__init__()
        self.value = random.randint(2,100)
        self.problem_text = "Find Factors of {}".format(self.value)
        self.points_right = 5
        self.points_wrong = -1

    def solve(self, response):
        if self.value % response == 0:
            return self.points_right
        else:
            return self.points_wrong

class Player(arcade.Sprite):

    def __init__(self):
        super().__init__()
        self.texture = arcade.load_texture("penguin.png")
        self.scale = 0.1
        self.center_x = WIN_WIDTH//2
        self.center_y = 50
    
    def move_left(self):
        if self.center_x <= 10:
            self.center_x <= 10
        else:
            self.center_x -= 5

    def move_right(self):
        if self.center_x >= WIN_WIDTH - 10:
            self.center_x = WIN_WIDTH - 10
        else:        
            self.center_x += 5

class Precip(arcade.Sprite):

    def __init__(self):
        super().__init__()
        self.center_x = random.randint(10, WIN_WIDTH-10)
        self.center_y = WIN_HEIGHT - 10
        self.change_x = random.uniform(-2, 2)
        self.change_y = random.uniform(-0.1, -2)

    def update(self):
        self.center_x += self.change_x
        self.center_y += self.change_y
        if self.center_x < 0 or self.center_x > WIN_WIDTH:
            self.change_x *= -1
        if self.center_y < 0:
            self.remove_from_sprite_lists()

    @abstractmethod
    def hit(self, problem):
        pass

class Number_Precip(Precip):

    def __init__(self):
        super().__init__()
        self.number = random.randint(2,9)
        self.texture = Number_Precip.convert_text_to_texture(str(self.number))

    @staticmethod
    def convert_text_to_texture(text_value):
        img = Image.new('RGBA', (75,75), color = (255, 255, 255, 0))
        d = ImageDraw.Draw(img) 
        fnt = ImageFont.truetype('absender1.ttf', 100)
        d.text((15,5), text_value, font=fnt, fill=(255, 0, 0)) 
        texture = arcade.Texture(str(text_value), img) 
        return texture

    def hit(self, problem):
        self.remove_from_sprite_lists()
        return problem.solve(self.number)

class Snow_Precip(Precip):

    def __init__(self):
        super().__init__()
        self.texture = arcade.load_texture("snowflake.png")
        self.scale = 0.1

    def hit(self, problem):
        self.remove_from_sprite_lists()
        return 5 

class Lightning_Precip(Precip):

    def __init__(self):
        super().__init__()
        self.texture = arcade.load_texture("lightning.png")
        self.scale = 0.05

    def hit(self, problem):
        self.remove_from_sprite_lists()
        return -5

    
class Game(arcade.Window):

    def __init__(self):
        super().__init__(WIN_WIDTH,WIN_HEIGHT,"Math Showers")
        self.player = Player()
        self.precip = arcade.SpriteList()
        self.keys_pressed = set()
        self.score = 0
        self.background = arcade.load_texture("background.jpg")
        self.problem = None
        self.problem_timer = 0
        
    def on_draw(self):
        arcade.start_render()
        arcade.draw_texture_rectangle(WIN_WIDTH//2, WIN_HEIGHT//2, WIN_WIDTH, WIN_HEIGHT, self.background)
        
        self.player.draw()
        self.precip.draw()

        if self.problem is not None:
            arcade.draw_text(self.problem.problem_text, WIN_WIDTH//3, WIN_HEIGHT - 50, arcade.color.WHITE, 36)

        output = f"Score: {self.score}"
        arcade.draw_text(output, 10, 20, arcade.color.WHITE, 14)

        output = f"Timer: {self.problem_timer // 100}"
        arcade.draw_text(output, WIN_WIDTH - 100, 20, arcade.color.WHITE, 14)
   

    def on_update(self, delta_time):
        self.check_pressed_keys()
        self.create_precip()
        self.create_problem()
        self.precip.update()
        hit_list = arcade.check_for_collision_with_list(self.player, self.precip)
        for precip in hit_list:
            self.score += precip.hit(self.problem)

    def create_problem(self):
        if self.problem_timer == 0:
            self.problem = Factors_Problem()
            self.problem_timer = 2000
        else:
            self.problem_timer -= 1
     
    def create_precip(self):
        if random.randint(1,80) == 1:
            precip = Number_Precip()
            self.precip.append(precip)
        if random.randint(1,200) == 1:
            precip = Snow_Precip()
            self.precip.append(precip)
        if random.randint(1,200) == 1:
            precip = Lightning_Precip()
            self.precip.append(precip)

    def on_key_press(self, key, modifiers):
        self.keys_pressed.add(key)

    def on_key_release(self, key, modifiers):
        self.keys_pressed.remove(key)

    def check_pressed_keys(self):
        if arcade.key.LEFT in self.keys_pressed:
            self.player.move_left()
        if arcade.key.RIGHT in self.keys_pressed:
            self.player.move_right()

window = Game()
arcade.run()
