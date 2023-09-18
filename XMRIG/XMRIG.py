#!/usr/bin/env python3
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
import sys
import os
import subprocess
import socket

HS_path = os.getcwd()
compose_dir = os.path.join(HS_path, "install_module", "XMRIG")

print(HS_path)

if sys.version_info < (3, 0):
    print("This script requires Python 3 or higher!")
    sys.exit(1)


def main():
    try:
        # Update the config file with user wallet address, import ip and add port
        url = os.environ.get('URL') + ':3007'
        env_vars = os.environ.copy()
        env_vars['URL'] = url
        subprocess.run(["python3", "wallet_update.py"], cwd=compose_dir, env=env_vars, check=True)
        
        # Build the XMRig image
        subprocess.run(["docker", "build", "-t", "myxmrig", "-f", "Dockerfile", "."], cwd=compose_dir, check=True)

        # Run the XMRig container
        subprocess.run(["docker", "run", "-dit", "--restart", "always", "--net=host", "--privileged", "--name", "myxmrig", "myxmrig", "/app/xmrig/build/xmrig", "-p", "-pause-on-active=5"], check=True)

        # Copy the config file into the container
        subprocess.run(["docker", "cp", "config.json", "myxmrig:/app/xmrig/build/config.json"], cwd=compose_dir, check=True)
        
        # Write to static/xmrig_script.js
        file_path = f'{HS_path}/static/'
        subprocess.run(["cp", f"{compose_dir}/XMRIG_script.js", f"{file_path}/XMRIG_script.js"], check=True)

    except subprocess.CalledProcessError as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()

