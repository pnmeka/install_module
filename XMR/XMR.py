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
#setup and run the xmr.py file that sets up running containers
import os
import subprocess

# Set the path to the directory containing docker-compose.yml
HS_path = os.getcwd()
compose_dir = os.path.join(os.getcwd(), "install_module", "XMR")

def main():
    try:

       # Create network
       subprocess.run(["docker", "network", "create", "mynetwork"])

       # Build the Flask image
       subprocess.run(["docker", "build", "-t", "flask_xmr", "-f", "Dockerfile", "."], cwd=compose_dir)

       # Run the Flask container
       subprocess.run(["docker", "run", "-dit", "--name", "flask_xmrnode", "--network=mynetwork", "-p", "5000:5000", "flask_xmr"])

       # Build the Monero image
       subprocess.run(["docker", "build", "-t", "my_monero_image", "-f", "Dockerfile-monerod", "."], cwd=compose_dir)

       # Run the Monero container
       subprocess.run(["docker", "run", "-dit", "--name", "my_monero_image", "--network=mynetwork", "-p", "18081:18081", "-v", f"{HS_path}:/home/monero/.bitmonero", "my_monero_image"])
    
       #write to static/XMR_script.js
       file_path = f'{HS_path}/static'
       command3 = f"cp {current_dir}/XMR_script.js {file_path}/XMR_script.js"
       subprocess.run(command3)
    
    except subprocess.CalledProcessError as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()

