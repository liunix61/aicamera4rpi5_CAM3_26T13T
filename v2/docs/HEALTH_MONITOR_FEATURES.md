# ฟีเจอร์ Health Monitor AI Camera v2

## คุณสมบัติหลัก

### 1. การตรวจสอบระบบอัตโนมัติ
- **การตรวจสอบตามช่วงเวลา**: ทำงานตาม `HEALTH_CHECK_INTERVAL` ใน config.py (ค่าเริ่มต้น: 3600 วินาที = 1 ชั่วโมง)
- **การบันทึกอัตโนมัติ**: ผลการตรวจสอบทั้งหมดถูกบันทึกลงฐานข้อมูล
- **การทำงานแบบ Background**: ทำงานใน thread แยกต่างหากไม่รบกวนการทำงานหลัก

### 2. การตรวจสอบส่วนประกอบต่างๆ

#### a. Camera (กล้อง)
- ตรวจสอบว่ากล้องเริ่มต้นแล้วหรือไม่
- ตรวจสอบว่ากล้องกำลังสตรีมอยู่หรือไม่
- สถานะ: PASS, WARNING, FAIL

#### b. Disk Space (พื้นที่ดิสก์)
- ตรวจสอบพื้นที่ว่างในดิสก์ที่ใช้บันทึกรูปภาพ
- แสดงข้อมูล: พื้นที่ว่าง, พื้นที่ใช้แล้ว, พื้นที่ทั้งหมด
- สถานะ: PASS (≥ 1GB), FAIL (< 1GB)

#### c. CPU & RAM (หน่วยประมวลผลและหน่วยความจำ)
- ตรวจสอบการใช้ CPU และ RAM
- แสดงข้อมูล: CPU usage, RAM usage, จำนวน cores, อุณหภูมิ CPU
- สถานะ: PASS (< 90%), WARNING (≥ 90%)

#### d. Detection Models (โมเดลการตรวจจับ)
- ตรวจสอบว่าไฟล์โมเดลการตรวจจับอยู่ครบถ้วน
- ตรวจสอบโฟลเดอร์ models และไฟล์ .hef
- สถานะ: PASS (พบทั้งหมด), FAIL (ไม่พบ)

#### e. EasyOCR
- ตรวจสอบว่า EasyOCR สามารถ import ได้
- ทดสอบการสร้าง Reader object
- สถานะ: PASS (ทำงานได้), FAIL (ไม่สามารถ import)

#### f. Database (ฐานข้อมูล)
- ตรวจสอบการเชื่อมต่อฐานข้อมูล
- ทดสอบการ query ข้อมูล
- สถานะ: PASS (เชื่อมต่อได้), FAIL (ไม่สามารถเชื่อมต่อ)

#### g. Network Connectivity (การเชื่อมต่อเครือข่าย)
- ตรวจสอบการเชื่อมต่อ Google DNS (8.8.8.8:53)
- ตรวจสอบการเชื่อมต่อ WebSocket server (ถ้ามีการตั้งค่า)
- สถานะ: PASS (เชื่อมต่อได้), WARNING (DNS ได้แต่ WebSocket ไม่ได้), FAIL (ไม่สามารถเชื่อมต่อ)

## การใช้งาน

### ผ่านหน้าเว็บ
1. เปิดเบราว์เซอร์ไปที่ `http://localhost:5000`
2. ดูส่วน "System Health Status" ที่แสดงสถานะปัจจุบัน
3. คลิก "Run Health Check" เพื่อตรวจสอบทันที
4. ดูส่วน "Health Check History" เพื่อดูประวัติการตรวจสอบ

### ผ่าน API

#### ตรวจสอบระบบทันที
```bash
curl -X POST http://localhost:5000/api/health_check
```

#### ดูสถานะล่าสุด
```bash
curl http://localhost:5000/api/health_status
```

#### เริ่มการตรวจสอบอัตโนมัติ
```bash
curl -X POST http://localhost:5000/api/start_health_monitoring
```

