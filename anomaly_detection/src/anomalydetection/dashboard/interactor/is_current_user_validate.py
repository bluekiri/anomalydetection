
class IsCurrentUserValidate(object):

    def __init__(self, request) -> None:
        super().__init__()
        print(request)

    def is_authenticated(self) -> bool:
        return False
