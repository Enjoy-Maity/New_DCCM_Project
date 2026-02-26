import sys
import logging
from tkinter import messagebox
from abc import ABC, abstractmethod
import re
from typing import List, Any
from pprint import pprint


class Abstract_class_file_lines_handler(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def file_lines_cleaner(self):
        pass

    @abstractmethod
    def file_lines_starter_filter(self):
        pass

    @abstractmethod
    def file_lines_contains_filter(self):
        pass

    @abstractmethod
    def file_lines_pattern_filter(self):
        pass

    @abstractmethod
    def file_lines_chunk_divisor(self):
        pass

    @abstractmethod
    def file_lines_chunk_divisor_pattern(self):
        pass


class File_lines_handler(Abstract_class_file_lines_handler):
    def __init__(self):
        super().__init__()

    def file_lines_left_side_cleaner(self, file_lines_list: list):
        """
            Strips the left side of each line of any character sequence and returns the clean list of lines

            Arguments : (file_lines_list)
                file_lines_list ===> list
                    description =====> contains the list of non-cleaned lines

            return cleaned_file_list
                cleaned_file_list ===> list
                    description =====> list of file lines without any escape sequences in file lines
        """
        try:
            # logging.info(f"Got the file_lines_list => {file_lines_list}")
            if isinstance(file_lines_list, list):
                cleaned_file_list = [line.lstrip() for line in file_lines_list if (len(line.lstrip()) > 0)]

                return cleaned_file_list

        except TypeError as e:
            logging.error(f"Exception Occurred!!\n\tTitle => {'TypeError'}\n\t\tMessage ==> {str(e)}")
            messagebox.showerror(title='TypeError',
                                 message=str(e))


    def file_lines_right_side_cleaner(self, file_lines_list: list):
        """
            Strips the right side of each line of any character sequence and returns the clean list of lines

            Arguments : (file_lines_list)
                file_lines_list ===> list
                    description =====> contains the list of non-cleaned lines

            return cleaned_file_list
                cleaned_file_list ===> list
                    description =====> list of file lines without any escape sequences in file lines
        """
        try:
            # logging.info(f"Got the file_lines_list => {file_lines_list}")
            if isinstance(file_lines_list, list):
                cleaned_file_list = [line.rstrip() for line in file_lines_list if (len(line.rstrip()) > 0)]

                return cleaned_file_list

        except TypeError as e:
            logging.error(f"Exception Occurred!!\n\tTitle => {'TypeError'}\n\t\tMessage ==> {str(e)}")
            messagebox.showerror(title='TypeError',
                                 message=str(e))

    def file_lines_cleaner(self, file_lines_list: list) -> list:
        """
            Strips the lines of any character sequence and returns the clean list of lines

            Arguments : (file_lines_list)
                file_lines_list ===> list
                    description =====> contains the list of non-cleaned lines

            return cleaned_file_list
                cleaned_file_list ===> list
                    description =====> list of file lines without any escape sequences in file lines
        """
        try:
            # logging.info(f"Got the file_lines_list => {file_lines_list}")
            if isinstance(file_lines_list, list):
                cleaned_file_list = [line.strip() for line in file_lines_list if (len(line.strip()) > 0)]

                return cleaned_file_list

        except TypeError as e:
            logging.error(f"Exception Occurred!!\n\tTitle => {'TypeError'}\n\t\tMessage ==> {str(e)}")
            messagebox.showerror(title='TypeError',
                                 message=str(e))

    def file_lines_starter_filter(self, file_lines_list: list, start_word: str) -> list:
        """
            Filters the lines from the given list of file lines starting from the given start word

            Arguments : (file_lines_list, start_word)
                file_lines_list ===> list
                    description =====> contains the list of lines from the file.

                start_word ===> str
                    description =====> contains the word for which we need to filter the list with lines starting from the given start_word

            return filtered_lines_list
                filtered_lines_list ===> list
                    description =====> contains the list of lines starting with the given start word
        """
        try:
            if isinstance(file_lines_list, list):
                start_word = start_word.strip()
                logging.info(f"Got the start_word => {start_word}")
                # compiled_pattern = re.compile(rf"^{start_word}[\s,\w]*$")
                file_lines_list = self.file_lines_cleaner(file_lines_list=file_lines_list)
                # print(file_lines_list)
                # print(start_word)
                # print(file_lines_list[0].startswith("Last"))
                # filtered_lines_list = [line for line in file_lines_list if (re.search(compiled_pattern, line))]
                filtered_lines_list = [line for line in file_lines_list if (line.startswith(start_word))]

                del file_lines_list
                # print(filtered_lines_list.sort())
                # return sorted(filtered_lines_list)
                return filtered_lines_list

        except TypeError as e:
            logging.error(f"Exception Occurred!!\n\tTitle => {'TypeError'}\n\t\tMessage ==> {str(e)}")
            messagebox.showerror(title='TypeError',
                                 message=str(e))

    def file_lines_contains_filter(self, file_lines_list: list, word_to_search_for: str) -> list:
        """
            Filters the lines from the given list of file lines containing the given word to search for

                Arguments : (file_lines_list, word_to_search_for)
                    file_lines_list ===> list
                        description =====> contains the list of lines from the file.

                    word_to_search_for ===> str
                        description =====> contains the word for which we need to filter the list with lines containing the given word_to_search_for

                return filtered_lines_list
                    filtered_lines_list ===> list
                        description =====> contains the list of lines starting with the given start word
        """
        try:
            if isinstance(file_lines_list, list):
                logging.info("Got the file_lines_list from the caller {}")
                file_lines_list = self.file_lines_cleaner(file_lines_list=file_lines_list)

                word_to_search_for = word_to_search_for.strip()

                filtered_lines_list = [line for line in file_lines_list if (line.__contains__(word_to_search_for))]

                del file_lines_list
                return filtered_lines_list

        except TypeError as e:
            logging.error(f"Exception Occurred!!\n\tTitle => {'TypeError'}\n\t\tMessage ==> {str(e)}")
            messagebox.showerror(title='TypeError',
                                 message=str(e))

    def file_lines_pattern_filter(self, file_lines_list: list, pattern_to_search_for: str) -> list:
        """
            Filters the lines from the given list of file lines containing the given word to search for

                Arguments : (file_lines_list, start_word)
                    file_lines_list ===> list
                        description =====> contains the list of lines from the file.

                    pattern_to_search_for ===> str
                        description =====> contains the regex pattern for which we need to filter the list with lines containing the regex pattern

                return filtered_lines_list
                    filtered_lines_list ===> list
                        description =====> contains the list of lines starting with the given pattern
        """
        try:
            logging.info(f'{isinstance(file_lines_list, list) = }')
            if isinstance(file_lines_list, list):
                compiled_pattern = re.compile(pattern=pattern_to_search_for)

                file_lines_list = self.file_lines_cleaner(file_lines_list=file_lines_list)

                filtered_lines_list = [line for line in file_lines_list if (re.search(pattern=compiled_pattern, string=line))]

                del file_lines_list
                return filtered_lines_list

        except TypeError as e:
            logging.error(f"Exception Occurred!!\n\tTitle => {'TypeError'}\n\t\tMessage ==> {str(e)}")
            messagebox.showerror(title='TypeError',
                                 message=str(e))

    def file_lines_chunk_divisor(self, file_lines_list: list, start_string: str, end_string_pattern: str) -> list:
        """Gets the chunks from file_lines_list

        Args:
            file_lines_list (list): _description_ : list of file lines
            start_string (str): _description_ : first keywords from where parsing of chunk lines will be started
            end_string_pattern (str): _description_ : last string pattern till where parsing of chunk lines will be terminated

        return:
            filtered_lines_list (list): _description_ : chunk of parsed file lines
        """
        try:
            logging.info(f'{isinstance(file_lines_list, list) = }')
            if isinstance(file_lines_list, list):
                file_lines_list = self.file_lines_cleaner(file_lines_list=file_lines_list)

                start_index = -sys.maxsize
                end_index = -sys.maxsize

                logging.info(f"Got the start string => {start_string}")
                logging.info(f"Got the end string pattern=> {end_string_pattern}")

                compiled_pattern = re.compile(end_string_pattern)

                i = 0
                while i < len(file_lines_list):
                    file_line = file_lines_list[i]

                    if file_line.startswith(start_string):
                        logging.info(f"Got the start string at {i} for start string {start_string}")
                        start_index = i

                    elif re.search(compiled_pattern, file_line) is not None:
                        if (i > start_index) and (start_index > -sys.maxsize):
                            logging.debug(f"{start_index = }")
                            logging.info(f"found end string pattern at {i}")
                            end_index = i
                            break
                    i += 1

                filtered_lines_list = file_lines_list[start_index:end_index]

                return filtered_lines_list

        except TypeError as e:
            logging.error(f"Exception Occurred!!\n\tTitle => {'TypeError'}\n\t\tMessage ==> {str(e)}")
            messagebox.showerror(title='TypeError',
                                 message=str(e))

    def file_lines_chunk_divisor_pattern(self, file_lines_list: list, starting_string_pattern: str, end_string_pattern: str):
        try:

            file_lines_list = self.file_lines_cleaner(file_lines_list= file_lines_list)
            filtered_lines_list = []
            # print(f"file_lines_list = \n{'\n'.join(file_lines_list)}\n\n")

            logging.info(f"Got the start string pattern => {starting_string_pattern}")
            logging.info(f"Got the end string pattern=> {end_string_pattern}")
            start_string_compiled_pattern = re.compile(pattern=starting_string_pattern)
            ending_string_compiled_pattern = re.compile(pattern=end_string_pattern)

            starting_index = -sys.maxsize
            ending_index = -sys.maxsize
            i = 0
            while i < len(file_lines_list):
                # print(f"{file_lines_list[i] = }  {(re.search(pattern=start_string_compiled_pattern, string=file_lines_list[i])) = }")
                if re.search(pattern=start_string_compiled_pattern, string=file_lines_list[i]):
                    logging.info("found start string at " + str(i) + " for start string " + starting_string_pattern)
                    starting_index = i
                    # print(starting_index)

                if (starting_index > -sys.maxsize) and (i > starting_index):
                    # print(f"finding end string in {file_lines_list[i] = } and {(re.search(pattern=ending_string_compiled_pattern, string=file_lines_list[i])) = }\n")
                    if re.search(pattern=ending_string_compiled_pattern, string=file_lines_list[i]):
                        # print("found end string at " + str(i) + " for end string " + end_string_pattern)
                        logging.info("found end string at " + str(i) + " for end string " + end_string_pattern)
                        ending_index = i
                        break
                i += 1

            if (starting_index > -sys.maxsize) and (ending_index > -sys.maxsize):
                filtered_lines_list = file_lines_list[starting_index : ending_index]

            return filtered_lines_list

        except TypeError as e:
            logging.error(f"Exception Occurred!!\n\tTitle => {'TypeError'}\n\t\tMessage ==> {str(e)}")
            messagebox.showerror(title='TypeError',
                                 message=str(e))

    def file_lines_chunk_division_based_on_next_lines(self, file_lines_list: list, starting_string_pattern: str, end_string_pattern: str, next_line_pattern_to_search_for: str, iterations_after_which_to_look_after_end_string_pattern: int|tuple|list) -> list:
        """
        Gets the chunks from file_lines_list based on next lines pattern iterations
        :param file_lines_list: list of file lines
        :type file_lines_list: list
        :param starting_string_pattern: first keywords from where parsing of chunk lines will be started
        :type starting_string_pattern: str
        :param end_string_pattern: last string pattern till where parsing of chunk lines will be terminated
        :type end_string_pattern: str
        :param next_line_pattern_to_search_for: next line pattern to search for
        :type next_line_pattern_to_search_for: str
        :param iterations_after_which_to_look_after_end_string_pattern: number of iterations after which to look for end string
        :type iterations_after_which_to_look_after_end_string_pattern: int|tuple|list
        :return: chunk of parsed file lines
        :rtype: list
        """
        try:
            logging.info(f'{isinstance(file_lines_list, list) = }')
            if isinstance(file_lines_list, list):
                file_lines_list = self.file_lines_cleaner(file_lines_list=file_lines_list)

                filtered_lines_list = []

                start_string_compiled_pattern = re.compile(pattern=starting_string_pattern)
                ending_string_compiled_pattern = re.compile(pattern=end_string_pattern)
                next_line_pattern_to_search_for_compiled_pattern = re.compile(pattern=next_line_pattern_to_search_for)

                starting_index = -sys.maxsize
                ending_index = -sys.maxsize
                if isinstance(iterations_after_which_to_look_after_end_string_pattern, int):
                    i = 0
                    while i < len(file_lines_list):
                        if re.search(pattern=start_string_compiled_pattern, string=file_lines_list[i]) and starting_index < 0:
                            logging.info("found start string at " + str(i) + " for start string " + starting_string_pattern)
                            starting_index = i

                        if (starting_index > -sys.maxsize) and (i > starting_index):
                            if i+iterations_after_which_to_look_after_end_string_pattern < len(file_lines_list):
                                if re.search(pattern=ending_string_compiled_pattern, string=file_lines_list[i]):
                                    if re.search(pattern=next_line_pattern_to_search_for_compiled_pattern, string=file_lines_list[i + iterations_after_which_to_look_after_end_string_pattern]):
                                        logging.info("found end string at " + str(i + iterations_after_which_to_look_after_end_string_pattern) + " for end string " + end_string_pattern)
                                        ending_index = i
                                        break

                        i += 1

                    if (starting_index > -sys.maxsize) and (ending_index > -sys.maxsize):
                        return file_lines_list[starting_index: ending_index+1]

                if isinstance(iterations_after_which_to_look_after_end_string_pattern, tuple) or isinstance(iterations_after_which_to_look_after_end_string_pattern, list):
                    i = 0
                    while i < len(file_lines_list):
                        if re.search(pattern=start_string_compiled_pattern, string=file_lines_list[i]) and starting_index < 0:
                            logging.info("found start string at " + str(i) + " for start string " + starting_string_pattern)
                            starting_index = i

                        if (starting_index > -sys.maxsize) and (i > starting_index):
                            if i < len(file_lines_list):
                                if re.search(pattern=ending_string_compiled_pattern, string=file_lines_list[i]):
                                    j = 0
                                    while j < len(iterations_after_which_to_look_after_end_string_pattern):
                                        selected_next_line_iteration = iterations_after_which_to_look_after_end_string_pattern[j]
                                        if i+selected_next_line_iteration < len(file_lines_list):
                                            if re.search(pattern=next_line_pattern_to_search_for_compiled_pattern, string=file_lines_list[i+selected_next_line_iteration]):
                                                logging.info("found end string at " + str(i+selected_next_line_iteration) + " for end string " + end_string_pattern)
                                                ending_index = i+selected_next_line_iteration
                                                break
                                        j += 1
                        if ending_index > 0:
                            break
                        i += 1

                    if (starting_index > -sys.maxsize) and (ending_index > -sys.maxsize):
                        filtered_lines_list = file_lines_list[starting_index: ending_index+1]
                        return filtered_lines_list

        except TypeError as e:
            logging.error(f"Exception Occurred!!\n\tTitle => {'TypeError'}\n\t\tMessage ==> {str(e)}")
            messagebox.showerror(title='TypeError',
                                 message=str(e))

    def file_line_index_finder(self, file_lines_list: list, starting_string: str) -> int:
        """
        :param file_lines_list: list of file lines
        :type file_lines_list: list
        :param starting_string: starting keywords of line for which index is to be searched
        :type starting_string: str
        :return: index of starting string
        :rtype: int
        """
        try:
            logging.info(f'{isinstance(file_lines_list, list) = }')
            if isinstance(file_lines_list, list):
                file_lines_list = self.file_lines_cleaner(file_lines_list=file_lines_list)

                i = 0
                while i < len(file_lines_list):
                    if str(file_lines_list[i]).startswith(starting_string):
                        logging.info("found start string at " + str(i) + " for start string " + starting_string)
                        return i
                    i += 1

        except TypeError as e:
            logging.error(f"Exception Occurred!!\n\tTitle => {'TypeError'}\n\t\tMessage ==> {str(e)}")
            messagebox.showerror(title='TypeError',
                                 message=str(e))

    def file_line_index_finder_pattern(self, file_lines_list: list, starting_string_pattern: str) -> int | None:
        """
        :param file_lines_list: list of file lines
        :type file_lines_list: list
        :param starting_string_pattern: starting keywords of line for which index is to be searched
        :type starting_string_pattern: str
        :return: index of starting string
        :rtype: int
        """
        try:
            logging.info(f'{isinstance(file_lines_list, list) = }')
            index = -sys.maxsize
            if isinstance(file_lines_list, list):
                file_lines_list = self.file_lines_cleaner(file_lines_list=file_lines_list)

                starting_string_compiled_pattern = re.compile(pattern=starting_string_pattern)
                i = 0
                while i < len(file_lines_list):
                    if re.search(pattern=starting_string_compiled_pattern, string=file_lines_list[i]):
                        logging.info("found start string at " + str(i) + " for start string " + starting_string_pattern)
                        return i
                    i += 1
            return index

        except TypeError as e:
            logging.error(f"Exception Occurred!!\n\tTitle => {'TypeError'}\n\t\tMessage ==> {str(e)}")
            messagebox.showerror(title='TypeError',
                                 message=str(e))

    def file_lines_reverse_line_fetcher(self, file_lines_list: list, starting_index: int, starting_string: str, line_to_search_for_starting_string: str | list) -> str | None:
        """
        This function, file_lines_reverse_line_fetcher, searches for a specific line in a list of file lines (file_lines_list) in reverse order, starting from a given starting_index.
        It looks for a line that starts with starting_string and then searches for a subsequent line that starts with line_to_search_for_starting_string. If found, it returns the line that matches line_to_search_for_starting_string.
        If not found, it returns None.

        :param file_lines_list: list of file lines
        :type file_lines_list: list
        :param starting_index: index of starting string
        :type starting_index: int
        :param starting_string: keywords of line for which index is to be searched
        :type starting_string: str
        :param line_to_search_for_starting_string: keywords of line for which index is to be searched
        :type line_to_search_for_starting_string: str
        :return: required line or None
        :rtype: str | None
        """
        try:
            logging.info(f'{isinstance(file_lines_list, list) = }')
            if isinstance(file_lines_list, list):
                file_lines_list = self.file_lines_cleaner(file_lines_list=file_lines_list)

                i = starting_index
                result_index = -sys.maxsize
                while i < len(file_lines_list):
                    if str(file_lines_list[i]).startswith(starting_string):
                        logging.info("found start string at " + str(i) + " for start string " + starting_string)
                        j = i - 1
                        while j > starting_index:
                            if str(file_lines_list[j]).startswith(line_to_search_for_starting_string):
                                logging.info("found end string at " + str(j) + " for end string " + line_to_search_for_starting_string)
                                result_index = j
                                break
                            j -= 1
                    i += 1

                if result_index > -sys.maxsize:
                    return file_lines_list[result_index]

                else:
                    return None
        except TypeError as e:
            logging.error(f"Exception Occurred!!\n\tTitle => {'TypeError'}\n\t\tMessage ==> {str(e)}")
            messagebox.showerror(title='TypeError',
                                 message=str(e))

    def file_lines_reverse_line_fetcher_pattern(self, file_lines_list: list, starting_index: int, starting_string_pattern: str, line_to_search_for_starting_string_pattern: str | list) -> str | None:
        """
         It takes in a list of file lines, a starting index, a starting string pattern, and a pattern for the line to search for the starting string. The method uses regular expressions to search for
         the starting string and the line to search for the starting string in the file lines.
         It then iterates through the file lines in reverse order starting from the starting index and returns the line that matches the line to search for the starting string.
         If no match is found, it returns None.

        :param file_lines_list: list of file lines
        :type file_lines_list: list
        :param starting_index: index of starting string
        :type starting_index: int
        :param starting_string_pattern: keywords of line for which index is to be searched
        :type starting_string_pattern: str
        :param line_to_search_for_starting_string_pattern: keywords of line for which index is to be searched
        :type line_to_search_for_starting_string_pattern: str
        :return: index of starting string
        :rtype: int
        """
        try:
            logging.info(f'{isinstance(file_lines_list, list) = }')
            if isinstance(file_lines_list, list):
                file_lines_list = self.file_lines_cleaner(file_lines_list=file_lines_list)

                starting_string_compiled_pattern = re.compile(pattern=starting_string_pattern)
                line_to_search_for_starting_string_compiled_pattern = re.compile(pattern=line_to_search_for_starting_string_pattern)
                i = starting_index
                result_index = -sys.maxsize
                while i < len(file_lines_list):
                    if re.search(pattern=starting_string_compiled_pattern, string=file_lines_list[i]):
                        logging.info("found start string at " + str(i) + " for start string " + starting_string_pattern)
                        j = i - 1
                        while j > starting_index:
                            if re.search(pattern=line_to_search_for_starting_string_compiled_pattern, string=file_lines_list[j]):
                                logging.info("found end string at " + str(j) + " for end string " + line_to_search_for_starting_string_pattern)
                                result_index = j
                                break
                            j -= 1
                    i += 1

                if result_index > -sys.maxsize:
                    return file_lines_list[result_index]

                else:
                    return None
        except TypeError as e:
            logging.error(f"Exception Occurred!!\n\tTitle => {'TypeError'}\n\t\tMessage ==> {str(e)}")
            messagebox.showerror(title='TypeError',
                                 message=str(e))

    def file_line_chunk_multiple_lines_fetcher(self, file_lines_list: list, first_line_check_string: str, actual_line_check_string: str) -> list[bool | list]:
        """
        It takes a list of file lines and two strings as input, and attempts to find the index of the first occurrence of the first_line_check_string and
        the actual_line_check_string in the list.

        :param file_lines_list: list of file lines
        :type file_lines_list: list
        :param first_line_check_string: keywords of line for which index is to be searched
        :type first_line_check_string: str
        :param actual_line_check_string: keywords of line for which index is to be searched
        :type actual_line_check_string: str
        :return: list of bool and list of strings
        :rtype: list
        """
        try:
            logging.info(f'{isinstance(file_lines_list, list) = }')
            if isinstance(file_lines_list, list):
                file_lines_list = self.file_lines_cleaner(file_lines_list=file_lines_list)
                finding_string_found: bool = False
                result_string_list: list = []

                i = 0
                while i < len(file_lines_list):
                    if str(file_lines_list[i]).startswith(first_line_check_string):
                        logging.info("found start string at " + str(i) + " for start string " + first_line_check_string)
                        j = i + 1
                        if j < len(file_lines_list) - 1:
                            while j < len(file_lines_list):
                                if (str(file_lines_list[j]).startswith(first_line_check_string) and (j > i)) or (j == len(file_lines_list) - 1):
                                    i = j
                                    break

                                if str(file_lines_list[j]).startswith(actual_line_check_string):
                                    finding_string_found = True
                                    result_string = file_lines_list[i]
                                    result_string_list.append(result_string)
                                j += 1
                        else:
                            i += 1
                    else:
                        i += 1

                return [finding_string_found, result_string_list]

        except TypeError as e:
            logging.error(f"Exception Occurred!!\n\tTitle => {'TypeError'}\n\t\tMessage ==> {str(e)}")
            messagebox.showerror(title='TypeError',
                                 message=str(e))

    def file_line_chunk_multiple_lines_fetcher_pattern(self, file_lines_list: list, first_line_check_string_pattern: str, actual_line_check_string_pattern: str) -> list[bool, list[str]]:
        """
        It takes a list of file lines and two strings as input, and attempts to find the index of the first occurrence of the first_line_check_string_pattern and
        the actual_line_check_string_pattern in the list.

        :param file_lines_list: list of file lines
        :type file_lines_list: list
        :param first_line_check_string_pattern: keywords of line for which index is to be searched
        :type first_line_check_string_pattern: str
        :param actual_line_check_string_pattern: keywords of line for which index is to be searched
        :type actual_line_check_string_pattern: str
        :return: list of bool and list of strings
        :rtype: list
        """
        try:
            logging.info(f'{isinstance(file_lines_list, list) = }')
            if isinstance(file_lines_list, list):
                file_lines_list = self.file_lines_cleaner(file_lines_list=file_lines_list)
                finding_string_found: bool = False
                result_string_list: list = []
                first_line_check_string_compiled_pattern = re.compile(pattern=first_line_check_string_pattern)
                actual_line_check_string_compiled_pattern = re.compile(pattern=actual_line_check_string_pattern)
                i = 0
                while i < len(file_lines_list):
                    if re.search(pattern=first_line_check_string_compiled_pattern, string=file_lines_list[i]):
                        logging.info("found start string at " + str(i) + " for start string " + first_line_check_string_pattern)
                        j = i + 1
                        if i < len(file_lines_list) - 1:
                            while j < len(file_lines_list):
                                if ((re.search(pattern=first_line_check_string_compiled_pattern, string=file_lines_list[j]) is not None and (j > i)) or
                                        (j == len(file_lines_list) - 1)):
                                    i = j
                                    break

                                if re.search(pattern=actual_line_check_string_compiled_pattern, string=file_lines_list[j]):
                                    finding_string_found = True
                                    result_string = file_lines_list[i]
                                    result_string_list.append(result_string)
                                j += 1
                        else:
                            i += 1
                    else:
                        i += 1

                return [finding_string_found, result_string_list]

        except TypeError as e:
            logging.error(f"Exception Occurred!!\n\tTitle => {'TypeError'}\n\t\tMessage ==> {str(e)}")
            messagebox.showerror(title='TypeError',
                                 message=str(e))

    def file_line_chunk_single_line_fetcher(self, file_lines_list: list, first_line_check_string: str, actual_line_check_string: str) -> list[bool | str]:
        """
        It takes a list of file lines and two strings as input, and attempts to find the index of the first occurrence of the first_line_check_string and
        the actual_line_check_string in the list.

        :param file_lines_list: list of file lines
        :type file_lines_list: list
        :param first_line_check_string: keywords of line after which actual string is to be searched
        :type first_line_check_string: str
        :param actual_line_check_string: keywords of line which is to be searched
        :type actual_line_check_string: str
        :return: list of bool and string
        :rtype: list
        """
        try:
            logging.info(f'{isinstance(file_lines_list, list) = }')
            if isinstance(file_lines_list, list):
                file_lines_list = self.file_lines_cleaner(file_lines_list=file_lines_list)
                finding_string_found: bool = False
                result_string: str = ""

                i = 0
                while i < len(file_lines_list):
                    if finding_string_found:
                        break

                    if str(file_lines_list[i]).startswith(first_line_check_string):
                        logging.info("found start string at " + str(i) + " for start string " + first_line_check_string)
                        j = i + 1
                        if j < len(file_lines_list) - 1:
                            while j < len(file_lines_list):
                                if (str(file_lines_list[j]).startswith(first_line_check_string) and (j > i)) or (j == len(file_lines_list) - 1):
                                    i = j
                                    break

                                if str(file_lines_list[j]).startswith(actual_line_check_string):
                                    finding_string_found = True
                                    result_string = file_lines_list[i]
                                    break
                                j += 1
                        else:
                            i += 1
                    else:
                        i += 1

                return [finding_string_found, result_string]

        except TypeError as e:
            logging.error(f"Exception Occurred!!\n\tTitle => {'TypeError'}\n\t\tMessage ==> {str(e)}")
            messagebox.showerror(title='TypeError',
                                 message=str(e))

    def file_lines_chunk_single_line_fetcher_pattern(self, file_lines_list: list, first_line_check_string_pattern: str, actual_line_check_string_pattern: str) -> list[bool | str]:
        """
        It takes a list of file lines and two strings as input, and attempts to find the index of the first occurrence of the first_line_check_string_pattern and
        the actual_line_check_string_pattern in the list.

        :param file_lines_list: list of file lines
        :type file_lines_list: list
        :param first_line_check_string_pattern: keywords of line after which actual string is to be searched
        :type first_line_check_string_pattern: str
        :param actual_line_check_string_pattern: keywords of line which is to be searched
        :type actual_line_check_string_pattern: str
        :return: list of bool and string
        :rtype: list
        """
        try:
            logging.info(f'{isinstance(file_lines_list, list) = }')
            if isinstance(file_lines_list, list):
                file_lines_list = self.file_lines_cleaner(file_lines_list=file_lines_list)
                finding_string_found: bool = False
                result_string: str = ""

                first_line_check_string_compiled_pattern = re.compile(pattern=first_line_check_string_pattern)
                actual_line_check_string_compiled_pattern = re.compile(pattern=actual_line_check_string_pattern)
                i = 0
                while i < len(file_lines_list):
                    if finding_string_found:
                        break

                    if first_line_check_string_compiled_pattern.search(str(file_lines_list[i])):
                        logging.info("found start string at " + str(i) + " for start string " + first_line_check_string_pattern)
                        j = i + 1
                        if j < len(file_lines_list) - 1:
                            while j < len(file_lines_list):
                                if (re.search(pattern=first_line_check_string_pattern, string=(str(file_lines_list[j]) is not None) and (j > i))
                                        or (j == len(file_lines_list) - 1)):
                                    i = j
                                    break

                                if re.search(pattern=actual_line_check_string_compiled_pattern, string=str(file_lines_list[j])):
                                    finding_string_found = True
                                    result_string = file_lines_list[i]
                                    break
                                j += 1
                        else:
                            i += 1
                    else:
                        i += 1

                return [finding_string_found, result_string]

        except TypeError as e:
            logging.error(f"Exception Occurred!!\n\tTitle => {'TypeError'}\n\t\tMessage ==> {str(e)}")
            messagebox.showerror(title='TypeError',
                                 message=str(e))

    def file_lines_multiple_lined_chunk_fetcher_till_end_pattern(self, file_lines_list: list, chunk_start_string_pattern: str, chunk_end_string_pattern: str, **kwargs) -> list[bool | list[Any]]:
        """
        This function, file_lines_multiple_lined_chunk_fetcher_till_end_pattern, fetches chunks of lines from a file based on a start and end pattern. It returns a list containing a boolean indicating whether the start string was found and a list of strings representing the chunk of lines.

        Here's a simplified explanation:

        1. It iterates through a list of file lines.
        2. When it finds a line matching the chunk_start_string_pattern, it starts collecting lines into a chunk.
        3. It continues collecting lines until it finds a line matching the chunk_end_string_pattern.
        4. It adds the collected chunk of lines to a list, starts again for next chunk till the end of the file lines is reached.
        5. It returns a list containing a boolean indicating whether the start string was found and the collected chunk of lines.
        6. The function is part of a class, as indicated by the self parameter, and uses a file_lines_cleaner method to preprocess the file lines. It also logs information and handles TypeError exceptions.

        Credits:@Codeium

        :param file_lines_list: file lines from which the chunks need to be fetched
        :type file_lines_list: list
        :param chunk_start_string_pattern: regex string pattern (not re.Pattern Object) from where the chunk need to be started
                                           to add to the returning string list.
        :type chunk_start_string_pattern: str
        :param chunk_end_string_pattern: regex string pattern (not re.Pattern Object) till where the chunk need to be
                                         added to the returning string list
        :type chunk_end_string_pattern: str
        :param kwargs: optional arguments, starting_index: int, starting index from where the search should start.

        :return: list of bool and list of strings
        :rtype: list[bool, list[str]]

        Note: Accepted kwargs:
        - include_last_line: bool, default False, if True, the last line of the chunk is included in the returning list.

        """
        try:
            logging.info(f'{isinstance(file_lines_list, list) = }')
            if isinstance(file_lines_list, list):
                file_lines_list = self.file_lines_cleaner(file_lines_list=file_lines_list)
                chunk_start_string_compiled_pattern = re.compile(pattern=chunk_start_string_pattern)
                chunk_end_string_compiled_pattern = re.compile(pattern=chunk_end_string_pattern)
                chunk_start_string_found = False

                if len(kwargs) > 0:
                    include_last_line = False
                    if 'include_last_line' in kwargs:
                        include_last_line = kwargs['include_last_line']

                    included_last_line = False

                    i = 0
                    chunk_list = []
                    while i < len(file_lines_list):
                        if re.search(pattern=chunk_start_string_compiled_pattern, string=str(file_lines_list[i])) is not None:
                            chunk_start_string_found = True
                            logging.warning("found start string at " + str(i) + " for start string " + chunk_start_string_pattern)
                            chunk_list.append(file_lines_list[i])
                            j = i + 1
                            if j < len(file_lines_list):
                                while j < len(file_lines_list):
                                    if re.search(pattern=chunk_end_string_compiled_pattern, string=str(file_lines_list[j])) is not None:
                                        logging.warning("found end string at " + str(j) + " for end string " + chunk_end_string_pattern)

                                        if include_last_line:
                                            chunk_list.append(file_lines_list[j])

                                        i = j
                                        break

                                    else:
                                        chunk_list.append(file_lines_list[j])

                                    j += 1

                        i += 1
                else:
                    i = 0
                    chunk_list = []
                    while i < len(file_lines_list):
                        if re.search(pattern=chunk_start_string_compiled_pattern, string=str(file_lines_list[i])) is not None:
                            chunk_start_string_found = True
                            logging.warning("found start string at " + str(i) + " for start string " + chunk_start_string_pattern)
                            chunk_list.append(file_lines_list[i])
                            j = i + 1
                            if j < len(file_lines_list):
                                while j < len(file_lines_list):
                                    if re.search(pattern=chunk_end_string_compiled_pattern, string=str(file_lines_list[j])) is not None:
                                        logging.warning("found end string at " + str(j) + " for end string " + chunk_end_string_pattern)
                                        i = j
                                        break

                                    else:
                                        chunk_list.append(file_lines_list[j])

                                    j += 1
                        i += 1

                return [chunk_start_string_found, chunk_list]

        except TypeError as e:
            logging.error(f"Exception Occurred!!\n\tTitle => {'TypeError'}\n\t\tMessage ==> {str(e)}")
            messagebox.showerror(title='TypeError',
                                 message=str(e))

    def file_lines_pattern_based_fixed_starting_and_ending_based_line_index_fetcher(self, file_lines_list: list, starting_string_pattern: str, end_string_pattern: str, finding_string_pattern: str, **kwargs):

        file_lines_list = self.file_lines_cleaner(file_lines_list)
        end_string_compiled_pattern = re.compile(pattern=end_string_pattern)
        finding_string_compiled_pattern = re.compile(pattern=finding_string_pattern)
        result_index = -sys.maxsize
        if len(kwargs) > 0:
            if 'starting_index' in kwargs:
                starting_index = kwargs['starting_index']
                starting_string_compiled_pattern = re.compile(pattern=starting_string_pattern)
                i = starting_index
                while i < len(file_lines_list):
                    if re.fullmatch(pattern=starting_string_compiled_pattern, string=file_lines_list[i]):
                        j = i+1
                        while j < len(file_lines_list) or re.fullmatch(pattern=end_string_compiled_pattern, string=file_lines_list[j]):
                            if re.fullmatch(pattern=finding_string_compiled_pattern, string=file_lines_list[j]) is not None:
                                result_index = j
                                break
                            j += 1
                    if result_index > 0:
                        break
                    i += 1
        else:
            starting_index = self.file_line_index_finder_pattern(file_lines_list=file_lines_list, starting_string_pattern=starting_string_pattern)
            i = starting_index
            while i < len(file_lines_list) or re.fullmatch(pattern=end_string_compiled_pattern, string=file_lines_list[i]):
                if re.fullmatch(pattern=finding_string_compiled_pattern, string=file_lines_list[i]) is not None:
                    result_index = i
                    break
                i += 1

        return result_index

    def file_lines_pattern_based_fixed_starting_and_ending_based_lines_chunk_indices_fetcher(self, file_lines_list: list, starting_string_pattern: str, end_string_pattern: str, finding_string_pattern: str, **kwargs):

        file_lines_list = self.file_lines_cleaner(file_lines_list)
        end_string_compiled_pattern = re.compile(pattern=end_string_pattern)
        finding_string_compiled_pattern = re.compile(pattern=finding_string_pattern)
        result_index_list = []
        if len(kwargs) > 0:
            if 'starting_index' in kwargs:
                starting_index = kwargs['starting_index']
                starting_string_compiled_pattern = re.compile(pattern=starting_string_pattern)
                i = starting_index
                while i < len(file_lines_list):
                    if re.fullmatch(pattern=starting_string_compiled_pattern, string=file_lines_list[i]):
                        result_index_list.append(i)
                        j = i+1
                        while j < len(file_lines_list) or re.fullmatch(pattern=end_string_compiled_pattern, string=file_lines_list[j]):
                            if re.fullmatch(pattern=finding_string_compiled_pattern, string=file_lines_list[j]) is not None:
                                result_index_list.append(j)
                                break
                            j += 1
                    if len(result_index_list) > 0:
                        break
                    i += 1
        else:
            starting_index = self.file_line_index_finder_pattern(file_lines_list=file_lines_list, starting_string_pattern=starting_string_pattern)
            result_index_list.append(starting_index)
            i = starting_index
            while i < len(file_lines_list) or re.fullmatch(pattern=end_string_compiled_pattern, string=file_lines_list[i]):
                if re.fullmatch(pattern=finding_string_compiled_pattern, string=file_lines_list[i]) is not None:
                    result_index_list.append(i)
                    break
                i += 1

        return result_index_list

    def raw_file_lines_simple_pattern_based_line_chunk_divisor(self, file_lines_list: list, starting_string_pattern: str, ending_string_pattern: str, **kwargs) -> list[str]:
        """
        This function takes a list of raw file lines, a starting string pattern, an ending string pattern, and a boolean indicating whether the ending string should be equal to the starting string. It returns a list of lists, where each sublist contains the lines between the starting and ending string patterns.

        Here's a simplified explanation:

        1. It iterates through a list of file lines.
        2. When it finds a line matching the starting_string_pattern, it starts collecting lines into a chunk.
        3. It continues collecting lines until it finds a line matching the ending_string_pattern.
        4. It adds the collected chunk of lines to a list, starts again for next chunk till the end of the file lines is reached.
        5. It returns a list of lists, where each sublist contains the lines between the starting and ending string patterns.

        :param file_lines_list: list of raw file lines
        :type file_lines_list: list
        :param starting_string_pattern: regex string pattern (not re.Pattern Object) from where the chunk need to be started
        :type starting_string_pattern: str
        :param ending_string_pattern: regex string pattern (not re.Pattern Object) till where the chunk need to be added
        :type ending_string_pattern: str
        :param kwargs: optional keyword arguments
        :type kwargs: dict
        :return: list of lines between starting and ending string patterns
        :rtype: list[list[str]]


        Possible kwargs:
            - number_of_lines_to_match: int - number of lines to match before and after the starting and ending string patterns
            - list_of_lines_to_match: list - list of lines to match before and after the starting and ending string patterns

            .note - both the number_of_lines_to_match and length of list_of_lines_to_match should be equal.
        """
        starting_index = -sys.maxsize
        ending_index = -sys.maxsize
        number_of_lines_to_match = -sys.maxsize
        list_of_lines_to_match = []

        starting_string_compiled_pattern = re.compile(pattern=starting_string_pattern)
        ending_string_compiled_pattern = re.compile(pattern=ending_string_pattern)
        file_lines_list = self.file_lines_right_side_cleaner(file_lines_list=file_lines_list)
        if len(kwargs) > 0:
            if 'number_of_lines_to_match' in kwargs:
                number_of_lines_to_match = kwargs['number_of_lines_to_match']

            if 'list_of_lines_to_match' in kwargs:
                list_of_lines_to_match = kwargs['list_of_lines_to_match']

        if (number_of_lines_to_match > 0 and len(list_of_lines_to_match) > 0) and (number_of_lines_to_match == len(list_of_lines_to_match)):
            i = 0
            while i < len(file_lines_list):
                if re.fullmatch(pattern=starting_string_compiled_pattern, string=file_lines_list[i]):
                    starting_index = i
                    j = i + 1
                    while j < len(file_lines_list):
                        if re.fullmatch(pattern=ending_string_compiled_pattern, string=file_lines_list[j]):
                            k = 1
                            while k < len(list_of_lines_to_match):
                                if re.fullmatch(pattern=list_of_lines_to_match[k], string=file_lines_list[j-k]) is None:
                                    break
                                if k == len(list_of_lines_to_match)-1:
                                    ending_index = j
                                    break
                                k += 1

                        if ending_index > 0:
                            break
                        j += 1

                    if ending_index > 0:
                        break
                i += 1

            if starting_index < 0:
                starting_index = 0

            if ending_index < 0:
                ending_index = len(file_lines_list)

        else:
            i = 0
            while i < len(file_lines_list):
                if re.search(pattern=starting_string_compiled_pattern, string=file_lines_list[i]) is not None:
                    logging.info("found start string at " + str(i) + " for start string " + starting_string_pattern)
                    starting_index = i
                    j = i + 1
                    while j < len(file_lines_list):
                        if re.search(pattern=ending_string_compiled_pattern, string=file_lines_list[j]) is not None:
                            logging.info("found end string at " + str(j) + " for end string " + ending_string_pattern)
                            ending_index = j
                            break
                        j += 1
                    if ending_index > 0:
                        break
                i += 1

            if starting_index < 0:
                starting_index = 0

            if ending_index < 0:
                ending_index = len(file_lines_list)

            logging.debug(f"starting_index = {starting_index}, ending_index = {ending_index}\n{'\n'.join(file_lines_list[starting_index:ending_index])}")

        return file_lines_list[starting_index:ending_index]

    def raw_file_lines_pattern_based_line_single_chunk_getter(self, file_lines_list: list, starting_string_pattern: str, ending_string_pattern: str, **kwargs) -> list[str]:
        """
        This function takes a list of raw file lines, a starting string pattern, an ending string pattern, and a boolean indicating whether the ending string should be equal to the starting string. It returns a list of lines between the starting and ending string patterns.
        :param file_lines_list: list of raw file lines
        :type file_lines_list: list
        :param starting_string_pattern: regex string pattern (not re.Pattern Object) from where the chunk need to be started
        :type starting_string_pattern: str
        :param ending_string_pattern: regex string pattern (not re.Pattern Object) till where the chunk need to be added
        :type ending_string_pattern: str
        :param kwargs: optional keyword arguments
        :type kwargs: dict
        :return: list of lines between starting and ending string patterns
        :rtype: list[str]
        """
        starting_index = -sys.maxsize
        ending_index = -sys.maxsize
        number_of_lines_to_match = -sys.maxsize
        list_of_lines_to_match = []

        starting_string_compiled_pattern = re.compile(pattern=starting_string_pattern)
        ending_string_compiled_pattern = re.compile(pattern=ending_string_pattern)

        if len(kwargs) > 0:
            if 'number_of_lines_to_match' in kwargs:
                number_of_lines_to_match = kwargs['number_of_lines_to_match']

            if 'list_of_lines_to_match' in kwargs:
                list_of_lines_to_match = kwargs['list_of_lines_to_match']

        if (number_of_lines_to_match > 0 and len(list_of_lines_to_match) > 0) and (number_of_lines_to_match == len(list_of_lines_to_match)):
            i = 0
            while i < len(file_lines_list):
                if re.fullmatch(pattern=starting_string_compiled_pattern, string=file_lines_list[i]) is not None:
                    starting_index = i
                    j = i + 1
                    while j < len(file_lines_list):
                        if re.fullmatch(pattern=ending_string_compiled_pattern, string=file_lines_list[j]) is not None:
                            k = 0
                            while k < len(list_of_lines_to_match):
                                __var = j + k + 1 - len(list_of_lines_to_match)
                                if re.fullmatch(pattern=list_of_lines_to_match[k], string=file_lines_list[__var]) is None:
                                    break
                                if k == len(list_of_lines_to_match)-1:
                                    ending_index = j
                                    break
                                k += 1

                        if ending_index > 0:
                            break
                        j += 1

                    if ending_index > 0:
                        break
                if ending_index > 0 or starting_index > 0:
                    break
                i += 1

            if starting_index < 0:
                starting_index = 0

            if ending_index < 0:
                ending_index = len(file_lines_list)

        else:
            i = 0
            while i < len(file_lines_list):
                if re.search(pattern=starting_string_compiled_pattern, string=file_lines_list[i]) is not None:
                    logging.info("found start string at " + str(i) + " for start string " + starting_string_pattern)
                    starting_index = i
                    j = i + 1
                    while j < len(file_lines_list):
                        if re.search(pattern=ending_string_compiled_pattern, string=file_lines_list[j]) is not None:
                            logging.info("found end string at " + str(j) + " for end string " + ending_string_pattern)
                            ending_index = j
                            break
                        j += 1
                    if ending_index > 0:
                        break
                if ending_index > 0 or starting_index > 0:
                    break
                i += 1

            if starting_index < 0:
                starting_index = 0

            if ending_index < 0:
                ending_index = len(file_lines_list)

            logging.debug(f"starting_index = {starting_index}, ending_index = {ending_index}\n{'\n'.join(file_lines_list[starting_index:ending_index])}")

        result_list = self.file_lines_right_side_cleaner(file_lines_list=file_lines_list[starting_index:ending_index])
        return result_list