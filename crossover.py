import random

# one point crossover - potong di 1 titik
def one_point_crossover(parent1, parent2):
    titik_potong = random.randint(1, len(parent1)-1)
    
    anak1 = parent1[:titik_potong] + parent2[titik_potong:]
    anak2 = parent2[:titik_potong] + parent1[titik_potong:]
    
    return anak1, anak2

# two point crossover - potong di 2 titik
def two_point_crossover(parent1, parent2):
    if len(parent1) < 3:
        # kalo gen kurang dari 3, pake one point aja
        return one_point_crossover(parent1, parent2)
    titik1 = random.randint(1, len(parent1)-2)
    titik2 = random.randint(titik1+1, len(parent1)-1)
    
    anak1 = parent1[:titik1] + parent2[titik1:titik2] + parent1[titik2:]
    anak2 = parent2[:titik1] + parent1[titik1:titik2] + parent2[titik2:]
    
    return anak1, anak2

# uniform crossover - pake mask random
def uniform_crossover(parent1, parent2):
    mask = [random.randint(0, 1) for _ in range(len(parent1))]
    anak1 = []
    anak2 = []
    
    for i in range(len(parent1)):
        if mask[i] == 0:
            # mask 0 = ambil dari parent sendiri
            anak1.append(parent1[i])
            anak2.append(parent2[i])
        else:
            # mask 1 = tuker gen
            anak1.append(parent2[i])
            anak2.append(parent1[i])
            
    return anak1, anak2

if __name__ == "__main__":
    parent1 = [1, 0, 1, 1, 0]
    parent2 = [0, 1, 0, 0, 1]
    
    anak1, anak2 = two_point_crossover(parent1, parent2)
    print("\nAnak Hasil Two-Point Crossover:")
    print(f"Anak1: {anak1}")
    print(f"Anak2: {anak2}")