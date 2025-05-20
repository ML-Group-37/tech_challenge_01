from enum import Enum


class ProcessamentoSubTables(str, Enum):
    sub_table1 = "Viníferas"
    sub_table2 = "Americanas e híbridas"
    sub_table3 = "Uvas de mesa"
    sub_table4 = "Sem classificação"


class ImportacaoSubTables(str, Enum):
    sub_table1 = "Vinhos de mesa"
    sub_table2 = "Espumantes"
    sub_table3 = "Uvas frescas"
    sub_table4 = "Uvas passas"
    sub_table5 = "Suco de uva"


class ExportacaoSubTables(str, Enum):
    sub_table1 = "Vinhos de mesa"
    sub_table2 = "Espumantes"
    sub_table3 = "Uvas frescas"
    sub_table4 = "Suco de uva"
