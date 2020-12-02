from math import log10
from random import random, sample, choice
from string import ascii_uppercase

QUADGRAMS = {}
MISSING = None

with open("english_quadgrams.txt", "r") as f:
    for line in f.readlines():
        s, n = line.split()
        QUADGRAMS[s] = int(n)
    
    total = sum(QUADGRAMS.values())
    for x, y in QUADGRAMS.items():
        QUADGRAMS[x] = log10(y / total)
    
    MISSING = log10(0.01 / total)

def crack_substitution(encoded):
    return GeneticSolver(encoded).solve()

class Gene:
    def __init__(self, chromosome):
        self.chromosome = chromosome
    
    @classmethod
    def create_random(cls, base):
        return cls("".join(sample(base, len(base))))
    
    def crossover(self, other):
        new_chromosome = []
        base = set(self.chromosome)

        for c1, c2 in zip(self.chromosome, other.chromosome):
            f1 = c1 in base
            f2 = c2 in base

            new_c = choice((c1, c2)) if f1 and f2 else c1 if f1 else c2 if f2 else base.pop()
            new_chromosome.append(new_c)
            base.discard(new_c)
        
        return Gene("".join(new_chromosome))

    def mutate(self):
        i, j = sample(range(len(self.chromosome)), 2)
        self.chromosome = list(self.chromosome)
        self.chromosome[i], self.chromosome[j] = self.chromosome[j], self.chromosome[i]
        self.chromosome = "".join(self.chromosome)
    
    def calculate_fitness(self, text):
        text = text.translate(str.maketrans(ascii_uppercase, self.chromosome))
        total_quadgrams = len(text) - 3
        self.fitness = -sum(QUADGRAMS.get(text[i:i+4], MISSING) for i in range(total_quadgrams)) / total_quadgrams
        return self.fitness

class GeneticSolver:
    def __init__(self, text):
        self.text = text
        self.maximum_genes = 500
        self.genes = [Gene.create_random(ascii_uppercase) for _ in range(self.maximum_genes)]
    
    def select(self):
        self.genes = sorted(self.genes, key=lambda x: x.fitness)[:100]
    
    def calculate_fitness(self):
        for x in self.genes:
            x.calculate_fitness(self.text)
    
    def crossover(self):
        existing_range = range(len(self.genes))

        for _ in range(self.maximum_genes - len(self.genes)):
            i, j = sample(existing_range, 2)
            self.genes.append(self.genes[i].crossover(self.genes[j]))
    
    def mutate(self):
        for x in self.genes:
            if random() < 0.1:
                x.mutate()
    
    def solve(self):
        self.calculate_fitness()

        best_gene = self.genes[0]
        generation = best_generation = 1

        while generation - best_generation < 20:
            self.select()
            self.crossover()
            self.mutate()
            self.calculate_fitness()

            generation += 1
            if best_gene.fitness - self.genes[0].fitness > 1e-3:
                best_gene.chromosome = self.genes[0].chromosome
                best_gene.fitness = self.genes[0].fitness
                best_generation = generation
        
        return self.text.translate(str.maketrans(ascii_uppercase, best_gene.chromosome))