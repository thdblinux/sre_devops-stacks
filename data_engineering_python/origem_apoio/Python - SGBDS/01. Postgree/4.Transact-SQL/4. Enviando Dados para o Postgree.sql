    
   CREATE TABLE IF NOT EXISTS Anac (
        Numero_da_Ocorrencia int,
        Classificacao_da_Ocorrencia VARCHAR(50),
        Data_da_Ocorrencia DATE,
        Municipio VARCHAR(50),
        UF VARCHAR(30),
        Regiao VARCHAR(30),
        Nome_do_Fabricante VARCHAR(100)
    )

insert into Anac (     
			Numero_da_Ocorrencia, 
            Classificacao_da_Ocorrencia, 
            Data_da_Ocorrencia, 
            Municipio, 
            UF, 
            Regiao, 
            Nome_do_Fabricante
        ) VALUES (
			1,
			'Acidente',
			'2022-01-01',
			'São Paulo',
			'SP',
			'Sudeste',
			'Jatinho 333')

