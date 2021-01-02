from datetime import date, datetime
import re


class Utility:
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
        text = text.replace("<", " ")
        text = text.replace(">", " ")
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

        matches = re.findall(r"[^0-9],",text)
        for match in matches:
            result = match.replace(",", " ")
            text = text.replace(match, result)

        return text

    def clean_slash_remover(self, text):
        text = re.sub(r"/[^a-zA-Z0-9]]", "", text)
        return text

    def empty_brackets_remover(self,text):
        text = re.sub(r"\(+\)+", "", text)
        text = re.sub(r"\(+[ ]+\)+", "", text)
        return text

    def replace_white_spaces_single_space(self, text):
        return text.replace("[\s]+", " ").strip()

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
                                   u"\U000024C2-\U0001F251"
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
