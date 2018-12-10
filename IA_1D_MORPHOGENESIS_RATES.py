
# Imtiaz Ali, Physics Graduate Student, Univeristy Of California, Merced
# Python 3.6.2 (v3.6.2:5fd33b5)
# 12/10/2016

# 1-D RANDOM WALK
# MORPHOGENESIS

# THIS CODE GETS THE DIFFUSION AND SOURCE RATE

# PART 1 DIFFUSION -> APPLY MONTE CARLO TO GET DIFFUSION IN SOLUTION
# PART 2 SOURCE -> APPLY FIXED RATE FOR THE SOURCE

# FIRST BOX -> ONLY LET PARTICLE MOVE RIGHT TO SECOND BOX => SOURCE
# SECOND BOX -> NOT ALLOWED TO MOVE PARTICLE TO FIRST BOX, IF LEFT OCCURS, DONT MOVE IT

# LAST BOX -> ONLY LET PARTICLE STAY IN LAST BOX => SINK
# SECOND TO LAST BOX -> NOT ALLOWED TO RECIEVE PARTICLE FROM LAST BOX


##############################################################################
##############################################################################

# FUTURE WORK

# 1. LOOK AT CELLS THAT ARE NOT THE SAME -> DIFFERENT K_ON
# 2. ALLOW CELLS TO RELEASE PARTICLES
# 3. ALLOW MORE THAN 1 PARTICLE TO MOVE INSTEAD OF JUST ONE
# 4. LOOK AT OARTICLES THAT ARE NOT THE SAME -> DIFFERENT DIFFUSION CONSTANT
# 5. APPLY DIFFERENT SOURCE RATES -> RELATING TO BOUNDAY CONDITIONS
# 6. LOOK AT FLUCTUATIONS IN CONCENTRATION -> MAYBE MORE THAT JUST HEAD PLAYS A ROLE HERE
# 7. SEE HOW STEADY-STATE FLUCTUATES WITH SYSTEM PERTURBATIONS

##############################################################################
##############################################################################



#!/use/bin/python

from random import choice as ch # ALIASING MODULES
import numpy as np
import matplotlib.pyplot as plt


npart = 50000       # TIME-STEPS => t = 0 TO npart-1 => TOTAL STEP = npart
side = 10           # NUMBER OF BOXES, SHOULD BE AN ODD NUMBER
nparticles_total  = 100000  # TOTAL NUMBER OF PARTICLES IN SYSTEM
nparticles = 10         # NUMBER OF PARTICLES TO START OFF WITH
nparticles_left = nparticles_total - nparticles  # NUMBER OF PARTICLES LEFT TO ADD TO SOURCE
steps = [-1,1]          # X STEP LENGTHS
grid = np.zeros((npart+1,side))
grid[0][0] = nparticles  # START ALL PARTICLES IN FIRST BOX
t_step_in = 5     # TIME-STEP WE ADD CERTAIN NUMBER OF PARTICLES TO SOURCE
rate_in = 3         # RATE WE ADD PARTICLES TO SOURCE BOX


for t in range(npart): # START AT INITIAL TIME

    # ADD PARTICLES TO SOURCE EVERY CERTAIN NUMBER OF TIME-STEPS
    # THIS IS NOT CORRECT, NEED PROPER CONDITIONAL FROM BOUNDAY CONDITION PDE
    if t != 0 and t%t_step_in == 0:
        grid[t][0] = grid[t][0] + rate_in
        nparticles_left = nparticles_left - rate_in

##    print(grid[t][0:side])
    grid_p = grid[t][0:side]
    
    # LOOP OVER EACH BOX
    for x in range(side):

        # FIRST CHECK TO SEE IF BOX IS NOT EMPTY -> NOT EMPTY IMPLIES WE CAN MOVE PARTICLE
        if grid_p[x] != 0: # NOT EMPTY

            # RNG TO MOVE LEFT OR RIGHT -> MONTE CARLO STEP
            r_move = round(np.random.rand(1)[0],4)  # 1 NUMBER ARRAY -> [0] IS POINTER TO FIRST ARRAY ELEMENT
