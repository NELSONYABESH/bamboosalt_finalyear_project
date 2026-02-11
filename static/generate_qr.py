import qrcode
import json
import os

def generate_qr(batch_id, quality_score, status):

    if not os.path.exists("static"):
        os.makedirs("static")

    qr_data = {
        "Batch ID": batch_id,
        "Quality Score": quality_score,
        "Status": status
    }

    filename = f"static/{batch_id}_qr.png"

    qr = qrcode.make(json.dumps(qr_data))
    qr.save(filename)

    return filename
