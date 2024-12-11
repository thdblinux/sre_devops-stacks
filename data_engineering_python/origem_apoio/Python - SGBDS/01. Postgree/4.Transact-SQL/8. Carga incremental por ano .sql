--criando coluna de ano 
select
extract(year from "Data_da_Ocorrencia") as ano,
* 
from public.anac_sqlalchemy;


-- trazendo anos distintos
select distinct
extract(year from "Data_da_Ocorrencia") as ano
from public.anac_sqlalchemy
order by 1 desc;


-- filtrando ano atual 
select
extract(year from "Data_da_Ocorrencia") as ano,
extract(year from current_date) as ano_atual,
* 
from public.anac_sqlalchemy
where extract(year from "Data_da_Ocorrencia")= extract(year from current_date)

-- Criando delete ano atual

delete from public.anac_sqlalchemy
where extract(year from "Data_da_Ocorrencia")= extract(year from current_date)



