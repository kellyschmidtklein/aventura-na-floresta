
import sys

import pygame


# ==================================================
# AVENTURA NA FLORESTA
# Jogo 2D desenvolvido com Python e Pygame
# ==================================================

# Configuracoes da janela
LARGURA = 800
ALTURA = 600
FPS = 60

# Paleta de cores
AZUL = (120, 190, 230)
VERDE = (65, 160, 75)
VERDE_ESCURO = (25, 95, 45)
MARROM = (120, 75, 35)
ROSA = (255, 105, 180)
ROSA_CLARO = (255, 190, 215)
PELE = (255, 220, 185)
BRANCO = (255, 255, 255)
PRETO = (40, 30, 30)
AMARELO = (255, 220, 50)
ROXO = (180, 80, 255)

# Estados do jogo
MENU = "menu"
JOGANDO = "jogando"
VITORIA = "vitoria"
DERROTA = "derrota"

# Configuracoes do jogador
LARGURA_JOGADOR = 40
ALTURA_JOGADOR = 50
VELOCIDADE_JOGADOR = 5

# Configuracoes da borboleta
VELOCIDADE_BORBOLETA_X = 3
VELOCIDADE_BORBOLETA_Y = 2

# Posicoes das flores
POSICOES_FLORES = [
    (150, 500),
    (270, 430),
    (390, 500),
    (510, 420),
    (630, 500),
    (730, 430),
]

TOTAL_FLORES = len(POSICOES_FLORES)


def escrever(tela, texto, fonte, cor, x, y):
    """Desenha um texto centralizado na tela."""
    imagem = fonte.render(texto, True, cor)
    retangulo = imagem.get_rect(center=(x, y))
    tela.blit(imagem, retangulo)


def desenhar_arvore(tela, x, y):
    """Desenha uma arvore no cenario."""
    pygame.draw.rect(tela, MARROM, (x + 20, y + 50, 25, 90))
    pygame.draw.circle(tela, VERDE_ESCURO, (x + 32, y + 30), 48)
    pygame.draw.circle(tela, VERDE, (x + 5, y + 45), 30)
    pygame.draw.circle(tela, VERDE, (x + 60, y + 45), 30)


def desenhar_cenario(tela):
    """Desenha o ceu, o gramado e os elementos do cenario."""
    tela.fill(AZUL)

    # Gramado
    pygame.draw.rect(tela, VERDE, (0, 180, LARGURA, 420))

    # Arvores
    for x in range(20, LARGURA, 150):
        desenhar_arvore(tela, x, 180)

    # Nuvem da esquerda
    pygame.draw.circle(tela, BRANCO, (150, 90), 25)
    pygame.draw.circle(tela, BRANCO, (180, 80), 30)
    pygame.draw.circle(tela, BRANCO, (210, 95), 23)

    # Nuvem da direita
    pygame.draw.circle(tela, BRANCO, (550, 75), 25)
    pygame.draw.circle(tela, BRANCO, (580, 65), 30)
    pygame.draw.circle(tela, BRANCO, (610, 80), 23)

    # Flores decorativas
    for x in range(30, LARGURA, 100):
        pygame.draw.line(
            tela, VERDE_ESCURO, (x, 530), (x, 545), 3
        )
        pygame.draw.circle(tela, ROSA, (x, 525), 6)
        pygame.draw.circle(tela, AMARELO, (x, 525), 3)


def desenhar_jogador(tela, jogador):
    """Desenha a personagem com vestido rosa."""
    x = jogador.x
    y = jogador.y

    # Pernas
    pygame.draw.line(
        tela, PELE, (x + 15, y + 40), (x + 12, y + 50), 4
    )
    pygame.draw.line(
        tela, PELE, (x + 25, y + 40), (x + 28, y + 50), 4
    )

    # Vestido
    pygame.draw.ellipse(tela, ROSA, (x + 5, y + 20, 30, 25))

    # Bracos
    pygame.draw.line(
        tela, PELE, (x + 7, y + 25), (x, y + 35), 5
    )
    pygame.draw.line(
        tela, PELE, (x + 33, y + 25), (x + 40, y + 35), 5
    )

    # Cabelo e rosto
    pygame.draw.circle(tela, (100, 55, 30), (x + 20, y + 11), 13)
    pygame.draw.circle(tela, PELE, (x + 20, y + 11), 9)

    # Olhos
    pygame.draw.circle(tela, PRETO, (x + 17, y + 10), 1)
    pygame.draw.circle(tela, PRETO, (x + 23, y + 10), 1)

    # Sorriso
    pygame.draw.arc(
        tela, (150, 50, 50), (x + 16, y + 11, 8, 6),
        3.14, 6.28, 1
    )

    # Lacinho
    pygame.draw.circle(tela, ROSA_CLARO, (x + 12, y + 1), 5)
    pygame.draw.circle(tela, ROSA_CLARO, (x + 20, y + 1), 5)


