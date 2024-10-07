class SettingsFile:
    def __init__(self, master_controller):
        self.controller = master_controller
        self.settings_file_name = "settings.ini"
        settings_file = self.open_file_read()
        contents = self.get_values(settings_file)
        self.controller.load_settings(contents)
        settings_file.close()
        self.save_settings(contents)
                
    def open_file_read(self):
        try:
            file = open(self.settings_file_name)
            return file
        except FileNotFoundError:
            file = open(self.settings_file_name, "a")
            return file

    def open_file_write(self):
        try:
            file = open(self.settings_file_name, "w")
            return file
        except FileNotFoundError:
            file = open(self.settings_file_name, "a")
            return file
                       
    def get_values(self, file):
        contents = file.readlines()
        if len(contents) == 4:
            path = self.validate_path(contents[0])
            size = self.validate_size(contents[1])
            filters = self.validate_filters(contents[2])
            inc_digital = self.validate_digital(contents[3])
        else:
            path = self.controller.get_default_path()
            size = self.controller.get_default_size()
            filters = self.controller.get_default_filters()
            inc_digital = self.controller.get_default_digital()
        return [ path, size, filters, inc_digital ]

    def validate_path(self, line_string):
        split_line = line_string.split('=')
        if len(split_line) == 2 and split_line[0] == "path":
            return split_line[1]
        else:
            return self.controller.get_default_path()

    def validate_size(self, line_string):
        sizes = ["small", "normal", "large", "png", "art_crop", "border_crop" ]
        split_line = line_string.split('=')
        if len(split_line) == 2 and split_line[0] == "size":
            if split_line[1] in sizes:
                return split_line[1]
            else:
                return self.controller.get_default_size()

    def validate_filters(self, line_string):
        filters = []
        split_line = line_string.split('=')
        if len(split_line) == 2 and split_line[0] == "filters":
            filters = split_line[1]
            if len(filters) == 23:
                for f in filters:
                    if f not in [ 0, 1]:
                        return self.controller.get_default_filters()
                return filters
            else:
                return self.controller.get_default_filters()

    def validate_digital(self, line_string):
        split_line = line_string.split('=')
        if len(split_line) == 2 and split_line[0] == "digital":
            if split_line[1] not in [ 0, 1 ]:
                return self.controller.get_default_digital()
            else:
                return split_line[1]

    def save_settings(self, settings):
        file = self.open_file_write()
        file.write("path=" + settings[0] + "\n")
        file.write("size=" + settings[1] + "\n")
        file.write("filters=" + str(settings[2]) + "\n")
        file.write("digital=" + str(settings[3]))
        file.close()
