# Introdução Essencial ao gRPC com Go: Tutorial Básico
![alt text](/assets/public/gRPC_go.png)

Este tutorial fornece uma introdução básica ao programador Go sobre como trabalhar com gRPC.

**Ao seguir este exemplo, você aprenderá como:**

- Defina um service em um `.proto` file.
- Gere código de servidor e cliente usando o compilador de buffer de protocolo.
- Use a API Go gRPC para escrever um cliente e servidor simples para seu service.
Ele pressupõe que você leu a Introdução ao gRPC e está familiarizado com buffers de protocolo. Observe que o exemplo neste tutorial usa a versão proto3 da linguagem de buffers de protocolo: você pode descobrir mais no guia da linguagem proto3e o guia de código gerado pelo Go.

## Por que usar gRPC?
Nosso exemplo é um aplicativo simples de mapeamento de rotas que permite aos clientes obter informações sobre recursos em suas rotas, criar um resumo de suas rotas e trocar informações de rotas, como atualizações de tráfego, com o servidor e outros clientes.

Com o gRPC, podemos definir nosso service uma vez em um .protoarquivo e gerar clientes e servidores em qualquer uma das linguagens suportadas pelo gRPC, que por sua vez podem ser executadas em ambientes que variam de servidores dentro de um grande data center até seu próprio tablet — toda a complexidade da comunicação entre diferentes linguagens e ambientes é tratada para você pelo gRPC. Também obtemos todas as vantagens de trabalhar com buffers de protocolo, incluindo serialização eficiente, um IDL simples e atualização fácil da interface.

## Setup
Você já deve ter instalado as ferramentas necessárias para gerar o código da interface do cliente e do servidor. Caso ainda não tenha, consulte a seção Pré-requisitos do Início rápido para obter instruções de configuração.

**Obtenha o código de exemplo:**

O código de exemplo faz parte do grpc-gorepositório.

