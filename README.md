# Nhân hai đa thức trong trường hữu hạn GF(2^4) và GF(2^8)

Bài tập: cài đặt thuật toán nhân hai đa thức trong GF(2^n) với n = 4 và n = 8,
tương ứng với một đa thức tối giản (irreducible polynomial) của từng trường.

## Đa thức tối giản đã chọn

| Trường   | Đa thức tối giản          | Dạng nhị phân | Hex     |
|----------|---------------------------|---------------|---------|
| GF(2^4)  | x^4 + x + 1               | 10011         | 0x13    |
| GF(2^8)  | x^8 + x^4 + x^3 + x + 1   | 100011011     | 0x11B   |

(GF(2^8) dùng đa thức của chuẩn AES. Chương trình tự kiểm tra tính tối giản
và từ chối đa thức không tối giản.)

## Ý tưởng thuật toán

1. Một đa thức hệ số 0/1 được lưu thành một số nguyên: bit i là hệ số của x^i.
2. Cộng hai đa thức = XOR (vì 1 + 1 = 0 trong GF(2)).
3. Nhân hai đa thức: với mỗi bit 1 của b ở vị trí i, XOR vào kết quả giá trị a dịch trái i bit.
4. Lấy kết quả chia dư cho đa thức tối giản p(x) để đưa bậc về nhỏ hơn n.

Có hai cách cài đặt, cho cùng kết quả (đã test với mọi cặp phần tử):

- `mul_schoolbook`: nhân đầy đủ rồi chia lấy dư.
- `mul`: dịch-và-cộng, rút gọn ngay từng bước (kiểu `xtime` của AES).

## Cách chạy

```bash
python3 test_gf.py   # chạy kiểm thử
python3 gf.py        # chạy demo: ví dụ từng bước và bảng nhân GF(2^4)
```

Chỉ cần Python 3, không cần cài thư viện.

## Dùng như thư viện

```python
from gf import GF16, GF256
GF16.mul(0b1011, 0b0101)   # = 1
GF256.mul(0x57, 0x83)      # = 0xC1 (ví dụ chuẩn trong FIPS-197)
```

## Cấu trúc

- `gf.py`: cài đặt chính
- `test_gf.py`: kiểm thử (giao hoán, kết hợp, phân phối, nghịch đảo, đếm số đa thức tối giản)
