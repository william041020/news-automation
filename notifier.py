"""
Telegram notification sender.
"""

import os
import asyncio
from pathlib import Path


async def send_telegram_async(preview: str, filepath: Path) -> bool:
    """Send message and file to Telegram chat asynchronously."""
    try:
        from telegram import Bot
    except ImportError:
        print("  Aviso: python-telegram-bot nao instalado.")
        return False

    token = os.getenv("TELEGRAM_BOT_TOKEN", "")
    chat_id = os.getenv("TELEGRAM_CHAT_ID", "")

    if not token or not chat_id:
        print("  Aviso: Telegram nao configurado no .env")
        return False

    try:
        bot = Bot(token=token)
        await bot.send_message(
            chat_id=chat_id,
            text=preview,
            parse_mode="Markdown",
        )
        with open(filepath, "rb") as f:
            await bot.send_document(
                chat_id=chat_id,
                document=f,
                filename=filepath.name,
                caption="2 roteiros + carrossel + thread + legenda por pauta. Bora gravar!",
            )
        print("  Enviado para Telegram!")
        return True
    except Exception as e:
        print(f"  Erro ao enviar para Telegram: {e}")
        return False


def send_telegram(preview: str, filepath: Path) -> bool:
    """Send notification to Telegram (wrapper for async function)."""
    try:
        return asyncio.run(send_telegram_async(preview, filepath))
    except RuntimeError:
        loop = asyncio.new_event_loop()
        result = loop.run_until_complete(send_telegram_async(preview, filepath))
        loop.close()
        return result
