import os
import re
import sys
from os import listdir
from pin_location_mapper import PinLocationMapper
from address import Address
from ms_office import MsOffice
from utility import Utility


# Step 1: New line between two addresses
# Step 2: Phone number clean up
# Step 3: Pin Code clean up
# Step 4: Stop character cleanup
# Step 5: Sort address by leanth
# Step 6: Export to MS Word
# Step 7: Export to Excel

################################### PHONE NUMBER CLEAN-UP ##############################
def collapse_phone_number(address_obj):
    regex_1 = "\d+[ ]\d+[ ]\d+"

    match_1 = re.findall(regex_1, address_obj.address)
    if len(match_1) > 0:
        for match in match_1:
            match_replacer = match.replace(" ", "")
            address_obj.address = address_obj.address.replace(match, match_replacer)
    return


def pad_phone_numer(address_obj, pad_word):
    space = " "
    collapse_phone_number(address_obj)

    regex_1 = "[ ][6-9]\d{9}[ ]|[ ][6-9]\d{9}$"  # " 7534564334 "
    regex_2 = "[6-9]\d{4}[ ]\d{5}"  # "65345 64334"
    regex_3 = "[^*0-9][6-9]\d{9}|[^*0-9][6-9]\d{9}$"  # "n4534564334"

    regex_1_matches = re.findall(regex_1, address_obj.address)
    if len(regex_1_matches) > 0:
        for match in regex_1_matches:
            regex_1_replacer = space + pad_word + match.strip() + pad_word + space
            address_obj.address = address_obj.address.replace(match, regex_1_replacer)
    regex_2_matches = re.findall(regex_2, address_obj.address)
    if len(regex_2_matches) > 0:
        for match in regex_2_matches:
            regex_2_replacer = (
                space + pad_word + match.replace(" ", "").strip() + pad_word + space
            )
            address_obj.address = address_obj.address.replace(match, regex_2_replacer)
    regex_3_matches = re.findall(regex_3, address_obj.address)
    if len(regex_3_matches) > 0:
        for match in regex_3_matches:
            left_outer_char = match[0]
            regex_3_replacer = (
                left_outer_char + space + pad_word + match[1:] + pad_word + space
            )
            regex_3_replacer = regex_3_replacer.replace(" ", "")
            match = match.replace(" ", "")
            address_obj.address = address_obj.address.replace(match, regex_3_replacer)
    return


def pad_phone(text, pad_word):
    regex = "\d{10}|\d{10}$|\d{5}[ ]{1}\d{5}"
    text = stop_character_cleanup(text)
    matches = re.findall(regex, text)
    for match in matches:
        paded_match = pad_word + match.replace(" ", "") + pad_word
        text = text.replace(match, paded_match, 3)
    return text


def mobile_number_text_remover(address_obj):
    address = address_obj.address.lower()
    phone_number_prefixes = [
        " contact no ", " mobile, no ", " mobail no ", " mobile no ", " mobal nbr ", " phone no ", " mobil no ",
        " cell no ", " cell ", " noumber ", " contact ", " mobile/", " mob no*", " wtsp ", " mobile ", " mb nbr ",
        " mob no ", " m no/*", " phone ", ",ph no ", " po no ", " mobil ", " ph no ", " m no_*", " m no/ ", " mob/*",
        " c no ", " phon ", " m no ", "phone ", " mob,", ",no *", " mob ", " mob*", " no *", ",mo *", " pn ", " po ",
        " ph ", " nm ", " mo ", " m *",
    ]
    phone_number_prefixes = sorted(list(set(phone_number_prefixes)), key=len)
    phone_number_prefixes = Reverse(phone_number_prefixes)
    for prefix in phone_number_prefixes:
        if (
                address.find(prefix) != -1
                and prefix.find(",") != -1
                and prefix.find("*") != -1
        ):
            address = address.replace(prefix, ", *")
        if address.find(prefix) != -1 and prefix.find("*") != -1:
            address = address.replace(prefix, " *")
        if address.find(prefix) != -1:
            address = address.replace(prefix, " ")
    address_obj.address = address
    return


