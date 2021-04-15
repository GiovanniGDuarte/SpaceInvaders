from PPlay.window import *
from PPlay.gameimage import *
from PPlay.sprite import *
from PPlay.collision import *

janela = Window(600,400)
janela.set_title("Space Invaders")
mouse = Window.get_mouse()
teclado = Window.get_keyboard()

##Game Images##
fundo = GameImage("Actors and background/space.png")
botaoJogar = GameImage("Buttons/jogar.png")
botaoDificuldade = GameImage("Buttons/dificuldade.png")
botaoRanking = GameImage("Buttons/ranking.png")
botaoSair = GameImage("Buttons/sair.png")
botaoEasy = GameImage("Buttons/easy.png")
botaoMedium = GameImage("Buttons/MEDIUM.png")
botaoHard = GameImage("Buttons/hard.png")
spaceShip = GameImage("Actors and background/spaceship.png")
gameOver = GameImage("Messages/gameOver.png")
gameOver.set_position((janela.width/2)-gameOver.width/2,(janela.height/2)-gameOver.height/2)
pressESC = Sprite("Messages/PressESC.png",2)
pressESC.set_position(janela.width/2-pressESC.width/2,janela.height-pressESC.height-spaceShip.height)
pressESC.set_total_duration(1500)
drawPressESC = False

##

##Variaveis e coordenadas iniciais##
jogarX = janela.width/2 - botaoJogar.width/2
jogarY = 100
dificuldadeX = janela.width / 2 - botaoDificuldade.width / 2
dificuldadeY = 100 + botaoJogar.height + 10
rankingX = janela.width / 2 - botaoRanking.width / 2
rankingY = 100 + botaoJogar.height + botaoDificuldade.height + 20
sairX =janela.width / 2 - botaoSair.width / 2
sairY =100 + botaoJogar.height + botaoDificuldade.height + botaoRanking.height+ 30
easyX, easyY, mediumX, mediumY, hardX, hardY = -200,-200,-200,-200,-200,-200
initial = janela.width/2 - spaceShip.width
jogar = False
gameOverBool = False
dificuldade = 0
chosen = False
velTiro = 200
tiros = []
velMonster = 100
monster_height = GameImage("Actors and background/spaceInvader.png").height
recarga = 0
pontuacao = 0

##

##Atualiza posicao do menu##
def set_menu():
    botaoJogar.set_position(jogarX, jogarY)
    botaoDificuldade.set_position(dificuldadeX, dificuldadeY)
    botaoRanking.set_position(rankingX, rankingY)
    botaoSair.set_position(sairX, sairY)
    botaoEasy.set_position(easyX, easyY)
    botaoMedium.set_position(mediumX, mediumY)
    botaoHard.set_position(hardX, hardY)
##

##Atualiza posicao da nave##
def spaceShipPosition(initial):
    spaceShip_x = initial
    if teclado.key_pressed("LEFT") and spaceShip_x > 0:
        velSpaceShip = -200
    elif teclado.key_pressed("RIGHT") and spaceShip_x + spaceShip.width < janela.width:
        velSpaceShip = 200
    else:
        velSpaceShip = 0
    spaceShip_x = spaceShip_x + velSpaceShip * janela.delta_time()
    spaceShip.set_position(spaceShip_x, janela.height - spaceShip.height)
    return spaceShip_x
##

##Cria matriz de tiros##
def shoot(initial):
    tiro = Sprite("Actors and background/tiro2.png",4)
    tirox = initial
    tiroY = janela.height - spaceShip.height
    tiros.append([tiro,tirox,tiroY])
    return(tiros)
##

