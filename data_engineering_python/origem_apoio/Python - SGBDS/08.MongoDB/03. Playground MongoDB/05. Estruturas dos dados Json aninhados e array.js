


//objeto JSON aninhado um objeto pode conter outros objetos como seus valores (subcategorias) ou tabela referencia no SQL

// estrutura de inerção
use('Aula')
db.clientes.insertMany([{},{}])

// insert aninhado
use('Aula')
db.clientes.insertMany([
    {"nome":"Lilian",   
    "idade": 25,
    "sexo": "F",
    "email": "lilian@teste222.com.br",
    "endereco":{rua:"rua x",
                numero:78,
                completomento:"casa"
            }

    }

]
)

use('Aula')
db.clientes.find({nome:"Lilian"})



//array  uma coleção de elementos do mesmo tipo

use('Aula')
db.clientes.insertMany([
    {"nome":"Matheus",   
    "idade": 45,
    "sexo": "M",
    "email": "Matheus@teste222.com.br",
    "endereco":{rua:"rua y",
                numero:88,
                completomento:"Apartamento"
            }

    }
,

{"nome":"Matias",   
"idade": 55,
"sexo": "M",
"email": "Matias@teste222.com.br",
"cores_preferidas":["Preto","Verde"],
"endereco":{rua:"rua sy",
            numero:98,
            completomento:"Apartamento"
        },
"lista_numeros":[20,30,56,89]

}

]
)