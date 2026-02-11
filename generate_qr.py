
import qrcode
import json

def generate_qr(batch_id, quality_score, status):
    qr_data = {
        "Batch ID": batch_id,
        "Quality Score": quality_score,
        "Status": status
    }

    qr = qrcode.make(json.dumps(qr_data))
    filename = f"static/{batch_id}_qr.png"
    qr.save(filename)

    return filename
