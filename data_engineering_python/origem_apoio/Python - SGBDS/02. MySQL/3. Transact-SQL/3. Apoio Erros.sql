SHOW VARIABLES;

# padrão tempo limite de espera por bloqueio (lock wait timeout) é de 50 segundos
SHOW VARIABLES LIKE 'innodb_lock_wait_timeout';

#alterar para 300
SET GLOBAL innodb_lock_wait_timeout = 300;

