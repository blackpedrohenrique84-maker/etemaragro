import os #Importa o módulo padrão "os" para acessar variáveis ​​de ambiente e recursos do sistema operacional.
import json #Importar o módulo "json" para ler e gerar dados estruturados no formato JSON.
import logging #Importar o módulo "logging" para registrar mensagens e avisos de execução da aplicação.
from pathlib import Path #Importar uma classe "Path" para manipular caminhos de arquivos e pastas de forma limpa e compatível entre sistemas operacionais.
try: #o código continua importando o FastAPI (com fallback caso não esteja instalado) e as dependências do sistema agrícola.
    
    from fastapi import FastAPI, HTTPException, Response #Importa FastAPI(classe principal da aplicação web), HTTPException(para retornar erros HTTP estruturados, como 400 ou 500) e Response(para respostas HTTP customizadas, com
    from fastapi.responses import FileResponse #Importa FileResponse, usado para devolver arquivos locais do disco (como o index.html) diretamente na resposta HTTP.
    from fastapi.middleware.cors import CORSMiddleware #Importe o middleware de CORS para liberar chamadas entre origens/portas diferentes (por exemplo, frontend rodando em outra porta acessando a API).
    from fastapi.staticfiles import StaticFiles #Importar StaticFilespara publicar uma pasta de arquivos estáticos (CSS, JS, imagens) em uma rotação da aplicação.
except Exception: #Captura qualquer exceção caso o pacote fastapi(ou alguns deles) não esteja disponível no ambiente Python atual.



    
    # Fallback stubs so linters/IDEs won't error when fastapi isn't installed.
    class FastAPI: #Crie uma classe substituta ( stub) com o mesmo nome FastAPIcaso a biblioteca real não esteja instalada.
        def __init__(self, *args, **kwargs): #Crie uma classe substituta ( stub) com o mesmo nome FastAPIcaso a biblioteca real não esteja instalada.
            raise ImportError("fastapi is required to run this application. Install it with 'pip install fastapi'.") #Ao tentar instanciar FastAPI(...)sem o pacote real, digite uma ImportErrormensagem orientando a instalação via pip install fastapi.
            

    class HTTPException(Exception):  #Cria uma classe substituta para HTTPExceptionherdando de Exception.
        def __init__(self, status_code: int = 500, detail: str | None = None):#Definir o construtor recebe status_code(padrão 500) e detail(texto opcional ou None).
            super().__init__(detail) #Repassa detailpara o construtor da classe base Exception.

    class Response:#Cria uma classe substituta para Response.
        def __init__(self, *args, **kwargs):#Definir o construtor aceitando argumentos genéricos.
            raise ImportError("fastapi is required to run this application. Install it with 'pip install fastapi'.") #Lança ImportErrorcaso Responseseja usado sem o fastapiinstalado.

    class FileResponse:#Cria uma classe substituta para FileResponse.
        def __init__(self, *args, **kwargs): #Definir o construtor com argumentos genéricos.
            raise ImportError("fastapi is required to run this application. Install it with 'pip install fastapi'.")#LançaImportErrorseFileResponsepara chamado sem ofastapiinstalado.

    class CORSMiddleware: #Cria uma classe substituta paraCORSMiddleware.
        def __init__(self, *args, **kwargs): #Definir o construtor com argumentos genéricos.
            raise ImportError("fastapi is required to run this application. Install it with 'pip install fastapi'.") #LançaImportErrorcasoCORSMiddlewareseja usado sem ofastapiinstalado.

    class StaticFiles:#Cria uma classe substituta paraStaticFiles.
        def __init__(self, *args, **kwargs):#Definir o construtor com argumentos genéricos.
            raise ImportError("fastapi is required to run this application. Install it with 'pip install fastapi'.") #Lança ImportErrorse StaticFilesfor chamado sem o fastapiinstalado.
import pydantic#Importação pydanticpara validação e modelagem de dados (como ConsultaAgro).
from typing import List, Dict #Importa Liste Dictfaz módulo typingpara digitar listas e dicionários.
from groq import AsyncGroq #Importa AsyncGroq, o cliente assíncrono da API da Groq para chamadas ao modelo de IA.
from dotenv import load_dotenv #Importaload_dotenvpara carregar variáveis ​​de ambiente de um arquivo.env.

load_dotenv() #Carrega as variáveis de ambiente definidas em um arquivo .env
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "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") #Buscar a chave GROQ_API_KEYnas variáveis ​​de ambiente; se não encontrar, use uma string literal de fallback (recomenda-se remover a chave literal antes de publicar).

