# Kế hoạch kiểm thử

## 1. Mục tiêu
Kiểm tra tính đúng đắn của phép nhân, phép cộng và tính chất trường GF(2^n) cho GF(2^4) và GF(2^8).

## 2. Test case

### 2.1 Test hợp lệ
- GF256.mul(0x57, 0x83) == 0xC1
- GF256.mul(0x57, 0x13) == 0xFE
- GF16.mul(0b0010, 0b1000) == 0b0011

### 2.2 Test không hợp lệ
- Khởi tạo trường với đa thức reducible 0b10101 phải ném ValueError.
- Giá trị ngoài phạm vi phải ném ValueError.

### 2.3 Test biên
- a = 0, b = 0
- a = 1, b = 1
- a = size - 1, b = size - 1
- a khác 0, kiểm tra `inv(a)`

### 2.4 Test tính chất trường
- Giao hoán: a × b = b × a
- Kết hợp: (a × b) × c = a × (b × c)
- Phân phối: a × (b + c) = a × b + a × c
- Đơn vị: a × 1 = a
- Nghịch đảo: a × a^{-1} = 1 với a != 0

## 3. Kết quả mong đợi độc lập
- 0x57 × 0x83 = 0xC1 theo chuẩn FIPS-197
- Có 3 đa thức tối giản bậc 4 và 30 đa thức tối giản bậc 8
- Mọi phần tử không bằng 0 trong trường đều có nghịch đảo

## 4. Lệnh chạy
```bash
cd project
python tests/test_gf.py
```

## 5. Trạng thái dự kiến
- PASS nếu tất cả test đều chạy và không có lỗi assertion.
- FAIL nếu có assert sai hoặc exception không đúng như mong đợi.
- BLOCKED nếu môi trường thiếu Python hoặc file import không tồn tại.
