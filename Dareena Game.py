import pygame
import random

clock = pygame.time.Clock()

pygame.init()

WIDTH, HEIGHT = 960, 540
FPS = 60
TICK = 0.5

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Dareena Math Game")
icon = pygame.image.load('resouses/icon.ico')
pygame.display.set_icon(icon)

background_imgs = [
    pygame.image.load('resouses/textures/bg_sky.png').convert(),
    pygame.image.load('resouses/textures/bg_clouds1.png').convert_alpha(),
    pygame.image.load('resouses/textures/bg_clouds2.png').convert_alpha(),
    pygame.image.load('resouses/textures/bg_clouds3.png').convert_alpha(),
    pygame.image.load('resouses/textures/bg_clouds4.png').convert_alpha(),
]

bird_imgs = [
    pygame.image.load('resouses/textures/bird_down.png').convert_alpha(),
    pygame.image.load('resouses/textures/bird_mid.png').convert_alpha(),
    pygame.image.load('resouses/textures/bird_up.png').convert_alpha(),
]

blocks_imgs = [
    pygame.image.load('resouses/textures/block.png').convert_alpha(),
    pygame.image.load('resouses/textures/wall.png').convert_alpha(),
]

score = 0

bg_x_sky = 0
bg_x_clouds1 = 0
bg_x_clouds2 = 0
bg_x_clouds3 = 0
bg_x_clouds4 = 0

block_x = 1200
block_distance = 600
block_ys = [
    0, 
    215,
    430
]
score_ys = [
    108,
    323
]
blocks_list = []
block_timer = pygame.USEREVENT + 1
pygame.time.set_timer(block_timer, 5)

player_x = WIDTH // 5
player_y = HEIGHT // 2
player_speed = 5
gravity = 0.3
player_jump = -5
is_jump = False
jump_timer = 0
answer_timer = 0
player_anim_count = 0

def generate_random_math_problem():
    # Генерируем два случайных целых числа
    num1 = random.randint(1, 20)
    num2 = random.randint(1, 20)

    # Выбираем случайное арифметическое действие (+, -, *, /)
    operator = random.choice(['+', '-', '*', '/'])

    # Проверяем, чтобы результат деления был целым числом
    while operator == '/' and num1 % num2 != 0:
        num1 = random.randint(1, 20)
        num2 = random.randint(1, 20)

    # Формируем строковое представление выражения
    math_problem = f"{num1} {operator} {num2}"

    # Вычисляем правильный ответ
    correct_answer = eval(math_problem)

    # Генерируем неправильный ответ, близкий к правильному
    incorrect_answer = correct_answer + random.randint(-5, 5)
    if incorrect_answer == correct_answer:
        incorrect_answer += 1

    return math_problem, correct_answer, incorrect_answer

font = pygame.font.Font('resouses/fonts/gamefont.ttf', 36)

def draw_text(text, x, y, color, size):
    text_surface = pygame.font.Font('resouses/fonts/gamefont.ttf', size).render(text, False , color)
    text_rect = text_surface.get_rect(topleft=(x, y))
    screen.blit(text_surface, text_rect)

