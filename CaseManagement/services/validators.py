class Validators:
    MAX_STRING_LENGTH: int = 2000

    @classmethod
    def is_valid_tag(cls, tag_request: dict) -> bool:
        result = []
        if "key" in tag_request.keys() and "value" in tag_request.keys():
            if isinstance(tag_request["key"], list):
                result.append(cls._is_valid_list(tag_request["key"]))
            
            if isinstance(tag_request["value"], list):
                result.append(cls._is_valid_list(tag_request["value"]))
            
            if isinstance(tag_request["key"], str):
                result.append(cls._is_valid_tag_key(tag_request["key"]))
            
            if isinstance(tag_request["value"], str):
                result.append(cls._is_valid_str(tag_request["value"]))


        else:
            result.append(False)

        return all(result)
        
    @classmethod
    def _is_valid_list(cls, the_list: list) -> bool:
        result = []
        
        result.append(len(the_list) > 0)

        return all(result)
    
    @classmethod
    def _is_valid_tag_key(cls, the_key: str) -> bool:
        result = []

        result.append(len(the_key) < 256)

        return all(result)
    
    @classmethod
    def _is_valid_str(cls, the_string: str) -> bool:
        result = []

        result.append(len(the_string) < cls.MAX_STRING_LENGTH)

        return all(result)
            