##Escolha de dificuldade##
def escolha_dificuldade(dificuldade):
    if mouse.is_button_pressed(BUTTON_LEFT):
        if mouse.is_over_area([easyX, easyY], [easyX + botaoEasy.width, easyY + botaoEasy.height]):
            dificuldade = 3
        elif mouse.is_over_area([mediumX, mediumY], [mediumX + botaoMedium.width, mediumY + botaoMedium.height]):
            dificuldade = 2
        elif mouse.is_over_area([hardX, hardY], [hardX + botaoHard.width, hardY + botaoHard.height]):
            dificuldade = 1
    if dificuldade == 3:
        janela.draw_text("EASY",10,10,color = (255,255,255))
    elif dificuldade == 2:
        janela.draw_text("MEDIUM",10,10,color = (255,255,255))
    elif dificuldade == 1:
        janela.draw_text("HARD",10,10,color=(255,255,255))
    return(dificuldade)
##

#Gera matriz de monstros
def generateMonsterMatrix(N, M):
    monsters = []
    for linha in range(N):
        monstersLinha = []
        for coluna in range(M):
            monster = GameImage("Actors and background/spaceInvader.png")
            monsterX = 20 + 20*coluna
            monsterY = 20 + 20*linha
            monstersLinha.append([monster,monsterX,monsterY])
        monsters.append(monstersLinha)
    return(monsters)
##

##Checa colisao da matriz de monstros com paredes laterais##
def wallCollision(monsters):
    for linha in monsters:
        if linha[len(linha) - 1][1] > janela.width:
            return("r")
        elif linha[0][1] < 0:
            return("l")
    return False
##

##Checa colisao de tiros com monstros (testa primeiro a colisao com a primeira linha e elimina os casos em que o tiro esta a direita ou a esquerda de um bloco)##
def monsterTiroCollision(tiro,monsters):
    intervalos = indexMonstro(tiro[1]-tiro[0].width,monsters)
    for linha in reversed(monsters):
        if intervalos[monsters.index(linha)][0] != intervalos[monsters.index(linha)][1] :
            for i in range(intervalos[monsters.index(linha)][0],intervalos[monsters.index(linha)][1]):
                if Collision.collided(tiro[0], linha[i][0]):
                    linha.remove(linha[i])
                    return True
        else:
            if len(linha) ==0:
                monsters.remove(linha)
            elif Collision.collided(tiro[0], linha[intervalos[monsters.index(linha)][0]][0]):
                linha.remove(linha[intervalos[monsters.index(linha)][0]])
                return True
##

##Acha o index de quais monstros devem ser testados##
def indexMonstro(tirox,monsters):
    min= 0
    intervalos = []
    for line in monsters:
        max = len(line)
        for n in range(0, len(line)):
            if tirox >= line[n][1]:
                min = n
            if tirox<= line[n][1]:
                max = n
        intervalos.append([min,max])
    return(intervalos)
##
##Desenha o menu##
def drawMenu():
    fundo.draw()
    botaoJogar.draw()
    botaoDificuldade.draw()
    botaoRanking.draw()
    botaoSair.draw()
    botaoEasy.draw()
    botaoMedium.draw()
    botaoHard.draw()
##

##Gerando a matriz dado NxM##
N,M = 2,10
monsters = generateMonsterMatrix(N,M)
##

