#%pylab inline
import pydotplus
from sklearn.utils.random import check_random_state
from sklearn.datasets import load_boston
from gplearn.genetic import SymbolicRegressor
import numpy as np
from sklearn.model_selection import train_test_split
from gplearn.complexity import complexity


rng = check_random_state(0)


#(X_train, y_train) = load_boston(return_X_y=True)
data = np.loadtxt("bioavailability.csv", delimiter=",")
print("Data:", "bioavailability.csv")
print("Input data size:", data.shape)
X_data = data[:, :data.shape[1]-1]
y_data = data[:, data.shape[1]-1]

ground_compl = complexity(X_data, y_data)
print("Ground complexity:", sum(ground_compl))

X_train, X_test, y_train, y_test = train_test_split(X_data, y_data, test_size=0.30, random_state=42)

ground_compl = complexity(X_train, y_train)
print("Ground complexity on training data:", sum(ground_compl))

est_gp = SymbolicRegressor(population_size=500,
                           generations=20, stopping_criteria=0.01,
                           p_crossover=0.9, p_subtree_mutation=0.1,
                           p_hoist_mutation=0, p_point_mutation=0,
                           parsimony_coefficient=0,
                            verbose=1,
                            random_state=42,
                           n_jobs=2,
                           safe_best_program_to_file=True,
                           tournament_size=10,
                           first_tournament="fitness",
                           #second_tournament="complexity",
                           second_tournament_size=1.4)
print("Run GP with parameters: ", est_gp.get_params())
est_gp.fit(X_train, y_train)

program = est_gp._program
graph = pydotplus.graphviz.graph_from_dot_data(program.export_graphviz())
filename = "final_best_program.pdf"
graph.write_pdf(filename)

y_pred = est_gp.predict(X_test)

print("test fitness:", np.average(np.abs(y_pred - y_test)))

score_gp = est_gp.score(X_test, y_test)
print(score_gp)

#print("final program complexity:", program.complexity_)

#print(est_gp._program.parents)
#
#idx = est_gp._program.parents['donor_idx']
#fade_nodes = est_gp._program.parents['donor_nodes']
#print(est_gp._programs[-2][idx])
#print('Fitness:', est_gp._programs[-2][idx].fitness_)
