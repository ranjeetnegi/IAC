import re
from services.utility import Utility


class PhoneNumber:

    def __init__(self):
        self.utility = Utility()
        phone_number_prefixes = [" contact no ", " mobile, no ", " mobail no ", " mobile no ", " mobal nbr ", "mobail",
                                 "mobail no",
                                 " phone no ", " mobil no ", " cell no ", " cell ", " noumber ", " contact ",
                                 " mobile/", " mob no*", " wtsp ", " mobile ", " mb nbr ", " mob no ", " m no/*",
                                 " phone ", ",ph no ", " po no ", " mobil ", " ph no ", " m no_*", " m no/ ",
                                 " mob/*", " c no ", " phon ", " m no ", "phone ", " mob,", ",no *", " mob ", " mb ",
                                 " mob*",
                                 " no *", ",mo *", " pn ", " po ", " ph ", " nm ", " mo ", " m *", " number "]
        self.phone_number_prefixes = self.utility.reverse_list(sorted(list(set(phone_number_prefixes)), key=len))

    def collapse_phone_number(self, text):
        regex_1 = '\d+[ ]\d+[ ]\d+'
        match_1 = re.findall(regex_1, text)
        if len(match_1) > 0:
            for match in match_1:
                match_replacer = match.replace(" ", "")
                text = text.replace(match, match_replacer)
        return text

    def pad_phone_number(self, text, pad_word):
        space = " "
        self.collapse_phone_number(text)

        regex_1 = "[ ][6-9]\d{9}[ ]|[ ][6-9]\d{9}$"  # " 7534564334 "
        regex_2 = "[6-9]\d{4}[ ]\d{5}"  # "65345 64334"
        regex_3 = "[^*0-9][6-9]\d{9}|[^*0-9][6-9]\d{9}$"  # "n4534564334"

        regex_1_matches = re.findall(regex_1, text)
        if len(regex_1_matches) > 0:
            for match in regex_1_matches:
                regex_1_replacer = space + pad_word + match.strip() + pad_word + space
                text = text.replace(match, regex_1_replacer)

        regex_2_matches = re.findall(regex_2, text)
        if len(regex_2_matches) > 0:
            for match in regex_2_matches:
                regex_2_replacer = space + pad_word + match.replace(" ", "").strip() + pad_word + space
                text = text.replace(match, regex_2_replacer)

        regex_3_matches = re.findall(regex_3, text)
        if len(regex_3_matches) > 0:
            for match in regex_3_matches:
                left_outer_char = match[0]
                regex_3_replacer = left_outer_char + space + pad_word + match[1:] + pad_word + space
                regex_3_replacer = regex_3_replacer.replace(" ", "")
                match = match.replace(" ", "")
                text = text.replace(match, regex_3_replacer)
        return text

    def pad_phone(self, text, pad_word):
        regex = "\d{10}|\d{10}$|\d{5}[ ]{1}\d{5}"
        text = stop_character_cleanup(text)
        matches = re.findall(regex, text)
        for match in matches:
            padded_match = pad_word + match.replace(" ", "") + pad_word
            text = text.replace(match, padded_match, 3)

    def mobile_number_text_remover(self, text):
        if text is not None:
            address = text.lower()
            for prefix in self.phone_number_prefixes:
                if address.find(prefix) != -1 and prefix.find(",") != -1 and prefix.find("*") != -1:
                    address = address.replace(prefix, ", *")
                if address.find(prefix) != -1 and prefix.find("*") != -1:
                    address = address.replace(prefix, " *")
                if address.find(prefix) != -1:
                    address = address.replace(prefix, " ")
            return address

    def get_hilighted_phone_number_from_address(self, address_obj):
        highlighted_phone_number_regex = "[*]\d{10}[*]"
        return list(set(re.findall(highlighted_phone_number_regex, address_obj.address)))

    def update_phone_number(self, address_obj):
        highlighted_phone_list = self.get_hilighted_phone_number_from_address(address_obj)
        if highlighted_phone_list is not None and len(highlighted_phone_list) > 0:
            if len(highlighted_phone_list) > 1:
                phone_list = []
                for highlighted_phone in highlighted_phone_list:
                    phone = highlighted_phone.replace("*", "")
                    phone_list.append(phone)
                    address_obj.address = address_obj.address.replace(highlighted_phone, "").strip()
                phones_as_string = ",".join(phone_list)
                address_obj.phone = phones_as_string
                address_obj.address = address_obj.address + " PH : " + phones_as_string
            elif len(highlighted_phone_list) > 0:
                highlighted_phone = highlighted_phone_list[0]
                phone = highlighted_phone.replace("*", "")
                address_obj.address = (address_obj.address.replace(highlighted_phone, "").strip() + " PH-" + phone)
                address_obj.phone = phone
