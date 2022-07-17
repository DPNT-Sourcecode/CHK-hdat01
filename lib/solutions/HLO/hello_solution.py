

# noinspection PyUnusedLocal
# friend_name = unicode string
def hello(friend_name: str):

    if not isinstance(friend_name, str):
        raise TypeError("friend_name must be a string")

    output_string = f"Hello, {friend_name}!"
    return output_string
