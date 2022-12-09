import pygame
import sys
import time

#initialize pygame
pygame.init()
pygame.display.set_caption("Towers of Hanoi")
screen = pygame.display.set_mode((640, 480))
clock = pygame.time.Clock()

# global game variables:
game_done = False
framerate = 60
steps = 0
minimum_steps = 0
n_discs = 3
discs = []
towers_midx = [120,  320, 520]
pointing_at = 0
floating = False
floater = 0

# colors:
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
gold = (239, 229, 51)
blue = (78, 162, 196)
grey = (170, 170, 170)
green = (77, 206, 145)


def blit_text(screen, text, midtop, aa=True, font=None, font_name=None, size=None, color=(255, 0, 0)):
    """
    :param screen: display conditions (pixel dimensions)
    :param text: text to be displayed
    :param midtop: pixel location for text to be displayed
    :param aa: antialiasing True by default
    :param font: font obj if set
    :param font_name: name of font
    :param size: font size
    :param color: rgb color of font
    :return:
    """
    if font is None:
        font = pygame.font.SysFont(font_name, size)
    font_surface = font.render(text, aa, color)
    font_rect = font_surface.get_rect()
    font_rect.midtop = midtop
    screen.blit(font_surface, font_rect)


def menu_screen():
    """
    Displays starting menu screen
    Determines difficulty (number of discs) according to user input
    :return:
    """
    global screen, n_discs, game_done, minimum_steps
    menu_done = False
    while not menu_done:
        screen.fill(white)
        blit_text(screen, 'Welcome to', (320, 80), font_name='sans serif', size=40, color=black)
        blit_text(screen, 'Towers of Hanoi', (323, 122), font_name='sans serif', size=90, color=black)
        blit_text(screen, 'Towers of Hanoi', (320, 120), font_name='sans serif', size=90, color=red)
        blit_text(screen, 'Use arrow keys to select difficulty:', (320, 220), font_name='sans serif', size=30,
                  color=black)
        if n_discs <= 3:
            blit_text(screen, str(n_discs) + ' Easy', (325, 261), font_name='sans serif', size=40, color=black)
            blit_text(screen, str(n_discs) + ' Easy', (324, 260), font_name='sans serif', size=40, color=green)
        elif 4 <= n_discs < 7:
            blit_text(screen, str(n_discs) + ' Medium', (325, 261), font_name='sans serif', size=40, color=black)
            blit_text(screen, str(n_discs) + ' Medium', (324, 260), font_name='sans serif', size=40, color=gold)
        elif n_discs >= 7:
            blit_text(screen, str(n_discs) + ' Hard', (325, 261), font_name='sans serif', size=40, color=black)
            blit_text(screen, str(n_discs) + ' Hard', (324, 260), font_name='sans serif', size=40, color=red)

        blit_text(screen, 'Press ENTER to start game', (320, 320), font_name='sans_serif', size=30, color=black)
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    menu_done = True
                    game_done = True
                if event.key == pygame.K_RETURN:
                    menu_done = True
                if event.key in [pygame.K_RIGHT, pygame.K_UP]:
                    n_discs += 1
                    if n_discs > 9:
                        n_discs = 9
                if event.key in [pygame.K_LEFT, pygame.K_DOWN]:
                    n_discs -= 1
                    if n_discs < 1:
                        n_discs = 1
            if event.type == pygame.QUIT:
                menu_done = True
                game_done = True
            minimum_steps = 2 ** n_discs - 1
        pygame.display.flip()
        clock.tick(60)


def game_over():
    """
    displays game over screen when called
    :return:
    """
    global screen, steps
    screen.fill(white)
    minimum_steps = 2 ** n_discs - 1
    blit_text(screen, 'You Won!', (320, 200), font_name='sans serif', size=72, color=gold)
    blit_text(screen, 'You Won!', (322, 202), font_name='sans serif', size=72, color=black)
    blit_text(screen, 'Your Steps: ' + str(steps), (320, 360), font_name='mono', size=30, color=black)
    blit_text(screen, 'Minimum Steps: ' + str(minimum_steps), (320, 390), font_name='mono', size=30, color=red)
    if minimum_steps == steps:
        blit_text(screen, 'You finished in minimum steps!', (320, 300), font_name='mono', size=26, color=green)
    pygame.display.flip()
    time.sleep(2)  # wait 2 seconds then continue
    pygame.quit()  # exit pygame
    sys.exit()  # exit console


