// selecionando apenas algumas colunas
use('Aula')
db.clientes.find({'idade':{$gt:18}},{email:0})



use('Aula')
db.clientes.find({},{email:0,'sexo':0  })
