from PPlay.window import *
from PPlay.gameimage import *
from PPlay.sprite import *
import SpaceInvadersLib
import random

janela = Window(600,400)
janela.set_title("Space Invaders")
mouse = Window.get_mouse()
teclado = Window.get_keyboard()

##Game Objects##
fundo = GameImage("Actors and background/space.png")
botaoJogar = GameImage("Buttons/jogar.png")
botaoDificuldade = GameImage("Buttons/dificuldade.png")
botaoRanking = GameImage("Buttons/ranking.png")
botaoSair = GameImage("Buttons/sair.png")
botaoEasy = GameImage("Buttons/easy.png")
botaoMedium = GameImage("Buttons/MEDIUM.png")
botaoHard = GameImage("Buttons/hard.png")
spaceShip = GameImage("Actors and background/spaceship.png")
spaceshipBlink = Sprite("Actors and background/spaceshipBlink.png",2)
spaceshipBlink.set_total_duration(500)
gameOver = GameImage("Messages/gameOver.png")
gameOver.set_position((janela.width/2)-gameOver.width/2,(janela.height/2)-gameOver.height/2)
pressESC = Sprite("Messages/PressESC.png",2)
pressESC.set_position(janela.width/2-pressESC.width/2,janela.height-pressESC.height)
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
tirosPlayer = []
superTiros = []
tirosMonstros = []
velMonster = 100
monster_height = GameImage("Actors and background/spaceInvader.png").height
recargaPlayer = 0
recargaSuperTiro = 0
tempoSuperTiro = 0
recargaMonstro = 0
lives = 3
invencivel = False
invencivelTempo = 0
pontuacao = 0
points = 0
drawTotalPoints = False
tempo = 0

##Gerando a matriz dado NxM##
N,M = 2,10
monsters = SpaceInvadersLib.generateMonsterMatrix(N,M)
##

while True:
    #Posicoes iniciais, atualizacao da posicao da Nave e contador de Tempo##
    SpaceInvadersLib.set_menu([botaoJogar,botaoDificuldade,botaoRanking,botaoSair,botaoEasy,botaoMedium,botaoHard],[jogarX,jogarY,dificuldadeX,dificuldadeY,rankingX,rankingY,sairX,sairY,easyX,easyY,mediumX,mediumY,hardX,hardY])
    initial = SpaceInvadersLib.spaceShipPosition(initial, spaceShip, teclado, janela)
    tempo = tempo + janela.delta_time()
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
            drawTotalPoints = False
            jogar = False
    ##

    ##Desenhando elementos do Menu##
    SpaceInvadersLib.drawMenu([fundo, botaoJogar, botaoDificuldade, botaoRanking, botaoSair,botaoEasy,botaoMedium,botaoHard])
    if drawPressESC:
        pressESC.draw()
        pressESC.update()

    ##Dentro da tela de jogo##
    if jogar:
        ##Tiros de monstros e player##
        recargaPlayer += janela.delta_time() * dificuldade*1.5
        recargaMonstro += (janela.delta_time()/(dificuldade))*1.5
        if recargaMonstro >= 1:
            monsterLinha = monsters[random.choice(range(0,len(monsters)))]
            monster = monsterLinha[random.choice(range(0,len(monsterLinha)))]
            SpaceInvadersLib.shootMonstros(monster[1],monster[2],tirosMonstros)
            recargaMonstro = 0
        if teclado.key_pressed("space") and recargaPlayer >= 1:
            if tempoSuperTiro == 0:
                SpaceInvadersLib.shootPlayer(initial,tirosPlayer,janela,spaceShip)
            if tempoSuperTiro >= 2:
                SpaceInvadersLib.shootSuperTiro(initial,superTiros,janela,spaceShip)
                tempoSuperTiro = 0
            recargaPlayer = 0
            tempoSuperTiro += janela.delta_time()*100
        elif not teclado.key_pressed("space"):
            tempoSuperTiro = 0
        ##

        ##Atualiza posicao do monstro e desenha##
        SpaceInvadersLib.monstersUpdate(monsters,velMonster,janela)
        ##

        ##Condicao para Game Over ou Vitoria
        if len(monsters)>0:
            if monsters[len(monsters)-1][0][2] + monster_height >= janela.height - spaceShip.height or lives<=0:
                gameOverBool = True
                jogar = False
        else:
            Invencivel = False
            drawPressESC = True
            drawTotalPoints = True
            jogar = False
            tirosPlayer = []
            tirosMonstros = []
            spaceShip.set_position((janela.width / 2) - spaceShip.width, janela.height - spaceShip.height)
            velMonster = 100
            monsters = SpaceInvadersLib.generateMonsterMatrix(N, M)
            points = pontuacao
            pontuacao = 0
            lives = 3
        ##

        ##Colisao dos monstros com as paredes laterais##
        velMonster = SpaceInvadersLib.wallCollision(monsters,janela,dificuldade,velMonster)
        ##

        ##Atualiza a matriz de tiros dos monstros e retorna verdadeiro se um tiro colidiu com o player##
        if SpaceInvadersLib.tirosMonstrosUpdate(tirosMonstros,janela,invencivel,velTiro,spaceShip) == True:
            lives -= 1
            initial = janela.width / 2 - spaceShip.width
            invencivel = True
        ##

        ##Estado de invencibilidade##
        if invencivel == True:
            invencivelTempo += janela.delta_time()
            spaceshipBlink.set_position(initial,janela.height - spaceshipBlink.height)
            spaceshipBlink.draw()
            spaceshipBlink.update()
            if invencivelTempo > 2:
                invencivel = False
                invencivelTempo = 0
        ##

        ##Atualiza posicao dos tirosPlayer, desenha, retorna verdadeiro se um monstro for atingido##
        if SpaceInvadersLib.tirosPlayerUpdate(tirosPlayer,monsters, velTiro,janela) == True or SpaceInvadersLib.superTirosUpdate(superTiros, monsters, velTiro, janela) == True:
                pontuacao+=int(100/tempo)
        ##

        ##Desenha nave, vidas e score##
        if invencivel == False:
            spaceShip.draw()
        janela.draw_text("LIVES: " + str(lives), janela.width/2-20, 0, color=(255, 255, 255))
        janela.draw_text("SCORE: " + str(pontuacao), janela.width - 80, 10, color=(255, 255, 255))
        ##

    ##Ocorre quando o jogador perde##
    elif gameOverBool:
        Invencivel = False
        drawPressESC = True
        lives = 3
        tirosPlayer = []
        tirosMonstros = []
        spaceShip.set_position((janela.width / 2) - spaceShip.width, janela.height - spaceShip.height)
        velMonster = 100
        monsters = SpaceInvadersLib.generateMonsterMatrix(N, M)
        pontuacao = 0
        gameOver.draw()
    ##

    ##Escolha e display de dificuldade, desenho de Total Score ao vencer##
    dificuldade = SpaceInvadersLib.escolha_dificuldade(dificuldade,easyX,easyY,botaoEasy,mediumX,mediumY,botaoMedium,hardX,hardY,botaoHard,janela,mouse)
    if pontuacao == 0 and drawTotalPoints:
        janela.draw_text("TOTAL SCORE: " + str(points), janela.width / 2 -175, janela.height / 2-40,size=(40), color=(255, 255, 255))
    ##
    janela.update()