################################### PIN CODE CLEAN-UP ##################################
def pad_pin_code(address_obj, pad_word):
    space = " "
    pin_regex_1 = "[ ]\d{6}$"  # | 334333|
    pin_regex_2 = "[ ]\d{6}[ ]"  # | 334333 |
    pin_regex_3 = "[^0-9*]\d{6}[^0-9*]"  # |n334333d|
    pin_regex_4 = "[ ]\d{4}[ ]\d{2}[ ]"  # | 3343 33 |
    pin_regex_5 = "[^0-9]\d{3}[ ]\d{3}"  # |334 333|
    pin_regex_6 = "[ ]\d{4}[ ]\d{2}$"  # | 3343 33|
    pin_regex_7 = "[ ]\d{4}[ ]\d{2}[ ]"  # | 3343 33 |
    pin_regex_8 = "[^0-9*]\d{6}[ ]"  # |n3343 33 |
    pin_regex_9 = "[ ]\d{6}[^0-9*]"  # |334333n|

    text = address_obj.address
    pin_regex_1_matches = re.findall(pin_regex_1, text)
    pin_regex_2_matches = re.findall(pin_regex_2, text)
    pin_regex_3_matches = re.findall(pin_regex_3, text)
    pin_regex_4_matches = re.findall(pin_regex_4, text)
    pin_regex_5_matches = re.findall(pin_regex_5, text)
    pin_regex_6_matches = re.findall(pin_regex_6, text)
    pin_regex_7_matches = re.findall(pin_regex_7, text)
    pin_regex_8_matches = re.findall(pin_regex_8, text)
    pin_regex_9_matches = re.findall(pin_regex_9, text)

    if len(pin_regex_1_matches) > 0:
        for match in pin_regex_1_matches:
            paded_match = space + pad_word + match.replace(" ", "") + pad_word + space
            address_obj.address = text.replace(match, paded_match)
            return
    if len(pin_regex_2_matches) > 0:
        for match in pin_regex_2_matches:
            paded_match = space + pad_word + match.replace(" ", "") + pad_word + space
            address_obj.address = text.replace(match, paded_match)
            return
    if len(pin_regex_3_matches) > 0:
        for match in pin_regex_3_matches:
            first_char = match[0]
            last_char = match[-1]
            pin = match[1:-1]
            paded_match = (
                first_char + space + pad_word + pin + pad_word + space + last_char
            )
            address_obj.address = text.replace(match, paded_match)
            return
    if len(pin_regex_4_matches) > 0:
        for match in pin_regex_4_matches:
            paded_match = space + pad_word + match.replace(" ", "") + pad_word + space
            address_obj.address = text.replace(match, paded_match)
            return
    if len(pin_regex_5_matches) > 0:
        for match in pin_regex_5_matches:
            paded_match = space + pad_word + match.replace(" ", "") + pad_word + space
            address_obj.address = text.replace(match, paded_match)
            return
    if len(pin_regex_6_matches) > 0:
        for match in pin_regex_6_matches:
            paded_match = space + pad_word + match.replace(" ", "") + pad_word + space
            address_obj.address = text.replace(match, paded_match)
            return
    if len(pin_regex_7_matches) > 0:
        for match in pin_regex_7_matches:
            paded_match = space + pad_word + match.replace(" ", "") + pad_word + space
            address_obj.address = text.replace(match, paded_match)
            return
    if len(pin_regex_8_matches) > 0:
        for match in pin_regex_8_matches:
            pin = match[1:-1]
            paded_match = space + pad_word + pin + pad_word + space
            address_obj.address = text.replace(match, paded_match)
            return
    if len(pin_regex_9_matches) > 0:
        for match in pin_regex_9_matches:
            pin = match[1:-1]
            last_char = match[-1]
            paded_match = space + pad_word + pin + pad_word + space + last_char
            address_obj.address = text.replace(match, paded_match)
            return
    return


