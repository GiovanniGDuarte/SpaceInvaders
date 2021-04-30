from PPlay.window import *
from PPlay.gameimage import *
from PPlay.sprite import *
from PPlay.collision import *
################### Menu ################################################
##Seta as posicoes dos botoes do Menu##
def set_menu(botoes,coordenadas):
    i = 0
    for botao in botoes:
        botao.set_position(coordenadas[i], coordenadas[i+1])
        i+=2
##

##Desenha o menu##
def drawMenu(list):
    for item in list:
        item.draw()
##

##Escolha de dificuldade##
def escolha_dificuldade(dificuldade,easyX,easyY,botaoEasy,mediumX,mediumY,botaoMedium,hardX,hardY,botaoHard,janela,mouse):
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

#################### Tiros e Colisoes com tiros #########################

##Cria matriz de tiros para Player##
def shootPlayer(initialx, tirosPlayer,janela, spaceShip):
    tiro = Sprite("Actors and background/tiro2.png", 4)
    tirox = initialx
    tiroY = janela.height - spaceShip.height
    tirosPlayer.append([tiro, tirox, tiroY])
##

## Cria matriz de super tiros##
def shootSuperTiro(initial,superTiros,janela,spaceShip):
    superTiro = Sprite("Actors and background/superTiro.png", 5)
    tirox = initial
    tiroY = janela.height-spaceShip.height
    superTiros.append([superTiro,tirox,tiroY])
##
##Cria matriz de tiros para Monstros##
def shootMonstros(initialx, initialy, tirosMonstros):
    tiro = Sprite("Actors and background/tiro.png", 4)
    tirox = initialx
    tiroy = initialy
    tirosMonstros.append([tiro, tirox, tiroy])
##

##Atualiza os tiros dos Monstros##
def tirosMonstrosUpdate(tirosMonstros,janela,invencivel,velTiro,spaceShip):
    for tiro in tirosMonstros:
        tiro[0].set_position(tiro[1], tiro[2])
        tiro[0].set_total_duration(1000)
        tiro[0].update()
        tiro[0].draw()
        tiro[2] = tiro[2] + velTiro * janela.delta_time()
        if tiro[2] >= janela.height:
            tirosMonstros.remove(tiro)
        if tiro[0].collided(spaceShip) and invencivel == False:
            tirosMonstros.remove(tiro)
            return True
##
## Atualiza matriz  de super tiros ##
def superTirosUpdate(superTiros, monsters, velTiro, janela):
    for superTiro in superTiros:
        superTiro[0].set_position(superTiro[1], superTiro[2])
        superTiro[0].set_total_duration(1000)
        superTiro[0].update()
        superTiro[0].draw()
        superTiro[2] = superTiro[2] - velTiro * janela.delta_time()
        if superTiro[2] <= 0:
            superTiros.remove(superTiro)
        if monsterTiroCollision(superTiro,monsters):
            return True
##

##Atualiza os tiros dos players##
def tirosPlayerUpdate(tirosPlayer,monsters, velTiro,janela):
        for tiro in tirosPlayer:
            tiro[0].set_position(tiro[1],tiro[2])
            tiro[0].set_total_duration(1000)
            tiro[0].update()
            tiro[0].draw()
            tiro[2] = tiro[2] -velTiro*janela.delta_time()
            if tiro[2]<=0:
                tirosPlayer.remove(tiro)
            if monsterTiroCollision(tiro,monsters):
                tirosPlayer.remove(tiro)
                return True
##

##Checa colisao de tiros do player com monstros (testa primeiro a colisao com a primeira linha e elimina os casos em que o tiro esta a direita ou a esquerda de um bloco)##
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

#######################################################################

#################### Monstros ####################
#Gera matriz de monstros##
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
def wallCollisionBool(monsters, janela):
    for linha in monsters:
        if linha[len(linha) - 1][1] > janela.width:
            return("r")
        elif linha[0][1] < 0:
            return("l")
    return False
##

##Incrementa a velocidade do monstro se ele colidir com paredes laterais##
def wallCollision(monsters,janela, dificuldade, velMonster):
    collided = wallCollisionBool(monsters,janela)
    if collided != False:
        for linha in monsters:
            if collided == "r":
                for i in range(len(linha)):
                    linha[i][1] = linha[i][1] - 20
                velMonster = -1 * (abs(velMonster) + 40 // dificuldade)
            elif collided == "l":
                for i in range(len(linha)):
                    linha[i][1] += 20
                velMonster = (abs(velMonster) + 40 // dificuldade)
            for i in range(len(linha)):
                linha[i][2] = linha[i][2] + 50
    return velMonster
##
##Atualiza a posicao dos montrsos##
def monstersUpdate(monsters,velMonster,janela):
    for monsterLinha in monsters:
        if len(monsterLinha) == 0:
            monsters.remove(monsterLinha)
        for monster in monsterLinha:
            monster[0].set_position(monster[1], monster[2])
            monster[1] = monster[1] + velMonster * janela.delta_time()
            monster[0].draw()
##

######################################################

############# Player #################################

##Atualiza posicao da nave##
def spaceShipPosition(initial,spaceShip, teclado, janela):
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

########################################################