##            print(r_move)

##############################################################################

            if r_move >= 0.00 and r_move < 0.50:  # MOVE RIGHT

                if x == 0: # -> PARTIALLY CORRECT
                    if grid_p[x] > 0:
                        grid_p[x] += steps[0] # LOSE 1 PARTICLE
                        grid_p[x+1] += steps[1]  # GAIN 1 PARTICLE

                if x > 0 and x < side-1: # ISSUE MAYBE
                    grid_p[x] += steps[0] # LOSE 1 PARTICLE
                    grid_p[x+1] += steps[1] # GAIN 1 PARTICLE
                        
                if x == side-1: # LAST BOX IS A SINK - NOTHING LEAVES IT -> CORRECT
                    grid_p[x] += 0


##############################################################################
                    
            if r_move >= 0.50 and r_move < 1: # MOVE LEFT
                # NOTE, IT DOESN'T ACCOUNT FOR THINGS ALREADY COMING IN AT TIME STEP BEFORE

                if x == 0: # FIRST BOX CAN ONLY MOVE RIGHT -> CORRECT
                    grid_p[x] += 0
                        
                if x == 1: # SECOND BOX CAN ONLY MOVE RIGHT -> PARTIALLY CORRECT
                    grid_p[x] += 0
     
                if x > 1 and x < side-1: # ISSUE MAYBE
                    grid_p[x] += steps[0]  # LOSE 1 PARTICLE
                    grid_p[x-1] += steps[1] # GAIN 1 PARTICLE  
                 
                if x == side-1: # LAST BOX IS A SINK -> NOTHING LEAVES IT -> CORRECT
                    grid_p[x] += 0


    grid[t+1][0:side] = grid_p[0:side]
                    
##############################################################################


# PLOT COUNT IN EACH BOX FOR SEPERATE TIME-STEPS

# PLOT ALL CELL BOXES AND WITHOUT SOURCE AND SINK -> SUBPLOT

##figure(num=None, figsize=(8, 6), dpi=80, facecolor='w', edgecolor='k')
fig, (ax1,ax2)=plt.subplots(1,2)
for i in range(npart//5000):
    ax1.plot(grid[i*5000][0:side], label ='time-step = %d' %(i*5000))
    ax2.plot(grid[i*5000][1:side-1], label ='time-step = %d' %(i*5000))

ax1.set_title('Concentration vs. Cell box')
ax2.set_title("Concentration vs. Cell box")
chartBox = ax2.get_position()
ax2.set_position([chartBox.x0, chartBox.y0, chartBox.width*0.6, chartBox.height])
ax2.legend(loc='upper center', bbox_to_anchor=(1.45, 0.8), shadow=True, ncol=1)
plt.show()



# PLOT ALL CELL BOXES

fig = plt.figure()
ax = plt.subplot(111)
for i in range(npart//5000):
    ax.plot(grid[i*5000][0:side], label ='time-step = %d' %(i*5000))

plt.title('Concentration vs. Cell box')
plt.xlim(0,side)
chartBox = ax.get_position()
ax.set_position([chartBox.x0, chartBox.y0, chartBox.width*0.6, chartBox.height])
ax.legend(loc='upper center', bbox_to_anchor=(1.45, 0.8), shadow=True, ncol=1)
plt.show()


# PLOT ALL CELL BOXES EXCEPT SOURCE AND SINK

fig = plt.figure()
ax = plt.subplot(111)
for i in range(npart//5000):
    ax.plot(grid[i*5000][1:side-1], label ='time-step = %d' %(i*5000))

plt.title('Concentration vs. Cell box')
##plt.xlim(1,side-1)
chartBox = ax.get_position()
ax.set_position([chartBox.x0, chartBox.y0, chartBox.width*0.6, chartBox.height])
ax.legend(loc='upper center', bbox_to_anchor=(1.45, 0.8), shadow=True, ncol=1)
plt.show()

    







