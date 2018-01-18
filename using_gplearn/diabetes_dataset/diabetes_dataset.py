#%pylab inline
import pydotplus
from sklearn.utils.random import check_random_state
from sklearn.datasets import load_diabetes
from gplearn.genetic import SymbolicRegressor
import numpy as np
from sklearn.model_selection import train_test_split
from gplearn.complexity import complexity


rng = check_random_state(2)


(X, y) = load_diabetes(return_X_y=True)
print("diabtes dataset")
print("size:", X.shape)
ground_compl = complexity(X, y)
print("Ground complexity:", sum(ground_compl))

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.70, random_state=42)

ground_compl = complexity(X_train, y_train)
print("Ground complexity on training data:", sum(ground_compl))

est_gp = SymbolicRegressor(population_size=600,
                           generations=40, stopping_criteria=0.01,
                           p_crossover=0.8, p_subtree_mutation=0.1,
                           p_hoist_mutation=0, p_point_mutation=0,
                           parsimony_coefficient=0,
                            verbose=1,
                            random_state=42,
                           n_jobs=2,
                           safe_best_program_to_file=False,
                           tournament_size=10,
                           first_tournament="fitness",
                           second_tournament="complexity",
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