def pin_number_text_remover(address_obj):
    address = address_obj.address.lower()
    pin_number_prefixes = [" pin ", " pin/ ", " pin_ ", " cod ", "p/c ", " pinn cod ", " code ", " cd ", " pincode ",
                           " cod ", "pin ", "pin,", " pinkod ", "pin-", ]
    pin_number_prefixes = sorted(list(set(pin_number_prefixes)), key=len)
    pin_number_prefixes = Reverse(pin_number_prefixes)
    for prefix in pin_number_prefixes:
        if (
            address.find(prefix) != -1
            and prefix.find(",") != -1
            and prefix.find("*") != -1
        ):
            address = address.replace(prefix, ", *")
        if address.find(prefix) != -1 and prefix.find("*") != -1:
            address = address.replace(prefix, " *")
        if address.find(prefix) != -1:
            address = address.replace(prefix, " ")
    address_obj.address = address
    return


################################### Clean up ##################################
def white_space_cleaner(text):
    text = re.sub(r"\s+", " ", text).strip()
    return re.sub("\,+", ",", text)


def clean_stoping_words(address):
    text = address.address

    # email cleanup
    text = re.sub(r"([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)", "", text)
    text = text.replace("EMAIL", "").replace("Email", "").replace("email", "")
    text = re.sub(r"[,]+", ",", text)

    # dot clean up
    text = text.replace(".", " ")
    # Colon cleanup
    text = text.replace(":", " ")
    # semi colon cleanup
    text = text.replace(";", " ")
    # - cleanup
    text = text.replace("-", " ")
    # +91
    text = text.replace("+91", " ")
    # text = text.replace("("," ")
    # text = text.replace(")"," ")
    text = text.replace("Name :", " ")
    text = text.replace("Name ", " ")
    text = text.replace("Name,", " ")
    text = text.replace("=", " ")
    text = text.replace("tq", "Tq")
    text = text.replace("taluk", "Tq")
    text = text.replace("code", " ")
    text = text.replace("Code", " ")
    text = text.replace("number", " ")
    text = text.replace("Number", " ")
    text = text.replace("num", " ")
    text = text.replace("(p)", " Post")
    text = text.replace("(P)", " Post")
    text = text.replace("&", " and ")
    text = text.replace("pincod", " pin ")
    text = text.replace(" number ", " ")
    text = text.replace('"', "")
    text = text.replace("*", "")
    text = text.replace("((", "(").replace("( ", "(")
    text = text.replace("))", ")").replace(" )", ")")
    text = (
        text.replace("E mail", "")
        .replace("e mail", "")
        .replace("email", "")
        .replace("eMail", "")
        .replace(" mail id ", "")
    )
    text = white_space_cleaner(text)

    address.address = text
    return


def replace_white_spaces_single_space(text):
    return text.replace("[\s]+", " ")


def Reverse(lst):
    new_lst = lst[::-1]
    return new_lst


############################ PRINT ADDRESS #############################
def print_address(address_list):
    for address in address_list:
        print(address.print_attributes())


############################ READ ADDRESSES FROM FILE ##################
def read_from_file(file_name):
    f = open(file_name, "r")
    text = f.read()
    f.close()
    return text


############################ GET ALL FILE TO RUN #######################
def get_all_file_name(path):
    files_array = []
    files_arr = listdir(path)
    for fileName in files_arr:
        extension = fileName.split(".")[-1]
        for ext_allowed in ALLOWED_EXTENSION_ARRAY:
            if ext_allowed.lower() == extension:
                files_arr.append(fileName)


############################ GET ADDRESS LIST FROM TEXT #################
def get_address_list(text):
    address_list = []
    regex_split_1 = r"\d{1,2}\/\d{1,2}\/\d{2}, \d+:\d+ - [a-zA-Z-0-9 ]+:"
    regex_split_2 = r"\d{1,2}\/\d{1,2}\/\d{2}, \d+:\d+ [ap]m - [a-zA-Z-0-9 ]+:"

    matches_1 = re.findall(regex_split_1, text)
    matches_2 = re.findall(regex_split_2, text)

    # print(matches)
    if len(matches_1) > 0 or len(regex_split_2) > 0:
        text = text.replace("\n", " ").replace("[\s]+", " ")
        text = white_space_cleaner(text)
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


