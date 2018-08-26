# Rapid Roll Lite 1.0
# By Arnob Paul
# https://arnobpl.github.io
# arnobpl@gmail.com


# The following values are game settings

Screen_Width = 1280
Screen_Height = 720
Screen_Center = 1
Screen_Left = 10
Screen_Top = 10
Full_Screen = 0
Focus_Locked = 1
Game_Speed = 30

building_width_screen = 0.25

safe_bar_width0 = 160
safe_bar_width1 = 200
safe_bar_width2 = 280

danger_bar_width0 = 160
danger_bar_width1 = 200
danger_bar_width2 = 280

window_difference_x = 200
window_difference_y = 200
first_window_x = 40
window_floor_distance = 57
karnisa_length = 100
window_karnisa_distance = 5

game_speed_factor = 1.0001
bar_create_frequency = 100
bar_move_step = 3
bar_type_condition = 80
safe_bar_size_condition0 = 30
safe_bar_size_condition1 = 70
danger_bar_size_condition0 = 30
danger_bar_size_condition1 = 70
max_danger_bar_once = 2
safe_bar_animation_condition = 8
danger_bar_animation_condition = 2

cloud_enabled = 1
cloud_create_frequency0 = 7
cloud_create_frequency1 = 15
cloud_move_step0 = 1
cloud_move_step1 = 2
cloud_scale = 0.7

initial_ball_position = 0.75
ball_move_step_x_keyboard_enabled = 1
ball_move_step_x_keyboard = 15
ball_move_step_x_keyboard_acceleration = 4
ball_move_step_x_mouse_enabled = 1
ball_move_step_y = 10
ball_move_step_y_acceleration = 1
ball_crashed_delay = 30

initial_life_items_gain = 2
max_life_items_gain = 5
initial_life_item_create_condition = 15
life_item_create_condition_factor = 0.999
life_item_crashed_delay = 10

data_directory_name = "Data"
icon_data_file_name = "rapid_roll_icon.png"
sprite_data_file_name = "rapid_roll_sprites.png"


# The above values are game settings


def f_range(start, stop, step):
    if step == 0 or (start > stop and step > 0) or (start < stop and step < 0):
        return []
    if start > stop:
        start, stop = stop, start
        step *= -1
    f_list = []
    while start < stop:
        f_list.append(start)
        start += step
    return f_list


def lerp(value, start, stop, step):
    value += step
    if value < start:
        return start, -step
    if value > stop:
        return stop, -step
    return value, step


ERROR = 0
try:
    print("\nPress ESC to exit the game...")
    from time import sleep

    sleep(1)
    loading_str = "Loading, Please Wait..."
    print("\n\n" + loading_str + "\n\n")

    import os
    import sys

    data_directory_full_path = os.path.join(sys.path[0], data_directory_name)

    import pygame
    from random import randrange
    from math import ceil, floor
    from pygame.locals import *

    pygame.init()

    if Full_Screen:
        # Screen_Width = pygame.display.Info().current_w
        # Screen_Height = pygame.display.Info().current_h
        screen = pygame.display.set_mode((Screen_Width, Screen_Height), FULLSCREEN | HWSURFACE | DOUBLEBUF | NOFRAME)
    else:
        if Screen_Center:
            os.environ["SDL_VIDEO_CENTERED"] = "1"
        else:
            os.environ["SDL_VIDEO_WINDOW_POS"] = "\"" + str(Screen_Left) + "," + str(Screen_Top) + "\""
        screen = pygame.display.set_mode((Screen_Width, Screen_Height), HWSURFACE | DOUBLEBUF | NOFRAME)

    ERROR = 1
    font = pygame.font.Font(None, 40)
    screen.blit(font.render(loading_str, True, (255, 255, 255)), (
        (Screen_Width >> 1) - (font.size(loading_str)[0] >> 1),
        (Screen_Height >> 1) - (font.size(loading_str)[1] >> 1)))
    pygame.display.update()

    ERROR = 2
    pygame.display.set_icon(pygame.image.load(os.path.join(data_directory_full_path, icon_data_file_name)))

    ERROR = 3
    image_data = pygame.image.load(os.path.join(data_directory_full_path, sprite_data_file_name)).convert_alpha()

    # Initial loading successful
    ERROR = 0

