# GF(2^n) Polynomial Multiplication

## Tổng quan
Dự án này triển khai phép nhân đa thức trong các trường hữu hạn GF(2^4) và GF(2^8) bằng cách lưu đa thức dưới dạng số nguyên và thực hiện XOR / modulo theo đa thức tối giản.

## Cấu trúc thư mục
```text
project/
├── src/
│   └── gf.py
├── tests/
│   └── test_gf.py
├── docs/
│   ├── requirements.md
│   └── test_plan.md
└── README.md
```

## Đa thức tối giản được chọn
- GF(2^4): x^4 + x + 1
- GF(2^8): x^8 + x^4 + x^3 + x + 1

## Chạy demo
```bash
cd project
python src/gf.py
```

## Chạy kiểm thử
```bash
cd project
python tests/test_gf.py
```

## Dùng như thư viện
```python
from src.gf import GF16, GF256

print(GF16.mul(0b1011, 0b0101))
print(GF256.mul(0x57, 0x83))  # 0xC1
```

## Ghi chú
- Chương trình tự kiểm tra tính tối giản và từ chối đa thức không tối giản.
- Hai phương pháp nhân được đồng bộ: `mul_schoolbook` và `mul`.
- Kết quả của ví dụ chuẩn AES là 0x57 × 0x83 = 0xC1.
