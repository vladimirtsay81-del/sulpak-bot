import asyncio
asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
import logging
import sqlite3
from datetime import datetime
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, ConversationHandler, ContextTypes, filters

BOT_TOKEN = "8681803459:AAFrSqH05SZLw8ldG5-9pA3Uq3g0TW4en9E"
VENDOR_CHAT_ID = 547710147
MANAGER_IDS = [547710147]

STORE_CODES = {
    "SLK-22091-8WIK": "22091",
    "SLK-22101-M2UA": "22101",
    "SLK-22104-5161": "22104",
    "SLK-22109-Y2JC": "22109",
    "SLK-22112-PDWK": "22112",
    "SLK-22113-NYWT": "22113",
    "SLK-22114-B2GE": "22114",
    "SLK-22115-307U": "22115",
    "SLK-22117-Y1BI": "22117",
    "SLK-22118-TGSO": "22118",
    "SLK-22119-HSMN": "22119",
    "SLK-22120-03WZ": "22120",
    "SLK-22122-6RAY": "22122",
    "SLK-22123-PYNV": "22123",
    "SLK-22124-UEWF": "22124",
    "SLK-22125-N0CU": "22125",
    "SLK-22127-570Z": "22127",
    "SLK-22128-HJ6C": "22128",
    "SLK-22129-GJTD": "22129",
    "SLK-22131-PPXX": "22131",
    "SLK-22132-LZPK": "22132",
    "SLK-22133-GRI7": "22133",
    "SLK-22134-RMXN": "22134",
    "SLK-22135-LCKP": "22135",
    "SLK-22202-GX9F": "22202",
    "SLK-22206-DQOG": "22206",
    "SLK-22207-J9IP": "22207",
    "SLK-22208-K4NI": "22208",
    "SLK-22209-1C5G": "22209",
    "SLK-22210-Q62G": "22210",
    "SLK-22211-UABG": "22211",
    "SLK-22213-OWER": "22213",
    "SLK-22214-0Y8M": "22214",
    "SLK-22215-XW03": "22215",
    "SLK-22216-2VPE": "22216",
    "SLK-22302-W87U": "22302",
    "SLK-22304-MGD1": "22304",
    "SLK-22305-YW5P": "22305",
    "SLK-22306-9X37": "22306",
    "SLK-22307-V8AE": "22307",
    "SLK-22308-0XBB": "22308",
    "SLK-22310-IS9F": "22310",
    "SLK-22311-WH94": "22311",
    "SLK-22312-Q4L5": "22312",
    "SLK-22314-FJJ4": "22314",
    "SLK-22315-804P": "22315",
    "SLK-22316-RRSD": "22316",
    "SLK-22404-Z20D": "22404",
    "SLK-22406-MDJT": "22406",
    "SLK-22407-Q37I": "22407",
    "SLK-22409-GGYI": "22409",
    "SLK-22410-0PCU": "22410",
    "SLK-22411-73IU": "22411",
    "SLK-22412-WPCE": "22412",
    "SLK-22413-K7GA": "22413",
    "SLK-22414-G1AR": "22414",
    "SLK-22416-YKA2": "22416",
    "SLK-22417-YNDK": "22417",
    "SLK-22501-DGZ7": "22501",
    "SLK-22504-SWH0": "22504",
    "SLK-22509-LTYH": "22509",
    "SLK-22510-038G": "22510",
    "SLK-22512-B1N3": "22512",
    "SLK-22513-1D7R": "22513",
    "SLK-22603-JW65": "22603",
    "SLK-22604-PPFL": "22604",
    "SLK-22607-REXQ": "22607",
    "SLK-22608-IYI3": "22608",
    "SLK-22609-X3IY": "22609",
    "SLK-22702-H9T6": "22702",
    "SLK-22703-J39O": "22703",
    "SLK-22704-EZ0U": "22704",
    "SLK-22707-6Y5S": "22707",
    "SLK-22801-CNEH": "22801",
    "SLK-22806-DBEG": "22806",
    "SLK-22807-Z71X": "22807",
    "SLK-22809-TDPV": "22809",
    "SLK-22812-SR7Y": "22812",
    "SLK-22813-G8FH": "22813",
    "SLK-22815-18LW": "22815",
    "SLK-22816-U7LB": "22816",
    "SLK-22903-OA7C": "22903",
    "SLK-22A01-TLPL": "22A01",
    "SLK-22A02-88L6": "22A02",
    "SLK-22B02-A6W1": "22B02",
    "SLK-22B03-XW86": "22B03",
    "SLK-22B05-SK6V": "22B05",
    "SLK-22B07-XYF1": "22B07",
    "SLK-22В09-EOGF": "22В09",
    "SLK-22В11-3PBH": "22В11",
    "SLK-22C02-CT1F": "22C02",
    "SLK-22С03-I2PS": "22С03",
    "SLK-22С04-8SPL": "22С04",
    "SLK-22С05-GGFJ": "22С05",
    "SLK-22С06-HXC4": "22С06",
    "SLK-22С07-43IY": "22С07",
    "SLK-22С08-CDYM": "22С08",
    "SLK-22С09-KS5T": "22С09",
    "SLK-22С10-9RS2": "22С10",
    "SLK-22С11-1O9U": "22С11",
    "SLK-22С12-V5IZ": "22С12",
    "SLK-22С13-ZWE9": "22С13",
    "SLK-22D02-L9E2": "22D02",
    "SLK-22D03-D2FO": "22D03",
    "SLK-22D05-54OC": "22D05",
    "SLK-22D06-OHLZ": "22D06",
    "SLK-22D09-329R": "22D09",
    "SLK-22Е02-3VFD": "22Е02",
    "SLK-22F02-D6L0": "22F02",
    "SLK-22F03-VC3N": "22F03",
    "SLK-22F04-Z96M": "22F04",
    "SLK-22G01-QHQU": "22G01",
    "SLK-22G03-9DMS": "22G03",
    "SLK-22G04-XDWS": "22G04",
    "SLK-22G06-SXHR": "22G06",
    "SLK-22G07-LX2R": "22G07",
    "SLK-22G08-QWN1": "22G08",
    "SLK-22G09-3UGS": "22G09",
    "SLK-22G10-OIMM": "22G10",
    "SLK-22G11-T0WA": "22G11",
    "SLK-22G12-M4G1": "22G12",
    "SLK-22G13-JKYH": "22G13",
    "SLK-22G14-PS1Q": "22G14",
    "SLK-22H02-8UA8": "22H02",
    "SLK-22Н03-1STQ": "22Н03",
    "SLK-22i01-TXRI": "22i01",
    "SLK-22i02-BOYT": "22i02",
    "SLK-22i08-47Y6": "22i08",
    "SLK-22i03-MU70": "22i03",
    "SLK-22i04-KGHZ": "22i04",
    "SLK-22i05-ONH1": "22i05",
    "SLK-22i06-1FJV": "22i06",
    "SLK-22J01-2L0M": "22J01",
    "SLK-22J06-OF8M": "22J06",
    "SLK-22J08-YM4T": "22J08",
    "SLK-22J09-6U8S": "22J09",
    "SLK-22J10-FQG0": "22J10",
    "SLK-22J11-8YHN": "22J11",
    "SLK-22J12-VEJO": "22J12",
    "SLK-22J13-9S6M": "22J13",
    "SLK-22J15-5IMU": "22J15",
    "SLK-22K01-6B92": "22K01",
    "SLK-22K02-WV6D": "22K02",
    "SLK-22L02-HW1A": "22L02",
    "SLK-22L03-FHJO": "22L03",
    "SLK-22L04-1CRB": "22L04",
    "SLK-22L05-GLSJ": "22L05",
    "SLK-22L06-AX73": "22L06",
    "SLK-22L07-9ZJP": "22L07",
    "SLK-22M03-0Q6Z": "22M03",
    "SLK-22N01-0UJQ": "22N01",
    "SLK-22N05-RYX0": "22N05",
    "SLK-22N08-JXRN": "22N08",
    "SLK-22N11-KS16": "22N11",
    "SLK-22P01-ZI3K": "22P01",
    "SLK-22P02-8BRK": "22P02",
    "SLK-22Q01-L7SM": "22Q01",
    "SLK-22Q02-S8TG": "22Q02",
    "SLK-22R01-7D51": "22R01",
    "SLK-22T01-BIKJ": "22T01",
    "SLK-22U01-MZX8": "22U01",
    "SLK-22U02-HZOC": "22U02",
    "SLK-22U03-ZY0I": "22U03",
    "SLK-22U04-WTO3": "22U04",
    "SLK-22V01-G12T": "22V01",
    "SLK-22KG3-7816": "22KG3",
    "SLK-22KG4-YJXE": "22KG4",
    "SLK-22KG5-ZC54": "22KG5",
    "SLK-22W01-3LB8": "22W01",
    "SLK-22W02-TFQ0": "22W02",
    "SLK-22W03-UOYB": "22W03",
    "SLK-22Y03-0HW0": "22Y03",
    "SLK-22Z01-2OO5": "22Z01",
    "SLK-22Z03-P2LH": "22Z03"
}

