from collections import deque

def bfs_labirin(labirin, start, finish):
    
    antrian = deque()
    antrian.append([start])  
    
    dikunjungi = set()
    dikunjungi.add(start)
    
    arah = [(-1, 0), (0, 1), (1, 0), (0, -1)]
    
    baris = len(labirin)
    kolom = len(labirin[0]) if baris > 0 else 0
    
    while antrian:
        jalur = antrian.popleft()
        posisi_terakhir = jalur[-1]

        if posisi_terakhir == finish:
            return jalur

        for dr, dc in arah:
            r, c = posisi_terakhir[0] + dr, posisi_terakhir[1] + dc

            if (0 <= r < baris and 0 <= c < kolom and 
                labirin[r][c] != 1 and (r, c) not in dikunjungi):

                jalur_baru = list(jalur)
                jalur_baru.append((r, c))
                antrian.append(jalur_baru)

                dikunjungi.add((r, c))
    
    return None

def cetak_labirin(labirin, jalur=None):

    tampilan = [row[:] for row in labirin]
    
    if jalur:
        for r, c in jalur[1:-1]: 
            tampilan[r][c] = 2
    
    simbol = {
        0: ' ',  
        1: '█', 
        2: '•',  
        3: 'S',  
        4: 'F'   
    }
    
    for i, row in enumerate(tampilan):
        for j, cell in enumerate(row):
            if (i, j) == jalur[0] if jalur else False:
                print('S', end=' ')
            elif (i, j) == jalur[-1] if jalur else False:
                print('F', end=' ')
            else:
                print(simbol.get(cell, '?'), end=' ')
        print()

if __name__ == "__main__":
    print("=====================================")
    print("Program Pencarian Jalur Labirin dengan BFS")
    print("=====================================")

    labirin = [
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
    [1,3,0,0,0,1,0,0,0,0,0,0,1,0,0,0,0,0,0,1],
    [1,0,1,0,1,1,1,0,1,1,1,0,1,1,1,1,0,1,0,1],
    [1,0,1,0,0,0,0,0,1,0,0,0,1,0,0,0,0,1,0,1],
    [1,0,1,1,1,0,1,1,1,0,1,1,1,0,1,1,1,1,0,1],
    [1,0,0,0,0,0,1,0,0,0,1,0,0,0,1,0,0,0,0,1],
    [1,1,1,1,1,0,1,0,1,1,1,0,1,1,1,0,1,1,0,1],
    [1,0,0,0,0,0,1,0,0,0,1,0,0,0,0,0,1,0,0,1],
    [1,0,1,1,1,1,1,1,1,0,1,1,1,1,1,0,1,1,1,1],
    [1,0,0,0,0,0,0,0,1,0,0,0,0,0,1,0,0,0,0,1],
    [1,1,1,0,1,1,1,0,1,1,1,1,1,0,1,1,1,1,0,1],
    [1,0,0,0,1,0,0,0,1,0,0,0,1,0,0,0,1,0,0,1],
    [1,0,1,1,1,0,1,1,1,0,1,0,1,1,1,0,1,1,1,1],
    [1,0,1,0,0,0,1,0,0,0,1,0,1,0,0,0,1,0,0,1],
    [1,0,1,1,1,0,1,1,1,1,1,0,1,1,1,0,1,1,1,1],
    [1,0,0,0,1,0,0,0,0,0,0,0,1,0,0,0,0,0,0,1],
    [1,1,1,0,1,1,1,1,1,1,1,0,1,1,1,1,1,0,1,1],
    [1,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,1,0,0,1],
    [1,0,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,4,1],
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
    ]

    start = None
    finish = None
    for i in range(len(labirin)):
        for j in range(len(labirin[i])):
            if labirin[i][j] == 3:
                start = (i, j)
            elif labirin[i][j] == 4:
                finish = (i, j)
    
    print("\nLabirin Awal:")
    cetak_labirin(labirin)
    
    print("\nMencari solusi dengan BFS...")
    solusi = bfs_labirin(labirin, start, finish)
    
    if solusi:
        print("\nSolusi ditemukan! Jalur terpendek:")
        print(" -> ".join([f"({r},{c})" for r, c in solusi]))
        print(f"Total langkah: {len(solusi)-1}")
        
        print("\nVisualisasi Labirin dengan Jalur Solusi:")
        cetak_labirin(labirin, solusi)
    else:
        print("\nTidak ditemukan solusi untuk labirin ini.")