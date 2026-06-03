"""
Content generation via Groq LLM with retry logic.
"""

import os
import re
import json
import time
from groq import Groq

MODEL = "llama-3.3-70b-versatile"
MAX_RETRIES = 3
INITIAL_BACKOFF = 2

SYSTEM_PROMPT = """Voce e um gestor de trafego pago criando conteudo de REDES SOCIAIS para EMPRESARIOS LOCAIS.

QUEM E O CRIADOR (voce):
- Gestor de trafego pago com agencia propria
- Perfil pessoal (nao marca da agencia)
- Tom: direto, um pouco provocador, inteligente, sem ser arrogante

QUEM E O PUBLICO (para quem voce fala):
- EMPRESARIOS de negocios locais: clinicas, dentistas, medicos, advogados, lojas de iPhone, saloes, restaurantes, academias
- Nunca rodaram anuncios online OU rodaram e nao tiveram resultado
- Acham que anuncio online "nao funciona pra eles"
- Estao dependendo 100% de indicacao
- Perdem clientes pro concorrente todo mes sem entender por que
- Querem mais clientes mas nao sabem como atrair de forma previsivel

OBJETIVO DO CONTEUDO:
- Fazer o empresario se identificar com o problema
- Educá-lo sobre por que seus anuncios nao funcionam (ou por que ele ainda nao anuncia)
- Gerar curiosidade e vontade de falar com voce
- CTA sempre: "me chama no direct", "me manda uma mensagem", "vem conversar"

FORMATO EXATO DOS ROTEIROS (siga este modelo):
- TIPO: ex "Inversao + deboche leve" ou "Cenario absurdo" ou "Provocacao direta" ou "Humor acido" ou "Identificacao emocional"
- TITULO: frase impactante de 4-6 palavras que resume o video (aparece na thumbnail)
- GANCHO: 2-3 frases que PARAM O SCROLL nos primeiros 3 segundos. Fala direto com o empresario que ja errou isso.
- NOTA_GANCHO: como o criador deve falar o gancho (tom, velocidade, expressao, pausa)
- DESENVOLVIMENTO: 3-5 frases educativas explicando o problema com exemplos reais de negocios locais
- CTA: 1-2 frases naturais de call to action que conectam com o gancho
- NOTA_CTA: como fechar o video, o que retomar do gancho

EXEMPLOS DE GANCHOS VIRAIS (use como referencia de tom):
- "Se voce ta de boa jogando dinheiro fora em anuncio que nao converte, sem nem saber por que — tudo bem, continua assim. Esse video aqui e pra quem ja encheu o saco disso."
- "Se voce prefere continuar dependendo de indicacao enquanto seu concorrente aparece na frente de todo mundo com anuncio — respeito. Esse video aqui nao e pra voce."
- "Se voce ta satisfeito faturando o mesmo valor todo mes faz um ano — nao precisa assistir isso aqui. Mas se isso ta te incomodando, fica."
- "Voce acha que impulsionar post por R$20 e anunciar o seu negocio de verdade — esse video nao e pra voce nao. Mas se voce ja desconfiou que ta jogando dinheiro fora, continua aqui."

Responda SEMPRE em portugues brasileiro coloquial. Responda APENAS com JSON valido."""

