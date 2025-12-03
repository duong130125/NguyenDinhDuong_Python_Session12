import json
import os
import csv
import matplotlib.pyplot as plt

DATA_FILE = "data.json"


# ==============================
# 1. Đọc dữ liệu từ file
# ==============================
def load_data():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


# ==============================
# 2. Lưu dữ liệu vào file
# ==============================
def save_data(students):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(students, f, ensure_ascii=False, indent=4)


# ==============================
# Tính điểm TB và xếp loại
# ==============================
def calculate_stats(toan, ly, hoa):
    diem_tb = round((toan + ly + hoa) / 3, 2)
    if diem_tb >= 8:
        xep_loai = "Giỏi"
    elif diem_tb >= 6.5:
        xep_loai = "Khá"
    elif diem_tb >= 5:
        xep_loai = "Trung Bình"
    else:
        xep_loai = "Yếu"
    return diem_tb, xep_loai


# ==============================
# 3. Hiển thị danh sách sinh viên
# ==============================
def show_students(students):
    if not students:
        print("\nDanh sách sinh viên trống!\n")
        return

    print("\n{:<10} {:<20} {:<6} {:<6} {:<6} {:<8} {:<10}".format(
        "Mã SV", "Tên", "Toán", "Lý", "Hóa", "TB", "Xếp loại"
    ))
    print("-" * 75)
    for sv in students:
        print("{:<10} {:<20} {:<6} {:<6} {:<6} {:<8} {:<10}".format(
            sv["ma_sv"], sv["ten"], sv["toan"], sv["ly"], sv["hoa"],
            sv["diem_tb"], sv["xep_loai"]
        ))
    print()


# ==============================
# 4. Thêm sinh viên
# ==============================
def add_student(students):
    ma_sv = input("Nhập mã sinh viên: ")

    if any(s["ma_sv"] == ma_sv for s in students):
        print("❌ Mã sinh viên đã tồn tại!")
        return

    ten = input("Nhập tên sinh viên: ")

    try:
        toan = float(input("Điểm Toán: "))
        ly = float(input("Điểm Lý: "))
        hoa = float(input("Điểm Hóa: "))
    except:
        print("❌ Điểm phải là số!")
        return

    if not (0 <= toan <= 10 and 0 <= ly <= 10 and 0 <= hoa <= 10):
        print("❌ Điểm phải nằm trong khoảng 0-10!")
        return

    diem_tb, xep_loai = calculate_stats(toan, ly, hoa)

    students.append({
        "ma_sv": ma_sv,
        "ten": ten,
        "toan": toan,
        "ly": ly,
        "hoa": hoa,
        "diem_tb": diem_tb,
        "xep_loai": xep_loai
    })

    print("✔️ Thêm sinh viên thành công!\n")


# ==============================
# 5. Cập nhật sinh viên
# ==============================
def update_student(students):
    ma_sv = input("Nhập mã sinh viên cần cập nhật: ")
    for sv in students:
        if sv["ma_sv"] == ma_sv:
            print("Nhập lại điểm:")
            try:
                toan = float(input("Điểm Toán: "))
                ly = float(input("Điểm Lý: "))
                hoa = float(input("Điểm Hóa: "))
            except:
                print("❌ Điểm phải là số!")
                return

            if not (0 <= toan <= 10 and 0 <= ly <= 10 and 0 <= hoa <= 10):
                print("❌ Điểm phải nằm trong 0-10!")
                return

            sv["toan"] = toan
            sv["ly"] = ly
            sv["hoa"] = hoa
            sv["diem_tb"], sv["xep_loai"] = calculate_stats(toan, ly, hoa)

            print("✔️ Cập nhật thành công!\n")
            return

    print("❌ Không tìm thấy sinh viên!\n")


