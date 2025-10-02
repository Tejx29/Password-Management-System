import random
import string

def fitness(password):
    length_score = len(password)
    variety_score = len(set([
        any(c.islower() for c in password),
        any(c.isupper() for c in password),
        any(c.isdigit() for c in password),
        any(not c.isalnum() for c in password)
    ]))
    return length_score + variety_score * 2

def generate_password(length=12):
    chars = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choice(chars) for _ in range(length))

def genetic_password(pop_size=20, generations=50):
    population = [generate_password() for _ in range(pop_size)]
    for _ in range(generations):
        population = sorted(population, key=fitness, reverse=True)
        if fitness(population[0]) > 20:
            return population[0]
        new_pop = population[:5]  # elitism
        while len(new_pop) < pop_size:
            p1, p2 = random.sample(population[:10], 2)
            cut = random.randint(1, len(p1) - 1)
            child = p1[:cut] + p2[cut:]
            if random.random() < 0.2:  # mutation
                pos = random.randint(0, len(child) - 1)
                child = child[:pos] + random.choice(string.ascii_letters + string.digits) + child[pos+1:]
            new_pop.append(child)
        population = new_pop
    return population[0]