#### หยุดการตรวจสอบอัตโนมัติ
```bash
curl -X POST http://localhost:5000/api/stop_health_monitoring
```

## โครงสร้างข้อมูล

### Health Check Record
```json
{
  "id": 316,
  "timestamp": "2025-08-04T21:52:11.330797",
  "component": "Network Connectivity",
  "status": "WARNING",
  "message": "Google DNS reachable but WebSocket server connection failed"
}
```

### Health Check Results
```json
{
  "status": "success",
  "message": "Health check completed",
  "results": {
    "camera": true,
    "disk_space": true,
    "cpu_ram": true,
    "detection_models": false,
    "easyocr": false,
    "database": true,
    "network": true
  }
}
```

## การแสดงผลในหน้าเว็บ

### 1. Health Summary
- **Overall Status**: สถานะรวมของระบบ (Healthy, Warning, Critical)
- **Last Check**: เวลาตรวจสอบล่าสุด

### 2. Component Status
- แสดงสถานะของแต่ละส่วนประกอบ
- ใช้สีเพื่อแสดงสถานะ:
  - 🟢 สีเขียว: PASS
  - 🟡 สีเหลือง: WARNING
  - 🔴 สีแดง: FAIL

### 3. Health History
- แสดงประวัติการตรวจสอบ 10 รายการล่าสุด
- แสดงเวลา, ส่วนประกอบ, สถานะ, และข้อความ
- ใช้สีขอบเพื่อแยกประเภทสถานะ

## การตั้งค่า

### ใน config.py
```python
# Health monitoring interval (in seconds, 3600 seconds = 1 hour)
HEALTH_CHECK_INTERVAL = 3600
```

### การปรับแต่งการตรวจสอบ
- เปลี่ยน `HEALTH_CHECK_INTERVAL` เพื่อปรับความถี่การตรวจสอบ
- แก้ไข `required_gb` ใน `check_disk_space()` เพื่อปรับเกณฑ์พื้นที่ว่าง
- แก้ไขเกณฑ์ CPU/RAM ใน `check_cpu_ram()` (ปัจจุบัน: 90%)

## การทดสอบ

### ทดสอบ Health Monitor
```bash
python test_health_monitor.py
```

### ทดสอบแอปพลิเคชันทั้งหมด
```bash
python test_simple_app.py
```

## ตัวอย่างผลลัพธ์

### สถานะปกติ
```
Camera: PASS - Camera initialized and streaming.
Disk Space: PASS - Disk space OK: 35.33 GB free (33.4% used, 57.4 GB total).
CPU & RAM: PASS - CPU: 40.6% (4 cores), RAM: 16.3% (13.3 GB available of 15.8 GB).
Database: PASS - Database connection is active and responsive.
Network: WARNING - Google DNS reachable but WebSocket server connection failed.
```

### สถานะมีปัญหา
```
Detection Models: FAIL - Models directory not found: /home/camuser/aicamera/v2/models
EasyOCR: FAIL - EasyOCR module not found or not importable.
```

## ข้อควรระวัง

1. **การตรวจสอบ EasyOCR** อาจใช้เวลานานในการเริ่มต้น
2. **การตรวจสอบ Network** อาจล้มเหลวหากไม่มีอินเทอร์เน็ต
3. **การตรวจสอบ CPU Temperature** อาจไม่ทำงานในบางระบบ
4. **การตรวจสอบ Detection Models** ขึ้นอยู่กับการตั้งค่าใน config.py

## การพัฒนาเพิ่มเติม

### ฟีเจอร์ที่อาจเพิ่มในอนาคต
- การแจ้งเตือนผ่าน email/SMS เมื่อพบปัญหา
- การสร้างรายงานสรุปประจำวัน/สัปดาห์
- การตั้งค่าเกณฑ์การแจ้งเตือนสำหรับแต่ละส่วนประกอบ
- การแสดงกราฟแนวโน้มการใช้งานระบบ
- การตรวจสอบการเชื่อมต่อกับเซิร์ฟเวอร์ภายนอกเพิ่มเติม 