# ==============================
# 6. Xóa sinh viên
# ==============================
def delete_student(students):
    ma_sv = input("Nhập mã sinh viên cần xóa: ")
    for sv in students:
        if sv["ma_sv"] == ma_sv:
            confirm = input("Bạn có chắc muốn xóa? (y/n): ")
            if confirm.lower() == "y":
                students.remove(sv)
                print("✔️ Đã xóa!\n")
            else:
                print("❌ Hủy xóa.\n")
            return

    print("❌ Không tìm thấy sinh viên!\n")


# ==============================
# 7. Tìm kiếm sinh viên
# ==============================
def search_student(students):
    keyword = input("Nhập tên hoặc mã SV cần tìm: ").lower()

    results = [
        s for s in students
        if keyword in s["ten"].lower() or keyword == s["ma_sv"].lower()
    ]

    if not results:
        print("❌ Không tìm thấy sinh viên nào!\n")
    else:
        print("\nKết quả tìm kiếm:")
        show_students(results)


# ==============================
# 8. Sắp xếp sinh viên
# ==============================
def sort_students(students):
    print("\n1. Sắp xếp theo điểm TB giảm dần")
    print("2. Sắp xếp theo tên tăng dần (A-Z)")
    choice = input("Chọn: ")

    if choice == "1":
        students.sort(key=lambda x: x["diem_tb"], reverse=True)
        print("✔️ Đã sắp xếp theo điểm TB!\n")
    elif choice == "2":
        students.sort(key=lambda x: x["ten"])
        print("✔️ Đã sắp xếp theo tên!\n")
    else:
        print("❌ Lựa chọn không hợp lệ!\n")


# ==============================
# 9. Thống kê điểm trung bình
# ==============================
def statistics(students):
    stats = {"Giỏi": 0, "Khá": 0, "Trung Bình": 0, "Yếu": 0}
    for sv in students:
        stats[sv["xep_loai"]] += 1

    print("\n=== THỐNG KÊ XẾP LOẠI ===")
    for k, v in stats.items():
        print(f"{k}: {v}")

    return stats


def save_csv(students):
    with open("students.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Mã SV", "Tên", "Toán", "Lý", "Hóa", "TB", "Xếp loại"])
        for sv in students:
            writer.writerow([
                sv["ma_sv"], sv["ten"], sv["toan"], sv["ly"], sv["hoa"], 
                sv["diem_tb"], sv["xep_loai"]
            ])
    print("✔️ Đã lưu vào file students.csv\n")


# ==============================
# 10. Vẽ biểu đồ thống kê
# ==============================
def draw_chart(stats):
    labels = list(stats.keys())
    values = list(stats.values())

    plt.figure(figsize=(6, 6))
    plt.pie(values, labels=labels, autopct="%1.1f%%")
    plt.title("Thống kê xếp loại")
    plt.show()


# ==============================
# MENU CHÍNH
# ==============================
def main():
    students = load_data()

    while True:
        print("\n===== MENU QUẢN LÝ SINH VIÊN =====")
        print("1. Hiển thị danh sách sinh viên")
        print("2. Thêm mới sinh viên")
        print("3. Cập nhật thông tin sinh viên")
        print("4. Xoá sinh viên")
        print("5. Tìm kiếm sinh viên")
        print("6. Sắp xếp danh sách sinh viên")
        print("7. Thống kê điểm TB")
        print("8. Vẽ biểu đồ thống kê")
        print("9. Lưu vào file CSV")
        print("10. Thoát")

        ch = input("Chọn chức năng: ")

        if ch == "1":
            show_students(students)
        elif ch == "2":
            add_student(students)
        elif ch == "3":
            update_student(students)
        elif ch == "4":
            delete_student(students)
        elif ch == "5":
            search_student(students)
        elif ch == "6":
            sort_students(students)
        elif ch == "7":
            stats = statistics(students)
        elif ch == "8":
            stats = statistics(students)
            draw_chart(stats)
        elif ch == "9":
            save_csv(students)
        elif ch == "10":
            save_data(students)
            print("✔️ Đã lưu dữ liệu và thoát chương trình.")
            break
        else:
            print("❌ Lựa chọn không hợp lệ!\n")


# Chạy chương trình
if __name__ == "__main__":
    main()
