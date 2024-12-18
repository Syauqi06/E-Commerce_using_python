import os
from datetime import datetime # untuk mengambil waktu saat ini

# data admin dan user yang disatukan dalam satu dictionary
users = {
    'admin': {'password': 'admin123', 'role': 'admin'},
    'user1': {'password': 'user123', 'role': 'user'}
}

produk = {} # dictionary untuk menyimpan data produk
keranjang = {} # dictionary untuk menyimpan data keranjang belanja
pesanan = [] # list untuk menyimpan data pesanan

def clear_screen(): # fungsi untuk me-refresh layar ketika membuka setiap menu/fungsi lainnya
    os.system('cls' if os.name == 'nt' else 'clear')

def login(): # fungsi login
    while True:
        print("\n=== LOGIN ===")
        username = input("Username: ")
        password = input("Password: ")
        
        if username in users and users[username]['password'] == password:
            return username, users[username]['role'] # mengembalikan username dan role user jika login berhasil
        print("Username atau password salah")

def register_user(): # fungsi register user
    while True:
        print("\n=== REGISTER USER ===")
        username = input("Masukkan username baru: ")
        if username in users:# cek apakah username sudah digunakan
            print("Username sudah digunakan! Tekan Enter untuk mencoba lagi.")
            input()
            continue

        password = input("Masukkan password: ")
        konfirmasi_password = input("Konfirmasi password: ")

        if password != konfirmasi_password: # cek apakah password dan konfirmasi password cocok
            print("Password tidak cocok! Tekan Enter untuk mencoba lagi.")
            input()
            continue

        users[username] = {'password': password, 'role': 'user'} # tambahkan user baru ke dictionary users
        print("Registrasi berhasil! Tekan Enter untuk kembali ke menu utama.")
        input()
        break

def admin_menu(): # fungsi menu admin
    while True:
        clear_screen()
        print("\n=== ADMIN MENU ===")
        print("1. Lihat Produk")
        print("2. Tambah Produk")
        print("3. Edit Produk")
        print("4. Hapus Produk")
        print("5. Lihat Pesanan")
        print("6. Logout")
        
        choice = input("Pilih menu (1-6): ")
        
        if choice == '1':
            lihat_produk()
        elif choice == '2':
            tambah_produk()
        elif choice == '3':
            edit_produk()
        elif choice == '4':
            hapus_produk()
        elif choice == '5':
            lihat_pesanan()
        elif choice == '6':
            break

def user_menu(username): # fungsi menu user
    while True:
        clear_screen()
        print("\n=== USER MENU ===")
        print("1. Lihat Produk")
        print("2. Tambah ke Keranjang")
        print("3. Lihat Keranjang")
        print("4. Checkout")
        print("5. Riwayat Pesanan")
        print("6. Logout")
        
        choice = input("Pilih menu (1-6): ")
        
        if choice == '1':
            lihat_produk()
        elif choice == '2':
            keranjang_belanja(username) # memanggil fungsi keranjang belanja dengan username
        elif choice == '3':
            lihat_keranjang(username)
        elif choice == '4':
            checkout(username)
        elif choice == '5':
            user_pesanan(username)
        elif choice == '6':
            break

def lihat_produk(): # fungsi lihat produk
    print("\n=== DAFTAR PRODUK ===")
    print("ID | Nama | Harga | Stok")
    print("-" * 40)
    for id_produk, product in produk.items():
        print(f"{id_produk} | {product['nama']} | Rp{product['harga']:,} | {product['stok']}") # menampilkan data produk dengan format ID, Nama, Harga dan Stok
    input("\nTekan Enter untuk kembali...")

