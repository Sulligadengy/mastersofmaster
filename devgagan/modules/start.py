
from pyrogram import filters
from devgagan import app
from config import OWNER_ID
from devgagan.core.func import subscribe
import asyncio
from pyrogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton, Message
from pyrogram.raw.functions.bots import SetBotInfo
from pyrogram.raw.types import InputUserSelf
from pyrogram.types import BotCommand, InlineKeyboardButton, InlineKeyboardMarkup
from pyrogram.enums import ParseMode

# Register bot commands
async def setup_commands():
    commands = [
        BotCommand("start", "🚀 Start the bot"),
        BotCommand("batch", "🫠 Extract in bulk"),
        BotCommand("login", "🔑 Get into the bot"),
        BotCommand("logout", "🚪 Get out of the bot"),
        BotCommand("token", "🎲 Get 3 hours free access"),
        BotCommand("adl", "👻 Download audio from 30+ sites"),
        BotCommand("dl", "💀 Download videos from 30+ sites"),
        BotCommand("transfer", "💘 Gift premium to others"),
        BotCommand("myplan", "⌛ Get your plan details"),
        BotCommand("add", "➕ Add user to premium"),
        BotCommand("rem", "➖ Remove from premium"),
        BotCommand("settings", "⚙️ Personalize things"),
        BotCommand("stats", "📊 Get stats of the bot"),
        BotCommand("plan", "🗓️ Check our premium plans"),
        BotCommand("terms", "🥺 Terms and conditions"),
        BotCommand("speedtest", "🚅 Speed of server"),
        BotCommand("get", "🗄️ Get all user IDs"),
        BotCommand("lock", "🔒 Protect channel from extraction"),
        BotCommand("gcast", "⚡ Broadcast message to bot users"),
        BotCommand("help", "❓ If you're a noob, still!"),
        BotCommand("cancel", "🚫 Cancel batch process")
    ]
    await app.set_bot_commands(commands)

# Start command handler
@app.on_message(filters.command("start") & filters.private)
async def start(client, message: Message):
    join = await subscribe(client, message)
    if join == 1:
        return

    # Create persistent bottom menu bar
    bottom_menu = [
        [InlineKeyboardButton("📋 Menu", callback_data="show_menu"),
         InlineKeyboardButton("💬 Message", callback_data="message"),
         InlineKeyboardButton("📎 Attachment", callback_data="attachment"),
         InlineKeyboardButton("🎤 Voice", callback_data="voice")]
    ]
    
    # Ensure commands are set up
    await setup_commands()

    # Create menu buttons matching the screenshot layout
    menu_buttons = [
        [InlineKeyboardButton("🚀 Start the bot", callback_data="/start")],
        [InlineKeyboardButton("🔑 Set up your user session for private channels", callback_data="/login")],
        [InlineKeyboardButton("🤖 Set up your custom bot for uploading", callback_data="/setbot")],
        [InlineKeyboardButton("📥 Download and upload media from a link", callback_data="/d")],
        [InlineKeyboardButton("📁 Start batch downloading process", callback_data="/batch")],
        [InlineKeyboardButton("⚙️ adjust bot working", callback_data="/settings")],
        [InlineKeyboardButton("📊 fetch stats of a user", callback_data="/getstats")],
        [InlineKeyboardButton("🌐 Set up a proxy for better connectivity", callback_data="/setproxy")],
        [InlineKeyboardButton("🔄 Set up a proxy for better connectivity", callback_data="/transfer")],
        [InlineKeyboardButton("🎟️ Redeem Coupon code for 1 day premium", callback_data="/redeem")],
        [InlineKeyboardButton("🔍 Check your current session", callback_data="/session")]
    ]

    # Add admin-only buttons if user is owner
    if message.from_user.id in OWNER_ID:
        menu_buttons.extend([
            [InlineKeyboardButton("➕ Add Premium", callback_data="cmd_add"),
             InlineKeyboardButton("➖ Remove Premium", callback_data="cmd_rem")],
            [InlineKeyboardButton("🗄️ Get IDs", callback_data="cmd_get"),
             InlineKeyboardButton("🔒 Lock Channel", callback_data="cmd_lock")],
            [InlineKeyboardButton("⚡ Broadcast", callback_data="cmd_gcast")]
        ])

    welcome_text = (
        "👋 **Welcome to Advance Content Saver Bot!**\n\n"
        "I can help you save and manage content from various sources. "
        "Here are some quick actions to get started:\n\n"
        "• Use /login to access private channels\n"
        "• Try /batch for bulk downloads\n"
        "• Check /help for detailed instructions\n"
        "• Get premium with /plan for more features"
    )

    # Send welcome message with bottom menu
    await message.reply(
        welcome_text,
        reply_markup=InlineKeyboardMarkup(bottom_menu)
    )

