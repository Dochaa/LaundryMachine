import threading
import time
import requests

class LaundryMachine:
    def __init__(self, name, price):
        self.name = name
        self.price = price
        self.used_by = []
        self.in_use = False
        self.remaining_time = 0

class CoinBank:
    def __init__(self):
        self.coins = {1: 0, 2: 0, 5: 0, 10: 0}

class NoteBank:
    def __init__(self):
        self.notes = {20: 0, 50: 0, 100: 0, 500: 0, 1000: 0}

class LaundryBusiness:
    def __init__(self):
        self.machines = [
            LaundryMachine("เครื่องที่ 1", 20),
            LaundryMachine("เครื่องที่ 2", 30),
            LaundryMachine("เครื่องที่ 3", 40),
            LaundryMachine("เครื่องที่ 4", 50)
        ]
        self.coin_bank = CoinBank()
        self.note_bank = NoteBank()

    def show_machine_list(self):
        for idx, machine in enumerate(self.machines):
            print(f"{idx + 1}. {machine.name} - {machine.price} บาท")

    def start_laundry(self, machine_idx):
        if not (1 <= machine_idx <= len(self.machines)):
            print("หมายเลขเครื่องไม่ถูกต้อง กรุณาใส่หมายเลขเครื่องที่ถูกต้อง")
            return

        selected_machine = self.machines[machine_idx - 1]
        print(f"คุณเลือกเครื่อง {selected_machine.name} ราคา {selected_machine.price} บาท")
        selected_machine.used_by.append("หมายเลขเครื่อง")
        selected_machine.in_use = True
        selected_machine.remaining_time = 2 * 60

        total_payment = selected_machine.price

        while total_payment > 0:
            self.show_payment_options()
            payment = input("กรุณาใส่เหรียญหรือแบงค์: ")
            
            if payment.isdigit():
                payment = int(payment)
                if payment in self.coin_bank.coins or payment in self.note_bank.notes:
                    if payment <= total_payment:
                        total_payment -= payment
                        if payment in self.coin_bank.coins:
                            self.coin_bank.coins[payment] += 1
                        else:
                            self.note_bank.notes[payment] += 1
                    else:
                        change = payment - total_payment
                        print(f"ต้องทอนเงิน {change} บาท")
                        self.calculate_change(change)
                        total_payment = 0
                else:
                    print("เงินที่ใส่ไม่ถูกต้อง")
            else:
                print("กรุณาใส่เงินเป็นตัวเลขเท่านั้น")

            if total_payment > 0:
                print(f"คุณต้องใส่เงินอีก {total_payment} บาท")

        self.process_laundry(selected_machine)

    def show_payment_options(self):
        print("เหรียญ: 1, 2, 5, 10 บาท")
        print("แบงค์: 20, 50, 100, 500, 1000 บาท")

    def calculate_change(self, change):
        available_notes = sorted(self.note_bank.notes.keys(), reverse=True)
        available_coins = sorted(self.coin_bank.coins.keys(), reverse=True)
        
        for note in available_notes:
            while change >= note and self.note_bank.notes[note] > 0:
                change -= note
                self.note_bank.notes[note] -= 1
                print(f"ทอน {note} บาท (แบงค์)")
        
        for coin in available_coins:
            while change >= coin and self.coin_bank.coins[coin] > 0:
                change -= coin
                self.coin_bank.coins[coin] -= 1
                print(f"ทอน {coin} บาท (เหรียญ)")

    def process_laundry(self, machine):
        print(f"กำลังซักผ้าด้วยเครื่อง {machine.name}...")
        countdown_thread = threading.Thread(target=self.countdown, args=(machine,))
        countdown_thread.start()

    def countdown(self, machine):
        while machine.remaining_time > 0:
            print(f"เครื่อง {machine.name} กำลังทำงานอยู่ เหลือเวลาอีก {machine.remaining_time // 60} นาที")
            
            # ส่งข้อความไปยังกลุ่ม Line ถ้าเวลานับถอยหลังน้อยกว่า 1 นาที
            if machine.remaining_time <= 60:
                self.send_line_notification(machine.name)
            
            
            time.sleep(30)  # แสดงสถานะทุก 30 วินาที
            machine.remaining_time -= 30

        machine.in_use = False
        machine.remaining_time = 0
        print(f"{machine.name} เสร็จสิ้นการทำงาน")
    
    def send_line_notification(self, machine_name):
        line_notify_token = "LeaW0kHxoLb9sZEQD1DcQYKIoB4irRrCyxeBf2NtOGh" 
          
        message = f" {machine_name} ใกล้เสร็จแล้ว!"
        
        headers = {
            "Authorization": f"Bearer {line_notify_token}"
        }
        
        payload = {
            "message": message
          
        }
        
        response = requests.post("https://notify-api.line.me/api/notify", headers=headers, data=payload)
        
        if response.status_code == 200:
            print("ส่งข้อความไปยังกลุ่ม Line สำเร็จ")
        else:
            print("เกิดข้อผิดพลาดในการส่งข้อความไปยังกลุ่ม Line")

    def show_machine_status(self):
        print("สถานะเครื่องซักผ้า:")
        for machine in self.machines:
            status = "กำลังทำงาน" if machine.in_use else "พร้อมทำงาน"
            remaining_time = machine.remaining_time // 60 if machine.in_use else 0
            print(f"{machine.name} - {status}, เหลือเวลา: {remaining_time} นาที")
            

    
# เครื่องซักผ้า
laundry_business = LaundryBusiness()

while True:
    print("ยินดีต้อนรับสู่ธุรกิจเครื่องซักผ้า")
    print("1. เริ่มซักผ้า")
    print("2. ตรวจสอบสถานะเครื่องซักผ้า")
    choice = input("กรุณาเลือก: ")

    if choice == "1":
        laundry_business.show_machine_list()
        machine_choice = input("กรุณาเลือกเครื่องที่คุณต้องการ (ใส่หมายเลข 1-4): ")
        
        if machine_choice.isdigit():
            machine_choice = int(machine_choice)
            if laundry_business.machines[machine_choice - 1].in_use:
                print(f"เครื่อง {laundry_business.machines[machine_choice - 1].name} กำลังทำงานอยู่ เหลือเวลาอีก {laundry_business.machines[machine_choice - 1].remaining_time // 60} นาที")
                continue_choice = input("คุณต้องการเริ่มซักผ้าใหม่หรือไม่? (y/n): ")
                if continue_choice.lower() == 'y':
                    continue
                else:
                    break
            else:
                laundry_business.start_laundry(machine_choice)
        else:
            print("กรุณาใส่หมายเลขเครื่องที่ถูกต้อง")

    elif choice == "2":
        laundry_business.show_machine_status()

print("ขอบคุณที่ใช้บริการ!")