def tambah_produk(): # fungsi tambah produk
    print("\n=== TAMBAH PRODUK ===")
    nama = input("Nama produk: ")
    harga = int(input("Harga: "))
    stok = int(input("Stok: "))
    
    # menentukan ID produk berikutnya jika ada produk sebelumnya
    id_produk = max(produk.keys()) + 1 if produk else 1 # atau jika tidak ada produk, ID produk awal adalah 1
    produk[id_produk] = { # menambahkan produk baru ke dictionary produk
        'nama': nama,
        'harga': harga,
        'stok': stok
    }
    print("Produk berhasil ditambahkan!")
    input("\nTekan Enter untuk kembali...")

def edit_produk(): # fungsi edit produk
    lihat_produk() # menampilkan daftar produk
    id_produk = int(input("\nMasukkan ID produk yang akan diedit: "))
    
    if id_produk in produk:
        print("\nMasukkan data baru (kosongkan jika tidak ingin mengubah):")
        nama = input(f"Nama ({produk[id_produk]['nama']}): ")
        harga = input(f"Harga ({produk[id_produk]['harga']}): ")
        stok = input(f"Stok ({produk[id_produk]['stok']}): ")
        
        if nama:
            produk[id_produk]['nama'] = nama
        if harga:
            produk[id_produk]['harga'] = int(harga)
        if stok:
            produk[id_produk]['stok'] = int(stok)
        
        print("Produk berhasil diedit!")
    else:
        print("ID produk tidak ditemukan!")
    input("\nTekan Enter untuk kembali...")

def hapus_produk(): # fungsi hapus produk
    lihat_produk() # menampilkan daftar produk
    id_produk = int(input("\nMasukkan ID produk yang akan dihapus: "))
    
    if id_produk in produk: # jika ID produk ditemukan dalam dictionary
        del produk[id_produk] # maka hapus produk dengan ID tersebut
        print("Produk berhasil dihapus!")
    else:
        print("ID produk tidak ditemukan!")
    input("\nTekan Enter untuk kembali...")

def keranjang_belanja(username): # fungsi keranjang belanja
    if username not in keranjang: # jika username belum ada dalam dictionary keranjang belanja
        keranjang[username] = {} # maka buat keranjang belanja baru
    
    lihat_produk() # menampilkan daftar produk
    id_produk = int(input("\nMasukkan ID produk: "))
    
    if id_produk in produk:
        kuantitas = int(input("Masukkan jumlah: "))
        if kuantitas <= produk[id_produk]['stok']:
            if id_produk in keranjang[username]:
                keranjang[username][id_produk] += kuantitas  # jika produk sudah ada dalam keranjang, tambahkan kuantitas
            else:
                keranjang[username][id_produk] = kuantitas # jika produk belum ada dalam keranjang, tambahkan produk baru
            print("Produk berhasil ditambahkan ke keranjang!")
        else:
            print("Stok tidak mencukupi!")
    else:
        print("ID produk tidak ditemukan!")
    input("\nTekan Enter untuk kembali...")

def lihat_keranjang(username): # fungsi lihat keranjang
    if username not in keranjang or not keranjang[username]:
        print("\nKeranjang kosong!")
        input("\nTekan Enter untuk kembali...")
        return
    
    print("\n=== ISI KERANJANG ===")
    total = 0
    for id_produk, kuantitas in keranjang[username].items(): # menampilkan isi keranjang belanja dengan format ID, Nama, Harga dan Kuantitas
        subtotal = kuantitas * produk[id_produk]['harga']
        total += subtotal
        print(f"{produk[id_produk]['nama']} | {kuantitas} x Rp{produk[id_produk]['harga']:,} = Rp{subtotal:,}")
    print("-" * 40)
    print(f"Total: Rp{total:,}")
    input("\nTekan Enter untuk kembali...")

