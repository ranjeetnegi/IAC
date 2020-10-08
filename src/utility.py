from datetime import date, time, datetime


class Utility:
    def __init__(self):
        pass

    def genrate_output_file_name(self, file_base_name):
        now = datetime.now()
        file_name_prefix_date = date.today().strftime("%Y%m%d")
        file_name_prefix_time = str(now.hour) + str(now.minute) + str(now.second)
        return "%s_%s_%s" % (
            file_name_prefix_date,
            file_name_prefix_time,
            file_base_name,
        )
