import pygame

pygame.init()
sc = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
            
    sc.fill("#ffffff")
    
    pygame.draw.rect(sc, "#ff0000", (10, 10, 100, 100), 10)
    pygame.draw.rect(sc, "#00ff00", (10, 10, 100, 100), 1)
    
    pygame.display.flip()
    clock.tick()