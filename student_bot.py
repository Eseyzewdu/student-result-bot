import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext, CallbackQueryHandler

# ========== CONFIGURATION ==========
BOT_TOKEN = "8854246490:AAFsdSKu1F5yCYdIEfL3MOS29m0BIMDOupE"  # Replace with your bot token from @BotFather

# ========== SETUP LOGGING ==========
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", 
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# ========== STUDENT DATA ==========
STUDENT_DATA = [
    {"Student ID": "NSR/0036/16", "FirstName": "ABINET", "Fath.Name": "BELEYNEH", "GF.Name": "TADELE", "Sex": "M", "Ass": 18, "ME": 26, "FE": 34, "Sum": 78},
    {"Student ID": "NSR/0065/16", "FirstName": "AISHA", "Fath.Name": "KABTU", "GF.Name": "MOHAMMED", "Sex": "F", "Ass": 17, "ME": 28.5, "FE": 37.5, "Sum": 83},
    {"Student ID": "NSR/0075/16", "FirstName": "ALEWYA", "Fath.Name": "SHRIF", "GF.Name": "MESHSESHA", "Sex": "F", "Ass": 17, "ME": 28.5, "FE": 43.5, "Sum": 89},
    {"Student ID": "NSR/0084/16", "FirstName": "AMEN", "Fath.Name": "WAKWAYA", "GF.Name": "GONFA", "Sex": "F", "Ass": 17, "ME": 28, "FE": 39, "Sum": 84},
    {"Student ID": "NSR/0090/16", "FirstName": "AMRIYA", "Fath.Name": "ASFAW", "GF.Name": "BENTI", "Sex": "F", "Ass": 17, "ME": 27.5, "FE": 37.5, "Sum": 82},
    {"Student ID": "NSR/0089/16", "FirstName": "AMRIYA", "Fath.Name": "SHERIF", "GF.Name": "JEMAL", "Sex": "F", "Ass": 17, "ME": 28.5, "FE": 40, "Sum": 85.5},
    {"Student ID": "NSR/0171/16", "FirstName": "BETHLEHEM", "Fath.Name": "BOGALE", "GF.Name": "MULUGETA", "Sex": "F", "Ass": 18, "ME": 20, "FE": 38, "Sum": 76},
    {"Student ID": "NSR/0184/16", "FirstName": "BINIAM", "Fath.Name": "YOSEPH", "GF.Name": "HAKAMO", "Sex": "M", "Ass": 17, "ME": 25, "FE": 30, "Sum": 72},
    {"Student ID": "NSR/0197/16", "FirstName": "BIRUK", "Fath.Name": "GETU", "GF.Name": "MENUTA", "Sex": "M", "Ass": 17.5, "ME": 29.5, "FE": 39, "Sum": 86},
    {"Student ID": "NSR/0217/16", "FirstName": "DAGMAWIT", "Fath.Name": "NEGASH", "GF.Name": "YADTE", "Sex": "F", "Ass": 17.5, "ME": 28, "FE": 45, "Sum": 90.5},
    {"Student ID": "NSR/2882/14", "FirstName": "DAWIT", "Fath.Name": "TARIKU", "GF.Name": "ABEBE", "Sex": "M", "Ass": 17.5, "ME": 20, "FE": 32.5, "Sum": 70},
    {"Student ID": "NSR/0233/16", "FirstName": "DEBELE", "Fath.Name": "DEMBOBA", "GF.Name": "KEBU", "Sex": "M", "Ass": 17.5, "ME": 24, "FE": 33.5, "Sum": 75},
    {"Student ID": "NSR/0272/16", "FirstName": "ELILI", "Fath.Name": "TEKELEMARIAM", "GF.Name": "GIRMA", "Sex": "F", "Ass": 17.5, "ME": 28, "FE": 42, "Sum": 87.5},
    {"Student ID": "NSR/0284/16", "FirstName": "ERMIYAS", "Fath.Name": "ASHENAFI", "GF.Name": "DURA", "Sex": "M", "Ass": 17.5, "ME": 23.5, "FE": 31.5, "Sum": 72.5},
    {"Student ID": "NSR/0285/16", "FirstName": "ESA", "Fath.Name": "ADEM", "GF.Name": "ALIYI", "Sex": "M", "Ass": 17, "ME": 24, "FE": 27, "Sum": 68},
    {"Student ID": "NSR/0286/16", "FirstName": "ESEY", "Fath.Name": "ZEWDU", "GF.Name": "MENUTA", "Sex": "M", "Ass": 17, "ME": 27, "FE": 38, "Sum": 82},
    {"Student ID": "NSR/0288/16", "FirstName": "ESKEDAR", "Fath.Name": "MESKELU", "GF.Name": "ABEBE", "Sex": "F", "Ass": 17, "ME": 24, "FE": 40, "Sum": 81},
    {"Student ID": "NSR/0377/16", "FirstName": "HABIBA", "Fath.Name": "ABDLHAKIM", "GF.Name": "BEDEWI", "Sex": "F", "Ass": 17, "ME": 23, "FE": 27, "Sum": 67},
    {"Student ID": "NSR/0395/16", "FirstName": "HANA", "Fath.Name": "TESFAYE", "GF.Name": "KIFLE", "Sex": "F", "Ass": 17, "ME": 22, "FE": 30, "Sum": 69},
    {"Student ID": "NSR/0409/16", "FirstName": "HAYMANOT", "Fath.Name": "NIGUSIE", "GF.Name": "AYTENEW", "Sex": "M", "Ass": 17, "ME": 21, "FE": 29.5, "Sum": 67.5},
    {"Student ID": "NSR/0415/16", "FirstName": "HERAN", "Fath.Name": "DEMOZE", "GF.Name": "LEGESE", "Sex": "F", "Ass": 17, "ME": 25.5, "FE": 29, "Sum": 71.5},
    {"Student ID": "NSR/0426/16", "FirstName": "HIWOT", "Fath.Name": "ABEBE", "GF.Name": "MERGA", "Sex": "F", "Ass": 17, "ME": 26.5, "FE": 28, "Sum": 71.5},
    {"Student ID": "NSR/0431/16", "FirstName": "HUSNYA", "Fath.Name": "KASSIM", "GF.Name": "BEREKA", "Sex": "F", "Ass": 17, "ME": 24.5, "FE": 31, "Sum": 72.5},
    {"Student ID": "NSR/0434/16", "FirstName": "IMAN", "Fath.Name": "SULEYMAN", "GF.Name": "AYALEW", "Sex": "F", "Ass": 17, "ME": 22.5, "FE": 21.5, "Sum": 61},
    {"Student ID": "NSR/0875/16", "FirstName": "KALKIDAN", "Fath.Name": "TADESSE", "GF.Name": "DIR", "Sex": "F", "Ass": 17, "ME": 28, "FE": 27.5, "Sum": 72.5},
    {"Student ID": "NSR/0462/16", "FirstName": "KALKIDAN", "Fath.Name": "TAREKEGN", "GF.Name": "WOLDE", "Sex": "F", "Ass": 17, "ME": 27, "FE": 36, "Sum": 80},
    {"Student ID": "NSR/0474/16", "FirstName": "KEFALE", "Fath.Name": "MIHRET", "GF.Name": "GETIE", "Sex": "M", "Ass": 18, "ME": 23, "FE": 34.5, "Sum": 75.5},
    {"Student ID": "NSR/0481/16", "FirstName": "KEROD", "Fath.Name": "GINBARU", "GF.Name": "HAILEMARIAM", "Sex": "M", "Ass": 17, "ME": 27.5, "FE": 36.5, "Sum": 81},
    {"Student ID": "NSR/0489/16", "FirstName": "KIDIST", "Fath.Name": "NURGA", "GF.Name": "BIREDA", "Sex": "F", "Ass": 18, "ME": 29, "FE": 43, "Sum": 90},
    {"Student ID": "NSR/0512/16", "FirstName": "LEMI", "Fath.Name": "GIRMA", "GF.Name": "LEGESE", "Sex": "M", "Ass": 18, "ME": 28, "FE": 30, "Sum": 76},
    {"Student ID": "NSR/0876/16", "FirstName": "MELAT", "Fath.Name": "MEKONNEN", "GF.Name": "AMERGA", "Sex": "F", "Ass": 19, "ME": 24.5, "FE": 40.5, "Sum": 84},
    {"Student ID": "NSR/0580/16", "FirstName": "MINTESNOT", "Fath.Name": "GENNE", "GF.Name": "MENGETA", "Sex": "M", "Ass": 18, "ME": 24, "FE": 31.5, "Sum": 73.5},
    {"Student ID": "NSR/0585/16", "FirstName": "MOLALIGN", "Fath.Name": "WUCHE", "GF.Name": "DEBEBE", "Sex": "M", "Ass": 18, "ME": 26.5, "FE": 36, "Sum": 80.5},
    {"Student ID": "NSR/0601/16", "FirstName": "MUNIRA", "Fath.Name": "MOHAMED", "GF.Name": "AWEL", "Sex": "F", "Ass": 18, "ME": 29.5, "FE": 31.5, "Sum": 79},
    {"Student ID": "NSR/0608/16", "FirstName": "NAHOM", "Fath.Name": "SATANA", "GF.Name": "SANTA", "Sex": "M", "Ass": 17, "ME": 22, "FE": 26, "Sum": 65},
    {"Student ID": "NSR/1949*/14", "FirstName": "OBSA", "Fath.Name": "GEREMEW", "GF.Name": "WEADAJO", "Sex": "M", "Ass": 19, "ME": 25, "FE": 34.5, "Sum": 78.5},
    {"Student ID": "NSR/0665/16", "FirstName": "RIYAD", "Fath.Name": "HASSEN", "GF.Name": "REDIYU", "Sex": "M", "Ass": 19, "ME": 29.5, "FE": 38.5, "Sum": 87},
    {"Student ID": "NSR/1000/16", "FirstName": "SEID", "Fath.Name": "TEMAM", "GF.Name": "SHERIF", "Sex": "M", "Ass": 19, "ME": 26, "FE": 31.5, "Sum": 76.5},
    {"Student ID": "NSR/0703/16", "FirstName": "SEMIRA", "Fath.Name": "YIBRO", "GF.Name": "HUSSEN", "Sex": "F", "Ass": 18, "ME": 21.5, "FE": 33.5, "Sum": 73},
    {"Student ID": "NSR/0730/16", "FirstName": "SURAFEL", "Fath.Name": "SIYUM", "GF.Name": "WORKU", "Sex": "M", "Ass": 17, "ME": 28, "FE": 43, "Sum": 88},
    {"Student ID": "NSR/0747/16", "FirstName": "TAMRAT", "Fath.Name": "MALISE", "GF.Name": "ANSA", "Sex": "M", "Ass": 17, "ME": 28, "FE": 46, "Sum": 91},
    {"Student ID": "NSR/0803/16", "FirstName": "TSION", "Fath.Name": "FIKADU", "GF.Name": "NIGANI", "Sex": "F", "Ass": 19, "ME": 24, "FE": 31.5, "Sum": 74.5},
    {"Student ID": "NSR/0823/16", "FirstName": "WUBALEM", "Fath.Name": "GASHAW", "GF.Name": "ABERA", "Sex": "F", "Ass": 19, "ME": 24, "FE": 38.5, "Sum": 81.5},
    {"Student ID": "NSR/0826/16", "FirstName": "YAFET", "Fath.Name": "YILMA", "GF.Name": "GEBERMARIYAM", "Sex": "M", "Ass": 17, "ME": 26.5, "FE": 40, "Sum": 83.5},
    {"Student ID": "NSR/0830/16", "FirstName": "YARED", "Fath.Name": "MELIKAMU", "GF.Name": "DAMITE", "Sex": "M", "Ass": 19, "ME": 17, "FE": 29.5, "Sum": 65.5},
    {"Student ID": "NSR/0833/16", "FirstName": "YASSIN", "Fath.Name": "MOHAMMED", "GF.Name": "HASSEN", "Sex": "M", "Ass": 19, "ME": 24.5, "FE": 25.5, "Sum": 69},
]

