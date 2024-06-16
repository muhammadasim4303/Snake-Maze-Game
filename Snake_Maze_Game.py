import pygame
import time
import random
import heapq

pygame.init()

white = (255, 255, 255)
yellow = (255, 255, 102)
black = (0, 0, 0)
red = (213, 50, 80)
green = (0, 255, 0)
blue = (50, 153, 213)

dis_width = 600
dis_height = 400

block_size = 10
snake_speed = 15

dis = pygame.display.set_mode((dis_width, dis_height))
pygame.display.set_caption('Snake Xenzia')
clock = pygame.time.Clock()

font_style = pygame.font.SysFont(None, 50)

def score(score):
    value = font_style.render("Snake Score: " + str(score), True, yellow)
    dis.blit(value, [0, 0])

def our_snake(block_size, snake_list):
    for x in snake_list:
        pygame.draw.rect(dis, black, [x[0], x[1], block_size, block_size])

def message(msg, color):
    mesg = font_style.render(msg, True, color)
    dis.blit(mesg, [dis_width / 6, dis_height / 3])

def astar(start, end, obstacles):
    open_list = []
    heapq.heappush(open_list, (0, start))
    came_from = {}
    g_score = {start: 0}
    f_score = {start: heuristic(start, end)}

    while open_list:
        current = heapq.heappop(open_list)[1]

        if current == end:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            return path[::-1]

        for neighbor in get_neighbors(current):
            if neighbor in obstacles or neighbor[0] < 0 or neighbor[0] >= dis_width or neighbor[1] < 0 or neighbor[1] >= dis_height:
                continue

            tentative_g_score = g_score[current] + 1

            if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g_score
                f_score[neighbor] = g_score[neighbor] + heuristic(neighbor, end)
                heapq.heappush(open_list, (f_score[neighbor], neighbor))

    return []

def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def get_neighbors(position):
    neighbors = [(0, -block_size), (0, block_size), (-block_size, 0), (block_size, 0)]
    return [(position[0] + n[0], position[1] + n[1]) for n in neighbors]

def gameLoop():
    game_over = False
    game_close = False

    x1 = dis_width / 2
    y1 = dis_height / 2

    snake_list = []
    length_of_snake = 1

    foodx = round(random.randrange(0, dis_width - block_size) / 10.0) * 10.0
    foody = round(random.randrange(0, dis_height - block_size) / 10.0) * 10.0

    obstacles = {(round(random.randrange(0, dis_width - block_size) / 10.0) * 10.0,
                  round(random.randrange(0, dis_height - block_size) / 10.0) * 10.0) for _ in range(30)}
    
    while (foodx, foody) in obstacles:
        foodx = round(random.randrange(0, dis_width - block_size) / 10.0) * 10.0
        foody = round(random.randrange(0, dis_height - block_size) / 10.0) * 10.0

    while not game_over:

        while game_close:
            dis.fill(blue)
            message("You Lost! Press C-Play Again or Q-Quit", red)
            score(length_of_snake - 1)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        gameLoop()

        snake_body_set = set(tuple(pos) for pos in snake_list)
        obstacles_with_snake = obstacles.union(snake_body_set)
        path = astar((x1, y1), (foodx, foody), obstacles_with_snake)

        if not path:
            game_close = True
        else:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_over = True

            if path:
                next_pos = path[0]
                x1, y1 = next_pos

            if x1 >= dis_width or x1 < 0 or y1 >= dis_height or y1 < 0:
                game_close = True

            dis.fill(blue)
            for obstacle in obstacles:
                pygame.draw.rect(dis, red, [obstacle[0], obstacle[1], block_size, block_size])
            pygame.draw.rect(dis, green, [foodx, foody, block_size, block_size])
            snake_head = []
            snake_head.append(x1)
            snake_head.append(y1)
            snake_list.append(snake_head)
            if len(snake_list) > length_of_snake:
                del snake_list[0]

            for x in snake_list[:-1]:
                if x == snake_head:
                    game_close = True

            our_snake(block_size, snake_list)
            score(length_of_snake - 1)

            pygame.display.update()

            if x1 == foodx and y1 == foody:
                foodx = round(random.randrange(0, dis_width - block_size) / 10.0) * 10.0
                foody = round(random.randrange(0, dis_height - block_size) / 10.0) * 10.0
                while (foodx, foody) in obstacles:
                    foodx = round(random.randrange(0, dis_width - block_size) / 10.0) * 10.0
                    foody = round(random.randrange(0, dis_height - block_size) / 10.0) * 10.0
                length_of_snake += 1

            clock.tick(snake_speed)

    pygame.quit()
    quit()

gameLoop()