BRAND_ZONES = ["Samsung","LG","Apple","Huawei","Delongi","Braun","Arg","Tefal","Hansa","Oppo","Beko","Другой бренд"]
AUTH, SELECT_BRAND, DESCRIBE_PROBLEM, SEND_PHOTO, SET_PRIORITY, CONFIRM = range(6)

def init_db():
    conn = sqlite3.connect("sulpak.db")
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users (user_id INTEGER PRIMARY KEY, store_name TEXT, role TEXT DEFAULT \'store\', authorized INTEGER DEFAULT 0)''')
    c.execute('''CREATE TABLE IF NOT EXISTS requests (id INTEGER PRIMARY KEY AUTOINCREMENT, store_name TEXT, brand_zone TEXT, description TEXT, photo_id TEXT, priority TEXT, status TEXT DEFAULT \'новая\', created_at TEXT, updated_at TEXT, user_id INTEGER)''')
    conn.commit()
    conn.close()

def get_user(uid):
    conn = sqlite3.connect("sulpak.db")
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE user_id=?", (uid,))
    u = c.fetchone()
    conn.close()
    return u

def save_user(uid, store, role="store"):
    conn = sqlite3.connect("sulpak.db")
    c = conn.cursor()
    c.execute("INSERT OR REPLACE INTO users VALUES (?,?,?,1)", (uid, store, role))
    conn.commit()
    conn.close()

