from src.pinlocationmapper import PinLocationMapper
from src.utility import Utility
import re


class PinCode:

    def __init__(self):
        self.utility = Utility()
        pin_number_prefixes = [" pin ", " pin/ ", " pin_ ", " cod ", "p/c ", " pinn cod ", " code ", " cd ",
                               " pincode ", " cod ", "pin ", "pin,", " pinkod ", "pin-", " pino "]
        self.pin_number_prefixes = self.utility.reverse_list(sorted(list(set(pin_number_prefixes)), key=len))

    def update_pin_number(self, address_obj):
        location_mapper = PinLocationMapper()

        hilighted_pin_list = self.get_pin_code_hilighted(address_obj)
        if hilighted_pin_list is not None and len(hilighted_pin_list) > 0:
            hilighted_pin = hilighted_pin_list[0]
            pin = hilighted_pin.replace("*", "")
            address_obj.pin = pin
            address_obj.address = address_obj.address.replace(hilighted_pin, "").strip()
            pin_location = location_mapper.get_address_details(pin)
            if pin_location is not None and len(pin_location) > 0:
                # print(pin_location)
                state, district, block = pin_location.split(",")
                if state is not None and district is not None and block is not None:
                    address_obj.state = state
                    address_obj.district = district
                    address_obj.block = block
            if pin is not None:
                address_obj.address = self.utility.white_space_cleaner(address_obj.address) + " Pin " + pin
        return

    def pad_pin_code(self, text_input, pad_word):
        text = text_input
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
            #print("match 1")
            for match in pin_regex_1_matches:
                padded_match = space + pad_word + match.replace(" ", "") + pad_word + space
                return text.replace(match, padded_match)
        if len(pin_regex_2_matches) > 0:
            #print("match 2")
            for match in pin_regex_2_matches:
                padded_match = space + pad_word + match.replace(" ", "") + pad_word + space
                return text.replace(match, padded_match)
        if len(pin_regex_3_matches) > 0:
            #print("match 3")
            for match in pin_regex_3_matches:
                first_char = match[0]
                last_char = match[-1]
                pin = match[1:-1]
                padded_match = (first_char + space + pad_word + pin + pad_word + space + last_char)
                text = text.replace(match, padded_match)
            return text
        if len(pin_regex_4_matches) > 0:
            #print("match 4")
            for match in pin_regex_4_matches:
                padded_match = space + pad_word + match.replace(" ", "") + pad_word + space
                text = text.replace(match, padded_match)
            return text
        if len(pin_regex_5_matches) > 0:
            #print("match 5")
            for match in pin_regex_5_matches:
                prefix = match[0]
                padded_match = prefix + space + pad_word + match.replace(" ", "") + pad_word + space
                text = text.replace(match, padded_match)
            return text
        if len(pin_regex_6_matches) > 0:
            #print("match 6")
            for match in pin_regex_6_matches:
                padded_match = space + pad_word + match.replace(" ", "") + pad_word + space
                text = text.replace(match, padded_match)
            return text
        if len(pin_regex_7_matches) > 0:
            #print("match 7")
            for match in pin_regex_7_matches:
                padded_match = space + pad_word + match.replace(" ", "") + pad_word + space
                text = text.replace(match, padded_match)
            return text
        if len(pin_regex_8_matches) > 0:
            #print("match 8")
            for match in pin_regex_8_matches:
                pin = match[1:-1]
                padded_match = space + pad_word + pin + pad_word + space
                text = text.replace(match, padded_match)
            return text
        if len(pin_regex_9_matches) > 0:
            #print("match 9")
            for match in pin_regex_9_matches:
                pin = match[1:-1]
                last_char = match[-1]
                padded_match = space + pad_word + pin + pad_word + space + last_char
                text = text.replace(match, padded_match)
            return text
        return text_input

    def pin_number_text_remover(self, text):
        if text is not None:
            address = text.lower()

            for prefix in self.pin_number_prefixes:
                if address.find(prefix) != -1 and prefix.find(",") != -1 and prefix.find("*") != -1:
                    address = address.replace(prefix, ", *")
                if address.find(prefix) != -1 and prefix.find("*") != -1:
                    address = address.replace(prefix, " *")
                if address.find(prefix) != -1:
                    address = address.replace(prefix, " ")
            return address

    def get_pin_code_hilighted(self, address_obj):
        #print(address_obj.address)
        highlighted_pin_code_regex = "[*]\d{6}[*]"
        pin_codes = re.findall(highlighted_pin_code_regex, address_obj.address)
        #print(pin_codes)
        return list(set(pin_codes))

    def pin_code_extender(self, text):
        #Bangalore
        regex_1 = r"[bB]angalore[ -]\d{2}[ ,]"
        matches_1 = re.findall(regex_1, text)
        if len(matches_1) > 0:
            for match in matches_1:
                result = re.sub(r"[^a-zA-Z0-9]", " ", match)
                pin_matches = re.findall(r"\d{2}", result)
                for short_pin in pin_matches:
                    pin = "5600" + short_pin
                    result = result.replace(short_pin, pin)
                text = text.replace(match, result)
        return text
