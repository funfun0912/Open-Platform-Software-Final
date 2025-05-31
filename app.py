import requests
from flask import Flask, request, jsonify
from flask_cors import CORS
app = Flask(__name__)
CORS(app)
client_id = 's1111528-a3f10b32-ab51-4ae5'
client_secret = '0e8e4133-2717-40fc-bb13-bf2f59400d6f'

def get_access_token():
    token_url = "https://tdx.transportdata.tw/auth/realms/TDXConnect/protocol/openid-connect/token"
    token_data = {
        'grant_type': 'client_credentials',
        'client_id': client_id,
        'client_secret': client_secret
    }
    token_headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    token_response = requests.post(token_url, data=token_data, headers=token_headers)
    return token_response.json().get('access_token')

@app.route('/liveboard', methods=['GET'])
def liveboard():
    station_code = request.args.get('station_code', default='0900')
    access_token = get_access_token()
    if access_token:
        api_url = f"https://tdx.transportdata.tw/api/basic/v3/Rail/TRA/StationLiveBoard/Station/{station_code}"
        params = {
            "$top": 30,
            "$format": "JSON"
        }
        headers = {
            'Authorization': f'Bearer {access_token}'
        }
        response = requests.get(api_url, params=params, headers=headers)
        if response.status_code == 200:
            return jsonify(response.json())
        else:
            return jsonify({"error": f"API 請求失敗，狀態碼: {response.status_code}"}), 500
    else:
        return jsonify({"error": "取得 access_token 失敗"}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5001)
