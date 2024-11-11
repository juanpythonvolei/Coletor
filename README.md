Este projeto visa auxiliar a gestão logística em diversos aspectos. Um deles é a localização de itens no armazenamento. Para manter e localizar os produtos, criei um sistema de endereçamento que informa onde e quantos itens de um código específico você possui.

Além disso, o sistema possui páginas integradas de recebimento e registro, onde você pode registrar novos produtos e recebê-los no armazenamento. Após receber um produto, você precisará levá-lo ao armazenamento transferindo-o do recebimento para um endereço específico.

Outra característica é o processo de faturamento. Com ele, você pode simplesmente fazer o upload das notas fiscais e ver todo o processo em execução. Nos bastidores, o faturamento extrai todas as informações relevantes das notas fiscais e as envia para o banco de dados. Uma vez que isso ocorre, o processo de separação começa. Esse processo ordena os produtos que serão enviados ao cliente final. Após a separação, ocorre o processo de conferência. Isso significa que você selecionará uma nota fiscal e todas as informações do produto, local e quantidade serão exibidas. No final, quando você separar a nota fiscal, ela será automaticamente anotada na lista de embalagem ou relação de itens.

Finalmente, além de tudo isso, você também pode criar uma rota de entrega indo para a aba de rotas e selecionando o dia e o transportador desejado.

Nota: Este projeto é um cenário fictício, e eu não possuo nenhuma credencial ou autorização para usar dados específicos e valiosos. O objetivo deste projeto é simular um caso. Se quiser, você pode incorporar essas funcionalidades ao que já existe ou alterá-las conforme desejar. Isso significa que algumas funcionalidades importantes, como APIs de Agências de Fiscalização Federais ou pedidos diretos de clientes, não estão presentes aqui.

Outro ponto é que todos os elementos de seleção são filtrados. Isso significa que você só selecionará um item, produto, usuário ou transportador que tenha relação com a data selecionada ou com outras variáveis. Isso foi feito para evitar erros humanos. Você pode usar essas bases para projetar sistemas preventivos ainda melhores do que o presente aqui.

O último ponto é a lógica de endereçamento. Eu usei um tipo, mas você pode substituir a lógica de entrada de endereços no backend por qualquer outro tipo que desejar.

Tecnologias:

pandas: Para criar dataframes que são exibidos e fornecidos para download em formato xlsx.

SQLAlchemy: Cria o banco de dados e armazena todos os dados com ORM. É a base de todo o backend.

Streamlit: Cria todos os elementos de frontend que são preenchidos com as informações das tabelas do banco de dados e os exibe nas páginas.

Google Generative AI: Usado para alimentar o assistente IA integrado que recebe todas as informações de todos os registros no sistema e, ao fazer uma pergunta, tenta ajudá-lo com análises de dados específicas.

openpyxl: Motor para o download de xlsx.

SpeechRecognition: Usado para capturar seu áudio e passá-lo como um prompt de texto para a IA.

xmltodict: Usado para extrair todas as informações das notas fiscais e fornecê-las às funções de criação e atualização de ORM em segundo plano.












