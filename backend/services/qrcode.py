import qrcode
from io import BytesIO
from aiogram.types import BufferedInputFile
from typing import Optional

def generate_early_qr_code(
    user_id: int,
    first_name: str,
    base_url: str = "https://saveas.pro/early"
) -> BufferedInputFile:
    ref_code = f"EB{user_id:06X}"
    url = f"{base_url}?ref={ref_code}&utm_source=telegram&utm_medium=qr"

    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=8,
        border=2,
    )
    qr.add_data(url)
    qr.make(fit=True)

    img = qr.make_image(
        fill_color="#1DA1F2",
        back_color="white"
    ).convert("RGB")

    buffer = BytesIO()
    img.save(buffer, format="PNG", optimize=True)
    buffer.seek(0)

    return BufferedInputFile(
        file=buffer.getvalue(),
        filename=f"saveas_early_{ref_code}.png"
    )
