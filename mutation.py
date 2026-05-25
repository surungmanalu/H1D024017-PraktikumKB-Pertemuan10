import random

# swap mutation - tuker posisi 2 gen
def swap_mutation(kromosom):
    kromosom = list(kromosom)
    if len(kromosom) < 2:
        return kromosom
    
    posisi1, posisi2 = random.sample(range(len(kromosom)), 2)
    kromosom[posisi1], kromosom[posisi2] = kromosom[posisi2], kromosom[posisi1]
    
    return kromosom

# inversion mutation - balik urutan segmen gen
def inversion_mutation(kromosom):
    kromosom = list(kromosom)
    if len(kromosom) < 2:
        return kromosom
        
    posisi1 = random.randint(0, len(kromosom) - 2)
    posisi2 = random.randint(posisi1 + 1, len(kromosom) - 1)
    
    # balik segmen dari posisi1 ke posisi2
    kromosom[posisi1:posisi2] = list(reversed(kromosom[posisi1:posisi2]))
    
    return kromosom

# uniform mutation - flip bit random
def uniform_mutation(kromosom, mutation_rate=0.1):
    kromosom = list(kromosom)
    
    for i in range(len(kromosom)):
        if random.random() < mutation_rate:
            kromosom[i] = 1 - kromosom[i] # 0 jadi 1, 1 jadi 0
            
    return kromosom

if __name__ == "__main__":
    kromosom = [0, 1, 1, 0, 1]
    print(f"Original: {kromosom}")
    print(f"Swap Mutation: {swap_mutation(kromosom.copy())}")
    print(f"Inversion Mutation: {inversion_mutation(kromosom.copy())}")
    print(f"Uniform Mutation: {uniform_mutation(kromosom.copy())}")