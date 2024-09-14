import inspect

class Settings:
    def __init__(self):
        pass


if __name__ == "__main__":
    abc = "123"

    # get_var_name(abc)


    s = Settings()
    s.add_var(abc)
    print(vars(s))
    # print(s.abc)
