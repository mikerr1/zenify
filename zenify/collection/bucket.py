from zenify.collection.item import CollectionItem

class CollectionBucket():
    def __init__(self):
        self.__number_of_items = 0
        self.__container = []
        pass

    def add(self, item: CollectionItem):
        self.__container.append(item)
        self.__number_of_items += 1

    def container(self) -> list:
        return self.__container

    def get_items(self) -> list:
        return self.__container

