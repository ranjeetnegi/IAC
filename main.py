import os
import re
import sys
from os import listdir
from src.address import Address
from src.utility import Utility
from src.pincode import PinCode
from src.phonenumber import PhoneNumber
from src.msoffice import MsOffice
from pathlib import Path


# from ms_office import MsOffice
# from utility import Utility

class Main:

    def __init__(self):
        self.utility = Utility()
        self.pincode = PinCode()
        self.phone_number = PhoneNumber()
        self.output_dir = "output_dir/"
        self.ms_office = MsOffice()
        self.utility = Utility()

    def process_addresses(self, addresses_file_text):
        address_list = []
        if addresses_file_text is not None and len(addresses_file_text) > 0:
            address_object_list = self.get_address_list(addresses_file_text)
            for address_obj in address_object_list:
                address_string = address_obj.address
                address_string = self.utility.clean_stoping_words(address_string)
                address_string = self.pincode.pad_pin_code(address_string, "*")
                address_string = self.phone_number.collapse_phone_number(address_string)
                address_string = self.phone_number.pad_phone_number(address_string, "*")
                address_string = self.phone_number.mobile_number_text_remover(address_string)
                address_string = self.pincode.pin_number_text_remover(address_string)
                address_obj.address = address_string
                self.pincode.update_pin_number(address_obj)
                self.phone_number.update_phone_number(address_obj)
                address_obj.address = self.utility.white_space_cleaner(address_obj.address)
                address_obj.capitalize_address()
                address_list.append(address_obj)
        address_list.sort()
        return address_list

    def main(self):
        files_list = []
        for arg in sys.argv[1:]:
            files_list.append(arg)
        for file_name in files_list:
            addresses_file_text = self.read_from_file(file_name)
            address_list = self.process_addresses(addresses_file_text)

            file_base_name = Path(file_name).stem

            output_file_name_xls = self.output_dir + self.utility.generate_output_file_name(file_base_name, "xls")
            print(output_file_name_xls)
            self.ms_office.export_to_MS_Excel(address_list, output_file_name_xls)

            output_file_name_docx = self.output_dir + self.utility.generate_output_file_name(file_base_name, "docx")
            self.ms_office.export_to_MS_word(address_list,output_file_name_docx)


    def get_address_list(self, text):
        address_list = []
        regex_split_1 = r"\d{1,2}\/\d{1,2}\/\d{2}, \d+:\d+ - [a-zA-Z-0-9 ]+:"
        regex_split_2 = r"\d{1,2}\/\d{1,2}\/\d{2}, \d+:\d+ [ap]m - [a-zA-Z-0-9 ]+:"

        matches_1 = re.findall(regex_split_1, text)
        matches_2 = re.findall(regex_split_2, text)

        # print(matches)
        if len(matches_1) > 0 or len(regex_split_2) > 0:
            text = text.replace("\n", " ").replace("[\s]+", " ")
            text = self.utility.white_space_cleaner(text)
            if len(matches_1) > 0:
                addresses_list = re.split(regex_split_1, text)
            elif len(matches_2) > 0:
                addresses_list = re.split(regex_split_2, text)

            for address_text in addresses_list:
                address_obj = Address(address_text, None, None, None, None, None)
                address_list.append(address_obj)
        else:
            addresses_list = re.split("\n", text)
            for address_text in addresses_list:
                if len(address_text.strip()) > 0:
                    address_obj = Address(address_text, None, None, None, None, None)
                    address_list.append(address_obj)
        return address_list

    def read_from_file(self, file_name):
        with open(file_name, "r", encoding="utf-8") as f:
            text = f.read()
        return text

if __name__ == "__main__":
    main_obj = Main()
    main_obj.main()
