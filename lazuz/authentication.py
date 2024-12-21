from lazuz.config import ApiCalls


def authentication_token() -> str:
    authentication = ApiCalls()["authentication"]

    response = authentication.request()

    return response.json()["result"]["accessToken"]