except Exception as exception:
    try:
        pygame.quit()
    except:
        pass
    print('\n' * 150 + "Fatal Error!")
    print(exception)

    if ERROR == 0:
        print("Pygame module is missing or invalid.\nPlease install Pygame using the command: \"pip install pygame\"")
    elif ERROR == 1:
        print("Font component of Pygame module is missing or invalid.")
    elif ERROR == 2:
        print("\"" + icon_data_file_name + "\" file is missing or invalid.")
    elif ERROR == 3:
        print("\"" + sprite_data_file_name + "\" file is missing or invalid.")

    print("\n Support: arnobpl@gmail.com\n\n https://arnobpl.github.io\n\n\nPress ENTER to exit..." + '\n' * 8)
    input()

if ERROR == 0:

    # Background
    background_colour = 153, 217, 234
    background = pygame.Surface((round(Screen_Width * (1 - building_width_screen)), Screen_Height))
    R_step = 20
    R_start = background_colour[0] - R_step
    R_stop = background_colour[0] + R_step
    G_step = 20
    G_start = background_colour[1] - G_step
    G_stop = background_colour[1] + G_step
    B_step = 20
    B_start = background_colour[2] - B_step
    B_stop = background_colour[2] + B_step
    R = randrange(R_start, R_stop)
    G = randrange(G_start, G_stop)
    B = randrange(B_start, B_stop)
    background.fill((R, G, B))
    background_left = round(Screen_Width * building_width_screen / 2)

    # Ball
    ball = []
    ball.append(image_data.subsurface((0, 0, 40, 40)))
    ball.append(image_data.subsurface((40, 0, 40, 40)))
    ball.append(image_data.subsurface((80, 0, 40, 40)))
    ball.append(image_data.subsurface((120, 0, 40, 40)))
    ball.append(pygame.transform.flip(ball[2], True, False))
    ball.append(pygame.transform.flip(ball[1], True, False))
    ball.append(image_data.subsurface((160, 0, 40, 40)))

    # Life Item
    life_item = []
    life_item.append(image_data.subsurface((160, 40, 40, 40)))
    life_item.append(pygame.transform.flip(life_item[0], True, False))
    life_item.append(image_data.subsurface((160, 80, 40, 40)))
    life_item.append(pygame.transform.flip(life_item[2], True, False))

    # Safe Bar Main
    safe_bar = []
    safe_bar.append(image_data.subsurface((120, 40, 10, 20)))
    safe_bar.append(image_data.subsurface((130, 40, 10, 20)))
    safe_bar.append(pygame.transform.flip(safe_bar[1], True, False))

    # Safe Bar 0
    safe_bar0 = []
    safe_bar0.append(pygame.Surface((safe_bar_width0, 20), SRCALPHA, 32).convert_alpha())
    for i in range(10, safe_bar_width0 - 10, 10):
        safe_bar0[0].blit(safe_bar[0], (i, 0))
    safe_bar0[0].blit(safe_bar[1], (0, 0))
    safe_bar0[0].blit(safe_bar[2], (safe_bar_width0 - 10, 0))
    safe_bar0.append(pygame.transform.flip(safe_bar0[0], True, False))

    # Safe Bar 1
    safe_bar1 = []
    safe_bar1.append(pygame.Surface((safe_bar_width1, 20), SRCALPHA, 32).convert_alpha())
    for i in range(10, safe_bar_width1 - 10, 10):
        safe_bar1[0].blit(safe_bar[0], (i, 0))
    safe_bar1[0].blit(safe_bar[1], (0, 0))
    safe_bar1[0].blit(safe_bar[2], (safe_bar_width1 - 10, 0))
    safe_bar1.append(pygame.transform.flip(safe_bar1[0], True, False))

    # Safe Bar 2
    safe_bar2 = []
    safe_bar2.append(pygame.Surface((safe_bar_width2, 20), SRCALPHA, 32).convert_alpha())
    for i in range(10, safe_bar_width2 - 10, 10):
        safe_bar2[0].blit(safe_bar[0], (i, 0))
    safe_bar2[0].blit(safe_bar[1], (0, 0))
    safe_bar2[0].blit(safe_bar[2], (safe_bar_width2 - 10, 0))
    safe_bar2.append(pygame.transform.flip(safe_bar2[0], True, False))

    # Danger Bar Main
    danger_bar = []
    danger_bar.append(image_data.subsurface((140, 40, 10, 20)))
    danger_bar.append(image_data.subsurface((150, 40, 10, 20)))
    danger_bar.append(pygame.transform.flip(danger_bar[1], True, False))

    # Danger Bar 0
    danger_bar0 = []
    danger_bar0.append(pygame.Surface((danger_bar_width0, 20), SRCALPHA, 32).convert_alpha())
    for i in range(10, danger_bar_width0 - 10, 10):
        danger_bar0[0].blit(danger_bar[0], (i, 0))
    danger_bar0[0].blit(danger_bar[1], (0, 0))
    danger_bar0[0].blit(danger_bar[2], (danger_bar_width0 - 10, 0))
    danger_bar0.append(pygame.transform.flip(danger_bar0[0], True, False))

    # Danger Bar 1
    danger_bar1 = []
    danger_bar1.append(pygame.Surface((danger_bar_width1, 20), SRCALPHA, 32).convert_alpha())
    for i in range(10, danger_bar_width1 - 10, 10):
        danger_bar1[0].blit(danger_bar[0], (i, 0))
    danger_bar1[0].blit(danger_bar[1], (0, 0))
    danger_bar1[0].blit(danger_bar[2], (danger_bar_width1 - 10, 0))
    danger_bar1.append(pygame.transform.flip(danger_bar1[0], True, False))

    # Danger Bar 2
    danger_bar2 = []
    danger_bar2.append(pygame.Surface((danger_bar_width2, 20), SRCALPHA, 32).convert_alpha())
    for i in range(10, danger_bar_width2 - 10, 10):
        danger_bar2[0].blit(danger_bar[0], (i, 0))
    danger_bar2[0].blit(danger_bar[1], (0, 0))
    danger_bar2[0].blit(danger_bar[2], (danger_bar_width2 - 10, 0))
    danger_bar2.append(pygame.transform.flip(danger_bar2[0], True, False))

    # Top Spike Main
    top_spike = []
    top_spike.append(pygame.transform.flip(image_data.subsurface((120, 60, 10, 20)), False, True))
    top_spike.append(pygame.transform.flip(image_data.subsurface((130, 60, 10, 20)), False, True))
    top_spike.append(pygame.transform.flip(top_spike[1], True, False))

    # Top Spike Object
    top_spike_surface = pygame.Surface((background.get_width(), 20), SRCALPHA, 32).convert_alpha()
    for i in range(10, background.get_width() - 10, 10):
        top_spike_surface.blit(top_spike[0], (i, 0))
    top_spike_surface.blit(top_spike[1], (0, 0))
    top_spike_surface.blit(top_spike[2], (background.get_width() - 10, 0))

    # Bottom Spike Main
    bottom_spike = []
    bottom_spike.append(image_data.subsurface((140, 60, 10, 20)))
    bottom_spike.append(image_data.subsurface((150, 60, 10, 20)))
    bottom_spike.append(pygame.transform.flip(bottom_spike[1], True, False))

    # Bottom Spike Object
    bottom_spike_surface = pygame.Surface((background.get_width(), 20), SRCALPHA, 32).convert_alpha()
    for i in range(10, background.get_width() - 10, 10):
        bottom_spike_surface.blit(bottom_spike[0], (i, 0))
    bottom_spike_surface.blit(bottom_spike[1], (0, 0))
    bottom_spike_surface.blit(bottom_spike[2], (background.get_width() - 10, 0))

    # Cloud
    cloud = []
    cloud.append(image_data.subsurface((0, 40, 120, 80)))
    cloud.append(pygame.transform.flip(cloud[0], True, False))
    cloud.append(pygame.transform.smoothscale(cloud[0], (round(120 * cloud_scale), round(80 * cloud_scale))))
    cloud.append(pygame.transform.flip(cloud[2], True, False))

    # Display
    score_display = image_data.subsurface((160, 120, 40, 40))
    life_display = image_data.subsurface((160, 160, 40, 40))

    # Building Texture 0
    building_texture0 = [image_data.subsurface((120, 80, 15, 15)),
                         pygame.transform.rotate(image_data.subsurface((120, 112, 15, 2)), 90)]

    # Building Texture 1
    building_texture1 = [image_data.subsurface((135, 80, 25, 15)),
                         pygame.transform.rotate(image_data.subsurface((135, 112, 15, 2)), 90)]

    # Building Window 0
    building_window0 = [image_data.subsurface((0, 120, 80, 80))]

    # Building Window 1
    building_window1 = [image_data.subsurface((80, 120, 80, 80))]

    # Building Ornaments 0
    building_ornaments0 = [image_data.subsurface((120, 95, 20, 10)),
                           image_data.subsurface((120, 105, 20, 5)),
                           pygame.transform.rotate(image_data.subsurface((120, 110, 10, 2)), 90),
                           pygame.transform.rotate(image_data.subsurface((140, 110, 5, 2)), 90)]

    # Building Ornaments 1
    building_ornaments1 = [image_data.subsurface((140, 95, 20, 10)),
                           image_data.subsurface((140, 105, 20, 5)),
                           pygame.transform.rotate(image_data.subsurface((130, 110, 10, 2)), 90),
                           pygame.transform.rotate(image_data.subsurface((145, 110, 5, 2)), 90)]

    # Window Karnisa 0
    window_karnisa_surface0 = pygame.Surface((karnisa_length, 10), SRCALPHA, 32).convert_alpha()
    for i in range(0, karnisa_length, 20):
        window_karnisa_surface0.blit(building_ornaments0[0], (i, 0))
    window_karnisa_surface0.blit(building_ornaments0[2], (0, 0))
    window_karnisa_surface0.blit(pygame.transform.flip(building_ornaments0[2], True, False), (karnisa_length - 2, 0))

    # Window Karnisa 1
    window_karnisa_surface1 = pygame.Surface((karnisa_length, 10), SRCALPHA, 32).convert_alpha()
    for i in range(0, karnisa_length, 20):
        window_karnisa_surface1.blit(building_ornaments1[0], (i, 0))
    window_karnisa_surface1.blit(building_ornaments1[2], (0, 0))
    window_karnisa_surface1.blit(pygame.transform.flip(building_ornaments1[2], True, False), (karnisa_length - 2, 0))

    building_width = ceil(Screen_Width * building_width_screen / 2)

    building0 = pygame.Surface((building_width, Screen_Height + 14), SRCALPHA, 32).convert_alpha()
    for i in range(0, Screen_Height + 15, 15):
        for j in range(0, building_width + 15, 15):
            building0.blit(building_texture0[0], (j, i))
    for i in range(0, Screen_Height + 15, 15):
        building0.blit(building_texture0[1], (0, i))

    building1 = pygame.Surface((building_width, Screen_Height + 14), SRCALPHA, 32).convert_alpha()
    for i in range(0, Screen_Height + 15, 15):
        for j in range(0, building_width + 25, 25):
            building1.blit(building_texture1[0], (j, i))
    for i in range(0, Screen_Height + 15, 15):
        building1.blit(building_texture1[1], (0, i))

    building_window_surface0 = pygame.Surface((building_width, Screen_Height + window_difference_y - 1),
                                              SRCALPHA, 32).convert_alpha()
    for i in range(0, Screen_Height + window_difference_y, window_difference_y):
        for j in range(first_window_x, building_width + window_difference_x, window_difference_x):
            building_window_surface0.blit(building_window0[0], (j, i))
    for i in range(window_floor_distance + 80, Screen_Height + window_difference_y, window_difference_y):
        for j in range(0, building_width + window_difference_x, 20):
            building_window_surface0.blit(building_ornaments0[1], (j, i))
        building_window_surface0.blit(building_ornaments0[3], (0, i))
    for i in range(window_difference_y - window_karnisa_distance - 10, Screen_Height + window_difference_y,
                   window_difference_y):
        for j in range(first_window_x - round(karnisa_length / 2) + 40, building_width + window_difference_x,
                       window_difference_x):
            building_window_surface0.blit(window_karnisa_surface0, (j, i))

    building_window_surface1 = pygame.Surface((building_width, Screen_Height + window_difference_y - 1), SRCALPHA,
                                              32).convert_alpha()
    for i in range(0, Screen_Height + window_difference_y, window_difference_y):
        for j in range(first_window_x, building_width + window_difference_x, window_difference_x):
            building_window_surface1.blit(building_window1[0], (j, i))
    for i in range(window_floor_distance + 80, Screen_Height + window_difference_y, window_difference_y):
        for j in range(0, building_width + window_difference_x, 20):
            building_window_surface1.blit(building_ornaments1[1], (j, i))
        building_window_surface1.blit(building_ornaments1[3], (0, i))
    for i in range(window_difference_y - window_karnisa_distance - 10, Screen_Height + window_difference_y,
                   window_difference_y):
        for j in range(first_window_x - round(karnisa_length / 2) + 40, building_width + window_difference_x,
                       window_difference_x):
            building_window_surface1.blit(window_karnisa_surface1, (j, i))

    ball_list = []
    life_item_list = []
    safe_bar_list = []
    danger_bar_list = []
    cloud_list0 = []
    cloud_list1 = []
    building_list = []
    building_window_surface_list = []

    focus_has_lost = True
    bar_create_condition = 0
    danger_bar_once = 0
    safe_bar_animation_condition_value = 0
    danger_bar_animation_condition_value = 0
    safe_bar_animation_value = 0
    danger_bar_animation_value = 0
    cloud_create_condition0 = 0
    cloud_create_condition1 = 0
    no_ball_state = True
    ball_crashed = False
    life_item_crashed = False
    ball_move_step_x_keyboard_state = 0
    ball_animation_value = 0
    ball_crashed_delay_value = 0
    life_item_crashed_delay_value = 0
    building_left_right_selector = randrange(0, 2)
    score = 0
    life_items_gain = initial_life_items_gain
    danger_item_collided = False

    bar_move_step_value = bar_move_step
    cloud_move_step0_value = cloud_move_step0
    cloud_move_step1_value = cloud_move_step1
    life_item_create_condition = initial_life_item_create_condition

    ball_move_step_y_value = ball_move_step_y
    ball_move_step_x_keyboard_value = ball_move_step_x_keyboard

    if cloud_enabled:
        for i in f_range(Screen_Height - cloud_create_frequency0, -cloud[2].get_height(),
                         -cloud_create_frequency0 - cloud_move_step0):
            cloud_type = randrange(2, 4)
            max_cloud_position = background.get_width() - cloud[2].get_width() + background_left
            cloud_position = randrange(background_left - cloud[2].get_width(),
                                       max_cloud_position + cloud[2].get_width())
            cloud_list0.append([[cloud[cloud_type]], [cloud_position, i]])
        cloud_list0.reverse()

        for i in f_range(Screen_Height - cloud_create_frequency1, -cloud[0].get_height(),
                         -cloud_create_frequency1 - cloud_move_step1):
            cloud_type = randrange(0, 2)
            max_cloud_position = background.get_width() - cloud[0].get_width() + background_left
            cloud_position = randrange(background_left - cloud[0].get_width(),
                                       max_cloud_position + cloud[0].get_width())
            cloud_list1.append([[cloud[cloud_type]], [cloud_position, i]])
        cloud_list1.reverse()

    if building_left_right_selector == 0:
        building_list.append([pygame.transform.flip(building0, True, False), [background_left - building_width, 0], 15])
        building_list.append([building1, [background_left + background.get_width(), 0], 15])
        building_window_surface_list.append(
            [pygame.transform.flip(building_window_surface0, True, False), [background_left - building_width, 0],
             window_difference_y])
        building_window_surface_list.append(
            [building_window_surface1, [background_left + background.get_width(), 0], window_difference_y])
    else:
        building_list.append([pygame.transform.flip(building1, True, False), [background_left - building_width, 0], 15])
        building_list.append([building0, [background_left + background.get_width(), 0], 15])
        building_window_surface_list.append(
            [pygame.transform.flip(building_window_surface1, True, False), [background_left - building_width, 0],
             window_difference_y])
        building_window_surface_list.append(
            [building_window_surface0, [background_left + background.get_width(), 0], window_difference_y])

    r_step = 0.1
    g_step = -0.2
    b_step = -0.3

    pygame.mouse.set_visible(False)
    clock = pygame.time.Clock()
    print('\n' * 150)
    while True:

        clock.tick(Game_Speed)

        background.fill((R, G, B))
        screen.blit(background, (background_left, 0))
        R, r_step = lerp(R, R_start, R_stop, r_step)
        G, g_step = lerp(G, G_start, G_stop, g_step)
        B, b_step = lerp(B, B_start, B_stop, b_step)

        if bar_create_condition == 0:
            bar_type = randrange(0, 100)
            bar_size = randrange(0, 100)
            if bar_type < bar_type_condition or danger_bar_once >= max_danger_bar_once:
                danger_bar_once = 0
                life_item_create = randrange(0, 100)
                if bar_size < safe_bar_size_condition0:
                    max_bar_position = background.get_width() - safe_bar_width0 + background_left
                    bar_position = randrange(background_left, max_bar_position)
                    safe_bar_list.append([safe_bar0, [bar_position, Screen_Height + 40]])
                    if life_item_create < life_item_create_condition:
                        max_life_item_position = bar_position + safe_bar_width0 - 40
                        life_item_position = randrange(bar_position, max_life_item_position)
                        if life_item_position < round(Screen_Width / 2):
                            life_item_type = 0
                        else:
                            life_item_type = 1
                        life_item_list.append([[life_item[life_item_type]], [life_item_position, Screen_Height]])
                elif bar_size < safe_bar_size_condition1:
                    max_bar_position = background.get_width() - safe_bar_width1 + background_left
                    bar_position = randrange(background_left, max_bar_position)
                    safe_bar_list.append([safe_bar1, [bar_position, Screen_Height + 40]])
                    if life_item_create < life_item_create_condition:
                        max_life_item_position = bar_position + safe_bar_width1 - 40
                        life_item_position = randrange(bar_position, max_life_item_position)
                        if life_item_position < round(Screen_Width / 2):
                            life_item_type = 0
                        else:
                            life_item_type = 1
                        life_item_list.append([[life_item[life_item_type]], [life_item_position, Screen_Height]])
                else:
                    max_bar_position = background.get_width() - safe_bar_width2 + background_left
                    bar_position = randrange(background_left, max_bar_position)
                    safe_bar_list.append([safe_bar2, [bar_position, Screen_Height + 40]])
                    if life_item_create < life_item_create_condition:
                        max_life_item_position = bar_position + safe_bar_width2 - 40
                        life_item_position = randrange(bar_position, max_life_item_position)
                        if life_item_position < round(Screen_Width / 2):
                            life_item_type = 0
                        else:
                            life_item_type = 1
                        life_item_list.append([[life_item[life_item_type]], [life_item_position, Screen_Height]])
            else:
                danger_bar_once += 1
                if bar_size < danger_bar_size_condition0:
                    max_bar_position = background.get_width() - danger_bar_width0 + background_left
                    bar_position = randrange(background_left, max_bar_position)
                    danger_bar_list.append([danger_bar0, [bar_position, Screen_Height + 40]])
                elif bar_size < danger_bar_size_condition1:
                    max_bar_position = background.get_width() - danger_bar_width1 + background_left
                    bar_position = randrange(background_left, max_bar_position)
                    danger_bar_list.append([danger_bar1, [bar_position, Screen_Height + 40]])
                else:
                    max_bar_position = background.get_width() - danger_bar_width2 + background_left
                    bar_position = randrange(background_left, max_bar_position)
                    danger_bar_list.append([danger_bar2, [bar_position, Screen_Height + 40]])

        if cloud_enabled and cloud_create_condition0 == 0:
            cloud_type = randrange(2, 4)
            max_cloud_position = background.get_width() - cloud[2].get_width() + background_left
            cloud_position = randrange(background_left - cloud[2].get_width(),
                                       max_cloud_position + cloud[2].get_width())
            cloud_list0.append([[cloud[cloud_type]], [cloud_position, Screen_Height]])

        if cloud_enabled and cloud_create_condition1 == 0:
            cloud_type = randrange(0, 2)
            max_cloud_position = background.get_width() - cloud[0].get_width() + background_left
            cloud_position = randrange(background_left - cloud[0].get_width(),
                                       max_cloud_position + cloud[0].get_width())
            cloud_list1.append([[cloud[cloud_type]], [cloud_position, Screen_Height]])

        for i in cloud_list0:
            screen.blit(i[0][0], (round(i[1][0]), round(i[1][1])))
            i[1][1] -= cloud_move_step0_value

        for i in cloud_list1:
            screen.blit(i[0][0], (round(i[1][0]), round(i[1][1])))
            i[1][1] -= cloud_move_step1_value

        for i in safe_bar_list[::-1]:
            screen.blit(i[0][safe_bar_animation_value], (round(i[1][0]), round(i[1][1])))
            if no_ball_state and i[1][1] <= round(initial_ball_position * Screen_Height) and life_items_gain >= 0:
                ball_list.append(ball[ball_animation_value])
                ball_list.append([i[1][0] - 20 + round(i[0][0].get_width() / 2), i[1][1] - 40])
                if pygame.mouse.get_focused(): pygame.mouse.set_pos(ball_list[1])
                no_ball_state = False
                danger_item_collided = False
            i[1][1] -= bar_move_step_value

        if life_items_gain < 0 and (not ball_crashed):
            pygame.quit()
            print("Game is over!\nYour score is " + str(
                round(score * 0.1)) + ".\nThank you for playing this mini-game.\n\n\nPress ENTER to exit..." + '\n' * 8)
            input()
            break

        for i in danger_bar_list:
            screen.blit(i[0][danger_bar_animation_value], (round(i[1][0]), round(i[1][1])))
            i[1][1] -= bar_move_step_value

        if not no_ball_state:
            if not ball_crashed: ball_list[0] = ball[ball_animation_value]
            screen.blit(ball_list[0], (round(ball_list[1][0]), round(ball_list[1][1])))

        for i in life_item_list:
            screen.blit(i[0][0], (round(i[1][0]), round(i[1][1])))
            i[1][1] -= bar_move_step_value

        for i in building_list, building_window_surface_list:
            for j in range(0, 2):
                i[j][1][1] -= bar_move_step_value % i[j][2]
                if i[j][1][1] <= -i[j][2]:
                    i[j][1][1] += i[j][2]
                screen.blit(i[j][0], (round(i[j][1][0]), round(i[j][1][1])))

        screen.blit(top_spike_surface, (background_left, 0))
        screen.blit(bottom_spike_surface, (background_left, Screen_Height - 20))

        screen.blit(score_display, (10, Screen_Height - 50))
        screen.blit(font.render(str(round(score * 0.1)), True, (0, 0, 0)), (51, Screen_Height - 39))
        screen.blit(font.render(str(round(score * 0.1)), True, (38, 255, 125)), (50, Screen_Height - 40))
        screen.blit(life_display, (Screen_Width - 150, Screen_Height - 47))
        screen.blit(font.render(str(life_items_gain), True, (0, 0, 0)), (Screen_Width - 99, Screen_Height - 39))
        screen.blit(font.render(str(life_items_gain), True, (255, 127, 39)), (Screen_Width - 100, Screen_Height - 40))

        pygame.display.update()

        bar_create_condition += bar_move_step_value
        if bar_create_condition > bar_create_frequency:
            bar_create_condition = 0

        safe_bar_animation_condition_value += 1
        if safe_bar_animation_condition_value > safe_bar_animation_condition:
            safe_bar_animation_value += 1
            if safe_bar_animation_value > 1: safe_bar_animation_value = 0
            safe_bar_animation_condition_value = 0

        danger_bar_animation_condition_value += 1
        if danger_bar_animation_condition_value > danger_bar_animation_condition:
            danger_bar_animation_value += 1
            if danger_bar_animation_value > 1: danger_bar_animation_value = 0
            danger_bar_animation_condition_value = 0

        cloud_create_condition0 += cloud_move_step0_value
        if cloud_create_condition0 > cloud_create_frequency0:
            cloud_create_condition0 = 0

        cloud_create_condition1 += cloud_move_step1_value
        if cloud_create_condition1 > cloud_create_frequency1:
            cloud_create_condition1 = 0

        if ball_crashed:
            ball_crashed_delay_value += 1
            if ball_crashed_delay_value > ball_crashed_delay:
                ball_crashed_delay_value = 0
                ball_crashed = False
                ball_list.clear()
                no_ball_state = True

        if life_item_crashed:
            life_item_crashed_delay_value += 1
            if life_item_crashed_delay_value > life_item_crashed_delay:
                life_item_crashed_delay_value = 0
                life_item_crashed = False
                i = 0
                while i < len(life_item_list):
                    if life_item_list[i][0][0] == life_item[2] or life_item_list[i][0][0] == life_item[3]:
                        del life_item_list[i]
                        i -= 1
                    i += 1

        for i in safe_bar_list, danger_bar_list, cloud_list0, cloud_list1, life_item_list:
            j = 0
            while j < len(i):
                if i[j][1][1] + i[j][0][0].get_height() <= 0:
                    del i[j]
                    j -= 1
                j += 1

        pygame.event.pump()
        keystate = pygame.key.get_pressed()
        event = pygame.event.poll()
        if not pygame.mouse.get_focused():
            focus_has_lost = True
            if Focus_Locked:
                if not no_ball_state:
                    pygame.mouse.set_pos(ball_list[1])
                else:
                    pygame.mouse.set_pos((0, 0))
        if keystate[K_ESCAPE]:
            pygame.quit()
            break
        if (not no_ball_state) and (not ball_crashed):
            if ball_move_step_x_keyboard_enabled and keystate[K_LEFT]:
                if ball_list[1][0] - ball_move_step_x_keyboard_value > background_left:
                    ball_list[1][0] -= ball_move_step_x_keyboard_value
                    ball_move_step_x_keyboard_state = -1
                    if ball_move_step_x_keyboard_state == -1: ball_move_step_x_keyboard_value += ball_move_step_x_keyboard_acceleration
                    ball_animation_value += 1
                    if ball_animation_value > 5: ball_animation_value = 0
                else:
                    ball_list[1][0] = background_left
                if pygame.mouse.get_focused(): pygame.mouse.set_pos(ball_list[1])
            elif ball_move_step_x_keyboard_enabled and keystate[K_RIGHT]:
                if ball_list[1][0] + ball_move_step_x_keyboard_value < background_left + background.get_width() - 40:
                    ball_list[1][0] += ball_move_step_x_keyboard_value
                    ball_move_step_x_keyboard_state = +1
                    if ball_move_step_x_keyboard_state == +1: ball_move_step_x_keyboard_value += ball_move_step_x_keyboard_acceleration
                    ball_animation_value -= 1
                    if ball_animation_value < 0: ball_animation_value = 5
                else:
                    ball_list[1][0] = background_left + background.get_width() - 40
                if pygame.mouse.get_focused(): pygame.mouse.set_pos(ball_list[1])
            elif ball_move_step_x_mouse_enabled and event.type == MOUSEMOTION:
                if Focus_Locked or (not focus_has_lost):
                    mouse_pos_x = pygame.mouse.get_pos()[0]
                    if mouse_pos_x < ball_list[1][0]:
                        if mouse_pos_x >= background_left:
                            ball_list[1][0] = mouse_pos_x
                            ball_animation_value += 1
                            if ball_animation_value > 5: ball_animation_value = 0
                        else:
                            ball_list[1][0] = background_left
                            if pygame.mouse.get_focused(): pygame.mouse.set_pos(ball_list[1])
                    elif mouse_pos_x > ball_list[1][0]:
                        if mouse_pos_x <= background_left + background.get_width() - 40:
                            ball_list[1][0] = mouse_pos_x
                            ball_animation_value -= 1
                            if ball_animation_value < 0: ball_animation_value = 5
                        else:
                            ball_list[1][0] = background_left + background.get_width() - 40
                            if pygame.mouse.get_focused(): pygame.mouse.set_pos(ball_list[1])
                else:
                    if pygame.mouse.get_focused(): pygame.mouse.set_pos(ball_list[1])
                    focus_has_lost = False
            else:
                ball_move_step_x_keyboard_state = 0
                ball_move_step_x_keyboard_value = ball_move_step_x_keyboard

        if (not no_ball_state) or ball_crashed:
            ball_collided = False
            for i in safe_bar_list:
                if i[1][1] + bar_move_step_value > 60 and i[1][1] - 40 < ball_list[1][
                    1] + ball_move_step_y_value and ceil(i[1][1] - 40 + bar_move_step_value - ball_list[1][1]) >= 0 and \
                        i[1][0] - 20 <= ball_list[1][0] < i[1][0] + i[0][0].get_width() - 20:
                    ball_list[1][1] = i[1][1] - 40
                    ball_collided = True
                    ball_move_step_y_value = ball_move_step_y
                    for j in life_item_list:
                        if j[1][0] - 40 <= ball_list[1][0] < j[1][0] + 40 and ceil(j[1][1]) == ceil(i[1][1]) - 40 and (
                                j[0][0] == life_item[0] or j[0][0] == life_item[1]):
                            if j[0][0] == life_item[0]:
                                j[0][0] = life_item[2]
                            else:
                                j[0][0] = life_item[3]
                            life_item_crashed = True
                            if life_items_gain < max_life_items_gain: life_items_gain += 1
                            break
                    break
            if not ball_collided:
                for i in danger_bar_list:
                    if (
                            i[1][1] + bar_move_step_value > 60 and
                            i[1][1] - 40 < ball_list[1][1] + ball_move_step_y_value and
                            ceil(i[1][1] - 40 + bar_move_step_value - ball_list[1][1]) >= 0 and
                            i[1][0] - 20 <= ball_list[1][0] < i[1][0] + i[0][0].get_width() - 20
                    ):
                        ball_list[1][1] = i[1][1] - 40
                        ball_collided = True
                        ball_move_step_y_value = ball_move_step_y
                        ball_list[0] = ball[6]
                        ball_crashed = True
                        if not danger_item_collided:
                            life_items_gain -= 1
                            danger_item_collided = True
                        break
            if not ball_collided:
                if ball_list[1][1] <= 20:
                    ball_collided = True
                    ball_move_step_y_value = ball_move_step_y
                    ball_list[0] = ball[6]
                    ball_crashed = True
                    if not danger_item_collided:
                        life_items_gain -= 1
                        danger_item_collided = True
            if not ball_collided:
                if ball_list[1][1] + ball_move_step_y_value > Screen_Height - 60:
                    ball_list[1][1] = Screen_Height - 60
                    ball_collided = True
                    ball_move_step_y_value = ball_move_step_y
                    ball_list[0] = ball[6]
                    ball_crashed = True
                    if not danger_item_collided:
                        life_items_gain -= 1
                        danger_item_collided = True
            if not ball_collided:
                ball_list[1][1] += ball_move_step_y_value
                score += ball_move_step_y_value + bar_move_step_value
                ball_move_step_y_value += ball_move_step_y_acceleration

        bar_move_step_value *= game_speed_factor
        cloud_move_step0_value *= game_speed_factor
        cloud_move_step1_value *= game_speed_factor
        life_item_create_condition *= life_item_create_condition_factor
