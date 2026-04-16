class Room:
    """
    Entity Room merepresentasikan kamar hotel (Base Class).
    Mengenkapsulasi state (availability) dan behavior (booking).
    """

    def __init__(self, room_type: str, price: int):
        """
        Inisialisasi objek kamar dengan tipe dan harga.
        
        Args:
            room_type (str): Tipe kamar (VIP/STANDARD)
            price (int): Harga kamar dalam Rupiah
        """
        self.__room_type = room_type
        self.__price = price
        self.__is_available = True

    @property
    def room_type(self):
        """
        Getter untuk tipe kamar.
        
        Returns:
            str: Tipe kamar yang dipilih
        """
        return self.__room_type

    @property
    def price(self):
        """
        Getter untuk harga kamar.
        
        Returns:
            int: Harga kamar dalam Rupiah
        """
        return self.__price

    @property
    def is_available(self):
        """
        Getter untuk status ketersediaan kamar.
        
        Returns:
            bool: True jika kamar tersedia, False jika sudah dipesan
        """
        return self.__is_available

    @price.setter
    def price(self, value: int):
        """
        Setter untuk harga kamar dengan validasi.
        Memastikan harga tidak negatif dan valid.
        
        Args:
            value (int): Harga baru kamar dalam Rupiah
            
        Raises:
            ValueError: Jika harga negatif
        """
        if value < 0:
            raise ValueError("Price cannot be negative")
        self.__price = value

    @is_available.setter
    def is_available(self, value: bool):
        """
        Setter untuk status ketersediaan kamar dengan validasi tipe.
        Memastikan parameter adalah boolean.
        
        Args:
            value (bool): Status ketersediaan kamar
            
        Raises:
            TypeError: Jika nilai bukan boolean
        """
        if not isinstance(value, bool):
            raise TypeError("is_available must be boolean")
        self.__is_available = value

    def book(self):
        """
        Mengubah status kamar menjadi tidak tersedia/terpesan.
        Memanggil method ini akan menandai kamar sebagai sudah dipesan.
        
        Raises:
            Exception: Jika kamar sudah dibooking sebelumnya
        """
        if not self.__is_available:
            raise Exception("Room is not available")
        self.__is_available = False

    def release(self):
        """
        Membebaskan kamar dengan mengubah status kembali menjadi tersedia.
        Digunakan ketika booking dibatalkan atau checkout dilakukan.
        """
        self.__is_available = True

    def get_room_info(self):
        """
        Mendapatkan informasi lengkap kamar dalam bentuk dictionary.
        Mengembalikan semua detail kamar termasuk tipe, harga, dan status.
        
        Returns:
            dict: Dictionary berisi informasi kamar (type, price, available)
        """
        return {
            "type": self.__room_type,
            "price": self.__price,
            "available": self.__is_available
        }


class VIPRoom(Room):
    """
    Child class untuk kamar VIP dengan fasilitas premium dan lengkap.
    Mewarisi dari Room dengan penambahan fasilitas mewah.
    """

    def __init__(self):
        """
        Inisialisasi kamar VIP dengan harga dan fasilitas premium.
        Harga default untuk VIP room adalah Rp 500.000.
        """
        super().__init__("VIP", 500000)
        self.__facilities = ["AC", "Wifi", "Bathtub", "Mini Bar", "Balcony"]

    @property
    def facilities(self):
        """
        Getter untuk daftar fasilitas kamar VIP.
        
        Returns:
            list: Daftar fasilitas premium yang tersedia
        """
        return self.__facilities

    def get_room_info(self):
        """
        Mendapatkan informasi lengkap kamar VIP termasuk fasilitas premium.
        Memanggil parent method dan menambahkan informasi fasilitas.
        
        Returns:
            dict: Dictionary berisi detail kamar VIP lengkap dengan fasilitas
        """
        info = super().get_room_info()
        info["facilities"] = self.__facilities
        return info

class StandardRoom(Room):
    """
    Child class untuk kamar Standard dengan fasilitas dasar dan terjangkau.
    Mewarisi dari Room dengan penambahan fasilitas standar.
    """

    def __init__(self):
        """
        Inisialisasi kamar Standard dengan harga dan fasilitas dasar.
        Harga default untuk Standard room adalah Rp 200.000.
        """
        super().__init__("STANDARD", 200000)
        self.__facilities = ["AC", "Wifi", "Shower"]

    @property
    def facilities(self):
        """
        Getter untuk daftar fasilitas kamar Standard.
        
        Returns:
            list: Daftar fasilitas dasar yang tersedia
        """
        return self.__facilities

    def get_room_info(self):
        """
        Mendapatkan informasi lengkap kamar Standard termasuk fasilitas dasar.
        Memanggil parent method dan menambahkan informasi fasilitas.
        
        Returns:
            dict: Dictionary berisi detail kamar Standard lengkap dengan fasilitas
        """
        info = super().get_room_info()
        info["facilities"] = self.__facilities
        return info