############################ replace_pin_and_phone_num ##################


def replace_pin_and_phone_num(address):
    address = address.replace("*", " ")
    return replace_white_spaces_single_space(address)


def get_pin_code_hilighted(address_obj):
    hilighted_pin_code_regex = "[*]\d{6}[*]"
    return list(set(re.findall(hilighted_pin_code_regex, address_obj.address)))


def get_hilighted_phone_number_from_address(address_obj):
    hilighted_phone_number_regex = "[*]\d{10}[*]"
    return list(set(re.findall(hilighted_phone_number_regex, address_obj.address)))


def update_phone_number(address_obj):
    hilighted_phone_list = get_hilighted_phone_number_from_address(address_obj)
    if hilighted_phone_list != None and len(hilighted_phone_list) > 0:
        if len(hilighted_phone_list) > 1:
            phone_list = []
            for hilighted_phone in hilighted_phone_list:
                phone = hilighted_phone.replace("*", "")
                phone_list.append(phone)
                address_obj.address = address_obj.address.replace(
                    hilighted_phone, ""
                ).strip()
            phones_as_string = ",".join(phone_list)
            address_obj.phone = phones_as_string
            address_obj.address = address_obj.address + " PH : " + phones_as_string
        elif len(hilighted_phone_list) > 0:
            hilighted_phone = hilighted_phone_list[0]
            phone = hilighted_phone.replace("*", "")
            address_obj.address = (
                address_obj.address.replace(hilighted_phone, "").strip()
                + " PH-"
                + phone
            )
            address_obj.phone = phone


def update_pin_number(address_obj):
    location_mapper = PinLocationMapper()

    hilighted_pin_list = get_pin_code_hilighted(address_obj)
    if hilighted_pin_list != None and len(hilighted_pin_list) > 0:
        hilighted_pin = hilighted_pin_list[0]
        pin = hilighted_pin.replace("*", "")
        address_obj.pin = pin
        pin_location = location_mapper.get_address_details(pin)
        if pin_location != None and len(pin_location) > 0:
            # print(pin_location)
            state, district, block = pin_location.split(",")
            address_obj.address = address_obj.address.replace(hilighted_pin, "").strip()
            if state != None and district != None and block != None:
                address_obj.state = state
                address_obj.district = district
                address_obj.block = block
                address_obj.address = address_obj.address + " Pin-" + pin
    return


def process_addresses(files_list):
    address_list = []
    if files_list != None and len(files_list) > 0:
        for file_name in files_list:
            addresses_file_text = read_from_file(file_name)
            address_object_list = get_address_list(addresses_file_text)
            # print_address(address_object_list)
            # address_object_list=import_from_Excel_sheet(file_name,"Sheet1",1)
            
            for address_obj in address_object_list:
                clean_stoping_words(address_obj)
                pad_pin_code(address_obj, "*")
                collapse_phone_number(address_obj)
                pad_phone_numer(address_obj, "*")
                mobile_number_text_remover(address_obj)
                pin_number_text_remover(address_obj)
                update_pin_number(address_obj)
                update_phone_number(address_obj)
                address_obj.address = white_space_cleaner(address_obj.address)
                # address_obj.capitalize_address()
                address_list.append(address_obj)
        address_list.sort()
    # print_address(address_list)
    return address_list


############################ MAIN CLASS #################################
def main():
    files_list = []
    for arg in sys.argv[1:]:
        files_list.append(arg)
    address_list = process_addresses(files_list)
    ms_office = MsOffice()
    
    utility = Utility()
    output_file_name_xls = utility.genrate_output_file_name("KA.xls")
    output_file_name_docx = utility.genrate_output_file_name("KA.docx")
    #ms_office.export_to_MS_word(address_list[4500:],output_file_name_docx)
    ms_office.export_to_MS_Excel(address_list, output_file_name_xls)


if __name__ == "__main__":
    main()

# TODO reprocess address wrong pin join: "28/09/20, 1:41 pm - Mangal: Rakshith. H. G No. #492  10 th main near post office M.C  layout  vijayanagara Bengaluru 560040 Mo 6360 959 577"
