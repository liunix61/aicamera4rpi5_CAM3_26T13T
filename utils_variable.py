import paramiko


provinces = [
    "กรุงเทพมหานคร", "กระบี่", "กาญจนบุรี", "กาฬสินธุ์", "กำแพงเพชร", "ขอนแก่น", "จันทบุรี", "ฉะเชิงเทรา",
    "ชลบุรี", "ชัยนาท", "ชัยภูมิ", "ชุมพร", "เชียงราย", "เชียงใหม่", "ตรัง", "ตราด", "ตาก", "นครนายก",
    "นครปฐม", "นครพนม", "นครราชสีมา", "นครศรีธรรมราช", "นครสวรรค์", "นนทบุรี", "นราธิวาส", "น่าน",
    "บึงกาฬ", "บุรีรัมย์", "ปทุมธานี", "ประจวบคีรีขันธ์", "ปราจีนบุรี", "ปัตตานี", "พระนครศรีอยุธยา",
    "พังงา", "พัทลุง", "พิจิตร", "พิษณุโลก", "เพชรบุรี", "เพชรบูรณ์", "แพร่", "พะเยา", "ภูเก็ต",
    "มหาสารคาม", "มุกดาหาร", "แม่ฮ่องสอน", "ยโสธร", "ยะลา", "ร้อยเอ็ด", "ระนอง", "ระยอง", "ราชบุรี",
    "ลพบุรี", "ลำปาง", "ลำพูน", "เลย", "ศรีสะเกษ", "สกลนคร", "สงขลา", "สตูล", "สมุทรปราการ",
    "สมุทรสงคราม", "สมุทรสาคร", "สระแก้ว", "สระบุรี", "สิงห์บุรี", "สุโขทัย", "สุพรรณบุรี", "สุราษฎร์ธานี",
    "สุรินทร์", "หนองคาย", "หนองบัวลำภู", "อ่างทอง", "อำนาจเจริญ", "อุดรธานี", "อุตรดิตถ์", "อุทัยธานี",
    "อุบลราชธานี"
]

# หมวดตัวอักษรสำหรับป้ายทะเบียน (เช่น กข, ขก, นบ)
lpr_categories = ["กข", "ขก", "นบ", "พค", "รย", "สก", "อท", "จบ", "ลพ", "ภค"]

def main():
    """Main function to run the script."""
    print("🚀 Starting the script...")
    # Call the function to get LTE info
    get_lte_info()
    # Call the function to generate mock data
    # generate_mock_data()  # Uncomment if you want to use this function

def get_lte_info():
    """Connects to router via SSH and runs commands."""
    try:
        # Router SSH details
        HOST = "192.168.103.1"
        USERNAME = "root"
        PASSWORD = ""  # Change to your actual password

        # Commands to execute
        COMMANDS = [
            "uqmi -d /dev/cdc-wdm0 --get-serving-cell",
            "uqmi -d /dev/cdc-wdm0 --get-signal-info"
        ]
        # Establish SSH connection
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(HOST, username=USERNAME, password=PASSWORD)

        for command in COMMANDS:
            print(f"Executing: {command}")
            stdin, stdout, stderr = ssh.exec_command(command)
            output = stdout.read().decode().strip()
            error = stderr.read().decode().strip()

            if output:
                print(f"✅ Output:\n{output}")
            if error:
                print(f"❌ Error:\n{error}")

        ssh.close()
        return output, error
    except Exception as e:
        print(f"❌ SSH Connection Failed: {e}")

if __name__ == "__main__":
    main()