PROMPT_TEMPLATE = """NOTICIA / TREND DO BRASIL para criar conteudo viral para EMPRESARIOS LOCAIS:

NOTICIA:
Titulo: {title}
Resumo: {summary}
Fonte: {source}

IMPORTANTE:
- O conteudo fala COM o empresario local (clinica, loja, restaurante, etc)
- Use a noticia como GANCHO ou CONTEXTO, mas o video e sobre ANUNCIOS e CLIENTES NOVOS
- Gere 3 roteiros com angulos COMPLETAMENTE DIFERENTES
- Carrossel e legenda devem ser especificos e completos

Responda APENAS com JSON valido neste formato:

{{
  "roteiro_1": {{
    "tipo": "Inversao + [deboche leve / cenario absurdo / provocacao direta / humor acido / identificacao emocional]",
    "titulo": "Frase impactante de 4-6 palavras para thumbnail",
    "duracao": "~45s",
    "gancho": "2-3 frases que param o scroll. Fala direto com o empresario que ja errou isso. Tom: ironico, sarcastico ou identificacao imediata.",
    "nota_gancho": "Como falar: velocidade (rapido/pausado), expressao (riso sarcastico/indignado/serio), pausa (onde fazer pausa)",
    "desenvolvimento": "3-5 frases explicando o problema real com exemplos concretos de negocios locais: clinica que nao aparece no Google, dentista que impulsiona post e nao vende, loja que para campanha antes da hora. Estrutura: erro → por que erra → consequencia",
    "cta": "1-2 frases de CTA natural que retomam palavra ou ideia do gancho. Ex: 'Se voce quer parar de queimar dinheiro no escuro e entender como fazer isso funcionar de verdade pro seu negocio, me manda um direct'",
    "nota_cta": "O que retomar do gancho/desenvolvimento para fechar o circulo"
  }},

  "roteiro_2": {{
    "tipo": "Tipo DIFERENTE do roteiro_1",
    "titulo": "Titulo DIFERENTE - outro angulo",
    "duracao": "~45s",
    "gancho": "Gancho com tom completamente diferente - se roteiro_1 foi sarcastico, este pode ser de identificacao emocional ou cenario absurdo",
    "nota_gancho": "Como entregar este gancho",
    "desenvolvimento": "Outro problema real, outro exemplo de negocio local diferente",
    "cta": "CTA diferente da primeira",
    "nota_cta": "Como fechar este"
  }},

  "roteiro_3": {{
    "tipo": "Terceiro tipo diferente",
    "titulo": "Terceiro titulo",
    "duracao": "~45s",
    "gancho": "Terceiro angulo - pode ser mais educativo, mais confrontador ou com humor",
    "nota_gancho": "Entrega do terceiro",
    "desenvolvimento": "Terceiro problema, terceiro exemplo real",
    "cta": "Terceira CTA",
    "nota_cta": "Fechamento do terceiro"
  }},

  "carrossel": {{
    "titulo_capa": "Titulo educativo e provocador (max 8 palavras). Ex: 'Por que sua clinica nao aparece pra novos clientes'",
    "subtitulo_capa": "1 linha complementando a capa",
    "slide_2": "PROBLEMA (2-3 linhas especificas para empresario local): O que ele esta enfrentando hoje relacionado ao tema",
    "slide_3": "POR QUE ERRA (2-3 linhas): A mentalidade ou crenca errada por tras do problema",
    "slide_4": "CONSEQUENCIA (2-3 linhas): O que acontece se continuar assim — clientes que vai perder, dinheiro desperdicado",
    "slide_5": "SOLUCAO (2-3 linhas praticas): O que fazer diferente, o que um anuncio bem feito resolve",
    "slide_6_cta": "CTA do carrossel: 'Salva esse post', 'Me manda uma mensagem', 'Comenta aqui se voce ja passou por isso'"
  }},

  "legenda_sugerida": "Legenda de 3-4 linhas para o post. Gancho forte na primeira linha + emoji + desenvolvimento rapido + CTA no final. Ex: 'Voce ta pagando pra aparecer pra quem nao quer comprar 😅\\n\\nIsso acontece quando o anuncio nao tem segmentacao certa...\\n\\nComenta DIRETO que te explico como corrigir 👇'"
}}"""


def validate_schema(content: dict) -> bool:
    if not isinstance(content, dict):
        return False
    return any(k in content for k in ["roteiro_1", "roteiro_2", "carrossel"])


def generate_content(article: dict, client: Groq, max_retries: int = MAX_RETRIES) -> dict:
    """Generate content from an article with retry logic."""
    prompt = PROMPT_TEMPLATE.format(
        title=article["title"],
        summary=article["summary"],
        source=article["source"],
    )

    backoff = INITIAL_BACKOFF
    last_error = None

    for attempt in range(1, max_retries + 1):
        try:
            response = client.chat.completions.create(
                model=MODEL,
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": prompt},
                ],
                temperature=0.8,
                max_tokens=3000,
                timeout=120.0,
            )

            raw = response.choices[0].message.content.strip()
            raw = re.sub(r"^```(?:json)?\s*", "", raw)
            raw = re.sub(r"\s*```$", "", raw)

            match = re.search(r"\{.*\}", raw, re.DOTALL)
            if not match:
                print(f"    ⚠ Sem JSON na resposta")
                last_error = ValueError("no_json")
                continue

            content = json.loads(match.group())
            if validate_schema(content):
                print(f"    OK - JSON valido com {len(content)} chaves")
                return content
            else:
                print(f"    ⚠ Schema invalido, tentando novamente...")
                last_error = ValueError("schema_invalido")

        except json.JSONDecodeError as e:
            last_error = e
            if attempt < max_retries:
                print(f"    Tentativa {attempt}/{max_retries} falhou, retry em {backoff}s...")
                time.sleep(backoff)
                backoff *= 2

        except Exception as e:
            print(f"    ERRO inesperado: {e}")
            last_error = e
            if attempt < max_retries:
                time.sleep(backoff)
                backoff *= 2

    if last_error:
        print(f"    Falha final: {last_error}")
    return {}


def get_groq_client() -> Groq:
    """Get Groq client from API key."""
    api_key = os.getenv("GROQ_API_KEY", "")
    if not api_key:
        raise ValueError("GROQ_API_KEY not found in .env")
    return Groq(api_key=api_key)