# ========== SEARCH FUNCTION ==========
def search_student(query):
    """Search for a student by ID or name (case-insensitive)"""
    query = query.strip().upper()
    results = []
    
    for student in STUDENT_DATA:
        # Search by ID
        if query in student["Student ID"].upper():
            results.append(student)
            continue
        
        # Search by First Name
        if query in student["FirstName"].upper():
            results.append(student)
            continue
        
        # Search by Full Name (First + Father)
        full_name = f"{student['FirstName']} {student['Fath.Name']}".upper()
        if query in full_name:
            results.append(student)
            continue
    
    return results

# ========== FORMAT RESULT ==========
def format_student_result(student):
    """Format a single student's result as a Telegram message"""
    total = student["Sum"]
    
    # Grade based on total
    if total >= 85:
        grade = "🌟 Excellent"
    elif total >= 75:
        grade = "✅ Good"
    elif total >= 65:
        grade = "📖 Average"
    else:
        grade = "📚 Needs Improvement"
    
    message = f"""
👤 <b>{student['FirstName']} {student['Fath.Name']}</b>
🆔 <code>{student['Student ID']}</code>
⚤ Sex: {student['Sex']}

📊 <b>Academic Results</b>
━━━━━━━━━━━━━━━━━
📝 Assignment:  {student['Ass']}/20
📈 Mid Exam:    {student['ME']}/30
📉 Final Exam:  {student['FE']}/50
━━━━━━━━━━━━━━━━━
🎯 <b>Total: {total}/100</b>
🏅 {grade}

👨‍👦 Father: {student['Fath.Name']}
👴 Grandfather: {student['GF.Name']}
"""
    return message