# Callback query handler for menu buttons
@app.on_callback_query(filters.regex(r"^(cmd_|menu_|show_|close_|message|attachment|voice)"))
async def handle_menu_callbacks(client, callback_query):
    data = callback_query.data
    
    if data == "show_menu":
        # Show full menu when Menu button is clicked
        menu_buttons_with_back = menu_buttons.copy()
        menu_buttons_with_back.append([InlineKeyboardButton("❌ Close", callback_data="close_menu")])
        await callback_query.message.edit_text(
            "🚀 **Bot Commands**\n\n"
            "Select a command to get started:",
            reply_markup=InlineKeyboardMarkup(menu_buttons_with_back)
        )
        return
    
    elif data == "message":
        await callback_query.answer("Send your message directly to chat")
        return
        
    elif data == "attachment":
        await callback_query.answer("Send your file as an attachment")
        return
        
    elif data == "voice":
        await callback_query.answer("Send your voice message")
        return
    
    elif data == "close_menu":
        # Delete the message when Close button is clicked
        await callback_query.message.delete()
        return
    
    elif data.startswith("menu_"):
        # Handle menu button clicks
        command = data.replace("menu_", "")
        if command == "start":
            await callback_query.message.edit_text(
                welcome_text,
                reply_markup=InlineKeyboardMarkup(bottom_menu)
            )
        return

    # Handle command info buttons
    command = data.replace("cmd_", "")
    # Map of commands to their descriptions
    command_info = {
        "start": "🚀 Use /start to begin",
        "batch": "🫠 Use /batch to extract in bulk",
        "login": "🔑 Use /login to access private channels",
        "logout": "🚪 Use /logout to sign out",
        "token": "🎲 Use /token for 3 hours free access",
        "adl": "👻 Use /adl to download audio",
        "dl": "💀 Use /dl to download videos",
        "transfer": "💘 Use /transfer to gift premium",
        "myplan": "⌛ Use /myplan to check your subscription",
        "add": "➕ Use /add to grant premium access",
        "rem": "➖ Use /rem to remove premium access",
        "settings": "⚙️ Use /settings to customize bot",
        "stats": "📊 Use /stats to view bot statistics",
        "plan": "🗓️ Use /plan to see premium options",
        "terms": "🥺 Use /terms to read conditions",
        "speedtest": "🚅 Use /speedtest to check server speed",
        "get": "🗄️ Use /get to fetch user IDs",
        "lock": "🔒 Use /lock to protect channels",
        "gcast": "⚡ Use /gcast to broadcast messages",
        "help": "❓ Use /help for instructions",
        "cancel": "🚫 Use /cancel to stop processes"
    }

    await callback_query.answer(command_info.get(command, "Command not found"))
# Set bot commands in one place
@app.on_message(filters.command("set"))
async def set(_, message):
    if message.from_user.id not in OWNER_ID:
        await message.reply("You are not authorized to use this command.")
        return
    # Setting all the bot commands
    await app.set_bot_commands([
        BotCommand("start", "🚀 Start the bot"),
        BotCommand("batch", "🫠 Extract in bulk"),
        BotCommand("login", "🔑 Get into the bot"),
        BotCommand("logout", "🚪 Get out of the bot"),
        BotCommand("token", "🎲 Get 3 hours free access"),
        BotCommand("adl", "👻 Download audio from 30+ sites"),
        BotCommand("dl", "💀 Download videos from 30+ sites"),
        BotCommand("transfer", "💘 Gift premium to others"),
        BotCommand("myplan", "⌛ Get your plan details"),
        BotCommand("add", "➕ Add user to premium"),
        BotCommand("rem", "➖ Remove from premium"),
        BotCommand("settings", "⚙️ Personalize things"),
        BotCommand("stats", "📊 Get stats of the bot"),
        BotCommand("plan", "🗓️ Check our premium plans"),
        BotCommand("terms", "🥺 Terms and conditions"),
        BotCommand("speedtest", "🚅 Speed of server"),
        BotCommand("get", "🗄️ Get all user IDs"),
        BotCommand("lock", "🔒 Protect channel from extraction"),
        BotCommand("gcast", "⚡ Broadcast message to bot users"),
        BotCommand("help", "❓ If you're a noob, still!"),
        BotCommand("cancel", "🚫 Cancel batch process")
    ])
    
    await message.reply("✅ Commands configured successfully!")

