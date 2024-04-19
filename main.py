import pygame
import sys
from cuboid import Cuboid

def load_cuboid(filename):
    vertices = []
    with open(filename, 'r') as file:
        for line in file:
            coords = line.strip().split()
            x, y, z = map(float, coords)
            vertices.append((x, y, z, 1))
    return Cuboid(vertices)

def main(filenames):
    WIDTH = 600
    HEIGHT = 600
    BLACK = (0,0,0)

    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('virtual-camera')

    cuboids = []
    for filename in filenames:
        cuboids.append(load_cuboid(filename))

    start_translation = 320
    for cuboid in cuboids:
            cuboid.translate(0, 0, start_translation)
    translation_step = 60
    rotation_step = 30
    near = 0.1
    far = 1000
    aspect_ratio = WIDTH/HEIGHT

    fov = 90

    clock = pygame.time.Clock()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    for cuboid in cuboids:
                        cuboid.translate(-translation_step, 0, 0)  
                elif event.key == pygame.K_LEFT:
                    for cuboid in cuboids:
                        cuboid.translate(translation_step, 0, 0)   
                elif event.key == pygame.K_UP:
                    for cuboid in cuboids:
                        cuboid.translate(0, translation_step, 0)   
                elif event.key == pygame.K_DOWN:
                    for cuboid in cuboids:
                        cuboid.translate(0, -translation_step, 0)
                elif event.key == pygame.K_BACKSPACE:
                    for cuboid in cuboids:
                        cuboid.translate(0, 0, translation_step)   
                elif event.key == pygame.K_SPACE:
                    for cuboid in cuboids:
                        cuboid.translate(0, 0, -translation_step) 
                elif event.key == pygame.K_d:
                    for cuboid in cuboids:
                        cuboid.rotate('y', -rotation_step)
                elif event.key == pygame.K_a:
                    for cuboid in cuboids:
                        cuboid.rotate('y', rotation_step)
                elif event.key == pygame.K_w:
                    for cuboid in cuboids:
                        cuboid.rotate('x', -rotation_step)
                elif event.key == pygame.K_s:
                    for cuboid in cuboids:
                        cuboid.rotate('x', rotation_step)
                elif event.key == pygame.K_e:
                    for cuboid in cuboids:
                        cuboid.rotate('z', -rotation_step)
                elif event.key == pygame.K_q:
                    for cuboid in cuboids:
                        cuboid.rotate('z', rotation_step)
                elif event.key == pygame.K_MINUS:
                        fov = adjust_fov(10, fov) 
                elif event.key == pygame.K_EQUALS:
                        fov = adjust_fov(-10, fov) 
                elif event.key == pygame.K_r:
                    print("run")

                screen.fill(BLACK)  
                for cuboid in cuboids:
                    cuboid.draw(screen, fov, aspect_ratio, near, far)  
                pygame.display.flip()   

                clock.tick(30)  

    pygame.quit()
    sys.exit()

def adjust_fov(fov_change, fov, fov_min=10, fov_max=170):
    new_fov = fov + fov_change
    if new_fov < fov_min:
        new_fov = fov_min
    elif new_fov > fov_max:
        new_fov = fov_max
    return new_fov

if __name__ == "__main__":
    filenames = ['cuboid1.txt', 'cuboid2.txt', 'cuboid3.txt', 'cuboid4.txt']
    main(filenames)