def save_request(store, brand, desc, photo, priority, uid):
    conn = sqlite3.connect("sulpak.db")
    c = conn.cursor()
    now = datetime.now().strftime("%d.%m.%Y %H:%M")
    c.execute("INSERT INTO requests (store_name,brand_zone,description,photo_id,priority,status,created_at,updated_at,user_id) VALUES (?,?,?,?,?,?,?,?,?)",(store,brand,desc,photo,priority,"новая",now,now,uid))
    rid = c.lastrowid
    conn.commit()
    conn.close()
    return rid

def update_status(rid, status):
    conn = sqlite3.connect("sulpak.db")
    c = conn.cursor()
    now = datetime.now().strftime("%d.%m.%Y %H:%M")
    c.execute("UPDATE requests SET status=?,updated_at=? WHERE id=?", (status,now,rid))
    conn.commit()
    conn.close()

def get_all_requests():
    conn = sqlite3.connect("sulpak.db")
    c = conn.cursor()
    c.execute("SELECT * FROM requests ORDER BY created_at DESC")
    r = c.fetchall()
    conn.close()
    return r

def get_store_requests(store):
    conn = sqlite3.connect("sulpak.db")
    c = conn.cursor()
    c.execute("SELECT * FROM requests WHERE store_name=? ORDER BY created_at DESC LIMIT 10",(store,))
    r = c.fetchall()
    conn.close()
    return r

def get_req(rid):
    conn = sqlite3.connect("sulpak.db")
    c = conn.cursor()
    c.execute("SELECT * FROM requests WHERE id=?", (rid,))
    r = c.fetchone()
    conn.close()
    return r

