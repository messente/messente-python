# -*- coding: utf-8 -*-


class MessenteError(Exception):
    pass


class ConfigurationError(MessenteError):
    pass


class ApiError(MessenteError):
    pass


class InvalidMessageError(MessenteError):
    pass


ERROR_CODES = {
    "ERROR 101": " ".join([
        "Access is restricted, wrong credentials.",
        "Check the username and password values.",
    ]),
    "ERROR 102": " ".join([
        "Parameters are wrong or missing.",
        "Check that all the required parameters are present.",
    ]),
    "ERROR 103": " ".join([
        "Invalid IP address.",
        "The IP address you made the request from,",
        "is not in the API whitelist settings.",
    ]),
    "FAILED 209": " ".join([
        "Server failure, try again after a few seconds or",
        "try the backup server.",
    ]),
}
