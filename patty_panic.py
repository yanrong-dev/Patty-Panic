import functools
import random

import pygame

import assets
import configs

from objects.background import Background
from objects.countdown import Countdown
from objects.customer import Customer
from objects.floor import Floor
from objects.game_over_message import GameOverMessage
from objects.game_phase import GamePhase
from objects.game_start_message import GameStartMessage
from objects.hamburger import Hamburger
from objects.ingredient import Ingredient, get_layer_from_name
from objects.jenny import Jenny
from objects.layer import Layer
from objects.level_complete_message import LevelCompleteMessage
from objects.score import Score
from objects.welcome import Welcome

pygame.init()

screen = pygame.display.set_mode((configs.SCREEN_WIDTH, configs.SCREEN_HEIGHT))
clock = pygame.time.Clock()
hide_welcome_event = pygame.USEREVENT
spawn_ingredient_event = pygame.USEREVENT + 1
next_level_event = pygame.USEREVENT + 2
reset_game_event = pygame.USEREVENT + 3
floor_y = 0
running = True
start_ticks = 0
cheat_mode = False
previous_ingredient = ""

assets.load_sprites()
assets.load_audio()

sprites = pygame.sprite.LayeredUpdates()

game_over_message = None
jenny = None
countdown = None
game_start_message = None
score = None
current_order_visualize = None
customer = None
current_order = []
ingredients_on_tray = []

game_phase = GamePhase.WELCOME
current_level = 1
welcome = Welcome(sprites)
pygame.time.set_timer(hide_welcome_event, 2000)
pygame.display.set_caption('Patty Panic')
pygame_icon = assets.get_sprite("icon")
pygame.display.set_icon(pygame_icon)


def setup_game(with_start=True):
    global floor_y, current_level
    global game_start_message, score
    global jenny, countdown, current_order_visualize, customer
    Background(sprites)
    floor = Floor(sprites)
    floor_y = floor.get_floor_y()
    jenny = Jenny(floor_y, sprites)
    countdown = Countdown(sprites)
    customer = Customer(floor_y, sprites)
    current_order_visualize = Hamburger(sprites, ingredients=[])
    generate_new_order(current_order_visualize)
    interval = configs.SPAWN_INGREDIENT_INTERVAL
    interval_noise = configs.SPAWN_INGREDIENT_NOISE * interval
    interval += random.uniform(-1 * interval_noise, interval_noise)
    pygame.time.set_timer(spawn_ingredient_event, int(interval))
    if with_start:
        game_start_message = GameStartMessage(sprites)
    score = Score(sprites)
    score.set_level(current_level)


def compare_ingredients(ing1, ing2):
    layer1 = int(get_layer_from_name(ing1))
    layer2 = int(get_layer_from_name(ing2))
    #print(ing1, " vs ", ing2, ", -> ", layer1, " vs ", layer2)
    if layer1 < layer2:
        return -1
    elif layer1 > layer2:
        return 1
    else:
        return 0


# Calling
def add_collected_ingredient(ingredient):
    global ingredients_on_tray
    ingredients_on_tray.append(ingredient)
    #print("Before", ingredients_on_tray)
    ingredients_on_tray = sorted(ingredients_on_tray, key=functools.cmp_to_key(compare_ingredients))
    #print("After", ingredients_on_tray)

def get_next_missing_ingredient():
    missing = []
    for ing in current_order:
        if ing not in ingredients_on_tray:
            missing.append(ing)
    if len(missing) == 1:
        #print("Spawn ", missing[0])
        return missing[0]
    else:
        #print("Spawn ", missing[0], " or ", missing[1])
        return missing[0] if missing[0] != previous_ingredient else missing[1]

def generate_new_order(visualize):
    global current_order
    order = ['bun-bottom']
    order += random.sample(assets.search_sprite_by_names(['meat-']).keys(), 1)
    if current_level >= 3:
        order += random.sample(assets.search_sprite_by_names(['cheese-']).keys(), 1)
    if current_level >= 5:
        order += random.sample(assets.search_sprite_by_names(['topping-']).keys(), 1)
    num_veggi = 1
    if current_level > 7:
        num_veggi = 2
    order += random.sample(assets.search_sprite_by_names(['veggi-']).keys(), num_veggi)
    order.append('bun-top')
    visualize.set_ingredients(order)
    current_order = order

frames_since_last_teleport = 0
def teleport_jenny():
    missing = None
    for ing in current_order:
        if ing not in ingredients_on_tray:
            missing = ing
            break
    if missing is None:
        return
    global frames_since_last_teleport
    frames_since_last_teleport += configs.FPS / 20
    jenny_width = jenny.rect.width
    jenny_y = jenny.rect.y
    if (frames_since_last_teleport % configs.FPS == 0):
        # teleport once per .05 second
        teleport_to_x = None
        teleport_to_y = None

        for sprite in sprites:
            if sprite.rect.y > jenny_y - 5:
                # probably too late
                continue
            if hasattr(sprite, 'ingredient_name') and sprite.ingredient_name == missing:
                if teleport_to_x is None or teleport_to_y < sprite.rect.y:
                    teleport_to_x = sprite.rect.x - sprite.rect.width / 2
                    teleport_to_y = sprite.rect.y
        if teleport_to_x is None:
            jenny.teleport_to(configs.SCREEN_WIDTH - jenny_width / 2)
        else:
            #print("Should teleport to ", teleport_to_x, teleport_to_y)
            if teleport_to_y < jenny_y - 100:
                # too far away
                #print("Wait a while")
                jenny.teleport_to(configs.SCREEN_WIDTH - jenny_width / 2)
            else:
                #print("Do it now")
                jenny.teleport_to(teleport_to_x)