app = FastAPI(title="ETEMAR AGRO - Logic Engine") #Cria a instância principal da aplicação FastAPI com o título ETEMAR AGRO - Logic Engine.
logging.getLogger('uvicorn.access').setLevel(logging.WARNING) #Ajusta o nível de log do servidor Uvicorn para WARNING, muitas vezes mensagens comuns de acesso HTTP no terminal.
@app.get("/") #Registra uma rota HTTP GETno caminho raiz /.
async def rota_principal(): #Definir uma função assíncrona que atende às requisições feitas em /.
    return {"status": "Online", "sistema": "E.T.E.M.A.R Agro Engine", "versao": "2.0"}#Retorna um objeto JSON indicando que o serviço está online, o nome do sistema e a versão

app.add_middleware( #Adicionado um middleware à aplicação FastAPI para interceptar/modificar requisições e respostas.
    CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"], #Configure o CORS para aceitar requisições de qualquer origem ( *), com credenciais, todos os métodos HTTP e todos os cabeçalhos.
) #Configure o CORS para aceitar requisições de qualquer origem ( *), com credenciais, todos os métodos HTTP e todos os cabeçalhos.

client = AsyncGroq(api_key=GROQ_API_KEY) #Instância do cliente assíncrono daGroqusando a chave obtida emGROQ_API_KEY.

@app.get('/favicon.ico') #Registre uma rotaGETpára/favicon.ico(ícone solicitado automaticamente pelos navegadores).
async def favicon(): #Definir a função assíncrona que trata/favicon.ico.
    return Response(status_code=204) #Retorna uma resposta vazia com status HTTP204(Sem conteúdo) para evitar erro 404.

@app.get('/') #Registar outra rota GETna raiz /(em FastAPI, rotas registadas depois sobrescrevem rotas anteriores com o mesmo caminho e método).
async def root(): #Defina uma função assíncrona de rotação /.
    return FileResponse(Path(__file__).resolve().parent / 'index.html') #Retorna o arquivo index.htmllocalizado na mesma pasta do arquivo server_agro.py.

@app.get('/index.html') #Registre a rota GETpara /index.html.
async def index_html(): #Defina uma função assíncrona para /index.html.
    return FileResponse(Path(__file__).resolve().parent / 'index.html') #Também devolve oindex.htmlda mesma pasta do script.

app.mount("/static", StaticFiles(directory=Path(__file__).resolve().parent), name="static") #Monta o diretório do script na rota/staticpara servir arquivos estáticos (como CSS,JS ou imagens).

class ConsultaAgro(pydantic.BaseModel): #Definir o modelo de validação de dadosConsultaAgroherdando depydantic.BaseModel
    pergunta: str #Declaração do campo obrigatórioperguntado tipo string.
    historico: List[Dict[str, str]] = [] #Declara o campo opcional historicocomo lista de dicionários de strings, com padrão lista vazia [].

