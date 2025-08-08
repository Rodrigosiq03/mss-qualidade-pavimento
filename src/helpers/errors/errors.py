class BaseError(Exception):
    def __init__(self, message: str):
        self.__message: str = message
        super().__init__(message)

    @property
    def message(self):
        return self.__message

class EntityError(BaseError):
    def __init__(self, message: str):
        super().__init__(f'Campo {message} não é válido')

class MissingParameters(BaseError):
    def __init__(self, message: str):
        super().__init__(f'Campo {message} está faltando')
        
class MissingFiles(BaseError):
    def __init__(self, message: str = None):
        super().__init__(f'Nenhum arquivo foi enviado' if not message else f'Arquivo {message} não encontrado')
        
class WrongTypeParameter(BaseError):
    def __init__(self, fieldName: str, fieldTypeExpected: str, fieldTypeReceived: str):
        super().__init__(f'Campo {fieldName} não está no tipo correto.\n Recebido: {fieldTypeReceived}.\n Esperado: {fieldTypeExpected}')

class NoItemsFound(BaseError):
    def __init__(self, message: str):
        super().__init__(f'Nenhum item encontrado: {message}')

class DuplicatedItem(BaseError):
    def __init__(self, message: str):
        super().__init__(f'Item duplicado: {message}')
        
class ForbiddenAction(BaseError):
    def __init__(self, message: str):
        super().__init__(f'Ação proibida: {message}')

class DatabaseException(BaseError):
    def __init__(self, message: str):
        super().__init__(f'Erro no banco de dados: {message}')