# ========== BOT COMMANDS ==========

async def start(update: Update, context: CallbackContext):
    """Send welcome message."""
    welcome_text = """
🎓 <b>Student Result Bot</b>

Welcome! I can help you check student results.

<b>How to use:</b>
• Send a <b>Student ID</b> (e.g., NSR/0036/16)
• Send a <b>First Name</b> (e.g., ABINET)
• Send a <b>Full Name</b> (e.g., ABINET BELEYNEH)

I'll show you the student's complete result! 📊
"""
    await update.message.reply_text(welcome_text, parse_mode="HTML")

async def help_command(update: Update, context: CallbackContext):
    """Send help message."""
    help_text = """
<b>📖 Help</b>

<b>Search by:</b>
• Student ID: <code>NSR/0036/16</code>
• First Name: <code>ABINET</code>
• Full Name: <code>ABINET BELEYNEH</code>

<b>Commands:</b>
/start - Welcome
/help - This help

<b>Example:</b>
Send <code>NSR/0036/16</code> to see ABINET's result.
"""
    await update.message.reply_text(help_text, parse_mode="HTML")

async def handle_message(update: Update, context: CallbackContext):
    """Handle user messages."""
    query = update.message.text.strip()
    
    if not query:
        await update.message.reply_text("Please enter a name or ID to search.")
        return
    
    results = search_student(query)
    
    if not results:
        await update.message.reply_text(
            f"❌ No student found with: <b>{query}</b>\n\n"
            "Please check the spelling or try a different search.",
            parse_mode="HTML"
        )
        return
    
    if len(results) == 1:
        student = results[0]
        message = format_student_result(student)
        await update.message.reply_text(message, parse_mode="HTML")
    else:
        response = f"🔍 Found <b>{len(results)}</b> student(s):\n\n"
        
        keyboard = []
        for student in results[:10]:
            button_text = f"{student['FirstName']} {student['Fath.Name']}"
            callback_data = f"view_{student['Student ID']}"
            keyboard.append([InlineKeyboardButton(button_text, callback_data=callback_data)])
        
        if len(results) > 10:
            response += f"\n<i>(Showing first 10 of {len(results)})</i>"
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text(response, parse_mode="HTML", reply_markup=reply_markup)

