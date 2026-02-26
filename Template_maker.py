import logging
import pickle
import os
from pathlib import Path
import pandas as pd
import numpy as np
import traceback
from tkinter import messagebox
from Custom_Exception import CustomException
from datetime import datetime
from CustomThread import CustomThread
from Section_splitter import section_splitter

flag = ''
selected_vendor_book_excel_file = None
node_to_section_dictionary = None


def error_message_filter(dictionary: dict) -> dict:
    """
    Filters the dictionary for removing empty dict or None values.
    :param dictionary: dictionary containing the error message dictionary
    :return: result_dictionary (dict): dictionary containing the cleaned dictionary for result dictionary
    """
    result_dictionary = {}
    # here the structure is
    # {
    #       node: {
    #               section: []
    #           }
    #      }

    if (dictionary is not None) and (isinstance(dictionary, dict)):
        if len(dictionary) > 0:
            nodes_list = list(dictionary.keys())
            i = 0
            while i < len(nodes_list):
                node = nodes_list[i]
                if (dictionary[node] is not None) and (isinstance(dictionary[node], dict)):
                    if len(dictionary[node]) > 0:
                        sections_list = list(dictionary[node].keys())
                        j = 0
                        while j < len(sections_list):
                            section = sections_list[j]
                            if (dictionary[node][section] is not None) and (isinstance(dictionary[node][section], dict)):
                                if len(dictionary[node][section]) > 0:
                                    reasons = list(dictionary[node][section].keys())
                                    if len(reasons) > 0:
                                        k = 0
                                        while k < len(reasons):
                                            reason = reasons[k]
                                            if (dictionary[node][section][reason] is not None) and (isinstance(dictionary[node][section][reason], (list, tuple))):
                                                if node not in result_dictionary:
                                                    result_dictionary[node] = {}
                                                    if section not in result_dictionary[node]:
                                                        result_dictionary[node][section] = {}
                                                        result_dictionary[node][section][reason] = dictionary[node][section][reason]
                                                    else:
                                                        result_dictionary[node][section][reason] = dictionary[node][section][reason]

                                                else:
                                                    if section not in result_dictionary[node]:
                                                        result_dictionary[node][section] = {}
                                                        result_dictionary[node][section][reason] = dictionary[node][section][reason]
                                                    else:
                                                        result_dictionary[node][section][reason] = dictionary[node][section][reason]

                                            k += 1
                            j += 1
                i += 1

    logging.info(
        "Got the cleaned result_dictionary ==> {\n" +
        f"{'\n\t'.join([f'{node}: {
            '\n\t\t'.join([f'{reason}: {reason_list}' for reason, reason_list in value.items()])}' for node, value in result_dictionary.items()])}" +
        "}"
    )
    return result_dictionary


def pickling_func(dictionary: dict, vendor_selected: str) -> None:
    username = os.popen(r'cmd.exe /C "echo %username%"').read()
    path_for_pickle_files = f"C:\\Users\\{username.strip()}\\AppData\\Local\\CLI_Automation\\Vendor_pickles\\{vendor_selected.upper()}.pickle"
    parent_dir = os.path.dirname(path_for_pickle_files)

    logging.debug("Creating the folder for the Application in Appdata if not exists")
    Path(parent_dir).mkdir(parents=True, exist_ok=True)

    with open(path_for_pickle_files, 'wb') as f:
        pickle.dump(dictionary, f)
        f.close()

    logging.debug("Checking the pickle file thus created")
    with open(path_for_pickle_files, 'rb') as f:
        logging.debug(f"Pickle file =====>\n\t{pickle.load(f)}")
        f.close()

    del f