def desenhar_borboleta(tela, borboleta_x, borboleta_y):
    """Desenha a borboleta que representa o inimigo."""
    x = int(borboleta_x)
    y = int(borboleta_y)

    # Asas
    pygame.draw.ellipse(tela, ROXO, (x - 17, y - 10, 20, 18))
    pygame.draw.ellipse(tela, ROSA_CLARO, (x + 2, y - 10, 20, 18))

    # Corpo
    pygame.draw.line(
        tela, PRETO, (x + 2, y - 8), (x + 2, y + 12), 4
    )

    # Antenas
    pygame.draw.line(
        tela, PRETO, (x + 2, y - 8), (x - 5, y - 17), 2
    )
    pygame.draw.line(
        tela, PRETO, (x + 2, y - 8), (x + 9, y - 17), 2
    )


def obter_area_borboleta(borboleta_x, borboleta_y):
    """Retorna a area usada para detectar colisao com a borboleta."""
    return pygame.Rect(
        int(borboleta_x - 15),
        int(borboleta_y - 12),
        30,
        25,
    )


def mover_borboleta(borboleta_x, borboleta_y, direcao_x, direcao_y):
    """Movimenta a borboleta e inverte a direcao ao atingir os limites."""
    borboleta_x += VELOCIDADE_BORBOLETA_X * direcao_x
    borboleta_y += VELOCIDADE_BORBOLETA_Y * direcao_y

    if borboleta_x >= 770 or borboleta_x <= 25:
        direcao_x *= -1

    if borboleta_y >= 455 or borboleta_y <= 100:
        direcao_y *= -1

    return borboleta_x, borboleta_y, direcao_x, direcao_y


def desenhar_flores(tela, flores):
    """Desenha as flores que podem ser coletadas."""
    for flor in flores:
        pygame.draw.line(
            tela,
            VERDE_ESCURO,
            (flor.centerx, flor.centery + 5),
            (flor.centerx, flor.centery + 16),
            3,
        )
        pygame.draw.circle(tela, ROSA, flor.center, 9)
        pygame.draw.circle(tela, AMARELO, flor.center, 4)


def desenhar_pontuacao(tela, fonte_normal, pontuacao):
    """Mostra a pontuacao durante o jogo."""
    texto = f"Flores: {pontuacao}/{TOTAL_FLORES}"
    imagem = fonte_normal.render(texto, True, BRANCO)

    pygame.draw.rect(
        tela, VERDE_ESCURO, (10, 10, 180, 40), border_radius=10
    )
    tela.blit(imagem, (20, 16))


def criar_flores():
    """Cria e retorna as areas de colisao das flores."""
    return [
        pygame.Rect(x - 10, y - 10, 20, 20)
        for x, y in POSICOES_FLORES
    ]


def desenhar_menu(tela, fonte_titulo, fonte_normal, fonte_pequena):
    """Apresenta o menu inicial e os comandos."""
    desenhar_cenario(tela)

    pygame.draw.rect(
        tela, VERDE_ESCURO, (110, 65, 580, 430), border_radius=25
    )

    escrever(
        tela, "AVENTURA NA FLORESTA",
        fonte_titulo, BRANCO, 400, 130
    )
    escrever(
        tela, "Ajude a menina a encontrar as flores!",
        fonte_normal, ROSA_CLARO, 400, 205
    )
    escrever(
        tela, "SETAS: movimentar a personagem",
        fonte_pequena, BRANCO, 400, 270
    )
    escrever(
        tela, "Colete todas as 6 flores para vencer.",
        fonte_pequena, BRANCO, 400, 305
    )
    escrever(
        tela, "Evite encostar na borboleta!",
        fonte_pequena, BRANCO, 400, 340
    )
    escrever(
        tela, "ENTER: iniciar o jogo",
        fonte_normal, AMARELO, 400, 405
    )
    escrever(
        tela, "ESC: sair",
        fonte_pequena, BRANCO, 400, 445
    )


