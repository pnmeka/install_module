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
from flask import Flask, render_template
import requests

app = Flask(__name__)

@app.route('/')
def progress():
    def get_metrics():
        try:
            url = "http://my_monero_image:18081/json_rpc"
            headers = {"Content-Type": "application/json"}
            data = {
                "jsonrpc": "2.0",
                "id": "0",
                "method": "get_info"
            }
            response = requests.post(url, json=data, headers=headers)

            if response.status_code == 200:
                result = response.json().get("result", {})
                data = {
                    "height": result.get("height", 0),
                    "status": result.get("status", "Not Synced"),
                    "difficulty": result.get("difficulty", 0),
                    "hash_rate": int(result.get("wide_difficulty", 0), 16),
                    "transaction_count": result.get("tx_count", 0),
                    "transaction_pool_size": result.get("tx_pool_size", 0),
                    "block_time": result.get("target", 0),
                    "network_connections": result.get("rpc_connections_count", 0),
                    "mem_pool_size": result.get("alt_blocks_count", 0),
                    "network_difficulty": int(result.get("wide_cumulative_difficulty", 0), 16),
                    "fee_per_byte": result.get("cumulative_difficulty", 0),
                    "node_uptime": result.get("start_time", 0),
                    "target_height": result.get("target_height", 0),
                    "block_size": result.get("block_size_limit", 0),
                    "percent_synced": 100 * result.get("height", 0) / result.get("target_height", 1),
                    "days_to_sync": (result.get("target_height", 1) - result.get("height", 0)) * result.get("block_time", 0) / (3600 * 24),
                    "memory_size_gb": result.get("database_size", 0) / (1024**3)
                }
                return data
            else:
                return {}
        except requests.RequestException as e:
            return {}

    data = get_metrics()
    return render_template('progress.html', data=data)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)

