from services.booking_service import BookingService, VIPBookingService, StandardBookingService
from services.payment_service import (
    CashPayment, CreditCardPayment, QRISPayment, 
    EWalletPayment, BankTransferPayment
)
from repositories.room_repository import RoomRepository
from utils.constants import VIP, STANDARD


def display_payment_methods():
    """Menampilkan pilihan metode pembayaran."""
    print("\n--- Payment Methods ---")
    print("1. Cash")
    print("2. Credit Card")
    print("3. QRIS")
    print("4. E-Wallet")
    print("5. Bank Transfer")
    return input("Select payment method (1-5): ").strip()


def get_payment_service(choice: str):
    """Mendapatkan service pembayaran berdasarkan pilihan user."""
    if choice == "1":
        return CashPayment()
    elif choice == "2":
        return CreditCardPayment()
    elif choice == "3":
        return QRISPayment()
    elif choice == "4":
        return EWalletPayment()
    elif choice == "5":
        return BankTransferPayment()
    else:
        raise ValueError("Invalid payment method choice")


def main():
    """
    Entry point aplikasi.
    Bertanggung jawab untuk interaksi dengan user (UI layer)
    dan mengorkestrasi pemanggilan service.
    """

    repository = RoomRepository()
    
    print("=== Hotel Rental System ===")

    try:
        name = input("Name: ").strip()
        room_type = input("Room type (VIP/STANDARD): ").upper()

        if room_type not in [VIP, STANDARD]:
            print("Invalid room type. Please use VIP or STANDARD")
            return

        if room_type == VIP:
            booking_service = VIPBookingService(repository)
        else:
            booking_service = StandardBookingService(repository)

        if not booking_service.check_availability(room_type):
            print("Room not available")
            return

        price = booking_service.book_room(room_type)

        payment_choice = display_payment_methods()
        payment_service = get_payment_service(payment_choice)

        use_discount = input("Use discount? (y/n): ").lower() == "y"
        total = payment_service.calculate_total(price, use_discount)

        print("\n--- RESULT ---")
        print("Name:", name)
        print("Room:", room_type)
        print("Price:", price)
        print("Total (with fee):", total)
        print("Payment Status: COMPLETED")

    except Exception as error:
        print("Error:", error)


if __name__ == "__main__":
    main()