async def button_callback(update: Update, context: CallbackContext):
    """Handle button clicks."""
    query = update.callback_query
    await query.answer()
    
    student_id = query.data.replace("view_", "")
    
    for student in STUDENT_DATA:
        if student["Student ID"] == student_id:
            message = format_student_result(student)
            await query.edit_message_text(message, parse_mode="HTML")
            return
    
    await query.edit_message_text("❌ Student not found.")

# ========== FIX FOR SSL ERROR ==========
def fix_ssl_issue():
    """Fix SSL certificate issue on Windows with Python 3.14"""
    try:
        import ssl
        import certifi
        import os
        
        # Set SSL certificate file
        os.environ['SSL_CERT_FILE'] = certifi.where()
        os.environ['REQUESTS_CA_BUNDLE'] = certifi.where()
        logger.info("SSL certificate fixed using certifi")
    except ImportError:
        logger.warning("certifi not installed, trying alternative fix")
        try:
            import ssl
            # Create default SSL context
            ssl._create_default_https_context = ssl._create_unverified_context
            logger.info("SSL verification disabled as fallback")
        except:
            logger.warning("Could not fix SSL issue")

# ========== MAIN ==========
def main():
    """Start the bot."""
    # Fix SSL issue first
    fix_ssl_issue()
    
    # Create application with custom request to avoid SSL issues
    from telegram.request import HTTPXRequest
    
    # Build request with custom settings
    request = HTTPXRequest(
        connection_pool_size=8,
        connect_timeout=30.0,
        read_timeout=30.0,
        write_timeout=30.0,
        pool_timeout=30.0,
    )
    
    # Build application
    application = (
        Application.builder()
        .token(BOT_TOKEN)
        .request(request)
        .build()
    )
    
    # Add handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    application.add_handler(CallbackQueryHandler(button_callback))
    
    # Start bot
    print("🤖 Student Result Bot is running...")
    print("Press Ctrl+C to stop.")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()