def action_blank_check(*args) -> dict[str, list | None]:
    try:
        assert isinstance(args[0], pd.DataFrame)
        dataframe = args[0]
        result = dict()

        # dataframe.fillna("TempNA", inplace = True)
        # Alternative for dataframe.fillna("TempNA", inplace = True)
        dataframe = dataframe.where(~dataframe.isna(), "TempNA")

        i = 0
        reason = "Blank \'Action\' input found in Design Template"
        while i < len(dataframe):
            if dataframe.iloc[i, dataframe.columns.get_loc('Action')] == "TempNA":
                if reason not in result:
                    result[reason] = []
                    result[reason].append(str(int(float(str(dataframe.iloc[i, dataframe.columns.get_loc('S.No.')]).strip()))))
                else:
                    result[reason].append(str(int(float(str(dataframe.iloc[i, dataframe.columns.get_loc('S.No.')]).strip()))))
            i += 1

        return result

    except AssertionError as e:
        logging.debug(f"Assertion Error====>\n{traceback.format_exc()}\n{e}")
        messagebox.showerror('Wrong Data Type!', str(e))


def serial_list_checks(*args) -> dict[str, list | None]:
    try:
        assert isinstance(args[0], pd.DataFrame)
        dataframe = args[0]
        dataframe = dataframe.where(~dataframe.isna(), "TempNA")
        result = dict()

        reason = "Blank \'S.No.\' found in Design Template"
        i = 0
        while i < len(dataframe):
            if dataframe.iloc[i, dataframe.columns.get_loc('S.No.')] == "TempNA":
                if reason not in result:
                    result[reason] = []
                    result[reason].append(str(dataframe.iloc[i, dataframe.columns.get_loc('S.No.')]))
                else:
                    result[reason].append(str(dataframe.iloc[i, dataframe.columns.get_loc('S.No.')]))
            i += 1

        reason = "Duplicate \'S.No.\' found in Design Template"
        temp_df = dataframe.loc[(dataframe.duplicated(subset=['S.No.'], keep=False))]

        temp_df = temp_df.loc[temp_df["S.No."] != "TempNA"]

        if temp_df.shape[0] > 0:
            result[reason] = temp_df["S.No."].astype(float).astype(int).to_list()

        return result

    except AssertionError as e:
        logging.debug(f"Assertion Error====>\n{traceback.format_exc()}\n{e}")
        messagebox.showerror('Wrong Data Type!', str(e))


