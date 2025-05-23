"""Bonjour Monsieur,

J'ai répondu aux questions du TP et regroupé toutes les illustrations dans un compte rendu disponible ici: https://github.com/OWMarko/TP4_Machine_Learning

Je vous remercie par avance pour l'attention portée à mon travail.
"""

import os
import neat
import visualize

xor_inputs = [
    (0.0, 0.0, 0.0), (0.0, 0.0, 1.0),
    (0.0, 1.0, 0.0), (0.0, 1.0, 1.0),
    (1.0, 0.0, 0.0), (1.0, 0.0, 1.0),
    (1.0, 1.0, 0.0), (1.0, 1.0, 1.0)]


xor_outputs = [
    (0.0,), (1.0,),
    (1.0,), (0.0,),
    (1.0,), (0.0,),
    (0.0,), (1.0,)]

def eval_genomes(genomes, config):
    for genome_id, genome in genomes:
        genome.fitness = len(xor_inputs) 
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        for xi, xo in zip(xor_inputs, xor_outputs):
            output = net.activate(xi)
            genome.fitness -= (output[0] - xo[0]) ** 2  

def run(config_file):
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_file)

    p = neat.Population(config)

    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    p.add_reporter(neat.Checkpointer(5))

    winner = p.run(eval_genomes, 300)

    print('\nBest genome:\n{!s}'.format(winner))

    print('\nOutput:')
    winner_net = neat.nn.FeedForwardNetwork.create(winner, config)
    for xi, xo in zip(xor_inputs, xor_outputs):
        output = winner_net.activate(xi)
        print("input {!r}, expected output {!r}, got {!r}".format(xi, xo, output))

    node_names = {-1: 'A', -2: 'B', -3: 'C', 0: 'A XOR B XOR C'}
    visualize.draw_net(config, winner, True, node_names=node_names)
    visualize.plot_stats(stats, ylog=False, view=True)
    visualize.plot_species(stats, view=True)

if __name__ == '__main__':
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'config-feedforward')
    run(config_path)