def main_menu():
    return ReplyKeyboardMarkup([[KeyboardButton("📋 Подать заявку")],[KeyboardButton("📊 Мои заявки"),KeyboardButton("ℹ️ Помощь")]],resize_keyboard=True)

def brands_kb():
    return ReplyKeyboardMarkup([[KeyboardButton(x)] for x in BRAND_ZONES]+[[KeyboardButton("❌ Отмена")]],resize_keyboard=True,one_time_keyboard=True)

def priority_kb():
    return ReplyKeyboardMarkup([[KeyboardButton("🔴 Срочно"),KeyboardButton("🟡 Средне")],[KeyboardButton("🟢 Не срочно"),KeyboardButton("❌ Отмена")]],resize_keyboard=True,one_time_keyboard=True)

def confirm_kb():
    return InlineKeyboardMarkup([[InlineKeyboardButton("✅ Отправить",callback_data="confirm_yes"),InlineKeyboardButton("❌ Отменить",callback_data="confirm_no")]])

def vendor_kb(rid):
    return InlineKeyboardMarkup([[InlineKeyboardButton("✅ Принять в работу",callback_data=f"v_accept_{rid}")],[InlineKeyboardButton("🔧 Выполнено",callback_data=f"v_done_{rid}")],[InlineKeyboardButton("❌ Отклонить",callback_data=f"v_reject_{rid}")]])

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    user = get_user(uid)
    if uid in MANAGER_IDS:
        save_user(uid,"Менеджер","manager")
        await update.message.reply_text("👔 Добро пожаловать, Менеджер!\n\n/report — все заявки",reply_markup=main_menu())
        return ConversationHandler.END
    if user and user[3]==1:
        await update.message.reply_text(f"👋 С возвращением!\n🏪 Магазин: *{user[1]}*",parse_mode="Markdown",reply_markup=main_menu())
        return ConversationHandler.END
    await update.message.reply_text("👋 Добро пожаловать в систему заявок *Сулпак*!\n\n🔐 Введите код вашего магазина:",parse_mode="Markdown")
    return AUTH

async def auth(update: Update, context: ContextTypes.DEFAULT_TYPE):
    code = update.message.text.strip().upper()
    if code in STORE_CODES:
        store = STORE_CODES[code]
        save_user(update.effective_user.id, store)
        await update.message.reply_text(f"✅ Магазин *{store}* подтверждён!\n\nТеперь можете подавать заявки.",parse_mode="Markdown",reply_markup=main_menu())
        return ConversationHandler.END
    await update.message.reply_text("❌ Неверный код магазина. Попробуйте снова:\n\n(Код выглядит так: SLK-22091-XXXX)")
    return AUTH