while running:
    if game_phase == GamePhase.WELCOME:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == hide_welcome_event:
                welcome.kill()
                game_phase = GamePhase.WAIT_TO_START
                setup_game()
    elif game_phase == GamePhase.WAIT_TO_START:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif (event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE) or event.type == pygame.MOUSEBUTTONDOWN:
                game_start_message.kill()
                if game_over_message is not None:
                    game_over_message.kill()
                game_phase = GamePhase.PLAYING
                start_ticks = pygame.time.get_ticks()
    elif game_phase == GamePhase.GAMEOVER:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == reset_game_event:
                pygame.time.set_timer(reset_game_event, 0)
            #elif (event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE) or event.type == pygame.MOUSEBUTTONDOWN:
                print("Restart game")
                game_over_message.kill()
                sprites.empty()
                setup_game()
                game_phase = GamePhase.WAIT_TO_START
    elif game_phase == GamePhase.LEVEL_COMPLETE:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == next_level_event:
                pygame.time.set_timer(next_level_event, 0)
                level_complete_message.kill()
                game_phase = GamePhase.PLAYING
                current_level += 1
                start_ticks = pygame.time.get_ticks()
                print("Playing level ", current_level)
                sprites.empty()
                setup_game(with_start=False)

    elif game_phase == GamePhase.PLAYING:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == spawn_ingredient_event:
                spawn_missing_ingredient_prob = configs.SPAWN_MISSING_INGREDIENT_PROB * configs.DIFFICULTY_FACTOR ** (
                            current_level - 1)
                if random.uniform(0, 1) <= spawn_missing_ingredient_prob:
                    if not configs.ENFORCE_INGREDIENTS_ORDER:
                        missing_ingredients = set(current_order) - set(ingredients_on_tray)
                        #print("Spawn one of ", missing_ingredients)
                        ingredient_name = random.sample(missing_ingredients, 1)[0]
                    else:
                        ingredient_name = get_next_missing_ingredient()
                    ing = Ingredient(floor_y, sprites, name=ingredient_name)
                else:
                    #print("Randomly spawn")
                    ing = Ingredient(floor_y, sprites, prevent=previous_ingredient)
                previous_ingredient = ing.get_ingredient_name()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    print("Restarted")
                    game_phase = GamePhase.WAIT_TO_START
                    sprites.empty()
                    setup_game()
                elif event.key == pygame.K_c:
                    cheat_mode = not cheat_mode
                else:
                    jenny.handle_event(event)
            elif event.type == pygame.MOUSEMOTION:
                jenny.handle_event(event)

    # screen.fill("pink")
    sprites.draw(screen)

    if game_phase == GamePhase.PLAYING:
        if cheat_mode:
            teleport_jenny()
        seconds_elapsed = (pygame.time.get_ticks() - start_ticks) / 1000
        seconds_left = configs.SECONDS_PER_ROUND - seconds_elapsed
        countdown.set_time(seconds_left)
        collected = jenny.check_collision(sprites)
        if collected != None:
            add_collected_ingredient(collected.get_ingredient_name())
            collected.kill()
            good_collection = True
            if configs.ENFORCE_INGREDIENTS_ORDER:
                good_collection = ingredients_on_tray[-1] == current_order[len(ingredients_on_tray) - 1]
            else:
                good_collection = len(set(ingredients_on_tray)) >= len(ingredients_on_tray) and (set(ingredients_on_tray) <= set(current_order))
            if not good_collection:
                assets.play_audio('buzzer')
                ingredients_on_tray = []
            elif len(set(ingredients_on_tray)) == len(current_order):
                score.value += 1
                if score.value < configs.GOALS_PER_ROUND:
                    assets.play_audio('hooray')
                generate_new_order(current_order_visualize)
                ingredients_on_tray = []
            else:
                assets.play_audio('collect')
            jenny.update_collected_ingredients(ingredients_on_tray)
            if score.value >= configs.GOALS_PER_ROUND:
                # level complete
                game_phase = GamePhase.LEVEL_COMPLETE
                level_complete_message = LevelCompleteMessage(sprites)
                assets.play_audio("trumpet")
                pygame.time.set_timer(next_level_event, 2500)
                print("Finished level ", current_level, " with ", countdown.time_left, " seconds left")
        if countdown.time_left <= 0:
            game_phase = GamePhase.GAMEOVER
            pygame.time.set_timer(reset_game_event, 2500)
            current_level = 1
            game_over_message = GameOverMessage(sprites)
            pygame.time.set_timer(spawn_ingredient_event, 0)
            assets.play_audio("error")

        sprites.update()

    pygame.display.flip()
    clock.tick(configs.FPS)
pygame.quit()
