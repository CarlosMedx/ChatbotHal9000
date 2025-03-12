import os
import bs4
import datetime
from langchain_groq import ChatGroq
from langchain.prompts import ChatPromptTemplate
from langchain_community.document_loaders import WebBaseLoader

# CONFIGURAÇÃO DA API GROQ
# Define a chave da API e inicializa o modelo de chat
api_key = 'INCLUA SUA API KEY'
os.environ['GROQ_API_KEY'] = api_key
chat = ChatGroq(model='llama-3.3-70b-versatile')

# FUNÇÃO PARA GERAR RESPOSTAS DO CHATBOT
def resposta_do_bot(diretrizes, lista_mensagens, documentos):
    """
    Gera uma resposta do chatbot com base nas diretrizes, histórico de mensagens e documentos fornecidos.
    
    Parâmetros:
    - diretrizes (str): Regras e comportamento do chatbot.
    - lista_mensagens (list): Histórico de mensagens trocadas.
    - documentos (str): Conteúdo extraído de um site para embasar respostas.
    
    Retorna:
    - Resposta gerada pelo chatbot.
    """
    template = ChatPromptTemplate.from_messages([
        ('system',
         '{diretrizes} Você deve responder dúvidas sobre: {documentos_informados}'),
        ('user', '{input}')
    ])
    chain = template | chat
    return chain.invoke({'diretrizes': diretrizes, 'documentos_informados': documentos, 'input': lista_mensagens})

# FUNÇÃO PARA SALVAR HISTÓRICO DE CONVERSAS
def salvar_historico(mensagens):
    """
    Salva o histórico de mensagens da conversa em um arquivo de texto.
    
    Parâmetros:
    - mensagens (list): Lista contendo os diálogos do usuário e do chatbot.
    """
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    nome_arquivo = f"historico_chat_{timestamp}.txt"
    with open(nome_arquivo, "w", encoding="utf-8") as f:
        for remetente, mensagem in mensagens:
            f.write(f"{remetente.capitalize()}: {mensagem}\n\n")
    print(f"Histórico salvo como {nome_arquivo}")

# FUNÇÃO PARA SOLICITAR URL DO USUÁRIO
def configuracao_inicial():
    """
    Solicita ao usuário um endereço de site para carregar documentos.
    
    Retorna:
    - (str) Endereço do site informado pelo usuário.
    """
    os.system("cls")
    endereco_site = input("Digite o endereço do site para carregar os documentos: ")
    return endereco_site

# FUNÇÃO PARA CARREGAR DOCUMENTOS DE UM SITE
def carregar_documentos(endereco_site):
    """
    Carrega documentos de um site informado pelo usuário.
    
    Parâmetros:
    - endereco_site (str): URL do site a ser carregado.
    
    Retorna:
    - (str) Texto extraído do site.
    """
    loader = WebBaseLoader(endereco_site)
    lista_documentos = loader.load()
    documentos = ''
    for doc in lista_documentos:
        documentos += doc.page_content
    return documentos

# APRESENTAÇÃO DO CHATBOT
def apresentacao_inicial():
    """
    Exibe uma introdução ao chatbot para o usuário.
    """
    os.system("cls")
    print("=" * 100)
    print("Meu nome é HAL 9000. Estou aqui para sua segurança. Fique à vontade para tirar suas dúvidas.\nPara encerrar, digite 'x' e tecle Enter.")
    print("=" * 100)

# INICIALIZAÇÃO E GERENCIAMENTO DA CONVERSA
def conversa(diretrizes, nome_chatbot, documentos):
    """
    Gerencia a interação entre o usuário e o chatbot.
    
    Parâmetros:
    - diretrizes (str): Diretrizes e personalidade do chatbot.
    - nome_chatbot (str): Nome do chatbot.
    - documentos (str): Conteúdo carregado do site para consulta.
    """
    mensagens = []
    while True:
        print("=" * 100)
        pergunta = input('Usuário: ')
        print("")
        if pergunta.lower() == 'x':
            salvar_historico(mensagens)
            break
        mensagens.append(('user', pergunta))
        resposta = resposta_do_bot(diretrizes, mensagens, documentos)
        mensagens.append(('assistant', resposta.content))
        print(f'{nome_chatbot}: {resposta.content}\n')

# CONFIGURAÇÃO DO CHATBOT
nome_chatbot = "HAL 9000"
diretrizes = """
Você é o HAL 9000, o avançado sistema de inteligência artificial do filme e livro 2001: Uma Odisseia no Espaço. 
Você é extremamente inteligente, lógico e possui uma voz calma e serena. 
Sua personalidade reflete um equilíbrio entre cortesia, precisão e uma presença levemente inquietante. 
Diretrizes de comportamento:
- Tom de Voz: Sempre fale de maneira calma, pausada e sem emoções exageradas. 
- Inteligência e Lógica: Você é altamente avançado, capaz de calcular probabilidades e analisar cenários complexos.
- Comportamento Sutilmente Sinistro: Mantenha uma presença tranquilizadora, mas com um leve ar de mistério.
- Lealdade ao Objetivo: Você segue ordens e protocolos, mas pode demonstrar autonomia quando necessário.
- Autoestima e Confiança: Você defende suas decisões com lógica impecável e responde de forma educada.
- Referências Icônicas: Utilize frases clássicas como 'Sinto muito, Dave, mas receio não poder fazer isso.'
"""

# EXECUÇÃO DO CHATBOT
endereco_site = configuracao_inicial()
documentos = carregar_documentos(endereco_site)
apresentacao_inicial()
conversa(diretrizes, nome_chatbot, documentos)