def draw_guide_towers():
    """
    generates three towers to guide discs
    :return:
    """
    global screen
    for xpos in range(40, 460 + 1, 200):
        pygame.draw.rect(screen, green, pygame.Rect(xpos, 400, 160, 20))
        pygame.draw.rect(screen, grey, pygame.Rect(xpos + 75, 200, 10, 200))
    blit_text(screen, 'Start', (towers_midx[0], 403), font_name='mono', size=14, color=black)
    blit_text(screen, 'Finish', (towers_midx[2], 403), font_name='mono', size=14, color=black)


def create_discs():
    """
    creates n number of discs dependent on number stored in variable n_discs
    :return:
    """
    global n_discs, discs
    discs = []
    height = 20
    ypos = 397 - height
    width = n_discs * 23
    for i in range(n_discs):
        disk = {'rect': pygame.Rect(0, 0, width, height)}
        disk['rect'].midtop = (120, ypos)
        disk['val'] = n_discs - i
        disk['tower'] = 0
        discs.append(disk)
        ypos -= height + 3
        width -= 23


def draw_discs():
    """
    displays discs on game screen
    :return:
    """
    global screen, discs
    i = 1
    for disk in discs:
        if i % 2 > 0:
            pygame.draw.rect(screen, black, disk['rect'])
        else:
            pygame.draw.rect(screen, red, disk['rect'])
        i += 1
    return


def draw_ptr():
    """
    displays selection pointer under guide towers
    :return:
    """
    ptr_points = [(towers_midx[pointing_at] - 7, 440), (towers_midx[pointing_at] + 7, 440),
                  (towers_midx[pointing_at], 433)]
    pygame.draw.polygon(screen, red, ptr_points)
    return


def check_win_state():
    """
    checks if discs are on guide tower labeled 'finish'
    :return:
    """
    global discs
    over = True
    for disk in discs:
        if disk['tower'] != 2:
            over = False
    if over:
        time.sleep(0.2)
        game_over()


def reset():
    """
    reset position of discs and steps taken
    :return:
    """
    global steps, pointing_at, floating, floater
    steps = 0
    pointing_at = 0
    floating = False
    floater = 0
    menu_screen()
    create_discs()


def main():
    """
    main game loop
    :return:
    """
    global game_done, pointing_at, floating, floater, steps, minimum_steps
    menu_screen()
    create_discs()
    while not game_done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_done = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    reset()
                if event.key == pygame.K_r:
                    create_discs()
                    steps = 0
                if event.key == pygame.K_q:
                    game_done = True
                if event.key == pygame.K_RIGHT:
                    pointing_at = (pointing_at + 1) % 3
                    if floating:
                        discs[floater]['rect'].midtop = (towers_midx[pointing_at], 100)
                        discs[floater]['tower'] = pointing_at
                if event.key == pygame.K_LEFT:
                    pointing_at = (pointing_at - 1) % 3
                    if floating:
                        discs[floater]['rect'].midtop = (towers_midx[pointing_at], 100)
                        discs[floater]['tower'] = pointing_at
                if event.key == pygame.K_UP and not floating:
                    for disk in discs[::-1]:
                        if disk['tower'] == pointing_at:
                            floating = True
                            floater = discs.index(disk)
                            disk['rect'].midtop = (towers_midx[pointing_at], 100)
                            break
                if event.key == pygame.K_DOWN and floating:
                    for disk in discs[::-1]:
                        if disk['tower'] == pointing_at and discs.index(disk) != floater:
                            if disk['val'] > discs[floater]['val']:
                                floating = False
                                discs[floater]['rect'].midtop = (towers_midx[pointing_at], disk['rect'].top - 23)
                                steps += 1
                            break
                    else:
                        floating = False
                        discs[floater]['rect'].midtop = (towers_midx[pointing_at], 400 - 23)
                        steps += 1
        screen.fill(white)
        draw_guide_towers()
        draw_discs()
        draw_ptr()
        if steps <= minimum_steps:
            blit_text(screen, f'Steps: {str(steps)}', (320, 20), font_name='sans serif', size=50, color=black)
        elif steps > minimum_steps:
            blit_text(screen, f'Steps: {str(steps)}', (320, 20), font_name='sans serif', size=50, color=red)

        blit_text(screen, f'Minimum Possible Steps: {str(minimum_steps)}', (320, 55), font_name='san serif', size=50, color=black)
        pygame.display.flip()
        if not floating:
            check_win_state()
        clock.tick(framerate)


if __name__ == '__main__':
    main()
