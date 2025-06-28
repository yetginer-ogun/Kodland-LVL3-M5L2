import sqlite3
import matplotlib

matplotlib.use('Agg')  # Matplotlib arka planını, pencere göstermeden dosyaları bellekte kaydetmek için ayarlama
import matplotlib.pyplot as plt
import cartopy.crs as ccrs  # Harita projeksiyonlarıyla çalışmamızı sağlayacak modülü içe aktarma
import cartopy.feature as cfeature

class DB_Map():
    def __init__(self, database):
        self.database = database  # Veri tabanı yolunu belirleme

    def create_user_table(self):
        conn = sqlite3.connect(self.database)  # Veri tabanına bağlanma
        with conn:
            # Kullanıcı şehirlerini depolamak için bir tablo oluşturma (eğer yoksa)
            conn.execute('''CREATE TABLE IF NOT EXISTS users_cities (
                                user_id INTEGER,
                                city_id TEXT,
                                FOREIGN KEY(city_id) REFERENCES cities(id)
                            )''')
            conn.commit()  # Değişiklikleri onaylama

    def add_city(self, user_id, city_name):
        conn = sqlite3.connect(self.database)
        with conn:
            cursor = conn.cursor()
            # Veri tabanında şehir adına göre sorgulama yapma
            cursor.execute("SELECT id FROM cities WHERE city=?", (city_name,))
            city_data = cursor.fetchone()
            if city_data:
                city_id = city_data[0]
                # Şehri kullanıcının şehir listesine ekleme
                conn.execute('INSERT INTO users_cities VALUES (?, ?)', (user_id, city_id))
                conn.commit()
                return 1  # İşlemin başarılı olduğunu belirtme
            else:
                return 0  # Şehir bulunamadı

    def select_cities(self, user_id):
        conn = sqlite3.connect(self.database)
        with conn:
            cursor = conn.cursor()
            # Kullanıcının tüm şehirlerini seçme
            cursor.execute('''SELECT cities.city 
                            FROM users_cities  
                            JOIN cities ON users_cities.city_id = cities.id
                            WHERE users_cities.user_id = ?''', (user_id,))
            cities = [row[0] for row in cursor.fetchall()]
            return cities  # Kullanıcının şehir listesini döndürme

    def get_coordinates(self, city_name):
        conn = sqlite3.connect(self.database)
        with conn:
            cursor = conn.cursor()
            # Şehrin adına göre koordinatlarını alma
            cursor.execute('''SELECT lat, lng
                            FROM cities  
                            WHERE city = ?''', (city_name,))
            coordinates = cursor.fetchone()
            return coordinates  # Şehrin koordinatlarını döndürme


    def create_graph(self, path, cities):
        ax = plt.axes(projection=ccrs.PlateCarree())
        ax.stock_img()
        for city in cities:
            # Şehrin koordinatlarını alma. Bu fonksiyon, şehrin enlem ve boylamını içeren bir demet döndürmelidir.
            coordinates = self.get_coordinates(city)

            # Şehrin koordinatlarının başarıyla alındığını kontrol etme.
            if coordinates:
                # Koordinat demetini enlem (lat) ve boylam (lng) değişkenlerine ayırma.
                lat, lng = coordinates

                # Şehrin koordinatlarına göre haritada bir işaretçi çizme.
                # 'color='r'' işaretçi rengini kırmızı yapar, 'linewidth=1' işaretçi çizgi kalınlığını belirler,
                # 'marker='.'' işaretçi şeklini (nokta) belirtir.
                plt.plot([lng], [lat], color='r', linewidth=1, marker='.', transform=ccrs.Geodetic())

                # İşaretçinin yanına şehrin adını ekleme.
                # '+3' ve '+12' boylam ve enleme göre metni işaretçiden uzaklaştırır,
                # böylece metin işaretçiyle çakışmaz ve okunabilir kalır.
                plt.text(lng + 3, lat + 12, city, horizontalalignment='left', transform=ccrs.Geodetic())

        # Oluşturulan görüntüyü 'path' argümanında belirtilen yola kaydetme.
        plt.savefig(path)

        # Matplotlib bağlamını kapatarak kaynakları serbest bırakma.
        plt.close()


    def draw_distance(self, city1, city2):
        # İki şehir arasındaki mesafeyi göstermek için bir çizgi çizme
        city1_coords = self.get_coordinates(city1)
        city2_coords = self.get_coordinates(city2)
        fig, ax = plt.subplots(subplot_kw={'projection': ccrs.PlateCarree()})
        ax.stock_img()
        plt.plot([city1_coords[1], city2_coords[1]], [city1_coords[0], city2_coords[0]], color='red', linewidth=2,
                 marker='o', transform=ccrs.Geodetic())
        plt.text(city1_coords[1] + 3, city1_coords[0] + 12, city1, horizontalalignment='left',
                 transform=ccrs.Geodetic())
        plt.text(city2_coords[1] + 3, city2_coords[0] + 12, city2, horizontalalignment='left',
                 transform=ccrs.Geodetic())
        plt.savefig('distance_map.png')
        plt.close()


if __name__ == "__main__":
    m = DB_Map("database.db")  # Veri tabanıyla etkileşime geçecek bir nesne oluşturma
    m.create_user_table()   # Kullanıcı şehirleri tablosunu oluşturma (eğer zaten yoksa)
    #m.draw_distance("Malatya", "New York")
