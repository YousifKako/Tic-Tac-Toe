import pygame

pygame.init()

size = width, height = 540, 540
screen = pygame.display.set_mode(size)

# Empty, X, O = range(3)
T_Empty = 0
T_X = 1
T_O = 2

W_StillPlaying = 0
W_X = 1
W_O = 2
W_Draw = 3

gameState = [
    [T_Empty, T_Empty, T_Empty],
    [T_Empty, T_Empty, T_Empty],
    [T_Empty, T_Empty, T_Empty]]

turn = True
winner = W_StillPlaying

black = 0, 0, 0
white = 255, 255, 255
red = 255, 0, 0
green = 0, 255, 0

s = 540
tw = s // 3

yesBox = [145, 400, 100, 50]
noBox = [300, 400, 100, 50]


def determineWinner():
    # Vertical Winner
    for a in range(3):
        if (gameState[0][a] == W_O) or (gameState[0][a] == W_X):
            current = gameState[0][a]
            if (current == gameState[1][a]) and (current == gameState[2][a]):
                return current
    # Horizontal Winner
    for a in range(3):
        if (gameState[a][0] == W_O) or (gameState[a][0] == W_X):
            current = gameState[a][0]
            if (current == gameState[a][1]) and (current == gameState[a][2]):
                return current
    # Angle Winners
    if (gameState[0][0] == W_O) or (gameState[0][0] == W_X):
        current = gameState[0][0]
        if (current == gameState[1][1]) and (current == gameState[2][2]):
            return current
    if (gameState[0][2] == W_O) or (gameState[0][2] == W_X):
        current = gameState[0][2]
        if (current == gameState[1][1]) and (current == gameState[2][0]):
            return current
    # If We Are Still Playing
    for i in range(3):
        for j in range(3):
            if gameState[i][j] == T_Empty:
                return W_StillPlaying
    # No Winner
    return W_Draw


def runAI():
    if not turn:
        me = T_O
        winMe = W_O
        other = T_X
        winOther = W_X
    else:
        me = T_X
        winMe = W_X
        other = T_O
        winOther = W_O

    for i in range(3):
        for j in range(3):
            if gameState[i][j] == T_Empty:
                gameState[i][j] = me
                w = determineWinner()
                if w == winMe:
                    return
                else:
                    gameState[i][j] = T_Empty

    for i in range(3):
        for j in range(3):
            if gameState[i][j] == T_Empty:
                gameState[i][j] = other
                w = determineWinner()
                if w == winOther:
                    gameState[i][j] = me
                    return
                else:
                    gameState[i][j] = T_Empty

    for i in range(3):
        for j in range(3):
            if gameState[i][j] == T_Empty:
                gameState[i][j] = me
                return

def mouseInput(x, y):
    global turn
    global winner

    if winner == W_StillPlaying:
        j = x // tw
        i = y // tw

        if gameState[i][j] != T_Empty:
            return True
        if turn:
            gameState[i][j] = T_X
            turn = False
        else:
            gameState[i][j] = T_O
            turn = True

        winner = determineWinner()

        if winner == W_StillPlaying:
            runAI()
            winner = determineWinner()
            turn = not turn

    else:
        if x < yesBox[0] + yesBox[2] and x > yesBox[0] and y < yesBox[1] + yesBox[3] and y > yesBox[1]:
            for i in range(0, 3):
                for j in range(0, 3):
                    gameState[i][j] = T_Empty
            winner = W_StillPlaying

        if x < noBox[0] + noBox[2] and x > noBox[0] and y < noBox[1] + noBox[3] and y > noBox[1]:
            return False

    return True


def handleEvent(event):
    if event.type == pygame.QUIT:
        return False
    elif event.type == pygame.KEYDOWN:
        if event.key == pygame.K_ESCAPE:
            return False
    elif event.type == pygame.MOUSEBUTTONUP:
        if event.button == 1:
            return mouseInput(event.pos[0], event.pos[1])
    return True


def drawX(color, x, y):
    pygame.draw.line(screen, color, [x + 30, y + 30], [x + 150, y + 150], 2)
    pygame.draw.line(screen, color, [x + 30, y + 150], [x + 150, y + 30], 2)


def drawO(color, x, y):
    pygame.draw.circle(screen, color, [x + 90, y + 90], 60, 2)


while handleEvent(pygame.event.wait()):
    # Render
    screen.fill(white)

    if winner == W_StillPlaying:
        # Draw Grid
        pygame.draw.rect(screen, black, [180, 0, 5, 540])
        pygame.draw.rect(screen, black, [360, 0, 5, 540])
        pygame.draw.rect(screen, black, [0, 360, 540, 5])
        pygame.draw.rect(screen, black, [0, 180, 540, 5])

        # Draw Tiles
        for i in range(0, 3):
            for j in range(0, 3):
                if gameState[i][j] == T_X:
                    drawX(red, j * tw, i * tw)
                elif gameState[i][j] == T_O:
                    drawO(green, j * tw, i * tw)

    else:
        # Initialize font; must be called after 'pygame.init()' to avoid 'Font not Initialized' error
        myfont = pygame.font.SysFont("monospace", 40)
        # Render text
        fontColor = 0, 0, 0
        if winner == W_X:
            label = myfont.render("Player X wins", 1, fontColor)
        elif winner == W_O:
            label = myfont.render("Player O wins", 1, fontColor)
        else:
            label = myfont.render("It's a draw", 1, fontColor)

        label2 = myfont.render("Want To play again?", 1, fontColor)
        yes = myfont.render("Yes", 1, fontColor)
        no = myfont.render("No", 1, fontColor)
        pygame.draw.rect(screen, black, [145, 400, 100, 50], 5)
        pygame.draw.rect(screen, black, [300, 400, 100, 50], 5)

        screen.blit(yes, (155, 400))
        screen.blit(no, (310, 400))
        screen.blit(label2, (80, 220))
        screen.blit(label, (80, 180))

    pygame.display.flip()