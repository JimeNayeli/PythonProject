import pygame
from sys import exit
from random import randint, choice
from Jugador import Avatar
from Obstaculos import Obstaculo


def display_score():
	current_time = int(pygame.time.get_ticks() / 1000) - start_time
	score_surf = test_font.render(f'Puntos: {current_time}',False,(64,64,64))
	score_rect = score_surf.get_rect(center = (400,50))
	screen.blit(score_surf,score_rect)
	return current_time


def collision_sprite():
    if pygame.sprite.spritecollide(player.sprite, obstacle_group, False):
        pygame.mixer.pause()
        obstacle_group.empty()
        game_over_sound.play(loops=0)
        pygame.time.delay(2300)
        return False
    else:
        return True

#####Juego########################################################
pygame.init()
screen = pygame.display.set_mode((800,400))
pygame.display.set_caption('Player Runner')
clock = pygame.time.Clock()
test_font = pygame.font.Font('font/Pixeltype.ttf', 50)
game_active = False
start_time = 0
puntos = 0
lista_puntos = [0]
puntaje_max = 0
bg_music = pygame.mixer.Sound('audio/music.wav')
bg_music.set_volume(0.1)
game_over_sound = pygame.mixer.Sound('audio/game_over.mp3')
game_over_sound.set_volume(0.1)
bg_music.play(loops = -1)

#Grupos
player = pygame.sprite.GroupSingle()
player.add(Avatar())

obstacle_group = pygame.sprite.Group()

sky_surface = pygame.image.load('imagenes/Sky.png').convert()
ground_surface = pygame.image.load('imagenes/ground.png').convert()
background_init = pygame.image.load('imagenes/background.png').convert()

# Pantalla inicial
img_avatar = pygame.image.load('imagenes/avatar/n_stand.png').convert_alpha()
img_avatar = pygame.transform.rotozoom(img_avatar,0,1.5)
rectan_avatar = img_avatar.get_rect(center = (400,200))

nombre_juego = test_font.render('Player Runner',False,(255, 99, 71))
rectangulo_nombre_juego = nombre_juego.get_rect(center = (400,80))

instrucciones = test_font.render('Presione ESPACIO para comenzar',False,(111,196,169))
rectan_instrucc = instrucciones.get_rect(center = (400,330))

# Tiempo/ Puntaje
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer,1500)

while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			exit()

		if game_active:
			if event.type == obstacle_timer:
				obstacle_group.add(Obstaculo(choice(['fly','crocodile','crocodile','crocodile'])))
		
		else:
			if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
				game_active = True
				start_time = int(pygame.time.get_ticks() / 1000)
		pygame.mixer.unpause()


	if game_active:
		screen.blit(sky_surface,(0,0))
		screen.blit(ground_surface,(0,300))
		puntos = display_score()
		player.draw(screen)
		player.update()

		obstacle_group.draw(screen)
		obstacle_group.update()

		game_active = collision_sprite()
		
	else:
		lista_puntos.append(puntos)
		puntaje_max = max(lista_puntos)
		screen.blit(background_init,(0,0))
		screen.blit(img_avatar,rectan_avatar)
		puntos_alcanzados = test_font.render(f'Puntos: {puntos}   Máximo: {puntaje_max}',True,(111,196,169))
		rectangulo_puntos = puntos_alcanzados.get_rect(center = (400,300))
		screen.blit(nombre_juego,rectangulo_nombre_juego)

		
		if puntos == 0: screen.blit(instrucciones,rectan_instrucc)
		elif puntaje_max == puntos:
			display3 = test_font.render(f"¡¡Nueva Puntuación Alta!!", True, (100,35,35))
			screen.blit(puntos_alcanzados,rectangulo_puntos)
			screen.blit(display3, (160,330))
		else: screen.blit(puntos_alcanzados,rectangulo_puntos)

	pygame.display.update()
	clock.tick(60)