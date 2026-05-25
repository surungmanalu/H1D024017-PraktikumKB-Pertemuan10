# hitung fitness tiap kromosom
def hitung_fitness(kromosom, barang, kapasitas_tas):
    total_harga = 0
    total_bobot = 0

    for i in range(len(kromosom)):
        if kromosom[i] == 1:
            total_harga += barang[i][1] # keuntungan
            total_bobot += barang[i][2] # ukuran

    # kalo melebihi kapasitas, fitness = 0
    if total_bobot > kapasitas_tas:
        return 0
    else:
        return total_harga

if __name__ == "__main__":
    # data barang (nama, keuntungan, ukuran)
    barang = [("Barang 1", 10, 5),
              ("Barang 2", 40, 4),
              ("Barang 3", 30, 6),
              ("Barang 4", 50, 3),
              ("Barang 5", 35, 7)]

    kapasitas_tas = 15

    # contoh populasi
    populasi_awal = [[1, 0, 1, 0, 1], # bobot 18 > 15 -> fitness 0
                     [0, 1, 0, 1, 0], # bobot 7 <= 15 -> fitness 90
                     [1, 1, 0, 0, 1]] # bobot 16 > 15 -> fitness 0

    fitness_populasi = [hitung_fitness(individu, barang, kapasitas_tas) for individu in populasi_awal]

    print("\nNilai Fitness:")
    for idx, fitness in enumerate(fitness_populasi):
        print(f"Individu {idx+1}: Fitness = {fitness}")