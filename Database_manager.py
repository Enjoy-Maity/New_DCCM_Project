import os
import logging
import sqlite3
import pandas as pd
from pathlib import Path
from datetime import datetime
from abc import ABC, abstractmethod


class Abstract_database_manager(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def table_creater(self):
        pass

    @abstractmethod
    def database_table_checker(self):
        pass

    @abstractmethod
    def data_adder(self, vendor_list: list):
        pass

    @abstractmethod
    def data_remover(self):
        pass

    @abstractmethod
    def auto_database_remover(self):
        pass

    @abstractmethod
    def database_updater(self, vendor: str, task: str, status: str):
        pass

    @abstractmethod
    def data_fetcher(self):
        pass


class Database_manager(Abstract_database_manager):
    def __init__(self):
        # log_file = "C:\\Ericsson_Application_Logs\\CLI_Automation_Logs\\Main_Application.log"
        # logging.basicConfig(filename=log_file,
        #                      filemode="a",
        #                      format=f"[ {'%(asctime)s'} ]: <<{'%(levelname)s'}>>: ({'%(module)s'}): {'%(message)s'}",
        #                      datefmt='%d-%b-%Y %I:%M:%S %p',
        #                      encoding= "UTF-8",
        #                      level=logging.DEBUG)
        super().__init__()
        self.table_creater_status = None
        self.current_time = None
        self.current_hour = None
        self.status = None
        self.cursor = None
        self.table_list = None
        self.conn = None
        username = (os.popen('cmd.exe /C "echo %username%"').read()).strip()
        self.db_path = f"C:\\Users\\{username}\\AppData\\Local\\CLI_Automation\\Database\\CLI_Automation_Database.db"
        Path(os.path.dirname(self.db_path)).mkdir(exist_ok=True, parents=True)

        self.table_name = "vendor_task_status"
        self.auto_database_remover()

    def database_table_checker(self) -> bool:
        """ Checks for the existence of 'vendor_task_status' table and returns bool value accordingly.

        Returns:
            bool: _description_ : 'True' if table exists and 'False' if table doesn't exist
        """
        self.conn = sqlite3.connect(self.db_path)
        command = "SELECT name FROM sqlite_master WHERE type = 'table';"

        self.cursor = self.conn.cursor()
        self.table_list = self.cursor.execute(command).fetchall()

        logging.debug(f"Got the list of tables from \'{self.db_path}\' => \n\'[{'\n'.join(str(x) for x in self.table_list)}]\'")

        self.status = False
        if len(self.table_list) > 0:
            if isinstance(self.table_list[0], tuple):
                self.table_list = list(self.table_list[0])

            if self.table_name in self.table_list:
                self.status = True
                self.conn.close()
                logging.debug(f"Returning True as {self.table_name} found in CLI_Automation_Database.db")
                return self.status

        else:
            logging.debug(f"Returning False as {self.table_name} not found in CLI_Automation_Database.db")
            self.conn.close()
            return self.status

    def auto_database_remover(self):
        """Auto deletes the database after a fixed time period
        """
        logging.debug("Checking the time for the auto database remover")
        self.current_time = datetime.now()
        self.current_hour = int(self.current_time.strftime("%H"))

        if os.path.exists(self.db_path):
            _modification_time = datetime.fromtimestamp(os.path.getmtime(self.db_path))
            _modification_time_timedelta_var = self.current_time - _modification_time
            _modification_time_timedelta_var_hour = int(_modification_time_timedelta_var.days * 24
                                                        +
                                                        _modification_time_timedelta_var.seconds // 3600)

            if self.current_hour >= 12:
                if (int(_modification_time_timedelta_var.days) >= 1) or (_modification_time_timedelta_var_hour >= 20):
                    self.data_remover()
        else:
            self.table_creater()

    def table_creater(self):
        """Creates the table for Vendor.
        """
        self.table_creater_status = self.database_table_checker()

        if not self.table_creater_status:
            self.conn = sqlite3.connect(self.db_path)
            self.cursor = self.conn.cursor()
            command = f"CREATE TABLE {self.table_name} (Vendor TEXT,\
                                                        Template_Checks TEXT,\
                                                        Running_Config_Pre_Checks TEXT,\
                                                        CLI_Preparation TEXT,\
                                                        Running_Config_Post_Checks TEXT);"

            logging.debug(f"Creating the table {self.table_name}\n")
            self.cursor.execute(command)
            logging.debug(f"Created the table {self.table_name} \n")

            self.conn.commit()

            self.conn.close()

    def data_adder(self, vendor_list: list):
        """Creates the rows for the unique vendors of vendor_list

        Args:
            vendor_list (list): _description_ : contains the list of unique vendors mentioned in the selected host details
            :param vendor_list:
        """
        if self.database_table_checker():
            logging.debug("Creating Table as the table itself doesn't exist")
            self.table_creater()
        self.conn = sqlite3.connect(self.db_path)
        self.cursor = self.conn.cursor()

        logging.debug("We are creating empty vendor rows in the vendor database")
        i = 0

        command = f"INSERT INTO {self.table_name} (Vendor,Template_Checks,Running_Config_Pre_Checks,CLI_Preparation,Running_Config_Post_Checks) VALUES (?,'','','','');"
        while i < len(vendor_list):
            self.cursor.execute(command, (vendor_list[i],))
            i += 1

        self.conn.commit()

        logging.debug(f"Created the empty rows for the vendors => {', '.join(vendor_list)}")

        self.conn.close()

    def database_updater(self, vendor, task, status):
        """Updates the database for vendor with data for given task and status

        Args:
            vendor (str): _description_ : Vendor for which the task status should be updated
            task (str): _description_ : Task column for which the vendor data should be updated
            status (str): _description_ : Status which needs to be entered in the database
        """
        logging.debug(f"Database Before Updating =>\n{self.data_fetcher().to_markdown()}")

        logging.debug("Updating the vendor database")

        self.conn = sqlite3.connect(self.db_path)
        self.cursor = self.conn.cursor()

        logging.debug(f"Updating \'{self.table_name}\', by setting \'{task}\' status => \'{status}\' where Vendor => \'{vendor}\'")
        command = f"UPDATE {self.table_name} SET {task} = ? WHERE Vendor = ?;"

        self.cursor.execute(command, [status, vendor])
        self.conn.commit()

        logging.debug(f"Updated the vendor database for {vendor} for task => {task} with status => {status}")
        self.conn.close()

    def data_fetcher(self) -> pd.DataFrame:
        """ Fetches all the data and returns the dataframe of all the rows
        
        Returns
            result_dataframe (pd.DataFrame) : _description_ : Getting all the results from the database and retuning all the data in a dataframe
            
        """
        if self.database_table_checker():
            self.conn = sqlite3.connect(self.db_path)
            self.cursor = self.conn.cursor()

            command = f"SELECT * FROM {self.table_name}"

            result_data = self.cursor.execute(command).fetchall()

            logging.debug(f"Got all the data from the database = > \n [{'\n'.join(str(data) for data in result_data)}]\n")

            self.conn.close()

            result_dataframe = pd.DataFrame.from_records(data=result_data, columns=["Vendor", "Template_Checks", "Running_Config_Pre_Checks", "CLI_Preparation", "Running_Config_Post_Checks"])

            logging.debug(f"Created the dataframe from the database records =>\n {result_dataframe.to_markdown()}")

            return result_dataframe

        else:
            logging.debug(f"Table {self.table_name} not found!")
            self.table_creater()

            return pd.DataFrame(columns=["Vendor", "Template_Checks", "Running_Config_Pre_Checks", "CLI_Preparation", "Running_Config_Post_Checks"])

    def data_remover(self):
        """ Dropping the rows from the entire table
        """
        if len(self.data_fetcher()) > 0:
            command = f"DELETE FROM {self.table_name};"

            self.conn = sqlite3.connect(self.db_path)
            self.cursor = self.conn.cursor()

            self.cursor.execute(command)
            self.conn.commit()

            logging.debug(f"Deleted all the rows in the table {self.table_name}")

            self.conn.close()