def main_func(**kwargs) -> str:
    """
        Performs the Initial General Template checks and then calls the module specific to the vendor to perform further Template checks.

        Arguments: (**kwargs) ===> provides a dictionary of arguments.
            kwargs ===> 'filename' : str
                            description =====> file name required to get the parent directory

                        'vendor_selected' : str
                            description =====> selected vendor by the user in GUI
        
        return flag
            flag: str
                description ===> contains 'Unsuccessful' or 'Successful' string corresponding to the status of execution completion
    """

    log_file_path = "C:/Ericsson_Application_Logs/CLI_Automation_Logs/"
    Path(log_file_path).mkdir(parents=True, exist_ok=True)

    log_file = os.path.join(log_file_path, "Template_checks.log")

    today = datetime.now()
    today = today.replace(hour=0, minute=0, second=0)

    filename = kwargs['filename']

    username = (os.popen('cmd.exe /C "echo %username%"').read()).strip()
    pickle_path = rf"C:\Users\{username}\AppData\Local\CLI_Automation\Host_details_Pickle_file\Host_details.pkl"
    file_name = pd.read_pickle(filepath_or_buffer=pickle_path)
    logging.info("#######################################################<<Starting the Root Template Checks Process>>########################################################################")

    global flag, selected_vendor_book_excel_file, node_to_section_dictionary
    try:
        logging.debug("Checking whether the file uploaded by the user is an excel file or not")
        # assert ((len(file_name) > 0) and (file_name.strip().endswith('.xlsx'))), 'Please Select the Host details Excel Workbook!'

        parent_folder = os.path.dirname(filename)
        input_design_file_name = "{}_Design_Input_Sheet.xlsx"

        logging.info("Reading the file selected by the user")
        # host_details_excelfile = pd.ExcelFile(file_name)
        # host_details_sheet     = pd.read_excel(host_details_excelfile,
        #                                        sheet_name='Host Details',
        #                                        engine='openpyxl')

        host_details_sheet = file_name

        logging.info(f"Read the Host Details ====>\n{host_details_sheet}")

        logging.info("Checking out the unique vendors mentioned in the Host Details")
        unique_vendors_mentioned = host_details_sheet['Vendor'].dropna().unique()

        logging.debug(f"Entering the loop for checking specific vendors Design Input workbooks mentioned:\n {'\n'.join(unique_vendors_mentioned)}")
        i = 0
        while i < unique_vendors_mentioned.size:
            if not Path(os.path.join(os.path.join(parent_folder, 'Design_Input_Sheets'), input_design_file_name.format(unique_vendors_mentioned[i]))).exists():
                # host_details_excelfile.close()
                # del host_details_excelfile
                raise CustomException("Design Input File Missing!",
                                      f"{input_design_file_name.format(unique_vendors_mentioned[i])} not found in {parent_folder}, Kindly Check!")
            i += 1

        vendor_selected = kwargs['vendor_selected']
        logging.debug(f"Looping through selected vendor {vendor_selected} design input workbook sheet-names")

        selected_vendor_book_excel_file = pd.ExcelFile(os.path.join(os.path.join(parent_folder, "Design_Input_Sheets"),
                                                                    input_design_file_name.format(vendor_selected.strip())))
        selected_vendor_book_excel_sheetnames = selected_vendor_book_excel_file.sheet_names

        logging.debug(f"Sheets Found in the {input_design_file_name.format(vendor_selected)} are :\n\t{'\n\t'.join(selected_vendor_book_excel_sheetnames)}")

        logging.debug(f"Filtering the Host Details for selected vendor = {vendor_selected}")
        host_details_sheet = host_details_sheet[host_details_sheet['Vendor'].str.strip().str.upper() == vendor_selected.strip().upper()]

        logging.debug("Getting the list of unique node ips present in the host details")
        unique_host_ips_present_in_the_host_details_sheet = host_details_sheet['Host_IP'].dropna().unique()
        logging.debug(f"{unique_host_ips_present_in_the_host_details_sheet = }")

        logging.info("Creating a list for the getting the host details not present in the host details sheet inside in vendor workbook.")
        host_details_not_present_in_the_workbook = []
        host_details_present_in_workbook_but_not_in_host_details = []

        i = 0
        while i < len(selected_vendor_book_excel_sheetnames):
            if selected_vendor_book_excel_sheetnames[i] not in unique_host_ips_present_in_the_host_details_sheet:
                host_details_present_in_workbook_but_not_in_host_details.append(selected_vendor_book_excel_sheetnames[i])
            i += 1

        i = 0
        while i < unique_host_ips_present_in_the_host_details_sheet.size:
            if unique_host_ips_present_in_the_host_details_sheet[i] not in selected_vendor_book_excel_sheetnames:
                host_details_not_present_in_the_workbook.append(unique_host_ips_present_in_the_host_details_sheet[i])
            i += 1

        response = None

        if ((len(host_details_not_present_in_the_workbook) > 0) and
                (len(host_details_present_in_workbook_but_not_in_host_details) > 0)):
            response = messagebox.askyesno(title="Wrong Data Input!",
                                           message=f"Host Details not found in {input_design_file_name.format(vendor_selected)} workbook:\n\n{', '.join(host_details_not_present_in_the_workbook)}\n\nand\n\n extra Host IP details found :\n\n{', '.join(host_details_present_in_workbook_but_not_in_host_details)}\n\nDo You want to proceed?",
                                           icon='warning')

        else:
            if len(host_details_not_present_in_the_workbook) > 0:
                response = messagebox.askyesno(title="Host Details Missing!",
                                               message=f"Host Details IPs Missing in {input_design_file_name.format(vendor_selected)}:\n\n{', '.join(host_details_not_present_in_the_workbook)}\n\nDo You want to proceed?",
                                               icon='warning')

            if len(host_details_present_in_workbook_but_not_in_host_details) > 0:
                response = messagebox.askyesno(title="Extra Host Details Found!",
                                               message=f"Extra Host IP details found in {input_design_file_name.format(vendor_selected)} but not present in uploaded Host Details:\n\n{', '.join(host_details_not_present_in_the_workbook)}\n\nDo You want to proceed?",
                                               icon='warning')

        if (response is not None) and (not response):
            # selected_vendor_book_excel_file.close()
            # del selected_vendor_book_excel_file
            # host_details_excelfile.close()
            # del selected_vendor_book_excel_file

            raise CustomException("User Selected 'No'!", "The User Have Selected 'No', so stopping the execution!")

        logging.info("Now calling the section splitter in a try except block.")

        try:
            logging.info("Creating a thread list")
            thread_list = []
            i = 0
            while i < len(selected_vendor_book_excel_sheetnames):
                df = pd.read_excel(selected_vendor_book_excel_file,
                                   selected_vendor_book_excel_sheetnames[i],
                                   engine='openpyxl')
                temp_thread = CustomThread(target=section_splitter, args=(df, 'Template_checks', selected_vendor_book_excel_sheetnames[i]))
                temp_thread.daemon = True
                thread_list.append(temp_thread)
                temp_thread.start()
                i += 1

            selected_vendor_book_excel_file.close()
            del selected_vendor_book_excel_file

            node_to_section_dictionary = {}
            logging.debug("Ending all the threads and getting their return Values")
            i = 0
            while i < len(selected_vendor_book_excel_sheetnames):
                node_to_section_dictionary[selected_vendor_book_excel_sheetnames[i]] = thread_list[i].join()
                i += 1

        except CustomException as e:
            # global flag;
            flag = 'Unsuccessful'
            logging.error(f"{traceback.format_exc()}\n\nraised CustomException==>\ntitle = {e.title}\nmessage = {e.message}")

        except Exception as e:
            flag = 'Unsuccessful'
            logging.error(f"{traceback.format_exc()}\n\nException:==>{e}")
            messagebox.showerror("Exception Occurred!", str(e))

        logging.info("Checking whether there is any worksheet, which contains no data for any of the sections")

        i = 0
        list_of_sheet_with_empty_section_data = []
        list_of_sheets_with_no_section_data = []
        keys_pertaining_nodes = list(node_to_section_dictionary.keys())
        while i < len(keys_pertaining_nodes):
            selected_node = keys_pertaining_nodes[i]

            if node_to_section_dictionary[selected_node] is None:
                list_of_sheets_with_no_section_data.append(selected_node)
            if len(node_to_section_dictionary[selected_node]) == 0:
                list_of_sheet_with_empty_section_data.append(selected_node)
            i += 1

        logging.debug("Raising exception if any sheet without any section data found!")

        if len(list_of_sheet_with_empty_section_data) > 0:
            raise CustomException("Empty Worksheet Found!",
                                  f"Worksheet with No Section data found, Kindly Check {input_design_file_name.format(vendor_selected)} for the below mentioned nodes:\n\n\t{'\n\t'.join(list_of_sheet_with_empty_section_data)}\n\nKindly Ckeck!")

        if len(list_of_sheets_with_no_section_data) > 0:
            raise CustomException("Worksheet with No Section Data Found!",
                                  f"Worksheet with No Section data found for the below mentioned nodes:\n\n\t{'\n\t'.join(list_of_sheets_with_no_section_data)}\n\nKindly Ckeck!")

        logging.debug("Checking if any section of any node ip sheet has blank value in the 'Action' column.")
        try:
            i = 0
            thread_list = []
            neo_thread_list = []
            while i < len(keys_pertaining_nodes):
                selected_node = keys_pertaining_nodes[i]
                sections = list(node_to_section_dictionary[selected_node].keys())

                j = 0
                while j < len(sections):
                    selected_section = sections[j]
                    dataframe = node_to_section_dictionary[selected_node][selected_section]
                    temp_thread = CustomThread(target=action_blank_check,
                                               args=(dataframe,))
                    temp_thread.daemon = True
                    thread_list.append(temp_thread)
                    temp_thread.start()

                    neo_temp_thread = CustomThread(target=serial_list_checks,
                                                   args=(dataframe,))
                    neo_temp_thread.daemon = True
                    neo_thread_list.append(neo_temp_thread)
                    neo_temp_thread.start()
                    j += 1
                i += 1

            thread_return_list = []
            neo_thread_return_list = []
            thread_list_len = len(thread_list)
            neo_thread_list_len = len(neo_thread_list)
            k = 0  # Incrementer for the thread_list

            dictionary_for_message = {}

            logging.debug("Getting all the return values from the section thread list for checking blank 'Action' value.")
            i = 0
            while i < thread_list_len:
                thread_return_list.append(thread_list[i].join())
                i += 1

            i = 0
            while i < neo_thread_list_len:
                neo_thread_return_list.append(neo_thread_list[i].join())
                i += 1

            logging.debug(f"Got the thread_return_list :-\n{thread_return_list}")

            logging.debug(f"Got the neo_thread_return_list :-\n{neo_thread_return_list}")

            i = 0
            while i < len(keys_pertaining_nodes):
                selected_node = keys_pertaining_nodes[i]
                sections = list(node_to_section_dictionary[selected_node].keys())

                section_dictionary_for_message = {}
                j = 0
                while j < len(sections):
                    selected_section = sections[j]
                    section_dictionary_for_message[selected_section] = dict()
                    try:
                        if len(thread_return_list[k]) != 0:
                            section_dictionary_for_message[selected_section].update(thread_return_list[k])

                        if len(neo_thread_return_list[k]) != 0:
                            section_dictionary_for_message[selected_section].update(neo_thread_return_list[k])
                    except Exception:
                        if thread_return_list[k] is not None:
                            section_dictionary_for_message[selected_section].update(thread_return_list[k])

                        if neo_thread_return_list[k] is not None:
                            section_dictionary_for_message[selected_section].update(neo_thread_return_list[k])
                    k += 1
                    j += 1

                if len(section_dictionary_for_message) != 0:
                    dictionary_for_message[selected_node] = section_dictionary_for_message

                i += 1

            dictionary_for_message = error_message_filter(dictionary=dictionary_for_message)

            error_folder = os.path.join(os.path.join(parent_folder, "Error_Folder"), "Design_Input_Checks_Results")
            logging.info(f"Created '{error_folder}' if not existed, if existed did not raised an exception")

            logging.debug("Creating the path for the folder for getting errors")
            Path(error_folder).mkdir(parents=True, exist_ok=True)

            logging.info("Creating the Error File path for writing into the exceptions")
            error_file = os.path.join(error_folder, f"{vendor_selected.strip()}_Nodes_Design_Input_Checks_Error.txt")

            message_to_be_written = ''

            if len(dictionary_for_message) > 0:
                dictionary_for_message_keys_list = list(dictionary_for_message.keys())

                if len(dictionary_for_message_keys_list) > 0:
                    message_to_be_written = f"General Check Issues:\n\nIssues have been found for below '{vendor_selected}' nodes for mentioned Sr.Nos on {datetime.now().strftime('%d-%b-%Y %I:%M %p')} ({datetime.now().strftime('%A')})\n\n"
                    i = 0
                    while i < len(dictionary_for_message_keys_list):
                        node_selected = dictionary_for_message_keys_list[i]
                        sections_in_dictionary_for_message = list(dictionary_for_message[node_selected].keys())

                        message_to_be_written = f"{message_to_be_written}Node:- '{node_selected}'\n\n"
                        j = 0
                        while j < len(sections_in_dictionary_for_message):
                            section_selected = sections_in_dictionary_for_message[j]
                            message_to_be_written = f"{message_to_be_written}\tSection: '{section_selected}':-\n"

                            reasons = list(dictionary_for_message[node_selected][section_selected].keys())
                            k = 0
                            while k < len(reasons):
                                message_to_be_written = f"{message_to_be_written}\t\t\t{k + 1}) {reasons[k]}: ({', '.join(str(element) for element in dictionary_for_message[node_selected][section_selected][reasons[k]])})\n"
                                k += 1
                            j += 1
                            message_to_be_written = f"{message_to_be_written}\n"

                        message_to_be_written = f"{message_to_be_written}\n\n"
                        i += 1

                with open(error_file, 'w', encoding='UTF-8') as f:
                    f.write(message_to_be_written)
                    f.close()

                raise CustomException("Input Issue!",
                                      ("Issues have been observed in uploaded input sheet. To find the issue in detail, " +
                                       "Please! check the 'Template_Checks_error_Vendor_wise' inside 'Error_Folder'"))

            # with open(error_file, 'w') as f:
            #     f.write('')
            #     f.close()

        except CustomException as e:
            # global flag;
            flag = 'Unsuccessful'
            logging.error(f"{traceback.format_exc()}\n\nraised CustomException==>\ntitle = {e.title}\nmessage = {e.message}")

            if e.title == 'Input Issue!':
                os.popen(cmd= f'notepad.exe {error_file}')
            # messagebox.showerror(title=e.title,
            #                      message=e.message)

        except Exception as e:
            flag = 'Unsuccessful'
            logging.error(f"{traceback.format_exc()}\n\nException:==>{e}")
            messagebox.showerror("Exception Occurred!", str(e))

        else:
            # logging.info(f"Deleting host_details_excelfile")
            # host_details_excelfile.close()
            # del host_details_excelfile

            logging.debug("Calling the Pickling Function to create pickles")
            pickling_func(dictionary=node_to_section_dictionary,
                          vendor_selected=vendor_selected)

            if vendor_selected.upper() == 'NOKIA':
                logging.info("Going to perform template checks on 'Nokia' Design Template")
                from Nokia.Nokia_Template_Checks import nokia_main_func
                flag = nokia_main_func(log_file=log_file,
                                       parent_folder=parent_folder)

            if vendor_selected.upper() == 'CISCO':
                logging.info("Going to perform template checks on 'Cisco' Design Template")
                from Cisco.Cisco_Template_Checks import cisco_main_func
                flag = cisco_main_func(log_file=log_file,
                                       parent_folder=parent_folder)

            if vendor_selected.upper() == 'HUAWEI':
                logging.info("Going to perform template checks on 'Huawei' Design Template")

            if vendor_selected.upper() == 'ERICSSON':
                logging.info("Going to perform template checks on 'Ericsson' Design Template")

        if flag == '':
            flag = 'Unsuccessful'

        if flag != 'Unsuccessful':
            flag = 'Successful'

    except CustomException as e:
        # global flag;
        flag = 'Unsuccessful'
        logging.error(f"{traceback.format_exc()}\n\nraised CustomException==>\n" +
                      f"title = {e.title}\nmessage = {e.message}")

    except AssertionError as e:
        flag = 'Unsuccessful'
        logging.error(f"{traceback.format_exc()}\n\nraised AssertionError==>\n" +
                      f"title = {type(e)}\nmessage = {str(e)}")
        messagebox.showerror("Wrong Input File", str(e))

    except Exception as e:
        flag = 'Unsuccessful'
        logging.error(f"{traceback.format_exc()}\n\nException:==>{e}")
        messagebox.showerror("Exception Occurred!", str(e))

    finally:
        import gc
        logging.info("Closing the Design input sheet workbook")

        logging.info(f"Returning {flag =}")
        logging.shutdown()

        gc.collect()
        return flag

# main_func(vendor_selected = 'Nokia')