while True:
    #Posicoes iniciais e atualizacao da posicao da Nave##
    set_menu()
    spaceShipPosition(initial)
    initial = spaceShipPosition(initial)
    ##

    ##Operando Menu##
    if mouse.is_button_pressed(BUTTON_LEFT):
        if mouse.is_over_area([jogarX,jogarY],[jogarX + botaoJogar.width, jogarY + botaoJogar.height]) and chosen:
            jogarX, dificuldadeX,rankingX, sairX = -200,-200,-200,-200
            jogar = True
        elif mouse.is_over_area([dificuldadeX,dificuldadeY],[dificuldadeX + botaoDificuldade.width, dificuldadeY + botaoDificuldade.height]):
            jogarX, dificuldadeX, rankingX, sairX = -200, -200, -200, -200
            easyX = janela.width/2 - botaoEasy.width/2
            easyY = 70
            mediumX = janela.width/2 - botaoMedium.width/2
            mediumY =80 + easyY
            hardX =janela.width/2 - botaoHard.width/2
            hardY = 90 + mediumY
            chosen = True
            drawPressESC = True
        elif mouse.is_over_area([rankingX, rankingY],[rankingX + botaoRanking.width, rankingY + botaoRanking.height]):
            jogarX, dificuldadeX, rankingX, sairX = -200, -200, -200, -200
        elif mouse.is_over_area([sairX, sairY],[sairX + botaoSair.width, sairY + botaoSair.height]):
            janela.close()
    if teclado.key_pressed("ESC"):
            jogarX, dificuldadeX, rankingX, sairX = janela.width/2 - botaoJogar.width/2, janela.width / 2 - botaoDificuldade.width / 2, janela.width / 2 - botaoRanking.width / 2, janela.width / 2 - botaoSair.width / 2
            easyX, easyY, mediumX, mediumY, hardX, hardY = -200, -200, -200, -200, -200, -200
            drawPressESC = False
            gameOverBool = False
            jogar = False
    ##

    ##Desenhando elementos do Menu##
    drawMenu()
    if drawPressESC:
        pressESC.draw()
        pressESC.update()

    ##Dentro da tela de jogo##
    if jogar:
        ##Tiro##
        recarga += janela.delta_time() * dificuldade * 1.5
        if teclado.key_pressed("space") and recarga >= 1:
            shoot(initial)
            recarga = 0
        ##

        ##Atualiza posicao do monstro e desenha##
        for monsterLinha in monsters:
            if len(monsterLinha) == 0:
                monsters.remove(monsterLinha)
            for monster in monsterLinha:
                monster[0].set_position(monster[1], monster[2])
                monster[1] = monster[1] + velMonster*janela.delta_time()
                monster[0].draw()
        ##

        ##Condicao para Game Over ou Vitoria
        if len(monsters)>0:
            if monsters[len(monsters)-1][0][2] + monster_height >= janela.height - spaceShip.height:
                pontuacao = 0
                gameOverBool = True
                jogar = False
        else:
            drawPressESC = True
            jogar = False
            tiros = []
            spaceShip.set_position((janela.width / 2) - spaceShip.width, janela.height - spaceShip.height)
            velMonster = 100
            monsters = generateMonsterMatrix(N, M)
            points = 0
        ##

        ##Colisao dos monstros com as paredes laterais##
        collided = wallCollision(monsters)
        if collided!=False:
            for linha in monsters:
                if collided=="r":
                    for i in range(len(linha)):
                        linha[i][1] = linha[i][1] - 20
                    velMonster = -1 * (abs(velMonster) + 20)
                elif collided=="l":
                    for i in range(len(linha)):
                        linha[i][1] += 20
                    velMonster = (abs(velMonster) + 20)
                for i in range(len(linha)):
                    linha[i][2] = linha[i][2] + 50
        ##

        ##Atualiza posicao dos tiros, desenha e remove monstros atingidos##
        for tiro in tiros:
            tiro[0].set_position(tiro[1],tiro[2])
            tiro[0].set_total_duration(1000)
            tiro[0].update()
            tiro[0].draw()
            tiro[2] = tiro[2] -velTiro*janela.delta_time()
            if tiro[2]<=0:
                tiros.remove(tiro)
            if monsterTiroCollision(tiro,monsters):
                pontuacao+=1
                tiros.remove(tiro)
        ##
        ##Desenha nave##
        spaceShip.draw()
    ##Ocorre quando o jogador perde##
    elif gameOverBool:
        drawPressESC = True
        tiros = []
        spaceShip.set_position((janela.width / 2) - spaceShip.width, janela.height - spaceShip.height)
        velMonster = 100
        monsters = generateMonsterMatrix(N, M)
        points = 0
        gameOver.draw()
    ##Escolha e display de dificuldade##
    escolha_dificuldade(dificuldade)
    dificuldade = escolha_dificuldade(dificuldade)
    janela.draw_text("POINTS:"+str(pontuacao), janela.width-60, 10, color=(255, 255, 255))
    ##
    janela.update()