# Function to split and manage the help message in multiple parts

# Function to split and manage the help message in multiple parts
help_pages = [
    (
        "📝 **Bot Commands Overview (1/2)**:\n\n"
        "1. **/add userID**\n"
        "> Add user to premium (Owner only)\n\n"
        "2. **/rem userID**\n"
        "> Remove user from premium (Owner only)\n\n"
        "3. **/transfer userID**\n"
        "> Transfer premium to your beloved major purpose for resellers (Premium members only)\n\n"
        "4. **/get**\n"
        "> Get all user IDs (Owner only)\n\n"
        "5. **/lock**\n"
        "> Lock channel from extraction (Owner only)\n\n"
        "6. **/dl link**\n"
        "> Download videos (Not available )\n\n"
        "7. **/adl link**\n"
        "> Download audio (Not available )\n\n"
        "8. **/login**\n"
        "> Log into the bot for private channel access\n\n"
        "9. **/batch**\n"
        "> Bulk extraction for posts (After login)\n\n"
    ),
    (
        "📝 **Bot Commands Overview (2/2)**:\n\n"
        "10. **/logout**\n"
        "> Logout from the bot\n\n"
        "11. **/stats**\n"
        "> Get bot stats\n\n"
        "12. **/plan**\n"
        "> Check premium plans\n\n"
        "13. **/speedtest**\n"
        "> Test the server speed (not available in v3)\n\n"
        "14. **/terms**\n"
        "> Terms and conditions\n\n"
        "15. **/cancel**\n"
        "> Cancel ongoing batch process\n\n"
        "16. **/myplan**\n"
        "> Get details about your plans\n\n"
        "17. **/session**\n"
        "> Generate Pyrogram V2 session\n\n"
        "18. **/settings**\n"
        "> 1. SETCHATID : To directly upload in channel or group or user's dm use it with -100[chatID]\n"
        "> 2. SETRENAME : To add custom rename tag or username of your channels\n"
        "> 3. CAPTION : To add custom caption\n"
        "> 4. REPLACEWORDS : Can be used for words in deleted set via REMOVE WORDS\n"
        "> 5. RESET : To set the things back to default\n\n"
        "> You can set CUSTOM THUMBNAIL, PDF WATERMARK, VIDEO WATERMARK, SESSION-based login, etc. from settings\n\n"
        "**__All Set ✅__**"    
    )
]

# Helper function to send or edit help messages with navigation buttons
async def send_or_edit_help_page(_, message, page_number):
    if page_number < 0 or page_number >= len(help_pages):
        return

    # Define the navigation buttons (previous, next)
    prev_button = InlineKeyboardButton("◀️ Previous", callback_data=f"help_prev_{page_number}")
    next_button = InlineKeyboardButton("Next ▶️", callback_data=f"help_next_{page_number}")

    # Add buttons conditionally
    buttons = []
    if page_number > 0:
        buttons.append(prev_button)
    if page_number < len(help_pages) - 1:
        buttons.append(next_button)

    # Create the keyboard
    keyboard = InlineKeyboardMarkup([buttons])

    # Delete the previous message before sending a new one
    await message.delete()

    # Send the appropriate help page
    await message.reply(
        help_pages[page_number],
        reply_markup=keyboard
    )

# Start command with help navigation
@app.on_message(filters.command("help"))
async def help(client, message):
    join = await subscribe(client, message)
    if join == 1:
        return
    
    # Show the first help page
    await send_or_edit_help_page(client, message, 0)

# Handle callback queries for help navigation
@app.on_callback_query(filters.regex(r"help_(prev|next)_(\d+)"))
async def on_help_navigation(client, callback_query):
    action, page_number = callback_query.data.split("_")[1], int(callback_query.data.split("_")[2])

    if action == "prev":
        page_number -= 1
    elif action == "next":
        page_number += 1

    # Edit the appropriate help page
    await send_or_edit_help_page(client, callback_query.message, page_number)

    # Acknowledge the callback query
    await callback_query.answer()


