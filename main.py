import pygame
from pygame import mixer

pygame.init()

WIDTH = 1400
HEIGHT = 800

black = (0, 0, 0)
white = (255, 255, 255)
gray = (128, 128, 128)
dark_gray = (169, 169, 169)
green = (0, 255, 0)
gold = (212, 175, 55)
blue = (0, 255, 255)

screen = pygame.display.set_mode([WIDTH, HEIGHT])

pygame.display.set_caption('Beat maker')
label_font = pygame.font.Font('freesansbold.ttf', 32)
medium_font = pygame.font.Font('freesansbold.ttf', 24)

fps = 60
timer = pygame.time.Clock()
beats = 8
instruments = 6
boxes = []
clicked = [[-1 for _ in range(beats)] for _ in range(instruments)]
bpm = 240
playing = True
active_length = 0
active_beat = 0
beat_changed = True

# load sounds
hi_hat = mixer.Sound('spSamples/openHat.wav')
snare = mixer.Sound('spSamples/snarePitched08.wav')


def play_notes():
    for i in range(len(clicked)):
        if clicked[i][active_beat] == 1:
            if i == 0:
                hi_hat.play()
            if i == 1:
                snare.play()


def draw_grid(clicks, beat):
    left_box = pygame.draw.rect(screen, gray, [0, 0, 200, HEIGHT - 200], 5)
    botton_box = pygame.draw.rect(
        screen, gray, [0, HEIGHT - 200, WIDTH, 200], 5)
    boxes = []
    color = [gray, white, gray]
    hi_hat_text = label_font.render('Hi Hat', True, white)
    screen.blit(hi_hat_text, (30, 30))
    kick_text = label_font.render('Kick', True, white)
    screen.blit(kick_text, (30, 130))
    snare_text = label_font.render('Snare', True, white)
    screen.blit(snare_text, (30, 230))
    crash_text = label_font.render('Crash', True, white)
    screen.blit(crash_text, (30, 330))
    floor_tom_text = label_font.render('Floor tom', True, white)
    screen.blit(floor_tom_text, (30, 430))
    clap_text = label_font.render('Clap', True, white)
    screen.blit(clap_text, (30, 530))
    for i in range(6):
        pygame.draw.line(
            screen, gray, (0, (i*100) + 100), (200, (i*100) + 100), 5)
    for i in range(beats):
        for j in range(instruments):
            if clicks[j][i] == -1:
                color = gray
            else:
                color = green

            rect = pygame.draw.rect(
                screen, color, [i*((WIDTH-200) // beats) + 205, j*(100) + 5, ((WIDTH-200)//beats) - 10, ((HEIGHT-200)//instruments) - 10], 0, 3)

            pygame.draw.rect(
                screen, gold, [i*((WIDTH-200) // beats) + 200, j*(100), ((WIDTH-200)//beats), ((HEIGHT-200)//instruments)], 5, 5)

            pygame.draw.rect(
                screen, black, [i*((WIDTH-200) // beats) + 200, j*(100), ((WIDTH-200)//beats), ((HEIGHT-200)//instruments)], 2, 5)

            boxes.append((rect, (i, j)))

        active = pygame.draw.rect(
            screen, blue, [beat*((WIDTH-200)//beats) + 200, 0, ((WIDTH-200)//beats), instruments*100], 5, 3)
    return boxes


run = True
while run:
    timer.tick(fps)
    screen.fill(black)
    boxes = draw_grid(clicked, active_beat)

    play_pause = pygame.draw.rect(
        screen, gray, [50, HEIGHT - 150, 200, 100], 0, 5)
    play_text = label_font.render('Play/pause', True, white)
    screen.blit(play_text, (70, HEIGHT-130))

    if playing:
        toggle_play_text = medium_font.render('Play', True, dark_gray)
    else:
        toggle_play_text = medium_font.render('Paused', True, dark_gray)
    screen.blit(toggle_play_text, (70, HEIGHT-100))

    bpm_rect = pygame.draw.rect(
        screen, gray, [300, HEIGHT-150, 220, 100], 5, 5)
    bpm_text = medium_font.render('Beats per minute', True, white)
    screen.blit(bpm_text, (308, HEIGHT-130))
    bpm_text_2 = label_font.render(f'{bpm}', True, white)
    screen.blit(bpm_text_2, (370, HEIGHT-100))

    bpm_add_rect = pygame.draw.rect(
        screen, gray, [530, HEIGHT-150, 48, 48], 0, 5)
    bpm_sub_rect = pygame.draw.rect(
        screen, gray, [530, HEIGHT-100, 48, 48], 0, 5)
    add_bpm_text = medium_font.render('+', True, white)
    sub_bpm_text = medium_font.render('-', True, white)
    screen.blit(add_bpm_text, (545, HEIGHT-140))
    screen.blit(sub_bpm_text, (547, HEIGHT-90))

    beats_rect = pygame.draw.rect(
        screen, gray, [650, HEIGHT-150, 180, 100], 5, 5)
    beats_text = medium_font.render('Beats in loop', True, white)
    screen.blit(beats_text, (658, HEIGHT-130))
    beats_text_2 = label_font.render(f'{beats}', True, white)
    screen.blit(beats_text_2, (720, HEIGHT-100))

    beats_add_rect = pygame.draw.rect(
        screen, gray, [840, HEIGHT-150, 48, 48], 0, 5)
    beats_sub_rect = pygame.draw.rect(
        screen, gray, [840, HEIGHT-100, 48, 48], 0, 5)
    add_beats_text = medium_font.render('+', True, white)
    sub_beats_text = medium_font.render('-', True, white)
    screen.blit(add_beats_text, (855, HEIGHT-140))
    screen.blit(sub_beats_text, (857, HEIGHT-90))

    if beat_changed:
        play_notes()
        beat_changed = False
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            for i in range(len(boxes)):
                if boxes[i][0].collidepoint(event.pos):
                    coords = boxes[i][1]
                    clicked[coords[1]][coords[0]] *= -1

        if event.type == pygame.MOUSEBUTTONUP:
            if play_pause.collidepoint(event.pos):
                if playing:
                    playing = False
                elif not playing:
                    playing = True
            elif bpm_add_rect.collidepoint(event.pos):
                bpm += 1
            elif bpm_sub_rect.collidepoint(event.pos):
                bpm -= 1
            elif beats_add_rect.collidepoint(event.pos):
                beats += 1
                for i in range(len(clicked)):
                    clicked[i].append(-1)
            elif beats_sub_rect.collidepoint(event.pos):
                beats -= 1
                for i in range(len(clicked)):
                    clicked[i].pop(-1)

    beat_length = fps*60//bpm
    if playing:
        if active_length < beat_length:
            active_length += 1
        else:
            active_length = 0
            if active_beat < beats - 1:
                active_beat += 1
                beat_changed = True
            else:
                active_beat = 0
                beat_changed = True

    pygame.display.flip()
pygame.quit()
