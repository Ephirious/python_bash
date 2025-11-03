class Option:
    description: str
    short_name: str
    full_name: str
    required_argument: bool
    repeatable: bool

    def __init__(self, description: str, short_name: str, full_name: str, required_argument: bool, repeatable: bool):
        """
        Initialize the option metadata container.
        :param description: Human readable description of the option.
        :type description: str
        :param short_name: Short option name (e.g. single character).
        :type short_name: str
        :param full_name: Long option name.
        :type full_name: str
        :param required_argument: Flag indicating whether an argument is required.
        :type required_argument: bool
        :param repeatable: Flag indicating whether the option can be repeated.
        :type repeatable: bool
        :return: None
        :rtype: None
        """
        self.description = description
        self.short_name = short_name
        self.full_name = full_name
        self.required_argument = required_argument
        self.repeatable = repeatable

    def get_description(self):
        """
        Retrieve the option description.
        :return: Human readable description of the option.
        :rtype: str
        """
        return self.description

    def get_short_name(self):
        """
        Retrieve the short option name.
        :return: Short name of the option.
        :rtype: str
        """
        return self.short_name

    def get_full_name(self):
        """
        Retrieve the long option name.
        :return: Long name of the option.
        :rtype: str
        """
        return self.full_name

    def is_required_argument(self):
        """
        Determine whether the option requires an argument.
        :return: Flag indicating if the option expects an argument.
        :rtype: bool
        """
        return self.required_argument

    def is_repeatable(self):
        """
        Determine whether the option can be repeated.
        :return: Flag indicating if the option is repeatable.
        :rtype: bool
        """
        return self.repeatable

    def __eq__(self, other) -> bool:
        """
        Compare this option to another option instance.
        :param other: Object to compare against.
        :type other: Any
        :return: Flag indicating if both options are equal.
        :rtype: bool
        """
        return (isinstance(other, Option)
                and self.description == other.description
                and self.short_name == other.short_name
                and self.full_name == other.full_name
                and self.required_argument == other.required_argument
                and self.repeatable == other.repeatable)

    def __hash__(self):
        """
        Compute the hash for the option instance.
        :return: Hash value for the option.
        :rtype: int
        """
        return hash((self.description,
                     self.short_name,
                     self.full_name,
                     self.required_argument,
                     self.repeatable))