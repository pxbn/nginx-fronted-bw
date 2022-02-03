#!/usr/bin/env python3
from string import ascii_letters, digits, punctuation
from random import choices
from subprocess import run, CalledProcessError
from datetime import datetime, timedelta
from os import remove, rmdir

today = str(datetime.now()).replace(" ", "T")[:-7]
backup_path = './sensetive/' + today + '/'


def main():
    # Stop server
    try: run(['systemctl', 'stop', 'nginx-bw-server.service'], check=True)
    except CalledProcessError as err: log_cleanup_error(err, "Couldn't stop server.")
    print("stopped server...")

    # Copy server files
    try: copy_server_files()
    except CalledProcessError as err: log_cleanup_error(err, "Couldn't copy files")
    print("copied files.")

    # Start server
    try: run(['systemctl', 'start', 'nginx-bw-server.service'], check=True)
    except CalledProcessError as err: log_cleanup_error(err, "Failed to start server again.")
    print("started server again.")

    # Archive the copied data
    try: run(['tar', '-czf', backup_path+'server-image.tar.gz', backup_path+'server-image/'], check=True)
    except CalledProcessError as err: log_cleanup_error(err, "Failed to archive the data. Cleaning up.")
    print("archived files")

    # Encrypt backup and key
    encrypt_backup()
    try: run(['openssl', 'rsautl', '-encrypt', '-pubin', '-inkey', 'secrets/config-dir-public-key.pem',
              '-in', backup_path+"key.txt", '-out', backup_path+"enc.key.txt"], check=True)
    except CalledProcessError as err: log_cleanup_error(err, "Couldn't encrypt passphrase.")
    print("encrypted everything")

    # Move to backups, delete older than 30 days and sync with gdrive
    try: move_files()
    except CalledProcessError as err: log_cleanup_error(err, "Couldn't move the backup to the backups folder.")
    print("moved files")
    delete_old()
    try: run(['rclone', 'sync', '--config', '/home/lukas/.config/rclone/rclone.conf', 'backups/', 'gdrive:/backups/'], check=True)
    except CalledProcessError as err:
        run(['rm', '-rf', './backups/'+today])
        log_cleanup_error(err, "Failed to synchronize with gdrive.")
    print("successfully synchronized with gdrive")

    # Cleanup
    print("cleaning up...")
    run(['rm', '-rf', './sensetive/'+today])
    exit(0)

def delete_old():
    old = str(datetime.now() - timedelta(days=1)).replace(" ", "T")[:-7]
    try:
        remove('./backups/'+old+'/enc.key.txt')
        remove('./backups/'+old+'/enc.server-image.tar.gz')
        rmdir('./backups/'+old)
        print("Deleted "+old)
    except OSError as err:
        print("Didn't find backup older than 30 days ("+old+"). Skipping...")



def move_files():
    gdrive_path = './backups/' + today + '/'
    run(['mkdir', gdrive_path])
    run(['mv', backup_path + 'enc.key.txt', gdrive_path], check=True)
    run(['mv', backup_path + 'enc.server-image.tar.gz', gdrive_path], check=True)


def encrypt_backup():
    """ Create passphrase file and encrypt the server image with it.
    """
    chars = ascii_letters + digits + punctuation
    with open(backup_path+"key.txt", "w") as file:
        file.write(''.join(choices(chars, k=32)))
        file.close()
    try:
        run(['openssl', 'enc', '-aes-256-cbc', '-pbkdf2', '-pass', 'file:'+backup_path+"key.txt",
             '-in', backup_path+'server-image.tar.gz', '-out', backup_path+'enc.server-image.tar.gz'], check=True)
    except CalledProcessError as err:
        log_cleanup_error(err, "Failed to encrypt the data.")


def copy_server_files():
    server_img_path = backup_path+'server-image/'
    run(['mkdir', '-p', server_img_path], check=True)
    run(['cp', '-r', '../data', server_img_path], check=True)
    run(['cp', '-r', '../secrets', server_img_path], check=True)
    run(['cp', '../docker-compose.yml', server_img_path], check=True)


def log_cleanup_error(err: CalledProcessError, additional_info=''):
    try: run(['rm', '-rf', backup_path], check=True)
    except CalledProcessError as err: print("!!!!! FAILED TO CLEANUP !!!!!")
    print("#######################")
    print(additional_info)
    print("#######################")
    print(err.stdout)
    print(err.stderr)
    raise


if __name__ == "__main__":
    main()

