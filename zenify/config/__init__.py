class Config:
    def __init__(self):
        self.__config_file = None
        self.__configs = None
        self.__env = None

    def set_config_file(self,
                        file_path: str | None = None
                        ):
        self.__config_file = file_path
        self.__configs = {}


    def load(self):
        f = open(self.__config_file, "r")
        for line in f.readlines():
            if line.strip() == "":
                continue
            if ";" in line.strip()[0]:
                continue
            # print(len(line.strip()), line.strip(), line.strip() == "")

            key = line.split("=")[0].strip()
            value = line.split("=")[1].strip()
            self.__setattr__(key, value)
            self.__configs[key] = value
        f.close()

    def get_config(self, key=None):
        return self.__configs[key]

    def __str__(self):
        string = "<Zenify Config Obj>\n"
        for k, v in self.__configs.items():
            string += " => ".join([str(k), str(v)])
            string += "\n"
        # return str("env: " + str(self.__env) + "\n" + str(self.__configs))
        return string