import os
import pickle
import pandas as pd


def read_host_details_pickle_file() -> pd.DataFrame | None:
    """
    This function reads the host details file and returns the data as a pandas dataframe.
    :return: host details as a pandas dataframe
    :rtype: pd.DataFrame
    """
    host_details_pickle_file_contents = None
    host_details_pickle_file_path = os.path.join(
        os.path.expanduser("~"),
        "AppData",
        "Local",
        "CLI_Automation",
        "Host_details_Pickle_file",
        "Host_details.pkl"
    )

    if os.path.exists(host_details_pickle_file_path):
        host_details_pickle_file_contents = pd.read_pickle(host_details_pickle_file_path)

    return host_details_pickle_file_contents


def host_details_parent_directory_accessor() -> str:
    """
    This function returns the parent directory of the host details file.
    :return: parent directory of the host details file
    :rtype: str
    """
    host_details_parent_directory = ""
    host_details_parent_directory_path = os.path.join(
        os.path.expanduser("~"),
        "AppData",
        "Local",
        "CLI_Automation",
        "host_details_file_path.txt"
    )

    if os.path.exists(host_details_parent_directory_path):
        with open(host_details_parent_directory_path, "r") as f:
            host_details_parent_directory = os.path.dirname(f.readline().strip())
            f.close()
            del f

    return host_details_parent_directory


def pre_config_backup_file_lines_accessor(ip_node: str) -> list[str]:
    """
    This function reads the backup file and returns the lines as a list.
    :return: backup file lines as a list
    :rtype: list[str]
    """
    backup_file_lines = []
    host_details_content = read_host_details_pickle_file()
    if host_details_content is not None:
        pre_config_backup_folder_path = os.path.join(
            host_details_parent_directory_accessor(),
            "Pre_Running_Config_Backup"
        )
        dict_of_ip_to_hostname = dict(
            zip(host_details_content["Host_IP"],
                host_details_content["Host_Name"])
        )

        if ip_node in dict_of_ip_to_hostname.keys():
            hostname = dict_of_ip_to_hostname[ip_node]
            backup_files = os.listdir(pre_config_backup_folder_path)
            for backup_file in backup_files:
                if hostname in backup_file:
                    with open(os.path.join(pre_config_backup_folder_path, backup_file), "r") as f:
                        backup_file_lines = f.readlines()
                        f.close()
                        del f
                    break

    return backup_file_lines


def post_config_backup_file_lines_accessor(ip_node: str) -> list[str]:
    """
    This function reads the backup file and returns the lines as a list.
    :return: backup file lines as a list
    :rtype: list[str]
    """
    backup_file_lines = []
    host_details_content = read_host_details_pickle_file()
    if host_details_content is not None:
        post_config_backup_folder_path = os.path.join(
            host_details_parent_directory_accessor(),
            "Post_Running_Config_Backup"
        )
        dict_of_ip_to_hostname = dict(
            zip(host_details_content["Host_IP"],
                host_details_content["Host_Name"])
        )

        if ip_node in dict_of_ip_to_hostname.keys():
            hostname = dict_of_ip_to_hostname[ip_node]
            backup_files = os.listdir(post_config_backup_folder_path)
            for backup_file in backup_files:
                if hostname in backup_file:
                    with open(os.path.join(post_config_backup_folder_path, backup_file), "r") as f:
                        backup_file_lines = f.readlines()
                        f.close()
                        del f
                    break

    return backup_file_lines