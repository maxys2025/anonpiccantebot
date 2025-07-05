from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, BotCommand
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes, CallbackQueryHandler
import random
import json
import os

# Nome del file dove salviamo i profili
FILE_PROFILI = "profili.json"

# Carica i profili all'avvio
def carica_profili():
    if os.path.exists(FILE_PROFILI):
        with open(FILE_PROFILI, "r", encoding="utf-8") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return {}
    return {}

# Salva i profili su file
def salva_profili():
    with open(FILE_PROFILI, "w", encoding="utf-8") as f:
        json.dump(profili, f, ensure_ascii=False, indent=4)

TOKEN = "7982478487:AAFyZf8_5JAknsmlwUMEYotnXYiiaV_t7Ww"

# Lista di domande hot 😏
domande = [
    "A che età hai dato il primo bacio?",
    "A che età hai fatto sesso la prima volta?",
    "Preferisci dominare o essere dominato?",
    "Che voto ti daresti come amante?",
    "Con chi faresti una cosa a tre?",
    "Con quale celebrità andresti a letto più di una volta?",
    "Cosa ne pensi delle relazioni aperte?",
    "Qual è il tuo preliminare preferito?",
    "Cos'hai provato la prima volta che hai fatto sesso orale?",
    "Cos'hai provato la prima volta che hai ricevuto sesso orale?",
    "Da quanto tempo non fai sesso?",
    "Quando ti sei masturbato l'ultima volta?",
    "Descrivi il tuo bacio più memorabile.",
    "Descrivi la tua stranezza che ti eccita di più.",
    "Faresti sesso con uno sconosciuto per 1000€?",
    "Faresti un account onlyfans?",
    "Faresti uno spogliarello per la persona con cui stai facendo questo gioco?",
    "Hai concretizzato qualche tua fantasia sessuale? Se si quale?",
    "Hai mai assaggiato lo sperma?",
    "Hai mai avuto dubbi sulla tua sessualità?",
    "Hai mai avuto un orgasmo in sogno?",
    "Hai mai avuto un’avventura di una notte?",
    "Hai mai avuto una cotta sul posto di lavoro?",
    "Hai mai avuto una scopamicizia?",
    "Hai mai beccato qualcuno masturbarsi o fare sesso?",
    "Hai mai dubitato della tua sessualità?",
    "Hai mai fantasticato sul partner di un conoscente?",
    "Hai mai fatto sesso anale?",
    "Hai mai fatto sesso con uno sconosciuto?",
    "Hai mai fatto sesso in pubblico?",
    "Hai mai fatto sesso in un bosco o su un prato?",
    "Hai mai fatto sesso orale?",
    "Hai mai fatto sexting?",
    "Hai mai fatto una cosa a tre?",
    "Hai mai fatto una videochat hot?",
    "Hai mai finto un orgasmo?",
    "Hai mai fatto foto o video mentre fai sesso? Se si mostrane una/o",
    "Hai mai fatto foto o video mentre ti masturbi? Se si mostrane una/o",
    "Hai mai inviato una foto nuda a qualcuno? Se si mostrane una",
    "Hai mai legato o bendato il partner?",
    "Hai mai pensato a qualcun altro mentre eri con il tuo partner?",
    "Hai mai pensato di provare il BDSM?",
    "Hai mai prenotato un hotel solo per fare sesso?",
    "Hai mai provato l’intimità tantrica?",
    "Hai mai sorpreso qualcuno fare sesso o masturbarsi?",
    "Hai tradito il tuo partner?",
    "Hai una perversione o fetish?",
    "Hai mai usato cibo a letto?",
    "Invieresti foto intime per soldi?",
    "Pensi che le dimensioni siano importanti?",
    "Preferiresti fare una cosa a tre con due uomini o due donne?",
    "Preferisci fare sesso con un pene lungo o con un pene largo?",
    "Qual è il luogo più strano in cui hai fatto sesso?",
    "Qual è il numero massimo di volte che hai fatto sesso in un giorno?",
    "Qual è il tuo posto preferito per una sveltina?",
    "Qual è il tuo preliminare preferito?",
    "Qual è il tuo sex toy preferito?",
    "Qual è il tuo sito web per adulti preferito?",
    "Hai mai usato sex toys?",
    "Qual è il tuo tipo di biancheria intima preferito?",
    "Qual è la cosa che ti dà più fastidio a letto?",
    "Qual è la tua più grande fantasia sessuale?",
    "Qual è la tua migliore abilità a letto?",
    "Qual è la tua parte del corpo del tuo partner che preferisci?",
    "Qual è la tua posizione preferita?",
    "Qual è la tua zona erogena più sensibile?",
    "Qual è stata la tua esperienza sessuale più imbarazzante?",
    "Di quanto è stato il tempo più lungo in cui sei stato senza fare sesso?",
    "Quanti cm è lungo il tuo pene?",
    "Sei mai stato beccato mentre facevi sesso o ti masturbavi?",
    "Sei mai uscito senza mutande?",
    "Ti depili le parti intime?",
    "Ti masturbi?",
    "Ti piace essere sculacciato/a?",
    "Ti sei mai masturbato pensando a qualcuno che conosci?",
    "Ti si è mai rotto un preservativo?",
    "Hai mai usato oggetti per masturbarti?",
    "Il dolore secondo te fa un po' parte del piacere?",
    "Quando hai visto il tuo primo pisello o la tua prima patata?",
    "É mai successo qualcosa con un tuo parente?",
    "Quanto duri prima di venire?",
    "Qual è stata la tua peggior scopata?",
    "Hai mai fatto o ricevuto una sega con i piedi?",
    "Hai mai fatto o ricevuto una spagnola?",
    "Sei più da sesso passionale o sesso selvaggio?",
    "Hai una tua foto, intima o provocante, che pensi possa essere eccitante? Se si mostrala",
    "Ti piace baciare durante il sesso?",
    "Ti ecciterebbe guardare il partner masturbarsi davanti a te?",
    "Preferisci fare sesso con le luci accese o spente?",
    "Qual è la posizione che ti piace di meno?",
    "Ti piace essere insultato/a?",
    "Hia mai fatto sesso non protetto?",
    "Ti piace tirare o essere tirata per i capelli?"
]

