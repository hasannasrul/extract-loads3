import paramiko

def get_sftp_file(ssh_host, ssh_user, ssh_password, remote_path):
    """
    Connects to SFTP and returns a file-like object for the remote file.
    """
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(ssh_host, username=ssh_user, password=ssh_password, look_for_keys=False)
    sftp = ssh.open_sftp()

    try:
        remote_file = sftp.open(remote_path, "rb")
        return remote_file, sftp, ssh
    except FileNotFoundError:
        sftp.close()
        ssh.close()
        raise FileNotFoundError(f"Remote file does not exist: {remote_path}")