gameplay = True
starter = True
running = True
while running:
    if starter:
        problem, correct, incorrect = generate_random_math_problem()
        one_or_zero = random.choice([0, 1])
        starter = not starter
    
    answer_timer -= 1
    screen.blit(background_imgs[0], (bg_x_sky, 0))
    screen.blit(background_imgs[0], (bg_x_sky + 1200, 0))
    screen.blit(background_imgs[1], (bg_x_clouds1, 0))
    screen.blit(background_imgs[1], (bg_x_clouds1 + 1200, 0))
    screen.blit(background_imgs[2], (bg_x_clouds2, 0))
    screen.blit(background_imgs[2], (bg_x_clouds2 + 1200, 0))
    screen.blit(background_imgs[3], (bg_x_clouds3, 0))
    screen.blit(background_imgs[3], (bg_x_clouds3 + 1200, 0))
    
    if gameplay:
        
        screen.blit(blocks_imgs[1], (block_x, score_ys[0]))
        screen.blit(blocks_imgs[1], (block_x, score_ys[1]))

        screen.blit(blocks_imgs[0], (block_x, block_ys[0]))
        screen.blit(blocks_imgs[0], (block_x, block_ys[1]))
        screen.blit(blocks_imgs[0], (block_x, block_ys[2]))
        
        draw_text(f"Score: {score}", 100, 50, (255, 255, 255), 36)
        draw_text(problem, 100, 100, (255, 255, 255), 36)
        if answer_timer < 0:
            draw_text(str(int(correct)), block_x-110, score_ys[one_or_zero]+43, (255, 255, 255), 36)
            draw_text(str(int(incorrect)), block_x-110, score_ys[not one_or_zero]+43, (255, 255, 255), 36)

        if player_speed > 0:
            screen.blit(bird_imgs[2], (player_x, player_y))
        elif player_speed == 0:
            screen.blit(bird_imgs[1], (player_x, player_y))
        elif player_speed < 0:
            screen.blit(bird_imgs[0], (player_x, player_y))
        
        screen.blit(background_imgs[4], (bg_x_clouds4, 0))
        screen.blit(background_imgs[4], (bg_x_clouds4 + 1200, 0))
        
        player_hitbox = bird_imgs[0].get_rect(topleft=(player_x, player_y))
        player_score_hitbox = bird_imgs[0].get_rect(center=(player_x+17, player_y+12))
        block_hitbox1 = blocks_imgs[0].get_rect(topleft=(block_x, block_ys[0]))
        block_hitbox2 = blocks_imgs[0].get_rect(topleft=(block_x, block_ys[1]))
        block_hitbox3 = blocks_imgs[0].get_rect(topleft=(block_x, block_ys[2]))
        score_hitbox1 = blocks_imgs[0].get_rect(topright=(block_x+40, score_ys[0]))
        score_hitbox2 = blocks_imgs[0].get_rect(topright=(block_x+40, score_ys[1]))
        score_hitbox1.width = 2
        score_hitbox2.width = 2
        player_score_hitbox.width, player_score_hitbox.height = 5, 5
        
        jump_timer -= 1
        keys = pygame.key.get_pressed()
        if (keys[pygame.K_SPACE] or keys[pygame.K_UP] or pygame.mouse.get_pressed()[0]) and jump_timer < 0:
            if not is_jump:
                is_jump = True
                player_speed = player_jump
                jump_timer = 2
        
        if is_jump:
            player_speed += gravity
            player_y += player_speed
            if player_y > player_y + player_jump:
                player_y = player_y
                is_jump = False
        
        player_speed += gravity
        player_y += player_speed
        
        if player_y >= HEIGHT-24:
            player_y = HEIGHT-24
        elif player_y <= 0:
            player_y = 0
            
        bg_x_sky -= TICK
        bg_x_clouds1 -= 2*TICK
        bg_x_clouds2 -= 3*TICK
        bg_x_clouds3 -= 4*TICK
        bg_x_clouds4 -= 5*TICK
        if bg_x_sky <= -1200:
            bg_x_sky = 0
        elif bg_x_clouds1 <= -1200:
            bg_x_clouds1 = 0
        elif bg_x_clouds2 <= -1200:
            bg_x_clouds2 = 0
        elif bg_x_clouds3 <= -1200:
            bg_x_clouds3 = 0
        elif bg_x_clouds4 <= -1200:
            bg_x_clouds4 = 0    
            
        block_x -= 5
        if block_x <= -40:
            block_x = 1200
            
        if player_hitbox.colliderect(block_hitbox1) or player_hitbox.colliderect(block_hitbox2) or player_hitbox.colliderect(block_hitbox3):
            #print("You lose!")
            gameplay = False
        
        if one_or_zero == 0:
            if player_score_hitbox.colliderect(score_hitbox1):
                score += 1
                answer_timer = 40
                problem, correct, incorrect = generate_random_math_problem()
                one_or_zero = random.choice([0, 1])
            elif player_score_hitbox.colliderect(score_hitbox2):
                score -= 1
                answer_timer = 40
                problem, correct, incorrect = generate_random_math_problem()
                one_or_zero = random.choice([0, 1])
        else:
            if player_score_hitbox.colliderect(score_hitbox2):
                score += 1
                answer_timer = 40
                problem, correct, incorrect = generate_random_math_problem()
                one_or_zero = random.choice([0, 1])
            elif player_score_hitbox.colliderect(score_hitbox1):
                score -= 1
                answer_timer = 40
                problem, correct, incorrect = generate_random_math_problem()
                one_or_zero = random.choice([0, 1])
    else:
        draw_text("Game over", WIDTH//5 , HEIGHT//2-80, (188, 162, 57), 65)
        draw_text(f"Score: {score}", WIDTH//2-150 , HEIGHT//2+30, (188, 162, 57), 36)
        FPS = 0
    pygame.display.update()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False  
            pygame.quit()

    clock.tick(FPS)