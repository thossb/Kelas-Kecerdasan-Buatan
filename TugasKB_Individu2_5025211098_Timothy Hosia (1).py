import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns; sns.set()
from sklearn.datasets import make_blobs

plot_size   = 7
plot_width  = 8
plot_height = 4

params = {'legend.fontsize': 'large',
          'figure.figsize': (plot_width,plot_height),
          'axes.labelsize': plot_size,
          'axes.titlesize': plot_size,
          'xtick.labelsize': plot_size*0.75,
          'ytick.labelsize': plot_size*0.75,
          'axes.titlepad': 25}
plt.rcParams.update(params)
plt.rcParams.update(params)

# generate random coordinates for homes
num_homes = 50
center_box = (100, 200) 
homes_coord, _ = make_blobs(n_samples=num_homes, 
                           centers=2, 
                           cluster_std=20, 
                           center_box=center_box, 
                           random_state = 2)

# create a dictionary of home names and their coordinates
homes_names = [i for i in range(num_homes)]
homes_coord_dict = {name: coord for name,coord in zip(homes_names, homes_coord)}

# plot the homes on a scatter plot
plt.scatter(homes_coord[:, 0], homes_coord[:, 1], s=plot_size*2, cmap='viridis')
plt.show()

# calculate the distance matrix between all pairs of homes
from scipy.spatial import distance
dist_matrix = distance.cdist(homes_coord, homes_coord, 'euclidean')

# import necessary tools from DEAP library
from deap import base, creator, tools
import copy

# set the random seed
np.random.seed(3) 

# define the chromosome creation function
def chromo_create(_homes_names):
    chromo = copy.deepcopy(_homes_names)
    np.random.shuffle(chromo)    
    return chromo

# define the chromosome evaluation function
def chromo_eval(_dist_matrix, _chromo):
    dist = 0
    for p in range(len(_chromo) - 1):
        _i = _chromo[p]
        _j = _chromo[p+1]
        dist += _dist_matrix[_i][_j]
        
    dist += dist_matrix[_chromo[-1], _chromo[0]]
    return dist,

# define the toolbox and create the necessary classes and functions
tb = base.Toolbox()
creator.create('Fitness_Func', base.Fitness, weights=(-1.0,))
creator.create('Individual', list, fitness=creator.Fitness_Func)

num_population = 200
num_generations = 1000
prob_crossover = .5
prob_mutation = .8

tb.register('indexes', chromo_create, homes_names)
tb.register('individual', tools.initIterate, creator.Individual, tb.indexes)
tb.register('population', tools.initRepeat, list, tb.individual)
tb.register('evaluate', chromo_eval, dist_matrix)
tb.register('select', tools.selTournament)
tb.register('mate', tools.cxPartialyMatched)
tb.register('mutate', tools.mutShuffleIndexes)

# create the initial population
population = tb.population(n=num_population)

# evaluate the fitness of each individual in the population
fitness_set = list(tb.map(tb.evaluate, population))
for ind, fit in zip(population, fitness_set):
    ind.fitness.values = fit
    
# initialize variables to keep track of the best solution and its fitness
best_fit_list = []
best_sol_list = []

best_fit = np.Inf

for gen in range(0, num_generations):
    
    if (gen % 50 == 0):
        print(f'Generation: {gen:4} | Fitness: {best_fit:.2f}' ) 
    
    offspring = tb.select(population, len(population), tournsize=3)
    offspring = list(map(tb.clone, offspring))
    
    for child1, child2 in zip(offspring[0::2], offspring[1::2]):
        if np.random.random() < prob_crossover:
            tb.mate(child1, child2)
            del child1.fitness.values
            del child2.fitness.values

    for chromo in offspring:
        if np.random.random() < prob_mutation:
            tb.mutate(chromo, indpb=0.01)
            del chromo.fitness.values

    invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
    fitness_set = map(tb.evaluate, invalid_ind)
    for ind, fit in zip(invalid_ind, fitness_set):
        ind.fitness.values = fit
    
    population[:] = offspring
    
    curr_best_sol = tools.selBest(population, 1)[0]
    curr_best_fit = curr_best_sol.fitness.values[0]
    
    if curr_best_fit < best_fit:
        best_sol = curr_best_sol
        best_fit = curr_best_fit

    best_fit_list.append(best_fit)
    best_sol_list.append(best_sol)
    
# plt.plot(best_fit_list)
# plt.show()

print(best_sol)

final_sol = best_sol + best_sol[0:1]

plt.scatter(homes_coord[:, 0], 
            homes_coord[:, 1], 
            s=plot_size*2, 
            cmap='viridis',
            zorder = 10000);

for i, txt in enumerate(homes_names):
    plt.annotate(txt, (homes_coord[i, 0]+1, homes_coord[i, 1]+1))

lines = []
for p in range(len(final_sol) - 1):
    i = final_sol[p]
    j = final_sol[p+1]
    colour = 'black'       
    plt.arrow(homes_coord[i][0], 
              homes_coord[i][1],
              homes_coord[j][0] - homes_coord[i][0], 
              homes_coord[j][1] - homes_coord[i][1], 
              color=colour)

plt.show()