**Baixe o repositório como um file zip descompacte-o ou clone o repositório:**
```
 git clone -b v1.66.2 --depth 1 https://github.com/grpc/grpc-go
```
Mude para o diretório de exemplo:
```sh
 cd grpc-go/examples/route_guide
```
### Definindo o service
Nosso primeiro passo (como você saberá na Introdução ao gRPC ) é definir o service `gRPC` e os tipos de solicitação e resposta do método usando buffers de protocolo. Para o .proto file completo, veja [routeguide/route_guide.proto.](https://github.com/grpc/grpc-go/blob/master/examples/route_guide/routeguide/route_guide.proto)

Para definir um service, você especifica um nome `service` no seu .`proto` file:
```
service RouteGuide {
   ...
}
```
Em seguida, você define `rpc` métodos dentro da definição do seu service, especificando seus tipos de solicitação e resposta. O `gRPC` permite que você defina quatro tipos de métodos de service, todos usados ​​no `RouteGuide` service:

- Um `RPC` simples em que o cliente envia uma solicitação ao servidor usando o stub e aguarda uma resposta, como uma chamada de função normal.
```
// Obtains the feature at a given position.
rpc GetFeature(Point) returns (Feature) {}
```

- Um `RPC` de `streaming` do lado do servidor(Server-side), em que o cliente envia uma solicitação ao servidor e obtém um fluxo para ler uma sequência de mensagens de volta. O cliente lê do fluxo retornado até que não haja mais mensagens. Como você pode ver em nosso exemplo, você especifica um método de streaming do lado do servidor colocando a stream palavra-chave antes do tipo de resposta .
```
// Obtains the Features available within the given Rectangle.  Results are
// streamed rather than returned at once (e.g. in a response message with a
// repeated field), as the rectangle may cover a large area and contain a
// huge number of features.
rpc ListFeatures(Rectangle) returns (stream Feature) {}
```
- Um `RPC` de `streaming` do lado do cliente em que o cliente grava uma sequência de mensagens e as envia ao servidor, novamente usando um fluxo fornecido. Depois que o cliente termina de gravar as mensagens, ele espera que o servidor leia todas elas e retorne sua resposta. Você especifica um método de `streaming` do lado do cliente colocando a `stream` palavra-chave (KeyWord) antes do tipo de solicitação .
```
// Accepts a stream of Points on a route being traversed, returning a
// RouteSummary when traversal is completed.
rpc RecordRoute(stream Point) returns (RouteSummary) {}
```
- Um RPC de `streaming` `bidirecional` onde ambos os lados enviam uma sequência de mensagens usando um fluxo de leitura-escrita. Os dois fluxos operam independentemente, então clientes e servidores podem ler e escrever em qualquer ordem que quiserem: por exemplo, o servidor pode esperar para receber todas as mensagens do cliente antes de escrever suas respostas, ou pode alternadamente ler uma mensagem e escrever uma mensagem, ou alguma outra combinação de leituras e escritas. A ordem das mensagens em cada fluxo é preservada. Você especifica esse tipo de método colocando a `stream` palavra-chave antes da solicitação e da resposta.
```
// Accepts a stream of RouteNotes sent while a route is being traversed,
// while receiving other RouteNotes (e.g. from other users).
rpc RouteChat(stream RouteNote) returns (stream RouteNote) {}
```
Nosso .proto file também contém definições de tipo de mensagem de `buffer` de protocolo para todos os tipos de solicitação e resposta usados ​​em nossos métodos de service - por exemplo, aqui está o `Point` tipo de mensagem:
```
// Points are represented as latitude-longitude pairs in the E7 representation
// (degrees multiplied by 10**7 and rounded to the nearest integer).
// Latitudes should be in the range +/- 90 degrees and longitude should be in
// the range +/- 180 degrees (inclusive).
message Point {
  int32 latitude = 1;
  int32 longitude = 2;
}
```
## Gerando código cliente e servidor
Em seguida, precisamos gerar as interfaces de cliente e servidor `gRPC` a partir da nossa `.proto` definição de service. Fazemos isso usando o compilador de buffer de protocolo protoc com um plugin gRPC Go especial. Isso é semelhante ao que fizemos no Início rápido .

No `examples/route_guide` diretório, execute o seguinte comando:
```
protoc --go_out=. --go_opt=paths=source_relative \
    --go-grpc_out=. --go-grpc_opt=paths=source_relative \
    routeguide/route_guide.proto
```
A execução deste comando gera os seguintes arquivos no  [routeguide](https://github.com/grpc/grpc-go/tree/master/examples/route_guide/routeguide) diretório:

- `route_guide.pb.go,` que contém todo o código do buffer de protocolo para preencher, serializar e recuperar tipos de mensagens de solicitação e resposta.
- `route_guide_grpc.pb.go,` que contém o seguinte:
   - Um tipo de interface (ou stub ) para clientes chamarem com os métodos definidos no `RouteGuide` service.
   -  Um tipo de interface para servidores implementarem, também com os métodos definidos no `RouteGuide` service.
  
## Criando o servidor
Primeiro, vamos ver como criamos um `RouteGuide` servidor. Se você estiver interessado apenas em criar clientes `gRPC`, pode pular esta seção e ir direto para Criando o cliente (embora você possa achar isso interessante de qualquer forma!).

Há duas partes para fazer nosso `RouteGuide` service funcionar:

- Implementando a interface de service gerada a partir da nossa definição de service: realizando o “trabalho” real do nosso service.
- Executar um servidor gRPC para escutar solicitações de clientes e despachá-las para a implementação de service correta.
Você pode encontrar nosso `RouteGuide` servidor de exemplo em [server/server.go.](https://github.com/grpc/grpc-go/blob/master/examples/route_guide/server/server.go) Vamos dar uma olhada mais de perto em como isso funciona.

## Implementando o RouteGuide
Como você pode ver, nosso servidor tem um `routeGuideServer` tipo struct que implementa a `RouteGuideServer` interface gerada:
```
type routeGuideServer struct {
        ...
}
...

func (s *routeGuideServer) GetFeature(ctx context.Context, point *pb.Point) (*pb.Feature, error) {
        ...
}
...

func (s *routeGuideServer) ListFeatures(rect *pb.Rectangle, stream pb.RouteGuide_ListFeaturesServer) error {
        ...
}
...

func (s *routeGuideServer) RecordRoute(stream pb.RouteGuide_RecordRouteServer) error {
        ...
}
...

func (s *routeGuideServer) RouteChat(stream pb.RouteGuide_RouteChatServer) error {
        ...
}
...
```
## RPC simples
O `routeGuideServer` implementa todos os nossos métodos de service. Vamos dar uma olhada no tipo mais simples primeiro, `GetFeature`, que apenas obtém um `Poin`t do cliente e retorna as informações de recurso correspondentes de seu banco de dados em um `Feature`.
```
func (s *routeGuideServer) GetFeature(ctx context.Context, point *pb.Point) (*pb.Feature, error) {
  for _, feature := range s.savedFeatures {
    if proto.Equal(feature.Location, point) {
      return feature, nil
    }
  }
  // No feature was found, return an unnamed feature
  return &pb.Feature{Location: point}, nil
}
```
O método recebe um objeto de contexto para o `RPC` e a `Point` solicitação de `buffer` de protocolo do cliente. Ele retorna um `Feature` protocol buffer object com as informações de resposta e um `error`. No método, preenchemos o `Feature` com as informações apropriadas e, em seguida, `return` junto com um `nil` erro para informar ao `gRPC` que terminamos de lidar com o `RPC` e que o `Feature` pode ser retornado ao cliente.

## RPC de streaming do lado do servidor (Server-side streaming RPC )
Agora, vamos dar uma olhada em um dos nossos RPCs de streaming. `ListFeatures` é um `RPC` de streaming do lado do servidor(server-side), então precisamos enviar vários` Features` para o nosso cliente.
```
func (s *routeGuideServer) ListFeatures(rect *pb.Rectangle, stream pb.RouteGuide_ListFeaturesServer) error {
  for _, feature := range s.savedFeatures {
    if inRange(feature.Location, rect) {
      if err := stream.Send(feature); err != nil {
        return err
      }
    }
  }
  return nil
}
```
Como você pode ver, em vez de obter objetos simples de solicitação e resposta em nossos parâmetros de método, desta vez obtemos um objeto de solicitação (o `Rectangle` qual nosso cliente deseja encontrar `Features`) e um objeto especial `RouteGuide_ListFeaturesServer` para escrever nossas respostas.

No método, populamos quantos `Feature` objetos precisamos retornar, escrevendo-os para o `RouteGuide_ListFeaturesServer` usando seu `Send()` método. Finalmente, como em nosso `RPC` simples, retornamos um `nil` erro para informar ao `gRPC` que terminamos de escrever respostas. Caso ocorra algum erro nessa chamada, retornamos um non-`nil` erro; a camada `gRPC` o traduzirá em um status RPC apropriado para ser enviado na conexão.

## RPC de streaming do lado do cliente (Client-side streaming RPC)
Agora, vamos dar uma olhada em algo um pouco mais complicado: o método de `streaming` do lado do cliente `RecordRoute`, onde obtemos um fluxo de `Points`do cliente e retornamos um único `RouteSummary` com informações sobre sua trip. Como você pode ver, desta vez o método não tem um parâmetro de solicitação. Em vez disso, ele obtém um `RouteGuide_RecordRouteServer` fluxo, que o servidor pode usar para ler e escrever mensagens - ele pode receber mensagens do cliente usando seu `Recv()` método e retornar sua resposta única usando seu `SendAndClose()` método.
```
func (s *routeGuideServer) RecordRoute(stream pb.RouteGuide_RecordRouteServer) error {
  var pointCount, featureCount, distance int32
  var lastPoint *pb.Point
  startTime := time.Now()
  for {
    point, err := stream.Recv()
    if err == io.EOF {
      endTime := time.Now()
      return stream.SendAndClose(&pb.RouteSummary{
        PointCount:   pointCount,
        FeatureCount: featureCount,
        Distance:     distance,
        ElapsedTime:  int32(endTime.Sub(startTime).Seconds()),
      })
    }
    if err != nil {
      return err
    }
    pointCount++
    for _, feature := range s.savedFeatures {
      if proto.Equal(feature.Location, point) {
        featureCount++
      }
    }
    if lastPoint != nil {
      distance += calcDistance(lastPoint, point)
    }
    lastPoint = point
  }
}
```
No corpo do método, usamos o método `RouteGuide_RecordRouteServer'`s `Recv()` para ler repetidamente as solicitações do nosso cliente para um objeto de solicitação (neste caso, um `Point`) até que não haja mais mensagens: o servidor precisa verificar o erro retornado de` Recv()` após cada chamada. Se for `nil`, o fluxo ainda está bom e pode continuar lendo; se for , `io.EOF` o fluxo de mensagens terminou e o servidor pode retornar seu `RouteSummary`. Se tiver qualquer outro valor, retornamos o erro "como está" para que ele seja traduzido para um status RPC pela camada gRPC.

## RPC de streaming bidirecional (Bidirectional streaming RPC)
Por fim, vamos dar uma olhada em nosso RPC de streaming bidirecional `RouteChat()`.
```
func (s *routeGuideServer) RouteChat(stream pb.RouteGuide_RouteChatServer) error {
  for {
    in, err := stream.Recv()
    if err == io.EOF {
      return nil
    }
    if err != nil {
      return err
    }
    key := serialize(in.Location)
                ... // look for notes to be sent to client
    for _, note := range s.routeNotes[key] {
      if err := stream.Send(note); err != nil {
        return err
      }
    }
  }
}
```
Desta vez, obtemos um `RouteGuide_RouteChatServer` fluxo que, como em nosso exemplo de fluxo do lado do cliente, pode ser usado para ler e escrever mensagens. No entanto, desta vez, retornamos valores por meio do fluxo do nosso método enquanto o cliente ainda está escrevendo mensagens para seu fluxo de mensagens.

A sintax para leitura e escrita aqui é muito similar ao nosso método de streaming de cliente, exceto que o servidor usa o `Send()` método do stream em vez de `SendAndClose()` porque ele está escrevendo múltiplas respostas. Embora cada lado sempre receba as mensagens do outro na ordem em que foram escritas, tanto o cliente quanto o servidor podem ler e escrever em qualquer ordem — os streams operam completamente independentes.

## Iniciando o servidor(Starting the server )
Depois que implementamos todos os nossos métodos, também precisamos iniciar um servidor gRPC para que os clientes possam realmente usar nosso service. O snippet a seguir mostra como fazemos isso para nosso `RouteGuid`e service:
```
lis, err := net.Listen("tcp", fmt.Sprintf("localhost:%d", port))
if err != nil {
  log.Fatalf("failed to listen: %v", err)
}
var opts []grpc.ServerOption
...
grpcServer := grpc.NewServer(opts...)
pb.RegisterRouteGuideServer(grpcServer, newServer())
grpcServer.Serve(lis)
```
**Para construir e iniciar um servidor, we:**

1. Especifique a porta que queremos usar para escutar solicitações do cliente usando:
- ``lis, err := net.Listen(...).``
2. Crie uma instância do servidor gRPC usando 
-   grpc.NewServer(...).
3. Registre nossa implementação de service com o servidor gRPC.
4. Chame `Serve()` o servidor com nossos detalhes de porta para fazer uma espera de bloqueio até que o processo seja encerrado ou `Stop()`chamado.

## Criando o cliente(Creating the client)
Nesta seção, veremos como criar um cliente Go para nosso `RouteGuide` service. Você pode ver nosso código de cliente de exemplo completo em [grpc-go/examples/route_guide/client/client.go.](https://github.com/grpc/grpc-go/blob/master/examples/route_guide/client/client.go)

## Criando um stub
Para chamar métodos de service, primeiro precisamos criar um `channel gRPC` para comunicar com o servidor. Criamos isso passando o endereço do servidor e o número da porta para `grpc.NewClient()`o seguinte:
```
var opts []grpc.DialOption
...
conn, err := grpc.NewClient(*serverAddr, opts...)
if err != nil {
  ...
}
defer conn.Close()
```
Você pode usar DialOptionspara definir as credenciais de autenticação (por exemplo, credenciais`TLS`, `GCE` ou credenciais `JWT`) quando `grpc.NewClient` um service as exigir. O `RouteGuide `service não exige nenhuma credencial.

Uma vez que o `channel gRPC` é configurado, precisamos de um `stub` de cliente para executar `RPCs`. Nós o obtemos usando o `NewRouteGuideClient` método fornecido pelo `pb` pacote gerado do` .proto` arquivo de exemplo.

```
client := pb.NewRouteGuideClient(conn)
```
## Métodos de service de chamada(Calling service methods)
Agora, vamos ver como chamamos nossos métodos de service. Note que no gRPC-Go, os RPCs operam em um modo de bloqueio/síncrono, o que significa que a chamada RPC espera que o servidor responda e retornará uma resposta ou um erro.

## RPC simples
Chamar o RPC simples GetFeatureé quase tão simples quanto chamar um método local.
```
feature, err := client.GetFeature(context.Background(), &pb.Point{409146138, -746188906})
if err != nil {
  ...
}
```
Como você pode ver, chamamos o método no stub que obtivemos anteriormente. Em nossos parâmetros de método, criamos e preenchemos um objeto de `buffer` de protocolo de solicitação (no nosso caso `Point`). Também passamos um `context.Context` objeto que nos permite alterar o comportamento do nosso RPC se necessário, como tempo `time-out/cancel`  um RPC em andamento. Se a chamada não retornar um `erro`, podemos ler as informações de resposta do servidor a partir do primeiro valor de retorno.
```
log.Println(feature)
```
## RPC de streaming do lado do servidor(Server-side streaming RPC)
É aqui que chamamos o método de `streaming` do lado do servidor(server-side) `ListFeatures`, que retorna um fluxo de` Feature S` geográficos. Se você já leu `Creating the server`, algumas dessas coisas podem parecer muito familiares - `RPCs` de `streaming` são implementados de forma semelhante em ambos os lados.
```
rect := &pb.Rectangle{ ... }  // initialize a pb.Rectangle
stream, err := client.ListFeatures(context.Background(), rect)
if err != nil {
  ...
}
for {
    feature, err := stream.Recv()
    if err == io.EOF {
        break
    }
    if err != nil {
        log.Fatalf("%v.ListFeatures(_) = _, %v", client, err)
    }
    log.Println(feature)
}
```
Assim como no RPC simples, passamos ao método um contexto e uma solicitação. No entanto, em vez de obter um objeto de resposta de volta, obtemos uma instância de `RouteGuide_ListFeaturesClient.` O cliente pode usar o `RouteGuide_ListFeaturesClient` fluxo para ler as respostas do servidor.

Usamos o método `RouteGuide_ListFeaturesClient's` ``Recv()``para ler repetidamente as respostas do servidor para um objeto de `buffer` de protocolo de resposta (nesse caso, um `Feature`) até que não haja mais mensagens: o cliente precisa verificar o `erro` `err` retornado de` Recv()`após cada chamada. Se `nil`, o fluxo ainda está bom e ele pode continuar lendo; se estiver,` io.EOF` o fluxo de mensagens terminou; caso contrário, deve haver um` erro RPC`, que é passado por `err`.

## RPC de streaming do lado do cliente(Client-side streaming RPC)
O método de streaming do lado do cliente `RecordRoute` é semelhante ao método do lado do servidor, exceto que apenas passamos um contexto ao método e obtemos um `RouteGuide_RecordRouteClient` fluxo de volta, que podemos usar para escrever e ler mensagens.
```
// Create a random number of random points
r := rand.New(rand.NewSource(time.Now().UnixNano()))
pointCount := int(r.Int31n(100)) + 2 // Traverse at least two points
var points []*pb.Point
for i := 0; i < pointCount; i++ {
  points = append(points, randomPoint(r))
}
log.Printf("Traversing %d points.", len(points))
stream, err := client.RecordRoute(context.Background())
if err != nil {
  log.Fatalf("%v.RecordRoute(_) = _, %v", client, err)
}
for _, point := range points {
  if err := stream.Send(point); err != nil {
    log.Fatalf("%v.Send(%v) = %v", stream, point, err)
  }
}
reply, err := stream.CloseAndRecv()
if err != nil {
  log.Fatalf("%v.CloseAndRecv() got error %v, want %v", stream, err, nil)
}
log.Printf("Route summary: %v", reply)
```
O `RouteGuide_RecordRouteClient` tem um `Send()` método que podemos usar para enviar solicitações ao servidor. Depois que terminarmos de escrever as solicitações do nosso cliente para o fluxo usando `Send()`, precisamos chamar` CloseAndRecv()`o fluxo para informar ao `gRPC` que terminamos de escrever e estamos esperando receber uma resposta. Obtemos nosso status` RPC` do `err` retornado de `CloseAndRecv().` Se o status for `nil`, o primeiro valor de retorno de `CloseAndRecv()será` uma resposta válida do servidor.

## RPC de streaming bidirecional(Bidirectional streaming RPC)
Por fim, vamos dar uma olhada em nosso RPC de streaming bidirecional `RouteChat()`. Como no caso de `RecordRoute`, passamos apenas um objeto de contexto para o método e obtemos um fluxo que podemos usar para escrever e ler mensagens. No entanto, dessa vez, retornamos valores por meio do fluxo do nosso método enquanto o servidor ainda está escrevendo mensagens para seu fluxo de mensagens.
```
stream, err := client.RouteChat(context.Background())
waitc := make(chan struct{})
go func() {
  for {
    in, err := stream.Recv()
    if err == io.EOF {
      // read done.
      close(waitc)
      return
    }
    if err != nil {
      log.Fatalf("Failed to receive a note : %v", err)
    }
    log.Printf("Got message %s at point(%d, %d)", in.Message, in.Location.Latitude, in.Location.Longitude)
  }
}()
for _, note := range notes {
  if err := stream.Send(note); err != nil {
    log.Fatalf("Failed to send a note: %v", err)
  }
}
stream.CloseSend()
<-waitc
```
A sintaxe para leitura e escrita aqui é muito similar ao nosso método de streaming do lado do cliente, exceto que usamos o `CloseSend()` método do stream assim que terminamos nossa chamada. Embora cada lado sempre receba as mensagens do outro na ordem em que foram escritas, tanto o cliente quanto o servidor podem ler e escrever em qualquer ordem — os streams operam completamente independentes.

Experimente!(Try it out!) 
Execute os seguintes comandos do `examples/route_guid`e diretório:

1. Execute o servidor:
```
 go run server/server.go
```
2. De outro terminal, execute o cliente:
```
 go run client/client.go
```
Você verá uma saída como esta:
```
Getting feature for point (409146138, -746188906)
name:"Berkshire Valley Management Area Trail, Jefferson, NJ, USA" location:<latitude:409146138 longitude:-746188906 >
Getting feature for point (0, 0)
location:<>
Looking for features within lo:<latitude:400000000 longitude:-750000000 > hi:<latitude:420000000 longitude:-730000000 >
name:"Patriots Path, Mendham, NJ 07945, USA" location:<latitude:407838351 longitude:-746143763 >
...
name:"3 Hasta Way, Newton, NJ 07860, USA" location:<latitude:410248224 longitude:-747127767 >
Traversing 56 points.
Route summary: point_count:56 distance:497013163
Got message First message at point(0, 1)
Got message Second message at point(0, 2)
Got message Third message at point(0, 3)
Got message First message at point(0, 1)
Got message Fourth message at point(0, 1)
Got message Second message at point(0, 2)
Got message Fifth message at point(0, 2)
Got message Third message at point(0, 3)
Got message Sixth message at point(0, 3)
```