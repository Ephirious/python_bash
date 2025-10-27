class Option:
    description: str
    short_name: str
    full_name: str
    required_argument: bool
    repeatable: bool

    def __init__(self, description: str, short_name: str, full_name: str, required_argument: bool, repeatable: bool):
        self.description = description
        self.short_name = short_name
        self.full_name = full_name
        self.required_argument = required_argument
        self.repeatable = repeatable

    def get_description(self):
        return self.description

    def get_short_name(self):
        return self.short_name

    def get_full_name(self):
        return self.full_name

    def is_required_argument(self):
        return self.required_argument

    def is_repeatable(self):
        return self.repeatable

    def __eq__(self, other) -> bool:
        return (isinstance(other, Option)
                and self.description == other.description
                and self.short_name == other.short_name
                and self.full_name == other.full_name
                and self.required_argument == other.required_argument
                and self.repeatable == other.repeatable)

    def __hash__(self):
        return hash((self.description,
                     self.short_name,
                     self.full_name,
                     self.required_argument,
                     self.repeatable))