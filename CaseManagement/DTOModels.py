import json


class BaseDTO():
    @classmethod
    def validate_parameters(cls, properties: dict):
        keys_to_remove = []
        for key in properties.keys():
            if key not in cls.__dict__.keys():
                keys_to_remove.append(key)
                # raise KeyError(f"That argument `{key}` is not valid!")
        return keys_to_remove

    def set_properties(self, props):
        properties_to_ignore = self.validate_parameters(props)
        for key, value in props.items():
            if key not in properties_to_ignore:
                setattr(self, key, value)

class DTOOrganization(BaseDTO):
    name: str = ""
    users: list|str = ""
    adminUsers: list|str = ""
    
    def __init__(self, *args, **kwargs) -> None:
        properties: str = kwargs.get("properties")
        loaded_properties: dict = json.loads(properties)
        self.set_properties(loaded_properties)

    def __str__(self) -> str:
        return json.dumps(self.get_dict())
    
    def get_dict(self) -> dict:
        return {
            "name": self.name,
            "users": self.users,
            "adminUsers": self.adminUsers
        }

class DTOCaseFile(BaseDTO):
    organization: dict = {}
    status: str  = ""
    caseIdentifier: str = ""

    def __init__(self, *args, **kwargs) -> None:
        properties: str = kwargs.get("properties")
        loaded_properties: dict = json.loads(properties)
        self.set_properties(loaded_properties)

    def __str__(self) -> str:
        return json.dumps(self.get_dict())
    
    def get_dict(self) -> dict:
        return {
            "organization": self.organization,
            "status": self.status,
            "caseIdentifier": self.caseIdentifier
        }

class DTOTargetOfInterest():
    firstName = ""
    middleNames = ""
    lastName = ""
    fullName = ""
    additionalNames = ""
    dateOfBirth = ""
    currentAddress = ""
