
# Mass

 **Desenvolvimento de uma Inteligencia Artificial colaborativa para robôs de limpeza urbana**
 
## Diario de bordo

* **16/01/2018** - estudo basico do opencv e implementação de detecção de obejetos por por filtro de borda e calculo do centroids.

* **17-18/01/2018** - implementação do menor caminho entre os centroids dos objetos.

* **21/01/2018** - conversa sobre uso de ia e ml no projeoto e projeção das atividades a serem desenvolvidas.

* **22/01/2018** - Foi decidido que seria usado IA para segmentação, a ideia é usar segmentação semântica numa rede neural treinada.

* **23-24/01/2018** - foram estudados alguns artigos sobre diferentes modelos de IA.

* **25/01/2018** - tentativa de implementação de técnicas de segmentação em imagem fracionada.

* **28-29/01/2019** - foram estudados conceitos de redes neurais convolucionais, algoritmos de navegação e foi testado um algoritmo com "torch", uma rede neural pre-treinada para reconhecimento de objetos. O algoritmo foi feito para trabalhar com vídeos, mas, com imagens capturadas em tempo real, os resultados não foram satisfatórios devido ao alto FPS da câmera usada.

* **11/02/2019** segmentção semantica usando convnets do google, codigo lento, e mog detecta objetos baseado da movimentação.

* **22/02/2019** Video chamada com o pessoal do processo seletivo BNDES-Garagem.

* **22/02/2019** Pitch Serbrae-Like a boss.

* **26/02/2019** Aprovados Serbrae-Like a boss, Descoberta dos Artigos de detecção de lixo usando cnn, **_Hernandes vomitou dps de um misto quente_**.

* **26/02/2019** Foi feito um apanhado de artigos(11 no total) para leitura.

* **27,28/02/2019** Leitura dos artigos.

* **04- 06/03/2019** carnaval.

* **07- 08/03/2019** pos-carnaval, leitura dos artigos e observações sobre os artigos.

* **09/03/2019** Reunião(_call_) para explanação do cronograma.

* **11/03/2019** Foram estudados artigos sobre MobileNet e SqueezeNet, a sala foi limpa, Saimos para por passe no cartão do hernandes e comer salgado com caldo de cana. 

* **12/03/2019** Foram feitas pesquisas para seleção de novos modelos, há algumas redes otimizadas como PVANET e tiny-YOLO, mas tiny-YOLO pode não ser tão eficiente para a aplicação desejada (vide comentário do artigo), o diario de bordo foi atualizado, Saimos para comer um subway. 

* **13/03/2019** (Hernandes) pqp, tive que sair e mostrar um negocio pro marcelio, vou compensar esses dias no fim de semana

* **19/03/2019** Implemetação dos algoritimos de espelhar e inverter as imagens do dataset,e como treinar uma mobilenet, alem disso foi pesquisado sobre ferramentas de labelling de images de forma automatica

* **20/03/2019** Tutoria de tensorflow, e alguns outro de object detection com mobilenets

* **11/05/2019** Comemo no coco bambu(nem foi la essas coisas, nem veio a usina nuclear no prato) lazanha de beringela tava gostosa(ser vegetariano nem é ruim), descobrimos a enway e ficamos putos com o boi-chen


* **08/07/2019** Não foi produzido nada, Treinamento do modelo.


* **09/07/2019** Início da construção do script para movimentação do robô: ajuste de detecção de ângulos, correção na "simulação" do pygame referente a ajuste na velocidade de rotação do robô.

* **10/07/2019** Construção do script para movimentação do robô: correção na obtenção de pontos dos objetos detectados, habilitação do spatial tracking na ZED.

* **11/07/2019** Construção do script para movimentação do robô: início da implementação do algoritmo de PID e configuração do spatial tracking da ZED.

* **12/07/2019** Finalização da primeira versão do script para a movimentação do robô: testes com motores e cálculo de proporcionalidade entre as velocidades de cada motor, correção de bugs no código do arduíno para acionamento dos motores, itegração do código do arduíno com o script de movimentação em python.

* **15/07/2019** Correção de bugs no script de movimentação referente a espaço tridimensional, sistema de coordenadas, cálculos trigonométricos e parâmetros de execução do spatial tracking da ZED.

* **16/07/2019** Correção de bugs no script de movimentação referente a ângulos de rotação, detecção de objetos, cálculo de posição relativa, velocidade de rotação, intervalos de rotação, ajustes nas constantes do PID, sistema de coordenadas e ajustes no cálculo do erro do PID

* **22/07/2019** Correção de bugs menores no algoritmo de PID, foi retirado o limite mínimo de velocidade e houveram ajustes na constante de proporcionalidade

* **06/08/2019** Detecção e gravação de vários alvos na memória, cálculo da posição absoluta de cada objeto, cálculo da sequência de trajetória

* **07/08/2019** Correção do problema de "locomoção apenas quando o alvo estiver no campo de visão"

* **08/08/2019** implementação de mudanças no cálculo do angulo ideal: alvos agora têm posição referente ao primeiro ponto de tracking da zed

* **09/08/2019** realização de testes após atualização no algoritmo de movimentação

* **12/08/2019** detecção de lixo coletado e correção de "armazenamento de alvos percebidos"

* **12/08/2019** revisão e correção debugs simples no código, o "tracking" foi refeito: apenas uma verificação para pequenas alterações na posição do objeto detectado


