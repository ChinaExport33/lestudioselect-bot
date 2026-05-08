{\rtf1\ansi\ansicpg1252\cocoartf2821
\cocoatextscaling0\cocoaplatform0{\fonttbl\f0\fswiss\fcharset0 Helvetica;}
{\colortbl;\red255\green255\blue255;}
{\*\expandedcolortbl;;}
\paperw11900\paperh16840\margl1440\margr1440\vieww11520\viewh8400\viewkind0
\pard\tx720\tx1440\tx2160\tx2880\tx3600\tx4320\tx5040\tx5760\tx6480\tx7200\tx7920\tx8640\pardirnatural\partightenfactor0

\f0\fs24 \cf0 import logging, json, os\
from datetime import datetime\
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, InputMediaPhoto\
from telegram.ext import (\
    Application, CommandHandler, MessageHandler,\
    CallbackQueryHandler, ContextTypes, filters\
)\
from apscheduler.schedulers.asyncio import AsyncIOScheduler\
\
# \uc0\u9472 \u9472  CONFIG \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \
BOT_TOKEN  = "8585016080:AAHoF3PSC3J3KplHkaGk9jewWnc6hEIjbfU"\
CHANNEL_ID = "@LeStudioSelect"\
ADMIN_ID   = 8341097745\
\
logging.basicConfig(format="%(asctime)s | %(levelname)s | %(message)s", level=logging.INFO)\
log = logging.getLogger(__name__)\
\
POSTS_FILE = "posts_planifies.json"\
\
# \uc0\u9472 \u9472  GESTION JSON \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \
def load_posts():\
    if not os.path.exists(POSTS_FILE):\
        return []\
    with open(POSTS_FILE, "r", encoding="utf-8") as f:\
        return json.load(f)\
\
def save_posts(posts):\
    with open(POSTS_FILE, "w", encoding="utf-8") as f:\
        json.dump(posts, f, ensure_ascii=False, indent=2)\
\
# \uc0\u9472 \u9472  BOUTON PARTAGE \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \
def share_keyboard():\
    return InlineKeyboardMarkup([[\
        InlineKeyboardButton("\uc0\u55357 \u56577  Partager", url="https://t.me/share/url?url=https://t.me/LeStudioSelect"),\
        InlineKeyboardButton("\uc0\u55357 \u56562  Rejoindre", url="https://t.me/LeStudioSelect"),\
    ]])\
\
# \uc0\u9472 \u9472  POSTS AUTO \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \
AUTO_POSTS = [\
    \{"cat": "Mode Femme \uc0\u55357 \u56407 ", "text": "\u55357 \u56407  *Nouveaut\'e9 Mode Femme*\\n\\nNouvelle robe midi \'e0 imprim\'e9 fleuri \'97 coupe ajust\'e9e, tissu premium.\\nDisponible en 3 coloris \'b7 Tailles S au XL\\n\\n\u55357 \u56562  @LeStudioSelect"\},\
    \{"cat": "Beaut\'e9 \uc0\u55357 \u56452 ",     "text": "\u55357 \u56452  *Drop Beaut\'e9 du jour*\\n\\nS\'e9rum \'e9clat vitamine C + cr\'e8me hydratante \'97 duo bestseller.\\nR\'e9sultats visibles en 7 jours \'b7 Sans paraben\\n\\n\u55357 \u56562  @LeStudioSelect"\},\
    \{"cat": "\'c9lectro \uc0\u55357 \u56488 ",    "text": "\u55357 \u56488  *Dyson en stock*\\n\\nS\'e8che-cheveux Dyson Supersonic + lisseur GHD disponibles.\\nPrix exclusif \'b7 Vente sur place\\n\\n\u55357 \u56562  @LeStudioSelect"\},\
    \{"cat": "Parfums \uc0\u55356 \u57144 ",    "text": "\u55356 \u57144  *S\'e9lection Parfums cette semaine*\\n\\nFragrances niche & orientales \'97 noms sur demande.\\nFlacons authentiques\\n\\n\u55357 \u56562  @LeStudioSelect"\},\
    \{"cat": "Accessoires \uc0\u55357 \u56462 ","text": "\u55357 \u56462  *Accessoires \'97 Nouveaux arrivages*\\n\\nMontres, bijoux dor\'e9s, ceintures cuir.\\nLook premium \'b7 Prix accessible\\n\\n\u55357 \u56562  @LeStudioSelect"\},\
    \{"cat": "Mode Homme \uc0\u55357 \u56404 ", "text": "\u55357 \u56404  *Mode Homme \'97 Collection printemps*\\n\\nChemises lin, joggers premium \'97 style urban \'e9l\'e9gant.\\nTailles M au XXL\\n\\n\u55357 \u56562  @LeStudioSelect"\},\
    \{"cat": "Offre Flash \uc0\u9889 ", "text": "\u9889  *OFFRE FLASH \'97 Aujourd'hui seulement*\\n\\nS\'e9lection sp\'e9ciale \'b7 Prix r\'e9duits \'b7 Stock tr\'e8s limit\'e9\\n\\n\u55357 \u56562  Vite \u8594  @LeStudioSelect\\n\u55357 \u56577  Partage avec tes amis !"\},\
    \{"cat": "Communaut\'e9 \uc0\u55358 \u56605 ", "text": "\u55358 \u56605  *LeStudioSelect grandit !*\\n\\nMode \'b7 Beaut\'e9 \'b7 \'c9lectrom\'e9nager \'b7 Parfums \'97 tout au m\'eame endroit.\\n\\n\u55357 \u56562  Rejoins-nous \u8594  @LeStudioSelect\\n\u55357 \u56492  Partage le canal \'e0 quelqu'un qui adore la mode \u55357 \u56908 "\},\
]\
\
CAT_DETAILS = \{\
    "cat_mf": "\uc0\u55357 \u56407  *Mode Femme*\\nRobes, tops, sacs \'97 nouvelles pi\'e8ces chaque semaine.\\n\\n\u55357 \u56562  @LeStudioSelect",\
    "cat_mh": "\uc0\u55357 \u56404  *Mode Homme*\\nStreetwear, chemises, pantalons.\\n\\n\u55357 \u56562  @LeStudioSelect",\
    "cat_ac": "\uc0\u55357 \u56462  *Accessoires*\\nBijoux, montres, ceintures.\\n\\n\u55357 \u56562  @LeStudioSelect",\
    "cat_be": "\uc0\u55357 \u56452  *Beaut\'e9*\\nSoins, maquillage, huiles.\\n\\n\u55357 \u56562  @LeStudioSelect",\
    "cat_el": "\uc0\u55357 \u56488  *\'c9lectrom\'e9nager*\\nDyson, lisseurs GHD, s\'e8che-cheveux.\\n\\n\u55357 \u56562  @LeStudioSelect",\
    "cat_pa": "\uc0\u55356 \u57144  *Parfums*\\nNiche, luxe, orientaux.\\n\\n\u55357 \u56562  @LeStudioSelect",\
\}\
\
post_idx = 0\
\
# \uc0\u9472 \u9472  COMMANDES \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \
async def cmd_start(update: Update, ctx: ContextTypes.DEFAULT_TYPE):\
    u = update.effective_user\
    kb = InlineKeyboardMarkup([[\
        InlineKeyboardButton("\uc0\u55357 \u56562  Rejoindre le canal", url="https://t.me/LeStudioSelect"),\
        InlineKeyboardButton("\uc0\u55357 \u56577  Inviter un ami", url="https://t.me/share/url?url=https://t.me/LeStudioSelect"),\
    ]])\
    await update.message.reply_text(\
        f"\uc0\u55357 \u56395  Salut *\{u.first_name\}* !\\n\\n"\
        f"Bienvenue sur *LeStudioSelect* \'97 s\'e9lection premium :\\n\\n"\
        f"\uc0\u55357 \u56407  Mode Femme & Homme\\n\u55357 \u56462  Accessoires\\n\u55357 \u56452  Beaut\'e9\\n\u55357 \u56488  \'c9lectrom\'e9nager Dyson\\n\u55356 \u57144  Parfums\\n\\n"\
        f"\uc0\u55357 \u56562  Rejoins le canal pour voir toutes nos offres !",\
        parse_mode="Markdown", reply_markup=kb\
    )\
\
async def cmd_catalogue(update: Update, ctx: ContextTypes.DEFAULT_TYPE):\
    cats = [\
        ("\uc0\u55357 \u56407  Mode Femme","cat_mf"), ("\u55357 \u56404  Mode Homme","cat_mh"),\
        ("\uc0\u55357 \u56462  Accessoires","cat_ac"), ("\u55357 \u56452  Beaut\'e9","cat_be"),\
        ("\uc0\u55357 \u56488  \'c9lectrom\'e9nager","cat_el"), ("\u55356 \u57144  Parfums","cat_pa"),\
    ]\
    rows = [[InlineKeyboardButton(l, callback_data=c)] for l,c in cats]\
    await update.message.reply_text(\
        "\uc0\u55357 \u56770  *Catalogue LeStudioSelect*\\nChoisis une cat\'e9gorie :",\
        parse_mode="Markdown", reply_markup=InlineKeyboardMarkup(rows)\
    )\
\
async def button_cb(update: Update, ctx: ContextTypes.DEFAULT_TYPE):\
    q = update.callback_query\
    await q.answer()\
    if q.data == "back_catalogue":\
        cats = [\
            ("\uc0\u55357 \u56407  Mode Femme","cat_mf"), ("\u55357 \u56404  Mode Homme","cat_mh"),\
            ("\uc0\u55357 \u56462  Accessoires","cat_ac"), ("\u55357 \u56452  Beaut\'e9","cat_be"),\
            ("\uc0\u55357 \u56488  \'c9lectrom\'e9nager","cat_el"), ("\u55356 \u57144  Parfums","cat_pa"),\
        ]\
        rows = [[InlineKeyboardButton(l, callback_data=c)] for l,c in cats]\
        await q.edit_message_text(\
            "\uc0\u55357 \u56770  *Catalogue LeStudioSelect*\\nChoisis une cat\'e9gorie :",\
            parse_mode="Markdown", reply_markup=InlineKeyboardMarkup(rows)\
        )\
        return\
    txt = CAT_DETAILS.get(q.data, "Cat\'e9gorie introuvable.")\
    back = [[\
        InlineKeyboardButton("\uc0\u11013 \u65039  Retour", callback_data="back_catalogue"),\
        InlineKeyboardButton("\uc0\u55357 \u56562  Rejoindre", url="https://t.me/LeStudioSelect")\
    ]]\
    await q.edit_message_text(txt, parse_mode="Markdown", reply_markup=InlineKeyboardMarkup(back))\
\
async def cmd_stats(update: Update, ctx: ContextTypes.DEFAULT_TYPE):\
    if update.effective_user.id != ADMIN_ID:\
        return\
    cnt = await ctx.bot.get_chat_member_count(CHANNEL_ID)\
    posts = load_posts()\
    pending = [p for p in posts if not p.get("sent")]\
    await update.message.reply_text(\
        f"\uc0\u55357 \u56522  *Stats \'97 LeStudioSelect*\\n"\
        f"Membres : *\{cnt\}*\\n"\
        f"Posts en attente : *\{len(pending)\}*\\n"\
        f"Date : \{datetime.now().strftime('%d/%m/%Y %H:%M')\}",\
        parse_mode="Markdown"\
    )\
\
async def cmd_posts(update: Update, ctx: ContextTypes.DEFAULT_TYPE):\
    if update.effective_user.id != ADMIN_ID:\
        return\
    posts = load_posts()\
    pending = [p for p in posts if not p.get("sent")]\
    if not pending:\
        await update.message.reply_text("\uc0\u9989  Aucun post en attente.")\
        return\
    lines = [\
        f"\{i\}. *\{p['categorie']\}* \'97 \{p['date_heure']\} \'97 \{len(p.get('photos', []))\} photo(s)"\
        for i, p in enumerate(pending, 1)\
    ]\
    await update.message.reply_text(\
        "\uc0\u55357 \u56517  *Posts planifi\'e9s :*\\n\\n" + "\\n".join(lines),\
        parse_mode="Markdown"\
    )\
\
async def cmd_ajouter(update: Update, ctx: ContextTypes.DEFAULT_TYPE):\
    if update.effective_user.id != ADMIN_ID:\
        return\
    try:\
        args = " ".join(ctx.args).split("|")\
        if len(args) < 4:\
            raise ValueError\
        cat, dh, texte, fids = [a.strip() for a in args]\
        photos = [f.strip() for f in fids.split(",") if f.strip()]\
        if not photos or len(photos) > 10:\
            await update.message.reply_text("\uc0\u10060  Entre 1 et 10 photos maximum.")\
            return\
        posts = load_posts()\
        posts.append(\{"categorie": cat, "date_heure": dh, "texte": texte, "photos": photos, "sent": False\})\
        save_posts(posts)\
        await update.message.reply_text(\
            f"\uc0\u9989  Post ajout\'e9 !\\n*\{cat\}* \'97 \{dh\}\\n\{len(photos)\} photo(s) planifi\'e9e(s).",\
            parse_mode="Markdown"\
        )\
    except ValueError:\
        await update.message.reply_text(\
            "\uc0\u10060  Format :\\n`/ajouter Cat\'e9gorie | JJ/MM HH:MM | Texte | file_id1,file_id2`",\
            parse_mode="Markdown"\
        )\
\
async def receive_photo(update: Update, ctx: ContextTypes.DEFAULT_TYPE):\
    if update.effective_user.id != ADMIN_ID:\
        return\
    if update.message.photo:\
        fid = update.message.photo[-1].file_id\
        await update.message.reply_text(\
            f"\uc0\u55357 \u56568  *file_id de ta photo :*\\n`\{fid\}`\\n\\nCopie-le pour l'utiliser dans /ajouter",\
            parse_mode="Markdown"\
        )\
\
async def new_member(update: Update, ctx: ContextTypes.DEFAULT_TYPE):\
    for m in update.message.new_chat_members:\
        if m.is_bot:\
            continue\
        kb = [[InlineKeyboardButton("\uc0\u55357 \u56577  Inviter un ami", url="https://t.me/share/url?url=https://t.me/LeStudioSelect")]]\
        await update.message.reply_text(\
            f"\uc0\u10024  Bienvenue *\{m.first_name\}* dans *LeStudioSelect* ! \u55356 \u57225 \\nPartage le canal avec tes amis \u55357 \u56908 ",\
            parse_mode="Markdown", reply_markup=InlineKeyboardMarkup(kb)\
        )\
\
# \uc0\u9472 \u9472  SCHEDULER \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \
async def auto_post(app: Application):\
    global post_idx\
    post = AUTO_POSTS[post_idx % len(AUTO_POSTS)]\
    try:\
        await app.bot.send_message(\
            chat_id=CHANNEL_ID, text=post["text"],\
            parse_mode="Markdown", reply_markup=share_keyboard()\
        )\
        log.info(f"Post auto envoy\'e9 : \{post['cat']\}")\
        post_idx += 1\
    except Exception as e:\
        log.error(f"Erreur post auto : \{e\}")\
\
async def check_and_publish(app: Application):\
    posts = load_posts()\
    now = datetime.now().strftime("%d/%m %H:%M")\
    modified = False\
    for post in posts:\
        if post.get("sent") or post.get("date_heure", "").strip() != now:\
            continue\
        try:\
            photos = post["photos"]\
            texte  = post.get("texte", "")\
            if len(photos) == 1:\
                await app.bot.send_photo(\
                    chat_id=CHANNEL_ID, photo=photos[0],\
                    caption=texte, parse_mode="Markdown",\
                    reply_markup=share_keyboard()\
                )\
            else:\
                media = [\
                    InputMediaPhoto(media=fid, caption=texte if i == 0 else None, parse_mode="Markdown")\
                    for i, fid in enumerate(photos[:10])\
                ]\
                await app.bot.send_media_group(chat_id=CHANNEL_ID, media=media)\
                await app.bot.send_message(\
                    chat_id=CHANNEL_ID,\
                    text="\uc0\u55357 \u56577  Partage ce post avec tes amis \u11015 \u65039 ",\
                    reply_markup=share_keyboard()\
                )\
            post["sent"] = True\
            modified = True\
            log.info(f"Post planifi\'e9 publi\'e9 : \{post['categorie']\} \'97 \{now\}")\
        except Exception as e:\
            log.error(f"Erreur publication : \{e\}")\
    if modified:\
        save_posts(posts)\
\
async def community_post(app: Application):\
    try:\
        cnt = await app.bot.get_chat_member_count(CHANNEL_ID)\
        await app.bot.send_message(\
            chat_id=CHANNEL_ID,\
            text=(\
                f"\uc0\u55357 \u56520  *\{cnt\} membres dans LeStudioSelect !*\\n\\n"\
                f"Merci \'e0 toute la communaut\'e9 \uc0\u55357 \u56911 \\n"\
                f"Mode \'b7 Beaut\'e9 \'b7 \'c9lectrom\'e9nager \'b7 Parfums\\n\\n"\
                f"Partage le canal avec tes amis \uc0\u11015 \u65039 "\
            ),\
            parse_mode="Markdown", reply_markup=share_keyboard()\
        )\
    except Exception as e:\
        log.error(f"Erreur post communaut\'e9 : \{e\}")\
\
# \uc0\u9472 \u9472  MAIN \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \
def main():\
    app = Application.builder().token(BOT_TOKEN).build()\
\
    app.add_handler(CommandHandler("start",     cmd_start))\
    app.add_handler(CommandHandler("catalogue", cmd_catalogue))\
    app.add_handler(CommandHandler("stats",     cmd_stats))\
    app.add_handler(CommandHandler("posts",     cmd_posts))\
    app.add_handler(CommandHandler("ajouter",   cmd_ajouter))\
    app.add_handler(CallbackQueryHandler(button_cb))\
    app.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, new_member))\
    app.add_handler(MessageHandler(filters.PHOTO & filters.ChatType.PRIVATE, receive_photo))\
\
    scheduler = AsyncIOScheduler(timezone="Europe/Paris")\
    scheduler.add_job(auto_post,         "cron", hour="9,17,21", minute=0, args=[app])\
    scheduler.add_job(community_post,    "cron", hour=12, minute=0, args=[app])\
    scheduler.add_job(check_and_publish, "cron", minute="*", args=[app])\
    scheduler.start()\
\
    log.info("\uc0\u9989  Bot LeStudioSelect d\'e9marr\'e9.")\
    app.run_polling()\
\
if __name__ == "__main__":\
    main()}