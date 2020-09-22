from models.message import Message
from exceptions.invalid_message import InvalidMessage


class Handler:

    def process_message(self, message):
        raise NotImplementedError("Subclass must implement abstract method")

    def validate_message(self, message, required_fields=None, prop_values=None):
        if required_fields:
            for field in required_fields:
                if not getattr(message, field):
                    raise InvalidMessage(f"{field} is required field!")
        if prop_values:
            for prop, values in prop_values:
                if getattr(message, prop) not in values:
                    raise InvalidMessage(f'{prop} must be one of {", ".join(values)}')

    @staticmethod
    def form_success_msg(**kwargs):
        return Message(success=True, **kwargs)

    @staticmethod
    def form_success_server_msg(**kwargs):
        return Handler.form_success_msg(sender='server', **kwargs)

    @staticmethod
    def form_error_msg(**kwargs):
        return Message(success=False, **kwargs)

    @staticmethod
    def form_error_server_msg(**kwargs):
        return Handler.form_error_msg(sender='server', **kwargs)
