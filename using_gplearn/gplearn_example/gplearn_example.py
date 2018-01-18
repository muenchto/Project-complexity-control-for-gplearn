#%pylab inline
import pydotplus
from sklearn.utils.random import check_random_state
from gplearn.genetic import SymbolicRegressor
import numpy as np
from gplearn.complexity import complexity

rng = check_random_state(0)



# Training samples
X_train = rng.uniform(-1, 1, 100).reshape(50, 2)
y_train = X_train[:, 0]**2 - X_train[:, 1]**2 + X_train[:, 1] - 1

rng = check_random_state(42)
# Testing samples
X_test = rng.uniform(-1, 1, 100).reshape(50, 2)
y_test = X_test[:, 0]**2 - X_test[:, 1]**2 + X_test[:, 1] - 1

print("Data:", "genereated data from gplearn example")
print("Input data size:", X_train.shape)


ground_compl = complexity(X_train, y_train)
print("Ground complexity:", sum(ground_compl))


est_gp = SymbolicRegressor(population_size=1000,
                           generations=100, stopping_criteria=0.01,
                           p_crossover=0.9, p_subtree_mutation=0.1,
                           p_hoist_mutation=0, p_point_mutation=0,
                            verbose=1,
                           safe_best_program_to_file=True,
                            random_state=0,
                           tournament_size=10,
                           first_tournament="fitness",
                           second_tournament="complexity",
                           second_tournament_size=1)
print("Run GP with parameters: ", est_gp.get_params())
est_gp.fit(X_train, y_train)

program = est_gp._program
graph = pydotplus.graphviz.graph_from_dot_data(program.export_graphviz())
filename = "final_best_program.pdf"
graph.write_pdf(filename)

y_pred = est_gp.predict(X_test)

print("test fitness:", np.average(np.abs(y_pred - y_test)))

score_gp = est_gp.score(X_test, y_test)
print("score (coefficient of determination R^2 of the prediction):", score_gp)

#print("final program complexity:", program.complexity_)

#print(est_gp._program.parents)
#
#idx = est_gp._program.parents['donor_idx']
#fade_nodes = est_gp._program.parents['donor_nodes']
#print(est_gp._programs[-2][idx])
#print('Fitness:', est_gp._programs[-2][idx].fitness_)
