import random
import copy

class ProtocolEvolution:
    def evolve(self, protocols):
        evolved = []

        for p in protocols:
            if p.reward < 2:
                mutant = copy.deepcopy(p)
                mutant.reward += random.uniform(-0.5, 0.5)
                mutant.name += "_mutant"
                evolved.append(mutant)

        return evolved
