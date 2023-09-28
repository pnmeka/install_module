#setup and run the xmr.py file that sets up running containers
import os
import subprocess
import shutil

# Set the path to the directory containing docker-compose.yml
HS_path = os.getcwd()
compose_dir = os.path.join(os.getcwd(), "install_module", "XMR")
file_path = f'{HS_path}/static'

# Build the source and destination file paths
source_file_path = os.path.join(compose_dir, "XMR_script.js")
destination_file_path = os.path.join(HS_path, "static", "XMR_script.js")


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
       shutil.copy(source_file_path, destination_file_path)
       print(f"File copied to {destination_file_path}")
    
    except subprocess.CalledProcessError as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()

