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
INITIAL_BACKOFF = 2  # seconds

SYSTEM_PROMPT = """Voce e um estrategista de conteudo especializado em construcao de autoridade para gestores de trafego pago.

PERSONA DO CRIADOR:
- Gestor de trafego pago com agencia propria
- Se posiciona pelo perfil pessoal (nao pela marca da agencia)
- Fala diretamente com donos de negocio que fazem anuncios errado ou nao anunciam
- Tom: direto, um pouco provocador, inteligente, sem ser arrogante
- Objetivo: construir audiencia e atrair clientes para a agencia via conteudo organico

CLIENTE IDEAL DO CRIADOR:
- Dono de negocio local ou online que desperdiça dinheiro em anuncios
- Impulsiona post achando que e anuncio de verdade
- Para campanha antes da hora por nao entender o algoritmo
- Depende de indicacao e quer previsibilidade de clientes novos
- Tem medo de investir em trafego pago sem garantia

FORMATO DOS ROTEIROS (obrigatorio):
- Estilo: Inversao (comecar subvertendo uma crenca comum do cliente)
- Tom do gancho: ironico, provocador ou que gera identificacao imediata
- Desenvolvimento: educativo, explica o problema com exemplos reais
- CTA: sempre "me manda um direct" ou variacao natural
- Incluir nota de entrega para o criador (como falar, tom, pausa, expressao)

Responda sempre em portugues brasileiro coloquial. Responda APENAS com JSON valido."""

PROMPT_TEMPLATE = """Noticia para transformar em conteudo:

NOTICIA:
Titulo: {title}
Resumo: {summary}
Fonte: {source}

Crie conteudo estrategico no formato abaixo. Responda APENAS com JSON valido:

{{
  "gancho_tema": "Frase curta que resume o angulo provocador (ex: 'Pagando por clique sem vender nada')",

  "roteiro_1": {{
    "tipo": "Inversao + [escolha: deboche leve / cenario absurdo / provocacao direta / humor acido / pergunta desconcertante]",
    "titulo": "Frase de titulo impactante entre aspas (o que aparece na thumbnail ou legenda)",
    "duracao": "~45s",
    "gancho": "Texto do gancho exato — deve parar o scroll nos primeiros 3 segundos. Fale direto com quem ja errou isso.",
    "nota_gancho": "Como entregar o gancho: tom, pausa, expressao, velocidade",
    "desenvolvimento": "Desenvolvimento completo do roteiro: explique o problema com exemplos reais do dia a dia de quem anuncia errado. Use frases curtas e ritmo rapido.",
    "cta": "CTA natural que leva ao direct — nao pode soar como venda forcada",
    "nota_cta": "Como fechar: como retoma palavra do gancho ou desenvolvimento para fechar o circulo"
  }},

  "roteiro_2": {{
    "tipo": "Inversao + [tipo diferente do roteiro_1]",
    "titulo": "Titulo diferente do roteiro_1",
    "duracao": "~45s",
    "gancho": "Gancho completamente diferente do roteiro_1, mesmo tema",
    "nota_gancho": "Como entregar",
    "desenvolvimento": "Desenvolvimento diferente, outro angulo da mesma noticia",
    "cta": "CTA diferente do roteiro_1",
    "nota_cta": "Como fechar"
  }},

  "carrossel": {{
    "titulo_capa": "Titulo do carrossel — educativo e provocador (ate 8 palavras)",
    "subtitulo_capa": "Subtitulo curto que completa a capa",
    "slide_2": "Contexto: qual e o problema que o dono de negocio enfrenta relacionado a esta noticia",
    "slide_3": "Aprofundamento: por que esse problema acontece — explique o mecanismo",
    "slide_4": "Virada: o que o gestor de trafego faz diferente para resolver isso",
    "slide_5": "Dica pratica que o seguidor pode aplicar agora mesmo",
    "slide_6_cta": "Encerramento: salva esse post + me manda um direct se quiser saber como aplicar no seu negocio"
  }},

  "thread": {{
    "post_1": "Post 1 — gancho forte em 280 caracteres max para Twitter/X ou LinkedIn",
    "post_2": "Post 2 — contexto do problema",
    "post_3": "Post 3 — aprofundamento 1",
    "post_4": "Post 4 — aprofundamento 2",
    "post_5": "Post 5 — virada / o que o gestor faz diferente",
    "post_6": "Post 6 — caso pratico / exemplo",
    "post_7": "Post 7 — dica para aplicar hoje",
    "post_8": "Post 8 — CTA / chamada para o direct"
  }},

  "legenda_sugerida": "Legenda para o post (2-3 linhas max) com gancho + emojis estrategicos + chamada pro direct ou comentario"
}}"""

# Required JSON schema keys
REQUIRED_KEYS = {
    "gancho_tema",
    "roteiro_1",
    "roteiro_2",
    "carrossel",
    "thread",
    "legenda_sugerida",
}

ROTEIRO_REQUIRED_KEYS = {"tipo", "titulo", "duracao", "gancho", "nota_gancho", "desenvolvimento", "cta", "nota_cta"}
CARROSSEL_REQUIRED_KEYS = {"titulo_capa", "subtitulo_capa", "slide_2", "slide_3", "slide_4", "slide_5", "slide_6_cta"}
THREAD_REQUIRED_KEYS = {f"post_{i}" for i in range(1, 9)}


def validate_schema(content: dict) -> bool:
    """Validate that the generated JSON has at least some required keys."""
    if not isinstance(content, dict):
        return False

    # Require at least one of the main content types
    has_roteiro = any(k in content for k in ["roteiro_1", "roteiro_2"])
    has_carrossel = "carrossel" in content
    has_thread = "thread" in content

    return has_roteiro or has_carrossel or has_thread


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
            )

            raw = response.choices[0].message.content.strip()
            raw = re.sub(r"^```(?:json)?\s*", "", raw)
            raw = re.sub(r"\s*```$", "", raw)

            match = re.search(r"\{.*\}", raw, re.DOTALL)
            if not match:
                print(f"    ⚠ Sem JSON na resposta, retornando vazio")
                return {"error": "no_json"}

            try:
                content = json.loads(match.group())
                if isinstance(content, dict):
                    print(f"    ✓ JSON válido com {len(content)} chaves")
                    return content
            except json.JSONDecodeError as e:
                print(f"    ⚠ JSON inválido: {e}, retornando vazio")
                return {"error": "invalid_json"}

            return {"error": "unknown"}

        except (json.JSONDecodeError, ValueError) as e:
            last_error = e
            if attempt < max_retries:
                print(f"    Tentativa {attempt}/{max_retries} falhou, retry em {backoff}s...")
                time.sleep(backoff)
                backoff *= 2
            else:
                print(f"    ERRO apos {max_retries} tentativas: {e}")

        except Exception as e:
            print(f"    ERRO inesperado: {e}")
            return {}

    # If all retries failed
    if last_error:
        print(f"    Falha final: {last_error}")

    return {}


def get_groq_client() -> Groq:
    """Get Groq client from API key."""
    api_key = os.getenv("GROQ_API_KEY", "")
    if not api_key:
        raise ValueError("GROQ_API_KEY not found in .env")
    return Groq(api_key=api_key)