def desenhar_fim(
    tela, titulo, mensagem, fonte_titulo, fonte_normal, fonte_pequena
):
    """Apresenta a tela de vitoria ou derrota."""
    desenhar_cenario(tela)

    pygame.draw.rect(
        tela, VERDE_ESCURO, (130, 170, 540, 260), border_radius=25
    )

    escrever(tela, titulo, fonte_titulo, AMARELO, 400, 235)
    escrever(tela, mensagem, fonte_normal, BRANCO, 400, 305)
    escrever(
        tela, "ENTER: jogar novamente",
        fonte_normal, ROSA_CLARO, 400, 365
    )
    escrever(
        tela, "ESC: sair",
        fonte_pequena, BRANCO, 400, 400
    )


def executar_jogo():
    """Inicializa os recursos e executa o ciclo principal do jogo."""
    pygame.init()

    tela = pygame.display.set_mode((LARGURA, ALTURA))
    pygame.display.set_caption("Aventura na Floresta")
    relogio = pygame.time.Clock()

    fonte_titulo = pygame.font.SysFont("Arial", 48, bold=True)
    fonte_normal = pygame.font.SysFont("Arial", 23)
    fonte_pequena = pygame.font.SysFont("Arial", 17)

    estado = MENU
    rodando = True

    jogador = pygame.Rect(60, 470, LARGURA_JOGADOR, ALTURA_JOGADOR)

    borboleta_x = 400.0
    borboleta_y = 300.0
    direcao_x = 1
    direcao_y = 1

    pontuacao = 0
    flores = criar_flores()

    while rodando:
        relogio.tick(FPS)

        # Eventos do teclado e da janela
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False

            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    rodando = False

                elif evento.key == pygame.K_RETURN:
                    if estado in (MENU, VITORIA, DERROTA):
                        jogador = pygame.Rect(
                            60, 470, LARGURA_JOGADOR, ALTURA_JOGADOR
                        )
                        borboleta_x = 400.0
                        borboleta_y = 300.0
                        direcao_x = 1
                        direcao_y = 1
                        pontuacao = 0
                        flores = criar_flores()
                        estado = JOGANDO

        # Tela do menu
        if estado == MENU:
            desenhar_menu(
                tela, fonte_titulo, fonte_normal, fonte_pequena
            )

        # Partida em andamento
        elif estado == JOGANDO:
            teclas = pygame.key.get_pressed()

            # Movimentacao da personagem
            if teclas[pygame.K_LEFT]:
                jogador.x -= VELOCIDADE_JOGADOR
            if teclas[pygame.K_RIGHT]:
                jogador.x += VELOCIDADE_JOGADOR
            if teclas[pygame.K_UP]:
                jogador.y -= VELOCIDADE_JOGADOR
            if teclas[pygame.K_DOWN]:
                jogador.y += VELOCIDADE_JOGADOR

            # Impede que a personagem saia da tela
            jogador.clamp_ip(tela.get_rect())

            # Movimentacao da borboleta
            (
                borboleta_x,
                borboleta_y,
                direcao_x,
                direcao_y,
            ) = mover_borboleta(
                borboleta_x, borboleta_y, direcao_x, direcao_y
            )

            # Coleta das flores
            flores_coletadas = [
                flor for flor in flores if jogador.colliderect(flor)
            ]

            for flor in flores_coletadas:
                flores.remove(flor)
                pontuacao += 1

            # Verificacao de colisao com a borboleta
            area_borboleta = obter_area_borboleta(
                borboleta_x, borboleta_y
            )

            if jogador.colliderect(area_borboleta):
                estado = DERROTA

            # Condicao de vitoria
            if pontuacao == TOTAL_FLORES:
                estado = VITORIA

            # Desenho da partida
            desenhar_cenario(tela)
            desenhar_flores(tela, flores)
            desenhar_borboleta(tela, borboleta_x, borboleta_y)
            desenhar_jogador(tela, jogador)
            desenhar_pontuacao(tela, fonte_normal, pontuacao)

        # Tela de vitoria
        elif estado == VITORIA:
            desenhar_fim(
                tela,
                "VOCE VENCEU!",
                "Todas as flores foram coletadas!",
                fonte_titulo,
                fonte_normal,
                fonte_pequena,
            )

        # Tela de derrota
        elif estado == DERROTA:
            desenhar_fim(
                tela,
                "FIM DE JOGO!",
                "A borboleta alcancou a personagem.",
                fonte_titulo,
                fonte_normal,
                fonte_pequena,
            )

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    try:
        executar_jogo()
    except pygame.error as erro:
        print(f"Erro do Pygame: {erro}")
    except Exception as erro:
        print(f"Erro inesperado: {erro}")
        raise
    finally:
        pygame.quit()
