from flask import Flask, render_template, request, make_response
import qrcode
import io

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/create', methods=['POST'])  
def create_qr():  
    shiyou_busho, pc_mei, shiriaru_bangou, note =  request.form['shiyou_busho'], request.form['pc_mei'], request.form['shiriaru_bangou'], request.form['note']  
    
    qr = qrcode.QRCode(
        version=1,  # バージョン（サイズの制御）
        error_correction=qrcode.constants.ERROR_CORRECT_L,  # エラー訂正レベル
        box_size=10,  # 各ボックスのサイズ
        border=4,  # ボーダーのサイズ
    )
    
    qr.add_data('使用部署：' + shiyou_busho + '\n')
    qr.add_data('PC名：' + pc_mei + '\n')
    qr.add_data('シリアル番号：' + shiriaru_bangou + '\n')
    qr.add_data('ノート：' + note)
    qr.make(fit=True)
    img = qr.make_image(fill='black', back_color='white')
    # Save the QR code image to a buffer
    buffer = io.BytesIO()
    img.save(buffer, format='PNG')
    buffer.seek(0)
    
    # Create the response object
    response = make_response(buffer.getvalue())
    response.headers['Content-Disposition'] = 'attachment; filename=QRcode.png'
    response.mimetype = 'image/png'
    return response