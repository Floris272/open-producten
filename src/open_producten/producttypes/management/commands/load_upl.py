from ..parsers import ParserCommand
from ..utils import load_upn


class Command(ParserCommand):
    plural_object_name = "upn"

    def handle(self, **options):
        super().handle(load_upn, **options)
