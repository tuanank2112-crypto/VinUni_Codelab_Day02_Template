"""Render the assignment workflow diagram with Pillow; no image generation API."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
FONT = next((p for p in [Path('/System/Library/Fonts/Supplemental/Arial.ttf'),
                         Path('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf')] if p.exists()), None)
if FONT is None:
    raise SystemExit('Install Arial or DejaVu Sans to render Vietnamese text.')

def font(size):
    return ImageFont.truetype(str(FONT), size)

im = Image.new('RGB', (1920, 1150), '#f3f6fa')
d = ImageDraw.Draw(im)
d.rectangle((0, 0, 1920, 165), fill='#142d40')
d.text((65, 34), 'VINHOMES INCIDENT INTELLIGENCE', font=font(40), fill='white')
d.text((65, 94), 'CURRENT-STATE WORKFLOW  /  Quy trình hiện tại cần kiểm chứng', font=font(29), fill='#a8dcd6')
steps = [
    ('01  TIẾP NHẬN', 'CSKH', 'Nội dung cư dân → phiếu', '3 phút', False),
    ('02  CHUẨN HÓA', 'CSKH', 'Triệu chứng · căn · giờ', '4 phút', False),
    ('03  ĐỐI CHIẾU', 'Điều phối', 'Phiếu + sơ đồ → phạm vi', '8 phút  /  B1', True),
    ('04  PHÂN CÔNG', 'Điều phối', 'Ca + vật tư → lệnh kiểm tra', '7 phút  /  B2', True),
    ('05  KIỂM TRA', 'Kỹ thuật viên', 'Lệnh → bằng chứng', '20 phút', False),
    ('06  XÁC MINH', 'Điều phối + CSKH', 'Cập nhật · tiếp tục theo dõi', '5 phút', False),
]
coords = [(65, 225), (695, 225), (1325, 225), (65, 565), (695, 565), (1325, 565)]
for (title, actor, desc, duration, bottleneck), (x,y) in zip(steps, coords):
    color = '#b33c38' if bottleneck else '#176c70'
    d.rounded_rectangle((x,y,x+530,y+250), radius=20, fill='white', outline=color, width=3)
    d.rectangle((x+1,y+25,x+8,y+225), fill=color)
    d.text((x+25,y+25), title, font=font(29), fill=color)
    d.text((x+25,y+86), actor, font=font(27), fill='#173448')
    d.text((x+25,y+135), desc, font=font(25), fill='#526573')
    d.text((x+25,y+191), duration, font=font(29), fill=color)

def arrow(points):
    d.line(points, fill='#637c91', width=4)
    x,y = points[-1]; px,py = points[-2]
    if x > px: tri=[(x,y),(x-14,y-9),(x-14,y+9)]
    elif x < px: tri=[(x,y),(x+14,y-9),(x+14,y+9)]
    else: tri=[(x,y),(x-9,y-14),(x+9,y-14)]
    d.polygon(tri, fill='#637c91')
for y in (350,690):
    arrow([(595,y),(695,y)])
    arrow([(1225,y),(1325,y)])
arrow([(1590,475),(1590,520),(330,520),(330,565)])
d.text((72,187), 'H1  Cư dân → CSKH', font=font(22), fill='#536a7b')
d.text((1250,187), 'H2  CSKH → điều phối', font=font(22), fill='#536a7b')
d.text((640,530), 'H3  Điều phối → kỹ thuật', font=font(22), fill='#536a7b')
d.text((1220,530), 'H4  Kỹ thuật → điều phối', font=font(22), fill='#536a7b')
d.text((1270,830), 'H5  CSKH ↔ cư dân', font=font(22), fill='#536a7b')
d.rounded_rectangle((65,890,1855,1095), radius=16, fill='#e3edf3')
d.text((90,910), '47 phút/phiếu = 3 + 4 + 8 + 7 + 20 + 5  |  Toàn bộ là giả định, chưa đo thực tế.', font=font(28), fill='#173448')
d.text((90,958), 'B1: Thông tin rời rạc, khó nhận ra sự cố chung.   B2: Tra nguồn lực và phân việc thủ công.', font=font(25), fill='#9e3431')
d.text((90,1003), 'H = handoff (chuyển giao). Chưa tính chờ, di chuyển và sửa chữa. Chưa xác minh → chưa đóng.', font=font(25), fill='#334f61')
d.text((90,1048), 'Nếu xác nhận lỗi: duyệt sửa → thực hiện → quay lại bước 06. Thời lượng sửa tùy lỗi.', font=font(25), fill='#334f61')
im.save(ROOT / '04-workflow-diagram.png')
print('Created 04-workflow-diagram.png (1920 × 1150)')
