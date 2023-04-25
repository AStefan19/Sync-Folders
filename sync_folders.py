import sys
import os
import shutil
import time

def sync_folders(source_folder, replica_folder, log_file):
    # Check if source folder exists
    if not os.path.exists(source_folder):
        print(f"Source folder {source_folder} does not exist")
        return

    # Check if replica folder exists
    if not os.path.exists(replica_folder):
        print(f"Replica folder {replica_folder} does not exist")
        return

    # Create log file
    with open(log_file, 'a') as f:
        f.write(f"Synchronization started at {time.ctime()}\n")

    # Sync folders
    for root, dirs, files in os.walk(source_folder):
        for file in files:
            source_file_path = os.path.join(root, file)
            replica_file_path = source_file_path.replace(source_folder, replica_folder)

            # Copy file to replica folder
            shutil.copy2(source_file_path, replica_file_path)

            # Log file operation
            with open(log_file, 'a') as f:
                f.write(f"Copied {source_file_path} to {replica_file_path}\n")
                print(f"Copied {source_file_path} to {replica_file_path}")

        for dir in dirs:
            source_dir_path = os.path.join(root, dir)
            replica_dir_path = source_dir_path.replace(source_folder, replica_folder)

            # Create directory in replica folder
            os.makedirs(replica_dir_path, exist_ok=True)

            # Log directory operation
            with open(log_file, 'a') as f:
                f.write(f"Created directory {replica_dir_path}\n")
                print(f"Created directory {replica_dir_path}")

    # Remove files and directories in replica folder that are not in source folder
    for root, dirs, files in os.walk(replica_folder):
        for file in files:
            replica_file_path = os.path.join(root, file)
            source_file_path = replica_file_path.replace(replica_folder, source_folder)

            if not os.path.exists(source_file_path):
                # Remove file from replica folder
                os.remove(replica_file_path)

                # Log file operation
                with open(log_file, 'a') as f:
                    f.write(f"Removed {replica_file_path}\n")
                    print(f"Removed {replica_file_path}")

        for dir in dirs:
            replica_dir_path = os.path.join(root, dir)
            source_dir_path = replica_dir_path.replace(replica_folder, source_folder)

            if not os.path.exists(source_dir_path):
                # Remove directory from replica folder
                shutil.rmtree(replica_dir_path)

                # Log directory operation
                with open(log_file, 'a') as f:
                    f.write(f"Removed directory {replica_dir_path}\n")
                    print(f"Removed directory {replica_dir_path}")

    # Log synchronization end time
    with open(log_file, 'a') as f:
        f.write(f"Synchronization ended at {time.ctime()}\n")

if __name__ == '__main__':
    # Get command line arguments
    source_folder = sys.argv[1]
    replica_folder = sys.argv[2]
    log_file = sys.argv[3]
    sync_interval = int(sys.argv[4])

    # Sync folders periodically
    while True:
        sync_folders(source_folder, replica_folder, log_file)
        time.sleep(sync_interval)
