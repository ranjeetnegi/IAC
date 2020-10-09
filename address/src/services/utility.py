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

    def clean_stoping_words(self, text):
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
        text = text.replace("E mail", "").replace("e mail", "").replace("email", "").replace("eMail", "").replace(" mail id ", "")

        text = self.white_space_cleaner(text)
        return text

    def white_space_cleaner(self, text):
        text = re.sub(r"\s+", " ", text).strip()
        return re.sub("\,+", ",", text)

    def replace_white_spaces_single_space(self,text):
        return text.replace("[\s]+", " ")

    def print_address(self, address_list):
        for address in address_list:
            print(address.print_attributes())