in_attesa = []  # Chi aspetta un partner
coppie = {}  # {utente_id: partner_id}
attesa_inizio = {}  # Chi ha cliccato "Inizia il gioco"
attesa_prossima = {}  # Chi ha cliccato per la prossima domanda
domande_shuffle = {}  # Domande mischiate per ogni coppia
indice_domanda = {}  # Indice della domanda per ogni utente
profili = carica_profili()
conta_messaggi = {}  # {coppia_id: numero_messaggi}

# START
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    testo = (
        "👋 *Benvenuto su AnonPiccanteBot!*\n\n"
        "Ecco come funziona il gioco:\n"
        "🔎 Scrivi `/cerca` per trovare un partner anonimo\n"
        "❓ Rispondete alle domande hot a turno\n"
        "💬 Potete scambiarvi messaggi, foto, sticker e vocali\n"
        "⏩ Quando entrambi cliccate su 'Prossima domanda' il gioco prosegue\n"
        "⚙️ Con `/profilo` imposti età, genere e orientamento\n"
    )
    await update.message.reply_text(testo, parse_mode="Markdown")




# CERCA PARTNER
async def cerca(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id

    if user_id in coppie:
        await update.message.reply_text("Sei già in chat anonima! 😏")
        return

    if user_id in in_attesa:
        await update.message.reply_text("Stai già aspettando un partner...⏳")
        return

    if in_attesa:
        partner_id = in_attesa.pop(0)
        # Dopo aver accoppiato:
        coppie[user_id] = partner_id
        coppie[partner_id] = user_id

        # Mostra profilo reciproco
        profilo_partner = formatta_profilo(partner_id)
        await context.bot.send_message(chat_id=user_id, text=profilo_partner)

        profilo_tuo = formatta_profilo(user_id)
        await context.bot.send_message(chat_id=partner_id, text=profilo_tuo)

        lista_mischiata = random.sample(domande, len(domande))
        domande_shuffle[user_id] = lista_mischiata
        domande_shuffle[partner_id] = lista_mischiata
        indice_domanda[user_id] = 0
        indice_domanda[partner_id] = 0
        attesa_prossima[user_id] = False
        attesa_prossima[partner_id] = False
        attesa_inizio[user_id] = False
        attesa_inizio[partner_id] = False

        tastiera = InlineKeyboardMarkup([
            [InlineKeyboardButton("Inizia il gioco 🔥", callback_data="inizia_gioco")]
        ])

        await update.message.reply_text("Partner trovato! Quando siete pronti, cliccate su 'Inizia il gioco' 🔥", reply_markup=tastiera)
        await context.bot.send_message(partner_id, "Partner trovato! Quando siete pronti, cliccate su 'Inizia il gioco' 🔥", reply_markup=tastiera)

    else:
        in_attesa.append(user_id)
        await update.message.reply_text("Aspettiamo che arrivi qualcuno...⏳")

def formatta_profilo(user_id):
    profilo = profili.get(user_id, {})
    eta = profilo.get("eta", "Non impostata")
    genere = profilo.get("genere", "Non impostato")
    orientamento = profilo.get("orientamento", "Non impostato")

    testo = (
        f"👤 Profilo della persona trovata:\n"
        f"📅 Età: {eta}\n"
        f"🚻 Genere: {genere}\n"
        f"❤️‍🔥 Orientamento: {orientamento}"
    )
    return testo

async def messaggio(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id

    if context.user_data.get("attesa_eta"):
        text = update.message.text.strip()
        if not text.isdigit() or not (18 <= int(text) <= 99):
            await update.message.reply_text("⛔ Inserisci un'età valida (18-99).")
            return

        profili.setdefault(user_id, {})["eta"] = text
        salva_profili()
        context.user_data["attesa_eta"] = False
        await update.message.reply_text(f"✅ Età impostata su: {text} anni")
        return

    if user_id not in coppie:
        await update.message.reply_text("🔎 Scrivi `/cerca` per trovare un partner anonimo!", parse_mode="Markdown")
        return

    partner_id = coppie[user_id]
    coppia_id = tuple(sorted([user_id, partner_id]))
    conta_messaggi[coppia_id] = conta_messaggi.get(coppia_id, 0) + 1

    # 1️⃣ MESSAGGIO TESTO
    if update.message.text:
        text = update.message.text.strip()
        if text.lower() == "prossima domanda":
            attesa_prossima[user_id] = True
            if attesa_prossima.get(partner_id):
                await invia_domanda(user_id, context)
            else:
                await update.message.reply_text("⏳ _Il tuo partner non ha ancora premuto su 'Prossima domanda'..._", parse_mode="Markdown")
        else:
            await context.bot.send_message(partner_id, f"🗨️ Anonimo dice: {text}")

    # 2️⃣ FOTO
    elif update.message.photo:
        foto = update.message.photo[-1].file_id
        await context.bot.send_photo(partner_id, foto, caption="📷 Foto anonima")

    # 3️⃣ VIDEO
    elif update.message.video:
        video = update.message.video.file_id
        await context.bot.send_video(partner_id, video, caption="🎥 Video anonimo")

    # 4️⃣ AUDIO / VOCALE
    elif update.message.voice:
        voce = update.message.voice.file_id
        await context.bot.send_voice(partner_id, voce)

    elif update.message.audio:
        audio = update.message.audio.file_id
        await context.bot.send_audio(partner_id, audio)

    # 5️⃣ STICKER
    elif update.message.sticker:
        sticker = update.message.sticker.file_id
        await context.bot.send_sticker(partner_id, sticker)

    # 6️⃣ DOCUMENTO (opzionale)
    elif update.message.document:
        doc = update.message.document.file_id
        await context.bot.send_document(partner_id, doc, caption="📄 Documento anonimo")

    else:
        await update.message.reply_text("⛔ _Questo tipo di contenuto non è supportato._", parse_mode="Markdown")

    # 7️⃣ Promemoria per la prossima domanda ogni 5 messaggi
    if conta_messaggi[coppia_id] >= 8:
        tastiera = InlineKeyboardMarkup([
            [InlineKeyboardButton("🔄 _Prossima domanda_", callback_data="prossima_domanda", parse_mode="Markdown")]
        ])
        await context.bot.send_message(user_id, "🔥 _Ti ricordo che puoi passare alla prossima domanda_ 🔥", reply_markup=tastiera, parse_mode="Markdown")
        await context.bot.send_message(partner_id, "🔥 _Ti ricordo che puoi passare alla prossima domanda_ 🔥", reply_markup=tastiera, parse_mode="Markdown")
        conta_messaggi[coppia_id] = 0  # Reset del contatore

# ESCI DALLA CHAT
async def esci(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id

    if user_id in coppie:
        partner_id = coppie.pop(user_id)
        coppie.pop(partner_id, None)
        attesa_prossima.pop(user_id, None)
        attesa_prossima.pop(partner_id, None)
        attesa_inizio.pop(user_id, None)
        attesa_inizio.pop(partner_id, None)
        domande_shuffle.pop(user_id, None)
        domande_shuffle.pop(partner_id, None)
        indice_domanda.pop(user_id, None)
        indice_domanda.pop(partner_id, None)

        await update.message.reply_text("Sei uscito dalla chat anonima 👋 Scrivi /cerca per continuare!")
        await context.bot.send_message(partner_id, "Il tuo partner è uscito dalla chat 😢 Scrivi /cerca per continuare!")
    else:
        await update.message.reply_text("Non sei in chat anonima al momento. Scrivi /cerca per iniziare!")

# INVIA DOMANDA CON PULSANTE
async def invia_domanda(user_id, context):
    partner_id = coppie[user_id]
    lista = domande_shuffle[user_id]
    indice = indice_domanda[user_id]

    if indice >= len(lista):
        await context.bot.send_message(user_id, "✅ _Avete completato tutte le domande disponibili!_ 🔥", parse_mode="Markdown")
        await context.bot.send_message(partner_id, "✅ _Avete completato tutte le domande disponibili!_ 🔥", parse_mode="Markdown")
        return

    domanda = lista[indice]

    # Invia solo il testo della domanda
    await context.bot.send_message(user_id, f"🔥 _Domanda: {domanda}_🔥", parse_mode="Markdown")
    await context.bot.send_message(partner_id, f"🔥 _Domanda: {domanda}_🔥", parse_mode="Markdown")

    # Invia il pulsante separato
    tastiera = InlineKeyboardMarkup([
        [InlineKeyboardButton("🔄 Prossima domanda", callback_data="prossima_domanda")]
    ])

    await context.bot.send_message(user_id, "➡️ _Premi il pulsante per la prossima domanda._", reply_markup=tastiera, parse_mode="Markdown")
    await context.bot.send_message(partner_id, "➡️ _Premi il pulsante per la prossima domanda._", reply_markup=tastiera, parse_mode="Markdown")

    attesa_prossima[user_id] = False
    attesa_prossima[partner_id] = False
    indice_domanda[user_id] += 1
    indice_domanda[partner_id] += 1

    # 🔥 Reset del contatore messaggi per la coppia
    coppia_id = tuple(sorted([user_id, partner_id]))
    conta_messaggi[coppia_id] = 0

async def profilo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id

    if user_id in coppie:
        await update.message.reply_text("❌ _Non puoi modificare il profilo mentre sei in chat anonima. Esci con /esci prima._", parse_mode="Markdown")
        return

    tastiera = InlineKeyboardMarkup([
        [InlineKeyboardButton("📅 Imposta età", callback_data="set_eta")],
        [InlineKeyboardButton("🚻 Imposta genere", callback_data="set_genere")],
        [InlineKeyboardButton("❤️‍🔥 Imposta orientamento", callback_data="set_orientamento")]
    ])

    await update.message.reply_text("🔧 Modifica il tuo profilo:", reply_markup=tastiera)

async def info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    profilo = profili.get(user_id, {})

    testo = f"📝 Il tuo profilo:\n"
    testo += f"Età: {profilo.get('eta', 'Non impostata')}\n"
    testo += f"Genere: {profilo.get('genere', 'Non impostato')}\n"
    testo += f"Orientamento: {profilo.get('orientamento', 'Non impostato')}"

    await update.message.reply_text(testo)

# GESTISCI PULSANTI INLINE
async def gestisci_pulsante(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id

    if user_id not in coppie and query.data not in ["set_eta", "set_genere", "set_orientamento", "genere_uomo", "genere_donna", "genere_altro", "orient_etero", "orient_gay", "orient_bisex", "orient_altro"]:
        await query.message.reply_text("Non sei in chat anonima al momento. Usa /cerca per iniziare.")
        return

    partner_id = coppie.get(user_id)

    if query.data == "inizia_gioco":
        attesa_inizio[user_id] = True
        if attesa_inizio.get(partner_id):
            await invia_domanda(user_id, context)
        else:
            await query.message.reply_text("Aspettiamo che anche il partner voglia iniziare...⏳")

    elif query.data == "prossima_domanda":
        attesa_prossima[user_id] = True
        if attesa_prossima.get(partner_id):
            await invia_domanda(user_id, context)
        else:
            await query.message.reply_text("_Aspettiamo che anche il partner voglia la prossima domanda...⏳_", parse_mode="Markdown")

    elif query.data == "set_eta":
        await query.message.reply_text("📅 Scrivimi la tua età:")
        context.user_data["attesa_eta"] = True

    elif query.data == "set_genere":
        tastiera = InlineKeyboardMarkup([
            [InlineKeyboardButton("Uomo", callback_data="genere_uomo"), InlineKeyboardButton("Donna", callback_data="genere_donna")],
            [InlineKeyboardButton("Altro", callback_data="genere_altro")]
        ])
        await query.message.reply_text("🚻 Scegli il tuo genere:", reply_markup=tastiera)

    elif query.data == "set_orientamento":
        tastiera = InlineKeyboardMarkup([
            [InlineKeyboardButton("Etero", callback_data="orient_etero"), InlineKeyboardButton("Gay", callback_data="orient_gay")],
            [InlineKeyboardButton("Bisex", callback_data="orient_bisex"), InlineKeyboardButton("Altro", callback_data="orient_altro")]
        ])
        await query.message.reply_text("❤️‍🔥 Scegli il tuo orientamento sessuale:", reply_markup=tastiera)

    elif query.data.startswith("genere_"):
        valore = query.data.split("_")[1]
        profili.setdefault(user_id, {})["genere"] = valore.capitalize()
        salva_profili()
        await query.message.reply_text(f"✅ Genere impostato su: {valore.capitalize()}")

    elif query.data.startswith("orient_"):
        valore = query.data.split("_")[1]
        profili.setdefault(user_id, {})["orientamento"] = valore.capitalize()
        salva_profili()
        await query.message.reply_text(f"✅ Orientamento impostato su: {valore.capitalize()}")

# IMPOSTA COMANDI MENU
async def setta_comandi(bot):
    comandi = [
        BotCommand("start", "Avvia il bot"),
        BotCommand("cerca", "Cerca un partner anonimo"),
        BotCommand("esci", "Esci dalla chat"),
        BotCommand("profilo", "Imposta il tuo profilo"),
        BotCommand("info", "Mostra il tuo profilo"),
    ]
    await bot.set_my_commands(comandi)


# AVVIO DEL BOT
if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()

    async def init_bot(app):
        await setta_comandi(app.bot)

    app.post_init = init_bot

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("cerca", cerca))
    app.add_handler(CommandHandler("esci", esci))
    app.add_handler(CommandHandler("profilo", profilo))
    app.add_handler(CommandHandler("info", info))
    app.add_handler(CallbackQueryHandler(gestisci_pulsante))
    app.add_handler(MessageHandler(filters.ALL, messaggio))  # L'ultimo, prende tutto il resto


    print("Bot in esecuzione...")
    app.run_polling()
