from enum import IntEnum, StrEnum


class StatusEnum(StrEnum):
    CADASTRADO = 'Cadastrado'
    ATIVO = 'Ativo'
    CANCELADO = 'Cancelado'
    AG_MODIFICACAO = 'Ag. modificação'


class ContaTipoEnum(StrEnum):
    CORRENTE = 'Corrente'
    POUPANCA = 'Poupança'
    INVESTIMENTO = 'Investimento'


class ImovelTipoEnum(StrEnum):
    CASA = 'Casa'
    APARTAMENTO = 'Apartamento'
    SOBRADO = 'Sobrado'


ContaStatusEnum = StatusEnum
ImovelStatusEnum = StatusEnum
UsuarioStatusEnum = StatusEnum