from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

@app.on_message(filters.command("terms") & filters.private)
async def terms(client, message):
    terms_text = (
        "📜 **Terms and Conditions** 📜\n\n"
        "✨ We are not responsible for user deeds, and we do not promote copyrighted content. If any user engages in such activities, it is solely their responsibility.\n"
        "✨ Upon purchase, we do not guarantee the uptime, downtime, or the validity of the plan. __Authorization and banning of users are at our discretion; we reserve the right to ban or authorize users at any time.__\n"
        "✨ Payment to us **__does not guarantee__** authorization for the /batch command. All decisions regarding authorization are made at our discretion and mood.\n"
    )
    # Buttons for "See Plans" and "Contact"
    buttons = InlineKeyboardMarkup(
        [
            [InlineKeyboardButton("📋 See Plans", callback_data="see_plan")],
            [InlineKeyboardButton("💬 Contact Now", url="https://t.me/She_who_remain")],
        ]
    )
    await message.reply_text(terms_text, reply_markup=buttons)


@app.on_message(filters.command("plan") & filters.private)
async def plan(client, message):
    plan_text = (
        "💰 **Premium Price**: Starting from $2 or 200 INR accepted via **__Amazon Gift Card__** (terms and conditions apply).\n"
        "📥 **Download Limit**: Users can download up to 100,000 files in a single batch command.\n"
        "🛑 **Batch**: You will get two modes /bulk and /batch.\n"
        "   - Users are advised to wait for the process to automatically cancel before proceeding with any downloads or uploads.\n\n"
        "📜 **Terms and Conditions**: For further details and complete terms and conditions, please send /terms.\n"
    )
    # Buttons for "See Terms" and "Contact"
    buttons = InlineKeyboardMarkup(
        [
            [InlineKeyboardButton("📜 See Terms", callback_data="see_terms")],
            [InlineKeyboardButton("💬 Contact Now", url="https://t.me/She_who_remain")],
        ]
    )
    await message.reply_text(plan_text, reply_markup=buttons)


@app.on_callback_query(filters.regex("see_plan"))
async def see_plan(client, callback_query):
    plan_text = (
        "💰 **Premium Price**: Starting from $2 or 200 INR accepted via **__Amazon Gift Card__** (terms and conditions apply).\n"
        "📥 **Download Limit**: Users can download up to 100,000 files in a single batch command.\n"
        "🛑 **Batch**: You will get two modes /bulk and /batch.\n"
        "   - Users are advised to wait for the process to automatically cancel before proceeding with any downloads or uploads.\n\n"
        "📜 **Terms and Conditions**: For further details and complete terms and conditions, please send /terms or click See Terms👇\n"
    )
    # Buttons for "See Terms" and "Contact"
    buttons = InlineKeyboardMarkup(
        [
            [InlineKeyboardButton("📜 See Terms", callback_data="see_terms")],
            [InlineKeyboardButton("💬 Contact Now", url="https://t.me/She_who_remain")],
        ]
    )
    await callback_query.message.edit_text(plan_text, reply_markup=buttons)


@app.on_callback_query(filters.regex("see_terms"))
async def see_terms(client, callback_query):
    terms_text = (
        "📜 **Terms and Conditions** 📜\n\n"
        "✨ We are not responsible for user deeds, and we do not promote copyrighted content. If any user engages in such activities, it is solely their responsibility.\n"
        "✨ Upon purchase, we do not guarantee the uptime, downtime, or the validity of the plan. __Authorization and banning of users are at our discretion; we reserve the right to ban or authorize users at any time.__\n"
        "✨ Payment to us **__does not guarantee__** authorization for the /batch command. All decisions regarding authorization are made at our discretion and mood.\n"
    )
    # Buttons for "See Plans" and "Contact"
    buttons = InlineKeyboardMarkup(
        [
            [InlineKeyboardButton("📋 See Plans", callback_data="see_plan")],
            [InlineKeyboardButton("💬 Contact Now", url="https://t.me/She_who_remain")],
        ]
    )
    await callback_query.message.edit_text(terms_text, reply_markup=buttons)
    
