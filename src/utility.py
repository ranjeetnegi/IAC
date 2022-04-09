from datetime import date, datetime
import re
from src.districtmapper import DistrictMapper
from src.statemapper import StateMapper


class Utility:
    def __init__(self, phone_lookup):
        self.district_mapper = DistrictMapper()
        self.state_mapper = StateMapper()
        self.phone_lookup = phone_lookup

    def generate_output_file_name(self, file_base_name, extension):
        now = datetime.now()
        file_name_prefix_date = date.today().strftime("%Y%m%d")
        file_name_prefix_time = str(now.hour) + str(now.minute) + str(now.second)
        return "%s_%s_%s.%s" % (file_name_prefix_date, file_name_prefix_time, file_base_name, extension)

    def reverse_list(self, lst):
        return lst[::-1]

    def clean_stopping_words_and_phrases(self, text):
        text = self.phrases_cleaner(text)

        text = text.replace("\n", ",")
        # email cleanup
        text = re.sub(r"([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)", "", text)

        text = re.sub(r"[,]+", ",", text)
        # dot clean up
        text = text.replace(".", " ")
        # Colon cleanup
        text = text.replace(":", " ")
        # semi colon cleanup
        text = text.replace(";", " ")
        text = text.replace("|", " ")
        # - cleanup
        text = text.replace("-", " ")
        # +91
        text = text.replace("+91", " ")
        text = text.replace("=", " ")
        text = text.replace("tq", "Tq")
        text = text.replace("taluk", "Tq")
        text = text.replace("(post)", "post")
        text = text.replace("(p)", " post ")
        text = text.replace("(v)", " village ")
        text = text.replace("(t)", " Tq ")
        text = text.replace("(d)", " dist ")
        text = text.replace("(state)", "state")
        text = text.replace("(villege)", " village ")
        # text = text.replace("<", " ")
        # text = text.replace(">", " ")
        text = text.replace("[", " ")
        text = text.replace("]", " ")
        text = text.replace("father", "S/O")

        text = text.replace("&", " and ")

        text = text.replace('"', " ")
        text = text.replace("*", "")
        text = text.replace("((", "(").replace("( ", "(")
        text = text.replace("))", ")").replace(" )", ")")
        text = re.sub(r"/ ", " ", text)
        text = re.sub(r"%", "", text)
        text = text.replace("address", "")
        text = re.sub("house no[ .:=\/\-*#~]+", "#", text)
        text = re.sub("house no", "#", text)

        # Hash Replacer
        text = re.sub("[#]+", "#", text)
        hash_matches = re.findall("#[^0-9]", text)
        if len(hash_matches) > 0:
            for match in hash_matches:
                replacer = match.replace("#", "")
                text = text.replace(match, replacer)
        text = self.white_space_cleaner(text)
        return text

    def phrases_cleaner(self, text):
        text = text.replace("plz comment madi in this format", "")
        text = text.replace("email", "")
        text = text.replace("name,", "").replace("name", "")
        text = text.replace("code", " ")
        text = text.replace("number", " ")
        text = text.replace(" num ", " ")
        text = text.replace("(p)", " post")
        text = text.replace("pincod", " pin ")
        text = text.replace(" number ", " ")
        text = text.replace("e mail", "").replace("email", "").replace("mail id", "")
        text = text.replace("satet", "state")
        text = text.replace(" Dt ", "Dist")
        return text

    def white_space_cleaner(self, text):
        text = self.remove_emoji(text)
        text = self.replace_white_spaces_single_space(text)
        text = self.comma_space_remover(text)
        text = self.empty_brackets_remover(text)
        text = self.clean_slash_remover(text)
        return text

    def comma_space_remover(self, text):
        # "     ," => ", "
        text = re.sub("[ ]+,", ", ", text)
        # ",,,,,,,,,"
        text = re.sub(',+', ", ", text)
        # leading commas
        text = re.sub(r"^,+", "", text)
        # ",,,,,,,,,         "
        text = re.sub(r",+[ ]+", ", ", text)
        # ",,,,,,,      ,,,,,,,,"
        text = re.sub(r"\,+[ ]+\,+", ", ", text)
        # "            ,,,,,,,,,,,,,"
        text = re.sub(r"[ ]+,+", ",", text)

        matches = re.findall(r"[^0-9],", text)
        for match in matches:
            result = match.replace(",", " ")
            text = text.replace(match, result)

        return text

    def clean_slash_remover(self, text):
        text = re.sub(r"/[^a-zA-Z0-9]]", "", text)
        return text

    def empty_brackets_remover(self, text):
        text = re.sub(r"\(+\)+", "", text)
        text = re.sub(r"\(+[ ]+\)+", "", text)
        return text

    def replace_white_spaces_single_space(self, text):
        return ' '.join(text.split())

    def print_address(self, address_list, diff=False):
        if diff is False:
            for address in address_list:
                print(address.print_attributes())
        else:
            for address in address_list:
                print("Old : " + address.address_old)
                print("New : " + address.address)

    # emoji Remover function
    def remove_emoji(self, text):
        emoji_pattern = re.compile("["
                                   u"\U0001F600-\U0001F64F"  # emoticons
                                   u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                                   u"\U0001F680-\U0001F6FF"  # transport & map symbols
                                   u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                                   u"\U00002702-\U000027B0"
                                   # u"\U000024C2-\U0001F251"
                                   "]+", flags=re.UNICODE)
        return emoji_pattern.sub(r'', text)

    def house_keeping(self, address_obj):
        address_text = address_obj.address
        text = self.remove_emoji(address_text)

        address_obj.address = text
        return text

    def is_valid_address(self, text):
        if len(re.findall(r"end-to-end encrypted", text)) > 0:
            return False
        return True

    def update_address_name(self, address):
        name_regex = "\[.*?\]|.*?\]"
        address_text = address.address
        name_regexes = re.findall(name_regex, address_text)
        if len(name_regexes) > 0:
            for name_regex in name_regexes:
                first_char = name_regex[0]
                if first_char == '[':
                    name = name_regex[1:-1]
                else:
                    name = name_regex[:-1]
                address_text = address_text.replace(name_regex, name)
                address.name = name
                address.address = address_text

    def star_remover(self, text):
        return text.replace("*", " ").strip()

    def whatsapp_text(self, address_text):
        address_text = address_text.lower()
        if address_text.find("भेज दी जी सेवा") != -1 or address_text.find("media omitted") != -1 or address_text.find(
                "this message was deleted") != -1 or address_text.find("end-to-end encrypted") != -1 or address_text.find(
            "message was deleted") != -1 or address_text.find("security code with") != -1 or address_text.find(
            "ou added") != -1 or address_text.find("removed") != -1:
            return True
        return False

    def get_data_from_address(self, address_string):
        dist_state, count = self.district_mapper.get_state_dist_from_add_string_by_add_rec(address_string)
        if dist_state is not None and len(dist_state) > 0 and count == 1:
            dist, state = dist_state.split(",")
            return state,dist,count
        elif count > 0:
            return dist_state,dist_state,count
        state = self.state_mapper.getStateFromString(address_string)
        if state is not None:
            return None, state, 0
        return None, None, 0

    def is_string_same(self, dist_add, district):
        output = "YES"
        if dist_add is None:
            return "NO"
        if district is None:
            return "NO"

        if dist_add.lower() == district.lower() :
            return output
        else:
            return "NO"

    def adjust_duplicate(self, add_list):
        new_address_list = []
        map = {}
        for add in add_list:
            if add.is_reorder and add.phone is not None:
                key_exists, key = self.has_key(add.phone, map)
                if key_exists:
                    map.get(key).append(add)
                else:
                    map[key] = [add]
            else:
                new_address_list.append(add)

        for key in map.keys():
            for add in map.get(key):
                if add is not None:
                    new_address_list.append(add)
        return new_address_list

    def has_key(self, phones, dict):
        phone_list = phones.split(",")
        if len(phone_list) == 1:
            if dict.get(phones[0]) is not None:
                return True, phones[0]
            else:
                for key in dict.keys():
                    if key.find(phones[0]) >= 0:
                        return True, key
        elif len(phone_list) > 1:
            for phone in phone_list:
                if dict.get(phone) is not None:
                    return True, phone

            for key in dict.keys():
                if phones.find(key) >= 0:
                    return True, phones
        return False, phones

    def update_reorder_and_repeat(self, address_list):
        phone_number_set = set()
        for address in address_list:
            if address.phone is not None:
                phone_set = set(address.phone.split(","))
                if len(phone_set & phone_number_set) > 1:
                    address.is_repeat = True
                phone_number_set.update(phone_set)

                for phone in phone_set:
                    is_reorder = self.phone_lookup.search_phone_number(phone)
                    if is_reorder:
                        address.is_reorder = is_reorder
                    else:
                        self.phone_lookup.save_phone_number(int(phone))