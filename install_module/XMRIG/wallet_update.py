#/* DARNA.HI
# * Copyright (c) 2023 Seapoe1809   <https://github.com/seapoe1809>
# * Copyright (c) 2023 pnmeka   <https://github.com/pnmeka>
# * 
# *
# *   This program is free software: you can redistribute it and/or modify
# *   it under the terms of the GNU General Public License as published by
# *   the Free Software Foundation, either version 3 of the License, or
# *   (at your option) any later version.
# *
# *   This program is distributed in the hope that it will be useful,
# *   but WITHOUT ANY WARRANTY; without even the implied warranty of
# *   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# *   GNU General Public License for more details.
# *
# *   You should have received a copy of the GNU General Public License
# *   along with this program. If not, see <http://www.gnu.org/licenses/>.
from flask import Flask, request, render_template
from werkzeug.serving import make_server, WSGIRequestHandler
import os
import json
import threading
import webbrowser



app = Flask(__name__)

class SilentHandler(WSGIRequestHandler):
    def log_request(self, *args, **kwargs):
        pass

server = make_server('0.0.0.0', 3007, app, request_handler=SilentHandler)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        wallet_address = request.form.get('wallet_address')

        # Read the existing config
        with open('config.json', 'r') as f:
            config = json.load(f)
        
        # Update the wallet address in the format config.pools[0].user
        config["pools"][0]["user"] = wallet_address

        # Save the updated config
        with open('config.json', 'w') as f:
            json.dump(config, f, indent=4)

        # Stop the server
        threading.Thread(target=server.shutdown).start()

        return f"Wallet address updated to: {wallet_address}"

    return render_template('index.html')

if __name__ == '__main__':
    print("Starting server at http://0.0.0.0:3007/")
    webbrowser.open('http://localhost:3007')
    server.serve_forever()

