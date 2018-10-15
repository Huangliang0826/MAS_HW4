import matplotlib.pyplot as plt
import numpy as np

grid = np.zeros((5,5))

print(grid.shape)

discountFactor =0.9

def evaluate_equal_prob(iter_times):
    for iteration in range(iter_times):
        for x in range(5):
            for y in range(5):
                if x==0 and y==1:
                    grid[x,y] = 10.0 + discountFactor*grid[4, 1]
                elif x== 0 and y==3:
                    grid[x,y] = 5.0 + discountFactor*grid[2, 3]
                else:
                    if x == 0 and y > 0 and y < 4 :
                        # top row, not corners
                        item1 =  (-1 + discountFactor * grid[x, y])
                        item2 =  discountFactor * grid[x+1,y]
                        item3 =  discountFactor * grid[x,y+1]
                        item4 =  discountFactor * grid[x,y-1]
                        grid[x,y] = max(item1, item2, item3 , item4)
                    elif x==0 and y==0:
                        # top left corner
                        item1 = -1 + discountFactor * grid[x, y]
                        item2 = discountFactor * grid[x, y+1]
                        item3 = discountFactor * grid[x+1, y]
                        grid[x,y] = max(item1 ,  item2 , item3)
                    elif x == 0 and y == 4:
                        # top right corner
                        grid[x, y] = max(( (-1 + discountFactor * grid[x, y])) , discountFactor * grid[x, y - 1] , discountFactor * grid[x + 1, y])
                    elif y == 0 and x > 0 and x < 4:
                        #left row not corner
                        grid[x, y] = max(((-1 + discountFactor * grid[x, y])) ,  discountFactor * grid[x + 1, y] , discountFactor * grid[x, y + 1] , discountFactor * grid[x-1,y])
                    elif y == 0 and x == 4:
                        #left bottom
                        grid[x, y] = max(((-1 + discountFactor * grid[x, y])) ,  discountFactor * grid[x, y + 1] , discountFactor * grid[x - 1, y])
                    elif y == 4 and x < 4 and x >0:
                        #right row, not corner
                        grid[x, y] = max(( (-1 + discountFactor * grid[x, y])) ,discountFactor * grid[x + 1, y] , discountFactor * grid[x, y - 1] ,discountFactor * grid[x-1,y])
                    elif y==4 and x==4:
                        #bottom right corner
                        grid[x, y] = max(((-1 + discountFactor * grid[x, y])) , discountFactor * grid[x, y - 1] , discountFactor * grid[x - 1, y])
                    elif x == 4 and y < 4 and y > 0:
                        #botom row, not corner
                        grid[x, y] = max( (-1 + discountFactor * grid[x, y]), discountFactor * grid[x - 1, y] ,discountFactor * grid[x, y + 1] , discountFactor * grid[x, y - 1])
                    else:
                        grid[x,y] = discountFactor* max(grid[x+1, y] , grid[x-1, y] , grid[x, y+1] , grid[x, y-1])

evaluate_equal_prob(100)
print(grid)
