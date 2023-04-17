import pygame
from sys import exit
from random import randint, choice
from Jugador import Player
from Obstaculo import Obstacle


def display_score():
	current_time = int(pygame.time.get_ticks() / 1000) - start_time
	score_surf = test_font.render(f'Score: {current_time}',False,(64,64,64))
	score_rect = score_surf.get_rect(center = (400,50))
	screen.blit(score_surf,score_rect)
	return current_time


def collision_sprite():
	if pygame.sprite.spritecollide(player.sprite,obstacle_group,False):
		obstacle_group.empty()
		game_over_sound.play(loops=0)
		pygame.time.delay(2000)
		return False
	else: return True


pygame.init()
screen = pygame.display.set_mode((800,400))
pygame.display.set_caption('Player Runner')
clock = pygame.time.Clock()
test_font = pygame.font.Font('font/Pixeltype.ttf', 50)
game_active = False
start_time = 0
score = 0
score_list = [0]
max_score = 0
bg_music = pygame.mixer.Sound('audio/music.wav')
bg_music.set_volume(0.1)
game_over_sound = pygame.mixer.Sound('audio/game_over.mp3')
game_over_sound.set_volume(0.1)
bg_music.play(loops = -1)

#Groups
player = pygame.sprite.GroupSingle()
player.add(Player())

obstacle_group = pygame.sprite.Group()

sky_surface = pygame.image.load('graphics/Sky.png').convert()
ground_surface = pygame.image.load('graphics/ground.png').convert()
background_init =pygame.image.load('graphics/background.png').convert()

# Intro screen
player_stand = pygame.image.load('graphics/player/n_stand.png').convert_alpha()
player_stand = pygame.transform.rotozoom(player_stand,0,1.5)
player_stand_rect = player_stand.get_rect(center = (400,200))

game_name = test_font.render('Player Runner',False,(255, 99, 71))
game_name_rect = game_name.get_rect(center = (400,80))

game_message = test_font.render('Press space to run',False,(111,196,169))
game_message_rect = game_message.get_rect(center = (400,330))

# Timer 
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer,1500)

while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			exit()

		if game_active:
			if event.type == obstacle_timer:
				obstacle_group.add(Obstacle(choice(['fly','snail','snail','snail'])))
		
		else:
			if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
				game_active = True
				start_time = int(pygame.time.get_ticks() / 1000)

	if game_active:
		screen.blit(sky_surface,(0,0))
		screen.blit(ground_surface,(0,300))
		score = display_score()
		player.draw(screen)
		player.update()

		obstacle_group.draw(screen)
		obstacle_group.update()

		game_active = collision_sprite()
		
	else:
		score_list.append(score)
		max_score = max(score_list)
		screen.blit(background_init,(0,0))
		screen.blit(player_stand,player_stand_rect)
		score_message = test_font.render(f'Score: {score} Maximo: {max_score}',True,(111,196,169))
		score_message_rect = score_message.get_rect(center = (400,300))
		screen.blit(game_name,game_name_rect)

		
		if score == 0: screen.blit(game_message,game_message_rect)
		elif score == max_score:
			display3 = test_font.render(f"New High Score!!", True, (100,35,35))
			screen.blit(score_message,score_message_rect)
			screen.blit(display3, (200,330))
		else: screen.blit(score_message,score_message_rect)

	pygame.display.update()
	clock.tick(60)