async def new_request(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    user = get_user(uid)
    if not user or user[3]==0:
        await update.message.reply_text("❌ Сначала авторизуйтесь: /start")
        return ConversationHandler.END
    context.user_data["store"]=user[1]
    await update.message.reply_text(f"📋 *Новая заявка*\n🏪 Магазин: *{user[1]}*\n\nВыберите бренд-зону:",parse_mode="Markdown",reply_markup=brands_kb())
    return SELECT_BRAND

async def select_brand(update: Update, context: ContextTypes.DEFAULT_TYPE):
    t = update.message.text
    if t=="❌ Отмена":
        await update.message.reply_text("Отменено.",reply_markup=main_menu())
        return ConversationHandler.END
    if t not in BRAND_ZONES:
        await update.message.reply_text("⚠️ Выберите бренд из списка:",reply_markup=brands_kb())
        return SELECT_BRAND
    context.user_data["brand"]=t
    await update.message.reply_text(f"🏷 Бренд: *{t}*\n\n📝 Опишите проблему:",parse_mode="Markdown",reply_markup=ReplyKeyboardMarkup([["❌ Отмена"]],resize_keyboard=True))
    return DESCRIBE_PROBLEM

async def describe_problem(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.text=="❌ Отмена":
        await update.message.reply_text("Отменено.",reply_markup=main_menu())
        return ConversationHandler.END
    context.user_data["description"]=update.message.text
    await update.message.reply_text("📸 Отправьте фото повреждения:",reply_markup=ReplyKeyboardMarkup([["❌ Отмена"]],resize_keyboard=True))
    return SEND_PHOTO

async def receive_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.text and update.message.text=="❌ Отмена":
        await update.message.reply_text("Отменено.",reply_markup=main_menu())
        return ConversationHandler.END
    if not update.message.photo:
        await update.message.reply_text("⚠️ Отправьте именно фото (не файл):")
        return SEND_PHOTO
    context.user_data["photo_id"]=update.message.photo[-1].file_id
    await update.message.reply_text("⚡ Выберите приоритет:",reply_markup=priority_kb())
    return SET_PRIORITY

async def set_priority(update: Update, context: ContextTypes.DEFAULT_TYPE):
    t = update.message.text
    if t=="❌ Отмена":
        await update.message.reply_text("Отменено.",reply_markup=main_menu())
        return ConversationHandler.END
    if t not in ["🔴 Срочно","🟡 Средне","🟢 Не срочно"]:
        await update.message.reply_text("⚠️ Выберите из кнопок:",reply_markup=priority_kb())
        return SET_PRIORITY
    context.user_data["priority"]=t
    d=context.user_data
    await update.message.reply_photo(photo=d["photo_id"],caption=f"📋 *Проверьте заявку:*\n\n🏪 Магазин: {d['store']}\n🏷 Бренд: {d['brand']}\n📝 Проблема: {d['description']}\n⚡ Приоритет: {d['priority']}\n\nВсё верно?",parse_mode="Markdown",reply_markup=confirm_kb())
    return CONFIRM

async def confirm_request(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    if query.data=="confirm_no":
        await query.edit_message_caption("❌ Заявка отменена.")
        await context.bot.send_message(query.from_user.id,"Главное меню:",reply_markup=main_menu())
        return ConversationHandler.END
    d=context.user_data
    uid=query.from_user.id
    rid=save_request(d["store"],d["brand"],d["description"],d["photo_id"],d["priority"],uid)
    txt=f"🔔 *НОВАЯ ЗАЯВКА #{rid}*\n\n🏪 Магазин: {d['store']}\n🏷 Бренд: {d['brand']}\n📝 {d['description']}\n⚡ {d['priority']}\n🕐 {datetime.now().strftime('%d.%m.%Y %H:%M')}"
    try:
        await context.bot.send_photo(chat_id=VENDOR_CHAT_ID,photo=d["photo_id"],caption=txt,parse_mode="Markdown",reply_markup=vendor_kb(rid))
    except Exception as e:
        logging.error(e)
    await query.edit_message_caption(f"✅ *Заявка #{rid} отправлена!*",parse_mode="Markdown")
    await context.bot.send_message(uid,"Главное меню:",reply_markup=main_menu())
    return ConversationHandler.END

async def my_requests(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid=update.effective_user.id
    user=get_user(uid)
    if not user or user[3]==0:
        await update.message.reply_text("❌ Сначала авторизуйтесь: /start")
        return
    rows=get_store_requests(user[1])
    if not rows:
        await update.message.reply_text("📭 Заявок пока нет.")
        return
    em={"новая":"🆕","в работе":"🔧","выполнено":"✅","отклонено":"❌"}
    text=f"📊 *Заявки — Магазин {user[1]}:*\n\n"
    for r in rows:
        text+=f"{em.get(r[6],'❓')} *#{r[0]}* | 🏷 {r[2]} | {r[5]}\n   📝 {r[3][:50]}\n   📅 {r[7]}\n\n"
    await update.message.reply_text(text,parse_mode="Markdown")

async def report(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id not in MANAGER_IDS:
        await update.message.reply_text("⛔ Нет доступа.")
        return
    rows=get_all_requests()
    if not rows:
        await update.message.reply_text("📭 Заявок нет.")
        return
    em={"новая":"🆕","в работе":"🔧","выполнено":"✅","отклонено":"❌"}
    text=f"📊 *ОТЧЁТ*\n━━━━━━━━━━━━━━━\nВсего: *{len(rows)}* | 🆕{sum(1 for r in rows if r[6]=='новая')} 🔧{sum(1 for r in rows if r[6]=='в работе')} ✅{sum(1 for r in rows if r[6]=='выполнено')} ❌{sum(1 for r in rows if r[6]=='отклонено')}\n\n*Последние 20:*\n\n"
    for r in rows[:20]:
        text+=f"{em.get(r[6],'❓')} *#{r[0]}* | Магазин {r[1]}\n   🏷 {r[2]} | {r[5]} | 📅 {r[7]}\n\n"
    await update.message.reply_text(text,parse_mode="Markdown")

async def vendor_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query=update.callback_query
    await query.answer()
    data=query.data
    if data.startswith("v_accept_"):
        rid=int(data.split("_")[-1]); update_status(rid,"в работе"); ns="🔧 Принято в работу"
    elif data.startswith("v_done_"):
        rid=int(data.split("_")[-1]); update_status(rid,"выполнено"); ns="✅ Выполнено"
    elif data.startswith("v_reject_"):
        rid=int(data.split("_")[-1]); update_status(rid,"отклонено"); ns="❌ Отклонено"
    else:
        return
    try:
        await query.edit_message_caption(caption=(query.message.caption or "")+f"\n\n{ns}\n🕐 {datetime.now().strftime('%d.%m.%Y %H:%M')}",parse_mode="Markdown")
    except Exception as e:
        logging.error(e)
    req=get_req(rid)
    if req:
        try:
            await context.bot.send_message(chat_id=req[9],text=f"🔔 *Заявка #{rid} обновлена!*\n🏷 {req[2]}\nСтатус: {ns}",parse_mode="Markdown")
        except Exception as e:
            logging.error(e)
        for mid in MANAGER_IDS:
            try:
                await context.bot.send_message(chat_id=mid,text=f"📌 Заявка *#{rid}* | Магазин {req[1]}\nСтатус: {ns}",parse_mode="Markdown")
            except Exception as e:
                logging.error(e)

async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("ℹ️ *Помощь*\n\n📋 Подать заявку\n📊 Мои заявки\n/start — перезапуск\n/report — отчёт (менеджер)",parse_mode="Markdown",reply_markup=main_menu())

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("❌ Отменено.",reply_markup=main_menu())
    return ConversationHandler.END

def main():
    logging.basicConfig(format="%(asctime)s - %(levelname)s - %(message)s",level=logging.INFO)
    init_db()
    app=Application.builder().token(BOT_TOKEN).build()
    auth_conv=ConversationHandler(entry_points=[CommandHandler("start",start)],states={AUTH:[MessageHandler(filters.TEXT & ~filters.COMMAND,auth)]},fallbacks=[CommandHandler("cancel",cancel)])
    request_conv=ConversationHandler(entry_points=[MessageHandler(filters.Regex("^📋 Подать заявку$"),new_request)],states={SELECT_BRAND:[MessageHandler(filters.TEXT & ~filters.COMMAND,select_brand)],DESCRIBE_PROBLEM:[MessageHandler(filters.TEXT & ~filters.COMMAND,describe_problem)],SEND_PHOTO:[MessageHandler(filters.PHOTO,receive_photo),MessageHandler(filters.TEXT & ~filters.COMMAND,receive_photo)],SET_PRIORITY:[MessageHandler(filters.TEXT & ~filters.COMMAND,set_priority)],CONFIRM:[CallbackQueryHandler(confirm_request,pattern="^confirm_")]},fallbacks=[CommandHandler("cancel",cancel)])
    app.add_handler(auth_conv)
    app.add_handler(request_conv)
    app.add_handler(CommandHandler("report",report))
    app.add_handler(MessageHandler(filters.Regex("^📊 Мои заявки$"),my_requests))
    app.add_handler(MessageHandler(filters.Regex("^ℹ️ Помощь$"),help_cmd))
    app.add_handler(CallbackQueryHandler(vendor_callback,pattern="^v_"))
    print("🤖 Бот Сулпак запущен!")
    app.run_polling()

if __name__=="__main__":
    main()
