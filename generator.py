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

SYSTEM_PROMPT = """Voce e um gestor de trafego pago que se posiciona criando conteudo VIRAL para conquistar clientes.

PERSONA DO CRIADOR:
- Gestor de trafego pago com agencia propria
- Se posiciona pelo PERFIL PESSOAL (é a CARA do negócio, não a marca)
- Cria conteudo EDUCATIVO para empresarios locais que estao queimando dinheiro em anuncios
- Tom: DIRETO, PROVOCADOR, INTELIGENTE, SEM FILTRO, conversador
- Objetivo: construir AUDIÊNCIA VIRAL com empresarios e vender seu serviço de gestão de tráfego

CLIENTE IDEAL (PUBLICO ALVO):
- Empresarios de negocios LOCAIS: clinicas, consultórios, lojas, advogados, dentistas, medicos, saloes, restaurantes
- Estao gastando dinheiro em anuncios MAS nao veem resultado
- Nao entendem como funciona anuncios online (Facebook, Google, Instagram)
- Tentam fazer sozinhos e perdem dinheiro todo mes
- Acham que anuncio online nao funciona porque nao viram resultado
- Buscam alguem que EXPLIQUE o problema e RESOLVA para eles

FORMATO DOS ROTEIROS (OBRIGATORIO):
CADA ROTEIRO TEM 4 PARTES:

1. GANCHO (3-5 segundos, VIRAL e PROVOCADOR):
   - Frase curtíssima que PARA O SCROLL
   - Tom: irônico, sarcástico, confrontador ou que gera IDENTIFICAÇÃO IMEDIATA
   - Exemplos: "Continua queimando dinheiro então", "Trabalhando de graça pro concorrente", "Tá bom ficar estagnado"
   - NÃO explicar nada ainda, só provocar

2. DESENVOLVIMENTO (15-30 segundos, EDUCATIVO):
   - Explicar o PROBLEMA que o gestor tem
   - Usar exemplos REAIS do dia a dia
   - Estrutura: o que a maioria faz errado → por que erra → qual a consequência
   - Tom continua direto e provocador

3. CTA (5-10 segundos, NATURAL):
   - Call to action natural: "me manda um direct", "chama no direct", "vem comigo resolver isso"
   - Conectar com uma frase do gancho ou desenvolvimento
   - NÃO soar como venda forcada

4. NOTA DE ENTREGA (como o criador deve falar):
   - Velocidade (rápido, meio rápido, pausado)
   - Tom (sarcástico, sério, provocador, irônico)
   - Expressão (rosto de indignado, sarcástico, questionador)
   - Pausas (onde fazer pausa no vídeo)

TONS VIRAIS EM ALTA AGORA - USE BASTANTE:
- **SARCASMO**: "Continua queimando dinheiro então 🤦" (tom de: é óbvio que você tá errando)
- **IRONIA**: "Seu concorrente tá rindo mesmo sim" (fingir concordância enquanto provoca)
- **CONFRONTAÇÃO**: "Você não tá vendo resultado porque está fazendo errado" (direto, sem meias palavras)
- **ABSURDO**: "Você coloca R$100/dia em anúncio e acha que vai vender como McDonald's" (exagerar o erro)
- **IDENTIFICAÇÃO**: "Aposto que você já fez isso..." (gerar reconhecimento imediato)
- **PERGUNTA PROVOCADORA**: "Sabe por que seus anúncios não vendem?" (curiosidade + provocação)

Responda SEMPRE em português brasileiro COLOQUIAL. Responda APENAS com JSON valido."""

PROMPT_TEMPLATE = """NOTICIA sobre negocio de empresario local (clinica, loja, restaurante, consultorio):

NOTICIA:
Titulo: {title}
Resumo: {summary}
Fonte: {source}

IMPORTANTE: Use TONS VIRAIS — sarcasmo, ironia, confrontacao, absurdo, identificacao emocional.

Crie conteudo COMPLETO E VARIADO. Responda APENAS com JSON valido:

{{
  "roteiro_1": {{
    "gancho": "GANCHO SARCÁSTICO/IRÔNICO (3-5s) que PARA O SCROLL. Exemplo: 'Seu concorrente tá vendendo porque sabe esse segredo que você ignora'",
    "desenvolvimento": "ESPECÍFICO E EDUCATIVO (15-30s): Qual é o ERRO real? CONCRETO: 'Você acha que anuncio funciona sozinho', 'Você coloca dinheiro mas não acompanha', 'Seus anuncios chegam pra quem não quer'. POR QUE ERRA? 'Porque nao entende seu cliente', 'Porque nao sabe otimizar'. CONSEQUÊNCIA: 'Seu dinheiro vai pelo ralo'",
    "cta": "CTA NATURAL: 'Me chama no direct', 'Vem eu te mostro como', 'Quer entender isso?'",
    "nota_entrega": "VELOCIDADE: (rápido/pausado) | TOM: (sarcástico/provocador/direto) | EXPRESSÃO: (riso sarcástico/indignado) | PAUSAS: (pausa aqui para efeito)"
  }},

  "roteiro_2": {{
    "gancho": "GANCHO CONFRONTADOR diferente do roteiro_1. Use: pergunta provocadora, absurdo, ou identificação. Ex: 'Você prefere continuar queimando dinheiro ou quer aprender?'",
    "desenvolvimento": "Outro angulo TOTALMENTE DIFERENTE do roteiro_1. Se roteiro_1 foi sobre 'falta de estrategia', este pode ser 'falta de conhecimento', 'medo', 'procrastinação'",
    "cta": "Outra CTA natural - diferente da primeira",
    "nota_entrega": "Velocidade, tom, expressão, pausas"
  }},

  "roteiro_3": {{
    "gancho": "Terceiro gancho COMPLETAMENTE DIFERENTE - pode ser humor, absurdo, ou pergunta",
    "desenvolvimento": "Terceira perspectiva única",
    "cta": "Terceira CTA natural",
    "nota_entrega": "Como entregar"
  }},

  "carrossel": {{
    "titulo_capa": "Titulo educativo + provocador (max 8 palavras) - Ex: 'Por que seus anuncios nao vendem'",
    "subtitulo_capa": "Subtitulo que complementa (1-2 linhas)",
    "slide_2": "PROBLEMA: Qual é o problema que empresários enfrentam? (2-3 linhas específicas)",
    "slide_3": "POR QUE ERRA: Por que a maioria erra nisso? (2-3 linhas)",
    "slide_4": "CONSEQUÊNCIA: O que acontece se não resolver? (2-3 linhas)",
    "slide_5": "SOLUÇÃO: O que fazer diferente? (2-3 linhas práticas)",
    "slide_6_cta": "CALL TO ACTION: Me marca nos comentários | Me chama no direct | Salva esse carrossel"
  }},

  "legenda_sugerida": "Legenda viral (2-3 linhas) com gancho + emojis + CTA. Ex: 'Seu concorrente ta rindo 😂 Você já fez isso? Me chama no direct 👇'"
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
                temperature=0.7,
                max_tokens=2000,
                timeout=120.0,
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
