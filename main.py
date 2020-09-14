import pygame, sys, random

pygame.mixer.pre_init(frequency=22050, size=16, channels=1, buffer=512)
pygame.init()
screen = pygame.display.set_mode((288, 512))
clock = pygame.time.Clock()
gamefont = pygame.font.Font(r'C:\Users\soumi\Downloads\04B_19.TTF', 20)
secondgamefont = pygame.font.Font(r'C:\Users\soumi\Downloads\04B_19.TTF', 30)


def floor_animate():
    screen.blit(floorsurface, (floorxpos, 450))
    screen.blit(floorsurface, (floorxpos + 288, 450))


def makepipe():
    pipepos = random.randint(175, 400)
    pipe = pipesurface.get_rect(midtop=(400, pipepos))
    toppipe = pipesurface.get_rect(midbottom=(400, pipepos - 125))
    return pipe, toppipe


def movepipe(pipes, difficulty):
    for pipe in pipes:
        pipe.centerx -= difficulty
    return pipes


def drawpipes(pipes):
    for pipe in pipes:
        if pipe.bottom >= 450:
            screen.blit(pipesurface, pipe)
        else:
            flippipe = pygame.transform.flip(pipesurface, False, True)
            screen.blit(flippipe, pipe)


def collisioncheck(pipes):
    for pipe in pipes:
        if birdrect.colliderect(pipe):
            hitsound.play()
            deathsound.play()
            return False
    if birdrect.top <= -50 or birdrect.bottom >= 450:
        deathsound.play()
        return False
    return True


def rotatebird(bird):
    newbirdsurface = pygame.transform.rotozoom(bird, -birdmovement * 3, 1)
    return newbirdsurface


def birdanimation():
    newbird = birdflaps[birdindex]
    newbirdrect = newbird.get_rect(center=(50, birdrect.centery))
    return newbird,newbirdrect


def scoredisplay(gamestate):
    if gamestate == 'gameon':
        scoresurface = gamefont.render(f'Score: {(int(score))}', True, (255, 255, 255))
        scorerect = scoresurface.get_rect(center=(144, 50))
        screen.blit(scoresurface, scorerect)
    if gamestate == 'gameover':
        highscoresurface = secondgamefont.render(f'High Score: {(int(highscore))}', True, (255, 255, 255))
        highscorerect = highscoresurface.get_rect(center=(144, 425))
        screen.blit(highscoresurface, highscorerect)


def updatehighscore(highscore, score):
    if score > highscore:
        highscore = score
    return highscore


gameoverscreen = pygame.image.load(r'C:\Users\soumi\Downloads\FlappyBird_Python-master\assets\message.png')\
    .convert_alpha()
gameoverect = gameoverscreen.get_rect(center=(144, 228))

# Game Variables
gravity = 0.2
birdmovement = 0
game_active = True
difficulty = 2
mode = 1200
score = 0
highscore = 0

backgroundsurface = pygame.image.load(r'C:\Users\soumi\Downloads\FlappyBird_Python-master\assets\background-day.png') \
    .convert()

floorsurface = pygame.image.load(r'C:\Users\soumi\Downloads\FlappyBird_Python-master\assets\base.png').convert()
floorxpos = 0


flappydown = pygame.image.load(r'C:\Users\soumi\Downloads\FlappyBird_Python-master\assets\yellowbird-downflap.png') \
    .convert_alpha()
flappymid = pygame.image.load(r'C:\Users\soumi\Downloads\FlappyBird_Python-master\assets\yellowbird-midflap.png') \
    .convert_alpha()
flappyup = pygame.image.load(r'C:\Users\soumi\Downloads\FlappyBird_Python-master\assets\yellowbird-upflap.png') \
    .convert_alpha()
birdflaps = [flappydown, flappymid, flappyup]
birdindex = 0
flappybird = birdflaps[birdindex]
birdrect = flappybird.get_rect(center=(50, 256))
BIRDFLAP = pygame.USEREVENT + 1
pygame.time.set_timer(BIRDFLAP, 200)

pipesurface = pygame.image.load(r'C:\Users\soumi\Downloads\FlappyBird_Python-master\assets\pipe-green.png')
pipelist = []
NEWPIPE = pygame.USEREVENT
pygame.time.set_timer(NEWPIPE, mode)

flapsound = pygame.mixer.Sound(r'C:\Users\soumi\Downloads\FlappyBird_Python-master\sound\sfx_wing.wav')
deathsound = pygame.mixer.Sound(r'C:\Users\soumi\Downloads\FlappyBird_Python-master\sound\sfx_die.wav')
hitsound = pygame.mixer.Sound(r'C:\Users\soumi\Downloads\FlappyBird_Python-master\sound\sfx_hit.wav')
scoresound = pygame.mixer.Sound(r'C:\Users\soumi\Downloads\FlappyBird_Python-master\sound\sfx_point.wav')

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_active == True:
                birdmovement = 0
                birdmovement -= 5

        elif event.type == pygame.MOUSEBUTTONDOWN:
            birdmovement = 0
            birdmovement -= 5
            flapsound.play()
        if event.type == pygame.MOUSEBUTTONDOWN and game_active == False:
            game_active = True
            pipelist.clear()
            birdrect.center = (50, 256)
            birdmovement = 0
            gravity = 0.2
            difficulty = 2
            mode = 1200
            score = 0

        if event.type == BIRDFLAP:
            if birdindex < 2:
                birdindex += 1
            else:
                birdindex = 0
            flappybird, birdrect = birdanimation()
        if event.type == NEWPIPE:
            pipelist.extend(makepipe())

    if game_active:
        screen.blit(backgroundsurface, (0, 0))
        birdmovement += gravity
        rotatebirdsurface = rotatebird(flappybird)
        birdrect.centery += birdmovement
        screen.blit(rotatebirdsurface, birdrect)
        pipelist = movepipe(pipelist, difficulty)
        drawpipes(pipelist)
        game_active = collisioncheck(pipelist)
        scoredisplay('gameon')
        score += 0.007
    else:
        highscore = updatehighscore(highscore, score)
        scoredisplay('gameover')
        screen.blit(gameoverscreen, gameoverect)


    floorxpos -= 1
    floor_animate()
    if floorxpos <= -288:
        floorxpos = 0

    pygame.display.update()
    clock.tick(120)
