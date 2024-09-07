class ItemError(BaseException):
    pass


class CollectionItem():
    allowed_attrs = [
        "description",
        "url",
        "request",
        "response_handler",
        "cache_dir",
        "url_parser"
    ]

    def __init__(self, *args, **kwargs):
        # print(kwargs)

        for i in args:
            if not isinstance(i, dict):
                raise ItemError(f"Item is not a dict type")

            for k, v in i.items():
                if k in CollectionItem.allowed_attrs:
                    self.__setattr__(k, v)

        for k, v in kwargs.items():
            if k in CollectionItem.allowed_attrs:
                self.__setattr__(k, v)



if __name__ == "__main__":
    from zenify.url import Url
    from zenify.response.handler.json import JsonResponseHandler
    from zenify.collection.bucket import CollectionBucket

    # Create an empty bucket
    bucket = CollectionBucket()


    item1 = CollectionItem(url=Url("http://one.one.com"),
                           request="empty_request",
                           response_handler=JsonResponseHandler(),
                           x="a")

    bucket.add(item1)

    my_item_dict = {
        "url": Url("http://two.two.com"),
        "request": "empty",
        "response_handler": JsonResponseHandler()
    }

    item2 = CollectionItem(my_item_dict)

    bucket.add(item2)

    print("Item 1:".ljust(20), item1.__dict__)
    print("Item 1 url:".ljust(20), item1.url)

    print("Bucket container".ljust(20), bucket)
    print("Total items in container:".ljust(20), len(bucket.container()))
    for item in bucket.container():
        print("\tItem key:", item)
        for k, v in vars(item).items():
            print("\t\t", k, "=>", v)
    # [print(var) for var in vars(item) for item in bucket.container()]

