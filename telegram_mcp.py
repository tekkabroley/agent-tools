#!/Users/alexbroley/github/agent-tools/.venv/bin/python3
import os
import asyncio
import html
from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP
from telegram import Bot, InlineKeyboardButton, InlineKeyboardMarkup

load_dotenv()

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
AUTH_ID = os.getenv("AUTHORIZED_USER_ID")

if not TOKEN or not AUTH_ID:
    raise ValueError("Missing TELEGRAM_BOT_TOKEN or AUTHORIZED_USER_ID in .env")

AUTH_ID = int(AUTH_ID)
bot = Bot(token=TOKEN)
mcp = FastMCP("Telegram Notification Server")

OFFSET_FILE = os.path.join(os.path.dirname(__file__), ".telegram_offset")

def get_offset():
    if os.path.exists(OFFSET_FILE):
        try:
            with open(OFFSET_FILE, "r") as f:
                return int(f.read().strip())
        except:
            pass
    return None

def save_offset(offset):
    with open(OFFSET_FILE, "w") as f:
        f.write(str(offset))

@mcp.tool()
async def send_telegram_notification(message: str) -> str:
    """Sends a text message to the authorized user."""
    await bot.send_message(chat_id=AUTH_ID, text=message)
    return "Notification sent."

@mcp.tool()
async def send_terminal_output(logs: str) -> str:
    """Sends formatted code blocks or terminal logs."""
    if len(logs) > 4000:
        logs = logs[:4000] + "\n...[truncated]"
    
    escaped_logs = html.escape(logs)
    html_text = f"<pre><code>{escaped_logs}</code></pre>"
    await bot.send_message(chat_id=AUTH_ID, text=html_text, parse_mode="HTML")
    return "Terminal output sent."

@mcp.tool()
async def request_approval(message: str) -> str:
    """Sends a message with 'Approve' and 'Reject' buttons and waits for response."""
    keyboard = [
        [InlineKeyboardButton("Approve", callback_data='approve'),
         InlineKeyboardButton("Reject", callback_data='reject')]
    ]
    reply_markup = InlineKeyboardMarkup(inline_keyboard=keyboard)
    sent_msg = await bot.send_message(chat_id=AUTH_ID, text=message, reply_markup=reply_markup)
    
    offset = None
    # Flush pending updates
    updates = await bot.get_updates(timeout=1)
    if updates:
        offset = updates[-1].update_id + 1

    while True:
        updates = await bot.get_updates(offset=offset, timeout=5)
        for update in updates:
            offset = update.update_id + 1
            if update.callback_query and update.callback_query.message.message_id == sent_msg.message_id:
                query = update.callback_query
                if query.from_user.id != AUTH_ID:
                    await query.answer("Unauthorized", show_alert=True)
                    continue
                    
                await query.answer()
                res = query.data
                await bot.edit_message_text(
                    chat_id=AUTH_ID,
                    message_id=sent_msg.message_id,
                    text=f"{message}\n\n[ {res.upper()} ]"
                )
                return res
        await asyncio.sleep(1)

@mcp.tool()
async def get_latest_messages() -> str:
    """Retrieves the last 5 new messages sent by the authorized user and marks them as read."""
    offset = get_offset()
    try:
        updates = await bot.get_updates(offset=offset, limit=100, timeout=5)
    except Exception as e:
        return f"Error fetching updates: {str(e)}"
    
    auth_messages = []
    new_offset = offset
    
    for u in updates:
        if u.message and u.message.from_user.id == AUTH_ID and u.message.text:
            auth_messages.append(f"[{u.message.date}] {u.message.text}")
        
        # Track the highest update_id to increment offset
        if new_offset is None or u.update_id >= new_offset:
            new_offset = u.update_id + 1
            
    if new_offset is not None and (offset is None or new_offset > offset):
        save_offset(new_offset)
        
    if not auth_messages:
        return "No new messages from authorized user."
        
    # Return last 5
    latest = auth_messages[-5:]
    count = len(auth_messages)
    header = f"Found {count} new messages (showing last 5):\n" if count > 5 else f"Found {count} new messages:\n"
    return header + "\n".join(latest)

if __name__ == "__main__":
    mcp.run()
