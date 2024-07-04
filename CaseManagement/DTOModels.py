import json


max_name_length = 120

class BaseDTO():
    @classmethod
    def verify_parameters(cls, properties: dict):
        keys_to_remove = []
        for key in properties.keys():
            if key not in cls.__dict__.keys():
                keys_to_remove.append(key)
                # raise KeyError(f"That argument `{key}` is not valid!")
        return keys_to_remove
    
    def is_valid(self, properties: dict) -> bool:
        raise NotImplementedError()

    def set_properties(self, props):
        properties_to_ignore = self.verify_parameters(props)
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
        if self.is_valid(loaded_properties):
            self.set_properties(loaded_properties)
        else:
            raise RuntimeError(f"Request object was not valid. Request: {properties}")

    def __str__(self) -> str:
        return json.dumps(self.get_dict())
    
    def get_dict(self) -> dict:
        return {
            "name": self.name,
            "users": self.users,
            "adminUsers": self.adminUsers
        }
    
    def is_valid(self, properties: dict) -> bool:
        validation_checks = [True]
        if properties["name"] is None or properties["name"] == "" or len(properties["name"]) > max_name_length:
            validation_checks.append(False)
        
        if properties["users"] is None:
            properties["users"] = []
        elif isinstance(properties["users"], str):
            pass

        if properties["adminUsers"] is None:
            validation_checks.append(False)

        return all(validation_checks)

class DTOCaseFile(BaseDTO):
    organization: dict = {}
    status: str = "ACTIVE"
    caseIdentifier: str = ""

    def __init__(self, *args, **kwargs) -> None:
        properties: str = kwargs.get("properties")
        loaded_properties: dict = json.loads(properties)
        if self.is_valid(loaded_properties):
            self.set_properties(loaded_properties)
        else:
            raise RuntimeError(f"Request object was not valid. Request: {properties}")

    def __str__(self) -> str:
        return json.dumps(self.get_dict())
    
    def get_dict(self) -> dict:
        return {
            "organization": self.organization,
            "status": self.status,
            "caseIdentifier": self.caseIdentifier
        }
    
    def is_valid(self, properties: dict) -> bool:
        validation_checks = [True]
        if properties["caseIdentifier"] is None or properties["caseIdentifier"] == "" or len(properties["caseIdentifier"]) > max_name_length:
            validation_checks.append(False)
        
        if properties["organization"] is None:
            validation_checks.append(False)
        
        # TODO: this needs refactored so that we don't use a hardcoded list.
        # We can't import the list from CaseFile model though for circular import.
        # Most likely the way to do it is to change the CaseFile.get_dto() to instead be
        # DTOCaseFile.get_model() and use that instead. That will allow us to get around the
        # circular import to pull in that hardcoded list.
        elif "status" in properties.keys() and properties["status"] not in ["PENDING", "INACTIVE","ACTIVE","ARCHIVE","LONGTERM MONITOR","DECEASED"]:
            validation_checks.append(False)

        return all(validation_checks)

class DTOTargetOfInterest():
    firstName = ""
    middleNames = ""
    lastName = ""
    fullName = ""
    additionalNames = ""
    dateOfBirth = ""
    currentAddress = ""
