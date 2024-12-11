
-- Rodar notebook 7. Enviando dados para Postgree com sqlalchemy para ter os dados completos

---  filtro de data manual 
select * from public.anac_sqlalchemy
where "Data_da_Ocorrencia" >='2023-10-16'


-- filtrando ultimos 3 meses
select * from  public.anac_sqlalchemy
WHERE "Data_da_Ocorrencia" >= CURRENT_DATE - INTERVAL '3 months';


-- validando ultimos 3 meses 
select  CURRENT_DATE - INTERVAL '3 months';

-- delete da base 
delete from public.anac_sqlalchemy	
WHERE "Data_da_Ocorrencia" >= CURRENT_DATE - INTERVAL '3 months';