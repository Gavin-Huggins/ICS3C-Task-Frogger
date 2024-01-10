# Programmer: 
# Description: 

# Import and initialize the pygame library
import pygame
from pygame.locals import *
pygame.init()

# Import functions for drawing gridlines and using sprites
from pygame_grid import make_grid
from ucc_sprite import Sprite

### SET UP GLOBAL CONSTANTS HERE
WIDTH = 640
HEIGHT = 480
BACKGROUND_COLOR = "#444444"
FONT_COLOR = "#6aa84f"
GAME_OVER_COLOR = "crimson"
PAUSED_COLOR = "gold"
START_TIME = 10

# Create and open a pygame screen with the given size
screen = pygame.display.set_mode((WIDTH, HEIGHT))
grid = make_grid()

# Set the title of the pygame screen
pygame.display.set_caption("Frogger")

# Create a clock to keep track of time
clock = pygame.time.Clock()

# Group to hold all of the active sprites
all_sprites = pygame.sprite.LayeredUpdates()

### SET UP YOUR GAME HERE

# Load the images

background_image = pygame.image.load("streets.png")

start_button_image = pygame.image.load("start.png")
start_button_image = pygame.transform.rotozoom(start_button_image, 0, 0.75)
pause_button_image = pygame.image.load("pause.png")
pause_button_image = pygame.transform.rotozoom(pause_button_image, 0, 0.75)
exit_button_image = pygame.image.load("exit.png")
exit_button_image = pygame.transform.rotozoom(exit_button_image, 0, 0.75)

bus_image = pygame.image.load("bus.png")
bus_image = pygame.transform.rotozoom(bus_image, 0, 0.3)
car_image = pygame.image.load("redcar.png")
car_image = pygame.transform.rotozoom(car_image, 0, 0.3)
cruiser_image = pygame.image.load("police.png")
cruiser_image = pygame.transform.rotozoom(cruiser_image, 0, 0.12)
taxi_image = pygame.image.load("taxi.png")
taxi_image = pygame.transform.rotozoom(taxi_image, 0, 0.3)

frog_image = pygame.image.load("frog.png")



# Sprites for the vehicles
vehicles = pygame.sprite.Group()

bus = Sprite(bus_image)
bus.center = (0, 186)

car = Sprite(car_image)
car.center = (WIDTH, 140)


cruiser = Sprite(cruiser_image)
cruiser.center = (WIDTH, 290)


taxi = Sprite(taxi_image)
taxi.center = (0, 340)

frog = Sprite(frog_image)
frog.center = (WIDTH / 2, 450)

# Sprite which displays the time remaining
baloo_font_small = pygame.font.Font("Baloo.ttf", 36)
time_left = START_TIME
timer = Sprite(baloo_font_small.render(f"{time_left}", True, FONT_COLOR))
timer.center = (2 * WIDTH / 3, 30)
timer.add(all_sprites)

# Sprite with GAME OVER message
baloo_font_large = pygame.font.Font("Baloo.ttf", 72)
game_over = Sprite(baloo_font_large.render("GAME OVER", True, GAME_OVER_COLOR))
game_over.center = (WIDTH / 2, HEIGHT / 2)

paused = Sprite(baloo_font_large.render("PAUSED", True, PAUSED_COLOR))
paused.center = (WIDTH / 2, HEIGHT / 2)
# Create a timer for the countdown clock
COUNTDOWN = pygame.event.custom_type()



### DEFINE HELPER FUNCTIONS
leave = Sprite(exit_button_image)
leave.center = (WIDTH / 1.4, 450)
leave.add(all_sprites)

start = Sprite(start_button_image)
start.center = (WIDTH / 5.2, 450)
start.add(all_sprites)

pause = Sprite(pause_button_image)
pause.center = (WIDTH / 3, 450)

# Main Loop
running = True
while running:
    # Set the frame rate to 60 frames per second
    clock.tick(60)

    for event in pygame.event.get():
        # Check if the quit (X) button was clicked
        if event.type == QUIT:
            running = False

        ### MANAGE OTHER EVENTS SINCE THE LAST FRAME
             
        elif event.type == COUNTDOWN:
            time_left -= 1
            timer.image = baloo_font_small.render(f"{time_left}", True, FONT_COLOR)
            timer.center = (2 * WIDTH / 3, 30)
            
            if time_left == 0:
                game_over.add(all_sprites)
                for vehicle in vehicles:
                    vehicle.kill()
                pause.kill()
                start.add(all_sprites)
                frog.kill()
        elif event.type == MOUSEBUTTONDOWN:
            if leave.mask_contains_point(event.pos):
                running = False
                
            if start.mask_contains_point(event.pos):
                if time_left == 0:
                    time_left = START_TIME
                    timer.image = baloo_font_small.render(f"{time_left}", True, FONT_COLOR)
                    timer.center = (2 * WIDTH / 3, 30)
                    game_over.kill()
                
                taxi.speed = 7
                taxi.add(all_sprites, vehicles)
                cruiser.speed = 3
                cruiser.add(all_sprites, vehicles)
                cruiser.direction = 180
                car.speed = 5
                car.add(all_sprites, vehicles)
                car.direction = 180
                bus.speed = 10
                bus.add(all_sprites, vehicles)
                pygame.time.set_timer(COUNTDOWN, 1000, time_left)
                start.kill()
                paused.kill()
                pause.add(all_sprites)
                frog.add(all_sprites)
            if pause.mask_contains_point(event.pos):
                for vehicle in vehicles:
                    vehicle.kill()
                frog.kill()
                pause.kill()
                paused.add(all_sprites)
                start.add(all_sprites)
                pygame.time.set_timer(COUNTDOWN, 0)
                
    keys = pygame.key.get_pressed()
    if keys[K_UP] and frog.top > 0:
        frog.y -= 1
    if keys[K_DOWN] and frog.bottom < HEIGHT - 60:
        frog.y += 1
    if keys[K_LEFT] and frog.left > 0:
        frog.x -= 1
    if keys[K_RIGHT] and frog.right < WIDTH:
        frog.x += 1
    ### MANAGE GAME STATE FRAME-BY-FRAME
    for vehicle in vehicles:
        if vehicle.left > WIDTH:
            vehicle.right = 0
        elif vehicle.right < 0:
            vehicle.left = WIDTH
        # Check when car hits frog
        
    

    # Update the sprites' locations
    all_sprites.update()

    # Clear the screen
    screen.fill(BACKGROUND_COLOR)
    screen.blit(background_image, (0, 60))

    # Redraw the sprites
    all_sprites.draw(screen)

    # Uncomment the next line to show a grid
    # screen.blit(grid, (0,0))

    # Flip the changes to the screen to the computer display
    pygame.display.flip()

# End the program
pygame.quit()