def checkout(username): # fungsi checkout
    if username not in keranjang or not keranjang[username]: # jika keranjang belanja kosong atau username tidak ada dalam keranjang
        print("\nKeranjang kosong!") # maka tampilkan pesan keranjang kosong
        input("\nTekan Enter untuk kembali...")
        return
    
    print("\n=== CHECKOUT ===")
    lihat_keranjang(username) # menampilkan isi keranjang belanja 
    confirm = input("\nLanjutkan checkout? (y/n): ") # meminta konfirmasi untuk melanjutkan checkout
    
    if confirm.lower() == 'y':
        order = { # membuat pesanan baru dengan data pesanan dari keranjang belanja
            'username': username,
            'items': {}, # dictionary untuk menyimpan item-item pesanan
            'total': 0, # variabel untuk menyimpan total harga
            'date': datetime.now() # variabel untuk menyimpan tanggal pesanan
        }
        
        for id_produk, kuantitas in keranjang[username].items(): # menambahkan item-item pesanan ke dictionary 
            if kuantitas <= produk[id_produk]['stok']:
                produk[id_produk]['stok'] -= kuantitas
                subtotal = kuantitas * produk[id_produk]['harga']
                order['items'][id_produk] = {
                    'nama': produk[id_produk]['nama'],
                    'kuantitas': kuantitas,
                    'harga': produk[id_produk]['harga'],
                    'subtotal': subtotal
                }
                order['total'] += subtotal # menambahkan subtotal ke total pesanan 
                print(f"Produk {produk[id_produk]['nama']} berhasil di-checkout")
            else:
                print(f"Stok {produk[id_produk]['nama']} tidak mencukupi!")
                return
        
        pesanan.append(order) # menambahkan pesanan baru ke list pesanan
        keranjang[username].clear() # mengosongkan keranjang belanja setelah checkout
        print("Checkout berhasil!")
    input("\nTekan Enter untuk kembali...")

def lihat_pesanan(): # fungsi lihat pesanan
    print("\n=== DAFTAR PESANAN ===")
    for i, order in enumerate(pesanan, 1): # menampilkan daftar pesanan dengan format ID, Username, Tanggal, Items, Total dan Status
        print(f"\nPesanan #{i}")
        print(f"Username: {order['username']}")
        print(f"Tanggal: {order['date'].strftime('%Y-%m-%d %H:%M:%S')}") # mengubah format tanggal menjadi YYYY-MM-DD HH:MM:SS
        print("Items:")
        for item in order['items'].values(): # menampilkan item-item pesanan dengan format Nama, Kuantitas, Harga dan Subtotal
            print(f"- {item['nama']} | {item['kuantitas']} x Rp{item['harga']:,} = Rp{item['subtotal']:,}")
        print(f"Total: Rp{order['total']:,}")
    input("\nTekan Enter untuk kembali...")

def user_pesanan(username): # fungsi riwayat pesanan user
    print(f"\n=== RIWAYAT PESANAN {username} ===")
    pesanan_pengguna = [order for order in pesanan if order['username'] == username] # menampilkan riwayat pesanan user dari list pesanan yang memiliki username yang sama
    
    for i, order in enumerate(pesanan_pengguna, 1):
        print(f"\nPesanan #{i}")
        print(f"Tanggal: {order['date'].strftime('%Y-%m-%d %H:%M:%S')}")
        print("Items:")
        for item in order['items'].values():
            print(f"- {item['nama']} | {item['kuantitas']} x Rp{item['harga']:,} = Rp{item['subtotal']:,}")
        print(f"Total: Rp{order['total']:,}")
    input("\nTekan Enter untuk kembali...")

def main(): # fungsi utama
    while True:
        clear_screen()
        print("=== SISTEM E-COMMERCE ===")
        print("1. Login")
        print("2. Registrasi")
        print("3. Keluar")
        
        choice = input("Pilih menu (1-3): ")
        
        if choice == '1':
            username, role = login()
            if role == 'admin':
                admin_menu()
            else:
                user_menu(username)
        elif choice == '2':
            register_user()
        elif choice == '3':
            print("Terima kasih! Sampai jumpa.")
            break
        else:
            print("Pilihan tidak valid! Tekan Enter untuk kembali.")
            input()

if __name__ == "__main__":
    main()