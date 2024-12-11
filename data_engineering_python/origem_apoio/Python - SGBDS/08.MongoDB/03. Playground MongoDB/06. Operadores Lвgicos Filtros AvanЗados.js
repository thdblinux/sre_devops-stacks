//Operadores Lógicos

// https://www.mongodb.com/pt-br/docs/manual/reference/operator/query-logical/
use('Aula')
db.anac.find()

//  filtros e escolher colunas 
//$and traz resultado quando cumpre todos criterios
use('Aula')
db.anac.find({$and:[{UF:"MG"},{Classificacao_da_Ocorrência:"Acidente"}]},
    {Numero_da_Ocorrencia:1,Classificacao_da_Ocorrência:1,UF:1,PSSO:1}
    )


//$not traz resultado quando Não cumpre o criterios (nega alguma coisa) 
use('Aula')
db.anac.find({UF:{$not:{$eq:"MG"}}},
    {Numero_da_Ocorrencia:1,Classificacao_da_Ocorrência:1,UF:1,PSSO:1}
    )

//$nor traz resultado quando nao oberecem os criterios   
use('Aula')
db.anac.find({$nor:[{UF:"MG"},{Classificacao_da_Ocorrência:"Acidente"}]},
    {Numero_da_Ocorrencia:1,Classificacao_da_Ocorrência:1,UF:1,PSSO:1}
    )   
//$nor exemplo2
use('Aula')
db.anac.find({$nor:[{UF:"SP"},{PSSO: "falso"}]},
    {Numero_da_Ocorrencia:1,Classificacao_da_Ocorrência:1,UF:1,PSSO:1}
    )
    
    
//$or  Traz resultado quando tiver qualquer um dos criterios
use('Aula')
db.anac.find({$or:[{UF:"GO"},{PSSO:"verdadeiro"}]},
    {Numero_da_Ocorrencia:1,Classificacao_da_Ocorrência:1,UF:1,PSSO:1}
    )

/*
$and Une cláusulas de query com um AND lógico e retorna todos os documentos que correspondem às condições de ambas as cláusulas.
$not Inverte o efeito de uma expressão de query e retorna documentos que não correspondem à expressão de query.
$or Une cláusulas de query com um OR lógico e retorna todos os documentos que correspondem às condições de qualquer cláusula.
$nor Une cláusulas de query com um NOR lógico e retorna todos os documentos que não correspondem a ambas as cláusulas.

*/