@app.post("/api/agro/consultar") #Registar o endpoint POSTem /api/agro/consultarpara consultas agrícolas.
async def consultar_ia_agro(req: ConsultaAgro): #Defina uma função assíncrona que recebe reqjá validada conforme ConsultaAgro.
    print(f"[API] /api/agro/consultar called with pergunta={req.pergunta!r}, historico_items={len(req.historico)}") #Imprime no console o texto da pergunta (com repr) e a quantidade de itens no histórico.
    if len(req.pergunta) < 2: #Verifique se req.perguntatem menos de 2 caracteres.
        raise HTTPException(status_code=400, detail="Entrada vazia. A pergunta deve conter pelo menos 2 caracteres.") #Disparar um erro HTTP400(Pedido ruim) se a pergunta for curta ou vazia.



    

    # PROMPT DE ALTO NÍVEL: O JSON do financeiro agora é estruturado
    prompt_sistema = """Você é o Pesquisador Chefe de Agronomia do sistema E.T.E.M.A.R. 
    Se o produtor der dados vagos, exija Área, Cultura, Local e Época retornando: {"precisa_info": true, "pergunta_ia": "..."}.
    
    REGRA DE OURO: 
    É ESTRITAMENTE PROIBIDO dar respostas rasas de 1 linha. Use negrito (**) para palavras-chave.
    Seja transparente e lógico na matemática.

    RETORNE OBRIGATORIAMENTE ESTE JSON ESTRITO:
    {
        "precisa_info": false,
        "rastreabilidade": {
            "fonte_clima": "🔵 INMET / MapBiomas",
            "fonte_mercado": "🔵 CEPEA / CONAB"
        },
        "diagnostico": {
            "texto": "Diagnóstico aprofundado com pelo menos 2 parágrafos. Explique cientificamente a causa.",
            "matriz_confianca": [
                {"causa": "Estresse Hídrico", "probabilidade": 90},
                {"causa": "Deficiência Nutricional", "probabilidade": 45}
            ]
        },
        "plano_acao": {
            "imediato": "Ação tática de campo imediata.",
            "dias_30": "Ação para os próximos 30 dias.",
            "proxima_safra": "Estratégia de investimento estrutural."
        },
        "textos_extras": {
            "clima": "Análise climática baseada no local.",
            "mercado": "Lei de oferta e demanda aplicada ao caso."
        },
        "financeiro": {
            "premissas": {
                "area": "80 ha",
                "produtividade_media": "30 t/ha",
                "cotacao_atual": "R$ 2,50/kg"
            },
            "impacto": {
                "taxa_perda": "50%",
                "volume_perdido": "1.200 t"
            },
            "resultado": "R$ 3.000.000,00",
            "formula_aplicada": "(80 ha * 30 t/ha) * 50% de perda = 1.200 t. (1.200 t * 1000 kg) * R$ 2,50 = R$ 3.000.000,00"
        },
        "graficos": [
            {"titulo": "Histórico de Preço (R$/kg)", "tipo": "line", "labels": ["Safra Ant", "Mês Passado", "Atual", "Proj"], "dados": [4.1, 4.3, 5.0, 5.2]},
            {"titulo": "Anomalia Climática (mm)", "tipo": "bar", "labels": ["Mês -2", "Mês -1", "Atual"], "dados": [80, 40, 10]}
        ]
    }
    """

    mensagens = [{"role": "system", "content": prompt_sistema}] #Cria uma lista mensagensiniciando com a instrução de sistema ( system).
    for msg in req.historico: mensagens.append(msg) #Itera sobre as mensagens anteriores em req.historicoe adiciona cada uma à lista mensagens.
    mensagens.append({"role": "user", "content": req.pergunta}) #Adicionado a pergunta atual do usuário ( req.pergunta) ao final de mensagens.

    try: #Abra o bloco trypara capturar falhas durante a requisição à API do Groq ou na conversão do JSON.
        res = await client.chat.completions.create( #Chama de forma assíncrona o método chat.completions.createno cliente clientda Groq
            messages=mensagens, #Passe a lista completa de mensagens ( system, histórico e pergunta atual).
            model="llama-3.3-70b-versatile", #Passe a lista completa de mensagens ( system, histórico e pergunta atual).
            max_tokens=4500, #Limita a resposta gerada no máximo4500fichas.
            temperature=0.3, #Defina temperatura0.3para manter a resposta mais determinística e focada.
            response_format={"type": "json_object"} #Instrui uma API para forçar a saída no formato do objeto JSON.
        ) #Fecha a chamadaclient.chat.completions.create(...).
        
        conteudo = res.choices[0].message.content.strip() #Pega o conteúdo textual da primeira resposta (choices[0]) e remova espaços em branco ou quebras de linha nas extremidades.
        if conteudo.startswith("```json"): #Verifique se o texto começa com o marcador de bloco de código JSON do Markdown ( ```json).
            conteudo = conteudo[7:] #Remova os 7 primeiros caracteres ( ```json) caso apresentado no início.
        if conteudo.endswith("```"): #Verifique se o texto termina com o fechamento do bloco Markdown ( ```).
            conteudo = conteudo[:-3] #Remova os últimos 3 caracteres ( ```) caso estejam presentes no final.
            
        return json.loads(conteudo) #Converte uma string JSON tratada em um dicionário/estrutura Python e retorna como resposta do endpoint.
        
    except Exception as e: #Captura qualquer exceção ocorrida dentro do bloco try.
        print(f"🚨 ERRO AGRO: {e}") #Imprima no terminal uma mensagem de erro com o prefixo 🚨 ERRO AGRO:.
        raise HTTPException(status_code=500, detail=str(e)) #Levanta uma HTTPExceptioncom status 500(erro interno do servidor) e a descrição do erro.

if __name__ == "__main__": #Garante que o bloco de inicialização só rode quando o arquivo for executado diretamente como script principal.
    import uvicorn #Importa o servidor ASGI uvicorn.
    uvicorn.run("server_agro:app", host="0.0.0.0", port=3001, reload=True) #Inicia o servidor rodando appo módulo server_agro, escutando 0.0.0.0na porta3001com recarga automática (reload=True) ao detectar alterações no arquivo.
