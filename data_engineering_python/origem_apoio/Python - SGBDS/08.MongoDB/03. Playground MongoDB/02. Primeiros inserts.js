// primeiras inserções de dados 
//insertOne  inseri apenas 1 documento

use("Aula")
db.getCollection("clientes").insertOne({
    "nome":"Edmilson",
    "idade":18,
    sexo:"M"
})


// Metodo 2
use('Aula')
db.clientes2.insertOne({    
    nome:"Edmilson",
    idade:18,
    sexo:"M",
    endereco:"Rua x numero 3445 bairoo de baixo"  
})

// insertmany inserindo varios documentos 

use('Aula')
db.clientes.insertMany([
    {nome:"Marcos",idade:25,sexo:"M"},
    {nome:"Mariana",idade:65,sexo:"F",email:"mariana@teste.com.br"},
    {nome:"Julio",idade:37}
])