import random
import os
import matplotlib.pyplot as plt

# buat folder output kalo belum ada
os.makedirs('output', exist_ok=True)

# import modul GA
from InisiasiPopulasi import inisialisasi_populasi
from EvaluasiFitness import hitung_fitness
from selection import tournament_selection
from crossover import two_point_crossover
from mutation import inversion_mutation

# data barang: (nama, keuntungan, ukuran)
barang = [
    ("Barang 1", 10, 5),
    ("Barang 2", 40, 4),
    ("Barang 3", 30, 6),
    ("Barang 4", 50, 3),
    ("Barang 5", 35, 7)
]

def run_ga(jumlah_generasi, jumlah_populasi, prob_crossover, prob_mutasi, kapasitas_tas, tournament_size=3):
    print("=" * 70)
    print("     TUGAS PRAKTIKUM KECERDASAN BUATAN - PERTEMUAN 10")
    print("     Optimasi Gudang (Knapsack) dengan Algoritma Genetika")
    print("     NIM: H1D024034")
    print("=" * 70)
    
    # print parameter
    print("[INFO] Parameter Algoritma Genetika:")
    print(f"  - Kapasitas Maksimal Gudang : {kapasitas_tas}")
    print(f"  - Jumlah Generasi           : {jumlah_generasi}")
    print(f"  - Jumlah Populasi           : {jumlah_populasi}")
    print(f"  - Probabilitas Crossover    : {prob_crossover}")
    print(f"  - Probabilitas Mutasi       : {prob_mutasi}")
    print(f"  - Metode Seleksi            : Tournament Selection (TS), k={tournament_size}")
    print(f"  - Metode Crossover          : Two-Point Crossover")
    print(f"  - Metode Mutasi             : Inversion Mutation\n")
    
    # print data barang
    print("[INFO] Data Barang Toko:")
    for b in barang:
        print(f"  - {b[0]}: Keuntungan = {b[1]}, Ukuran = {b[2]}")
    print("-" * 70)
    print("PROSES EVOLUSI")
    print("-" * 70)

    jumlah_gen = len(barang)
    
    # inisialisasi populasi
    populasi = inisialisasi_populasi(jumlah_populasi, jumlah_gen)
    
    # simpan statistik fitness
    best_fitness_list = []
    worst_fitness_list = []
    avg_fitness_list = []
    all_fitness = []
    
    # simpan individu terbaik
    best_individu = None
    best_fitness_overall = -1
    
    # proses evolusi
    for generasi in range(jumlah_generasi):
        # evaluasi fitness
        fitness_populasi = [hitung_fitness(individu, barang, kapasitas_tas) for individu in populasi]
        
        # catat statistik
        best_fitness = max(fitness_populasi)
        worst_fitness = min(fitness_populasi)
        avg_fitness = sum(fitness_populasi) / len(fitness_populasi)
        
        best_fitness_list.append(best_fitness)
        worst_fitness_list.append(worst_fitness)
        avg_fitness_list.append(avg_fitness)
        all_fitness.append(fitness_populasi.copy())
        
        # update best individu
        if best_fitness > best_fitness_overall:
            best_fitness_overall = best_fitness
            index_best = fitness_populasi.index(best_fitness)
            best_individu = populasi[index_best].copy()
            
        print(f"Generasi {generasi+1:02d} | Best: {best_fitness:5.1f} | Average: {avg_fitness:5.1f} | Worst: {worst_fitness:5.1f}")
        
        new_populasi = []
        used_indices = []
        
        # bikin populasi baru
        while len(new_populasi) < jumlah_populasi:
            # pilih parent 1
            parent1, idx1 = tournament_selection(populasi, fitness_populasi, k=tournament_size)
            used_indices.append(idx1)
            
            # pastiin parent 2 beda
            available_indices = [i for i in range(len(populasi)) if i not in used_indices]
            if not available_indices:
                used_indices = [idx1]
                available_indices = [i for i in range(len(populasi)) if i != idx1]
                
            available_pop = [populasi[i] for i in available_indices]
            available_fit = [fitness_populasi[i] for i in available_indices]
            
            # pilih parent 2
            parent2, idx2_in_available = tournament_selection(available_pop, available_fit, k=tournament_size)
            idx2 = available_indices[idx2_in_available]
            used_indices.append(idx2)
            
            # crossover
            if random.random() < prob_crossover:
                anak1, anak2 = two_point_crossover(parent1, parent2)
            else:
                anak1, anak2 = parent1[:], parent2[:]
                
            # mutasi
            if random.random() < prob_mutasi:
                anak1 = inversion_mutation(anak1)
            if random.random() < prob_mutasi:
                anak2 = inversion_mutation(anak2)
                
            new_populasi.extend([anak1, anak2])
            
        # update populasi
        populasi = new_populasi[:jumlah_populasi]
        
    # print hasil terbaik
    print("=" * 70)
    print("HASIL OPTIMASI TERBAIK")
    print("=" * 70)
    
    selected_items = [barang[i][0] for i in range(len(best_individu)) if best_individu[i] == 1]
    selected_weight = sum([barang[i][2] for i in range(len(best_individu)) if best_individu[i] == 1])
    
    print(f"Kromosom Terbaik     : {best_individu}")
    print(f"Total Keuntungan     : {best_fitness_overall}")
    print(f"Total Ukuran/Bobot   : {selected_weight} (Kapasitas: {kapasitas_tas})")
    print("\nDaftar Barang Terpilih:")
    if selected_items:
        for item in selected_items:
            detail_item = next(b for b in barang if b[0] == item)
            print(f"  [v] {item} (Keuntungan: {detail_item[1]}, Ukuran: {detail_item[2]})")
    else:
        print("  [x] Tidak ada barang yang muat di gudang.")
    print("-" * 70)
    
    # plot grafik fitness
    plt.figure(figsize=(10, 6))
    
    # scatter semua fitness
    for i in range(jumlah_generasi):
        x = [i + 1] * len(all_fitness[i])
        y = all_fitness[i]
        plt.scatter(x, y, color='gray', alpha=0.15, s=15)
        
    # plot garis best, worst, avg
    plt.plot(range(1, jumlah_generasi + 1), best_fitness_list, color='#17b978', linewidth=2, label='Fitness Tertinggi (Best)')
    plt.plot(range(1, jumlah_generasi + 1), worst_fitness_list, color='#ff6f61', linewidth=2, label='Fitness Terendah (Worst)')
    plt.plot(range(1, jumlah_generasi + 1), avg_fitness_list, color='#1e3d59', linewidth=2, linestyle='--', label='Fitness Rata-rata (Avg)')
    
    plt.title('Grafik Perkembangan Nilai Fitness per Generasi\nNIM: H1D024034', fontsize=12, fontweight='bold', pad=12)
    plt.xlabel('Generasi')
    plt.ylabel('Nilai Fitness')
    plt.legend(loc='lower right', frameon=True, facecolor='white', edgecolor='lightgray')
    plt.grid(True, linestyle=':', alpha=0.6)
    plt.tight_layout()
    
    # simpan grafik
    plt.savefig('output/fitness_history.png')
    print("[INFO] Grafik disimpan di output/fitness_history.png")
    plt.show()
    print("=" * 70)

if __name__ == "__main__":
    # jalankan GA
    run_ga(
        jumlah_generasi=50, 
        jumlah_populasi=20, 
        prob_crossover=0.8, 
        prob_mutasi=0.15, 
        kapasitas_tas=15,
        tournament_size=3
    )