import pygame as pg 
from allVariables import * 
from misc import *
from ga import * 

pg.init()

pg.display.set_caption('Self driving vehicles')

for i in range(numWalls) : 
    x = i*wallGap
    if i%2 == 0 : y = 0
    else : y = baseHeight - wallHeight
    walls.append(Wall(x,y,wallWidth,wallHeight))
walls.append(Wall(0,0,width,wallWidth))
walls.append(Wall(width-wallWidth/2,0,wallWidth,height))
# walls.append(Wall(0,baseHeight-wallWidth,width,wallWidth))
walls.append(Wall(wallGap,baseHeight-wallWidth,width-(2*wallGap),wallWidth))
walls.append(Wall(0,0,wallWidth,height))
walls.append(Wall(0,height-wallWidth/2,width,wallWidth))

for wall in walls : 
    edges = wall.edges()
    for edge in edges : 
        allEdges.append(edge)

for i in range(total) : 
    cars.append(Car(Vehicle()))

group.add(cars)

while running : 
    screen.fill(bgcol)
    if pg.mouse.get_pressed()[0] : 
        mx,my = pg.mouse.get_pos()
        print(points(mx,my,1))
    # drawGrid()
    for i in range(n) : 
        for car in cars : 
            car.vehicle.run()
            car.vehicle.checkPass(checkpt1,checkpt2)
            car.vehicle.think(allEdges)
            
        for i in range(len(cars)-1, -1, -1) : 
            if cars[i].vehicle.isDead : 
                group.remove(cars[i])
                savedVehicles.append(cars.pop(i).vehicle)
        # print(len(vehicles) , len(savedVehicles))

        if len(cars) == 0 : 
            group.remove(cars)
            nextGeneration()
            gen += 1
            print("generation No : " , gen)

    for car in cars : car.vehicle.showRays = showRays
    pg.draw.line(screen,(0,255,0), (int(checkpt2.x),int(checkpt2.y)),(int(checkpt2.x),height),3)
    for wall in walls : wall.show()
    for car in cars : car.drawCar()
    # render = cars[0].vehicle.lookForCast(allEdges)
    # Render(render)

    for event in pg.event.get() : 
        if event.type == pg.QUIT : 
            running = False 
        elif event.type == pg.KEYDOWN : 
            if event.key == pg.K_ESCAPE : 
                running = False 
            if event.key == pg.K_SPACE : 
                showRays = not showRays
                for car in cars : car.vehicle.showRays = showRays
            if event.key == pg.K_r : 
                for i in range(len(cars)-1, -1, -1) : 
                    group.remove(cars[i])
                    savedVehicles.append(cars.pop(i).vehicle)
            if event.key == pg.K_UP : 
                n += 2
                if n >= 30 : n = 30
                print(n)
            if event.key == pg.K_p : 
                for car in cars : print(car.vehicle.score)
            if event.key == pg.K_DOWN : 
                n -= 2
                if  n <= 0 : n = 1
                print(n)
            if event.key == pg.K_s : 
                fittestVehicle = cars[0].vehicle
                saveVehicle(fittestVehicle)
            if event.key == pg.K_l : 
                for i in range(len(cars)-1, -1, -1) : 
                    group.remove(cars[i])
                    savedVehicles.append(cars.pop(i).vehicle)
                fittestVehicleRun = True
                runFittestVehicle()
    group.draw(screen)
    group.update()
    pg.display.flip()
    clock.tick(30)
pg.quit()
