// consulta 
//select * from Aula.Clientes
use('Aula')
db.clientes.find()

// filtro nome = Marcos
use('Aula')
db.clientes.find({nome:"Marcos"})


// varios nomes $in
use('Aula')
db.clientes.find({nome:{$in:['Marcos','Edmilson']}})

//  valores
use('Aula')
db.clientes.find({idade:25})

// pessoas maiores de 18

use('Aula')
db.clientes.find({'idade':{$gt:18}})

/*
Igual a:           $eq
Diferente de:      $ne
Maior que:         $gt
Maior ou igual a:  $gte
Menor que:         $lt
Menor ou igual a:  $lte
Dentro de:         $in
Não dentro de:     $nin
Existe:            $exists
*/
