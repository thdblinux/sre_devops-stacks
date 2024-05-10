## Nginx

### O papel de um servidor web  na prática, via de regra.
 Um servidor web vai ficar esperando uma conexão chegar. Quando ela chegar, o servidor web faz seu trabalho, garantindo que a mensagem recebida está no formato `HTTP` e depois fazendo o que deve fazer segundo suas configurações.
  
### Mas como o nginx e o computador sabem o que significa "localhost"?
Todo `sistema operacional` possui um arquivo de hosts. No `Linux`, por padrão fica em `/etc/hosts`. No Mac, `/private/etc/hosts`. Já no` Windows`, `C:\Windows\System32\Drivers\Etc\hosts`. Esse arquivo informa ao sistema operacional que quando uma conexão for estabelecida usando algum nome, o` IP` correspondente deve ser usado. Para o nome` localhost`, temos o IP da nossa própria máquina `(127.0.0.1)`.

### Install nginx whith Docker
```sh
docker run --name docker-nginx -p 80:80 -d nginx
```
```sh
Output
b91f3ce26553f3ffc8115d2a8a3ad2706142e73d56dc279095f673580986257
```
```sh
docker ps
```
```sh
Output
CONTAINER ID   IMAGE     COMMAND                  CREATED          STATUS          PORTS                               NAMES
b91f3ce26553   nginx     "/docker-entrypoint.…"   56 seconds ago   Up 54 seconds   0.0.0.0:80->80/tcp, :::80->80/tcp   docker-nginx
```

```sh
navegador web
localhost:80
```

```sh
docker stop docker-nginx
```
```sh
docker rm docker-nginx
```
```sh
mkdir -p ~/docker-nginx/html
```

```sh
cd ~/docker-nginx/html
```
```sh
vim index.html
```

```html
<html>
  <head>
    <title>Docker nginx Tutorial</title>
  </head>

  <body>
    <div class="container">
      <h1>This is the way!</h1>
      <p>This Nginx page is brought to you by Docker</p>
    </div>
  </body>
</html>
```

```sh
docker run --name docker-nginx -p 80:80 -d -v ~/docker-nginx/html:/usr/share/nginx/html nginx
```
```sh
navegador web
localhost:80
```
![alt text](/nginx/nginx1.png)

### Como saber onde está o arquivo de configuração principal?
Este comando nos fornece diversas informações. Ao digitarmos `nginx -h` uma ajuda é exibida, e lá podemos ver o caminho do arquivo de configuração.

```sh
root@d4af018e55e6:/# nginx -h
```
**Output** 
```sh
nginx version: nginx/1.25.5
Usage: nginx [-?hvVtTq] [-s signal] [-p prefix]
             [-e filename] [-c filename] [-g directives]

Options:
  -?,-h         : this help
  -v            : show version and exit
  -V            : show version and configure options then exit
  -t            : test configuration and exit
  -T            : test configuration, dump it and exit
  -q            : suppress non-error messages during configuration testing
  -s signal     : send signal to a master process: stop, quit, reopen, reload
  -p prefix     : set prefix path (default: /etc/nginx/)
  -e filename   : set error log file (default: /var/log/nginx/error.log)
  -c filename   : set configuration file (default: /etc/nginx/nginx.conf)
  -g directives : set global directives out of configuration file
```
**Comands nginx CLI**
**For example**
```sh
 nginx -s reload 
```

```sh
 nginx -s stop 
```
```sh
 nginx -s quit
```
## Criando um servidor
```sh
server {
    listen 80;
    server_name localhost;

    location / {
        root /usr/share/nginx/html;
        index index.html
    }
}
```

Finalmente configuramos um servidor web, usando a diretiva server e dentro dela temos a diretiva chamada location.

- Qual o propósito dessa diretiva location na configuração de um servidor web no nginx? <p>
Informar qual caminho acessado cairá nas regras a seguir<p>
Se definirmos um location /, tudo que começar com / (que no caso é literalmente tudo) cairá nesse conjunto de regras. Nessas regras podemos definir qual o diretório raiz do projeto, qual o arquivo padrão, regras de redirecionamento, etc.

## Criando uma pagina de erro no nginx

Infelizmente quando desenvolvemos uma aplicação, um site ou um sistema, erros acontecem.
Quando estamos falando de` HTTP`, erros são representados através de códigos` HTTP`. De novo, por isso é importante fazermos o treinamento de` HTTP`, para entendermos melhor como isso funciona, mas eu vou super simplificar um conceito aqui.<p>
Se aconteceu algum erro e estamos utilizando bem o` HTTP`, um código de resposta é devolvido. Então, o código de erro `“404”` indica que algum recurso que eu estou tentando acessar não foi encontrado.<p>
O código `“200”` indica que está tudo OK, que nós encontramos o que tinha que encontrar e processamos o que tinha que processar. 
Então existem diversos códigos` HTTP`.<p>
Os códigos de erro estão na faixa` “400”` quando é algum erro do cliente, ou seja, o cliente digitou a URL errada, por exemplo. Ou na faixa `“500”` quando é erro no servidor. Então, por exemplo: o servidor não está disponível, o servidor de aplicação caiu, meu banco de dados está fora ou alguma coisa assim.
- Então vamos configurar exatamente o erro `“404”` para ser direcionado para uma página nossa, uma página que nós podemos configurar como quisermos, deixar ela bonita etc.
```sh
server {
    listen 80;
    server_name localhost;

    location / {
        root /usr/share/nginx/html;
        index index.html
    }
    error_page 404 400 401 /erro.html;
}
```
```sh
root@d4af018e55e6:/usr/share/nginx/html# nginx -t
nginx: the configuration file /etc/nginx/nginx.conf syntax is ok
nginx: configuration file /etc/nginx/nginx.conf test is successful
```

```sh
root@d4af018e55e6:/usr/share/nginx/html# vim erro.html
```
```sh
erro code 400
```

```sh
root@d4af018e55e6:/usr/share/nginx/html# nginx -s reload
2024/05/04 22:22:31 [notice] 428#428: signal process started
```
```sh
localhost/erro.html  
```
![alt text](/nginx/nginx2.png)

## Proxy Reverso
Por que o nome é Proxy REVERSO e não apenas Proxy?
Porque normalmente um proxy fica no lado do cliente

O conceito padrão de proxy é algo que fica no lado do cliente interceptando os pacotes de rede. Como nesse caso o proxy está no lado do servidor, chamamos de proxy reverso.

**Configurando o proxy reverso com NGINX**
```sh
server {
    listen 80;
    server_name localhost;

    location / {
        proxy_pass http://localhost;
    }
    error_page 404 400 401 /erro.html;
}
```
