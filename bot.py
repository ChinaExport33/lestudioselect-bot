import logging, json, os
from datetime import datetime
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, InputMediaPhoto
from telegram.ext import (
    Application, CommandHandler, MessageHandler,
    CallbackQueryHandler, ContextTypes, filters
)
from apscheduler.schedulers.asyncio import AsyncIOScheduler

# CONFIG
BOT_TOKEN = os.environ.get("TELEGRAM_TOKEN", "")
CHANNEL_ID = "@LeStudioSelect"
ADMIN_ID = 8341097745

logging.basicConfig(format="%(asctime)s | %(levelname)s | %(message)s", level=logging.INFO)
log = logging.getLogger(__name__)

POSTS_FILE = "posts_planifies.json"

# GESTION JSON
def load_posts():
        if not os.path.exists(POSTS_FILE):
                    return []
                with open(POSTS_FILE, "r", encoding="utf-8") as f:
                            return json.load(f)

def save_posts(posts):
        with open(POSTS_FILE, "w", encoding="utf-8") as f:
                    json.dump(posts, f, ensure_ascii=False, indent=2)

# BOUTON PARTAGE
def share_keyboard():
        return InlineKeyboardMarkup([[
            InlineKeyboardButton("Partager", url="https://t.me/share/url?url=https://t.me/LeStudioSelect"),
            InlineKeyboardButton("Rejoindre", url="https://t.me/LeStudioSelect"),
]])

# POSTS AUTO
AUTO_POSTS = [
        {"cat": "Mode Femme", "text": "*Nouveaute Mode Femme*\n\nNouvelle robe midi a imprime fleuri, coupe ajustee, tissu premium.\nDisponible en 3 coloris - Tailles S au XL\n\n@LeStudioSelect"},
        {"cat": "Beaute", "text": "*Drop Beaute du jour*\n\nSerum eclat vitamine C + creme hydratante, duo bestseller.\nResultats visibles en 7 jours - Sans paraben\n\n@LeStudioSelect"},
        {"cat": "Electro", "text": "*Dyson en stock*\n\nSeche-cheveux Dyson Supersonic + lisseur GHD disponibles.\nPrix exclusif - Vente sur place\n\n@LeStudioSelect"},
        {"cat": "Parfums", "text": "*Selection Parfums cette semaine*\n\nFragrances niche & orientales, noms sur demande.\nFlacons authentiques\n\n@LeStudioSelect"},
        {"cat": "Accessoires", "text": "*Accessoires - Nouveaux arrivages*\n\nMontres, bijoux dores, ceintures cuir.\nLook premium - Prix accessible\n\n@LeStudioSelect"},
        {"cat": "Mode Homme", "text": "*Mode Homme - Collection printemps*\n\nChemises lin, joggers premium, style urban elegant.\nTailles M au XXL\n\n@LeStudioSelect"},
        {"cat": "Offre Flash", "text": "*OFFRE FLASH - Aujourd'hui seulement*\n\nSelection speciale - Prix reduits - Stock tres limite\n\nVite -> @LeStudioSelect\nPartage avec tes amis !"},
        {"cat": "Communaute", "text": "*LeStudioSelect grandit !*\n\nMode - Beaute - Electromenager - Parfums, tout au meme endroit.\n\nRejoins-nous -> @LeStudioSelect\nPartage le canal !"},
]

CAT_DETAILS = {
        "cat_mf": "*Mode Femme*\nRobes, tops, sacs, nouvelles pieces chaque semaine.\n\n@LeStudioSelect",
        "cat_mh": "*Mode Homme*\nStreetwear, chemises, pantalons.\n\n@LeStudioSelect",
        "cat_ac": "*Accessoires*\nBijoux, montres, ceintures.\n\n@LeStudioSelect",
        "cat_be": "*Beaute*\nSoins, maquillage, huiles.\n\n@LeStudioSelect",
        "cat_el": "*Electromenager*\nDyson, lisseurs GHD, seche-cheveux.\n\n@LeStudioSelect",
    "cat_pa": "*Parfums*\nNiche, luxe, orientaux.\n\n@LeStudioSelect",
}

post_idx = 0

# COMMANDES
async def cmd_start(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
        u = update.effective_user
    kb = InlineKeyboardMarkup([[
                InlineKeyboardButton("Rejoindre le canal", url="https://t.me/LeStudioSelect"),
                InlineKeyboardButton("Inviter un ami", url="https://t.me/share/url?url=https://t.me/LeStudioSelect"),
    ]])
    await update.message.reply_text(
                f"Salut *{u.first_name}* !\n\n"
                f"Bienvenue sur *LeStudioSelect* - selection premium :\n\n"
                f"Mode Femme & Homme\nAccessoires\nBeaute\nElectromenager Dyson\nParfums\n\n"
                f"Rejoins le canal pour voir toutes nos offres !",
                parse_mode="Markdown", reply_markup=kb
    )

async def cmd_catalogue(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
        cats = [
            ("Mode Femme", "cat_mf"), ("Mode Homme", "cat_mh"),
            ("Accessoires", "cat_ac"), ("Beaute", "cat_be"),
            ("Electromenager", "cat_el"), ("Parfums", "cat_pa"),
]
    rows = [[InlineKeyboardButton(l, callback_data=c)] for l, c in cats]
    await update.message.reply_text(
                "*Catalogue LeStudioSelect*\nChoisis une categorie :",
                parse_mode="Markdown", reply_markup=InlineKeyboardMarkup(rows)
    )

async def button_cb(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
        q = update.callback_query
    await q.answer()
    if q.data == "back_catalogue":
                cats = [
                                ("Mode Femme", "cat_mf"), ("Mode Homme", "cat_mh"),
                                ("Accessoires", "cat_ac"), ("Beaute", "cat_be"),
                                ("Electromenager", "cat_el"), ("Parfums", "cat_pa"),
                ]
                rows = [[InlineKeyboardButton(l, callback_data=c)] for l, c in cats]
            await q.edit_message_text(
                            "*Catalogue LeStudioSelect*\nChoisis une categorie :",
                            parse_mode="Markdown", reply_markup=InlineKeyboardMarkup(rows)
            )
        return
    txt = CAT_DETAILS.get(q.data, "Categorie introuvable.")
    back = [[
                InlineKeyboardButton("Retour", callback_data="back_catalogue"),
                InlineKeyboardButton("Rejoindre", url="https://t.me/LeStudioSelect")
    ]]
    await q.edit_message_text(txt, parse_mode="Markdown", reply_markup=InlineKeyboardMarkup(back))

async def cmd_stats(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
        if update.effective_user.id != ADMIN_ID:
                    return
                cnt = await ctx.bot.get_chat_member_count(CHANNEL_ID)
    posts = load_posts()
    pending = [p for p in posts if not p.get("sent")]
    await update.message.reply_text(
                f"*Stats LeStudioSelect*\n"
                f"Membres : *{cnt}*\n"
                f"Posts en attente : *{len(pending)}*\n"
                f"Date : {datetime.now().strftime('%d/%m/%Y %H:%M')}",
                parse_mode="Markdown"
    )

async def cmd_posts(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
                return
            posts = load_posts()
    pending = [p for p in posts if not p.get("sent")]
    if not pending:
                await update.message.reply_text("Aucun post en attente.")
                return
            lines = [
                        f"{i}. *{p['categorie']}* - {p['date_heure']} - {len(p.get('photos', []))} photo(s)"
                        for i, p in enumerate(pending, 1)
            ]
    await update.message.reply_text(
                "*Posts planifies :*\n\n" + "\n".join(lines),
                parse_mode="Markdown"
    )

async def cmd_ajouter(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
        if update.effective_user.id != ADMIN_ID:
                    return
                try:
                            args = " ".join(ctx.args).split("|")
                            if len(args) < 4:
                                            raise ValueError
                                        cat, dh, texte, fids = [a.strip() for a in args]
        photos = [f.strip() for f in fids.split(",") if f.strip()]
        if not photos or len(photos) > 10:
                        await update.message.reply_text("Entre 1 et 10 photos maximum.")
            return
        posts = load_posts()
        posts.append({"categorie": cat, "date_heure": dh, "texte": texte, "photos": photos, "sent": False})
        save_posts(posts)
        await update.message.reply_text(
                        f"Post ajoute !\n*{cat}* - {dh}\n{len(photos)} photo(s) planifiee(s).",
                        parse_mode="Markdown"
        )
except ValueError:
        await update.message.reply_text(
                        "Format :\n`/ajouter Categorie | JJ/MM HH:MM | Texte | file_id1,file_id2`",
                        parse_mode="Markdown"
        )

async def receive_photo(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
        if update.effective_user.id != ADMIN_ID:
                    return
    if update.message.photo:
                fid = update.message.photo[-1].file_id
        await update.message.reply_text(
                        f"*file_id de ta photo :*\n`{fid}`\n\nCopie-le pour l'utiliser dans /ajouter",
                        parse_mode="Markdown"
        )

async def new_member(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
        for m in update.message.new_chat_members:
                    if m.is_bot:
                                    continue
                                kb = [[InlineKeyboardButton("Inviter un ami", url="https://t.me/share/url?url=https://t.me/LeStudioSelect")]]
        await update.message.reply_text(
                        f"Bienvenue *{m.first_name}* dans *LeStudioSelect* !\nPartage le canal avec tes amis !",
                        parse_mode="Markdown", reply_markup=InlineKeyboardMarkup(kb)
        )

# SCHEDULER
async def auto_post(app: Application):
        global post_idx
    post = AUTO_POSTS[post_idx % len(AUTO_POSTS)]
    try:
                await app.bot.send_message(
                                chat_id=CHANNEL_ID, text=post["text"],
                                parse_mode="Markdown", reply_markup=share_keyboard()
                )
        log.info(f"Post auto envoye : {post['cat']}")
        post_idx += 1
except Exception as e:
        log.error(f"Erreur post auto : {e}")

async def check_and_publish(app: Application):
        posts = load_posts()
    now = datetime.now().strftime("%d/%m %H:%M")
    modified = False
    for post in posts:
                if post.get("sent") or post.get("date_heure", "").strip() != now:
                                continue
                            try:
                                            photos = post["photos"]
                                            texte = post.get("texte", "")
                                            if len(photos) == 1:
                                                                await app.bot.send_photo(
                                                                                        chat_id=CHANNEL_ID, photo=photos[0],
                                                                                        caption=texte, parse_mode="Markdown",
                                                                                        reply_markup=share_keyboard()
                                                                )
                            else:
                                                media = [
                                                                        InputMediaPhoto(media=fid, caption=texte if i == 0 else None, parse_mode="Markdown")
                                                                        for i, fid in enumerate(photos[:10])
                                                ]
                                                await app.bot.send_media_group(chat_id=CHANNEL_ID, media=media)
                                                await app.bot.send_message(
                                                    chat_id=CHANNEL_ID,
                                                    text="Partage ce post avec tes amis !",
                                                    reply_markup=share_keyboard()
                                                )
                                            post["sent"] = True
            modified = True
            log.info(f"Post planifie publie : {post['categorie']} - {now}")
except Exception as e:
            log.error(f"Erreur publication : {e}")
    if modified:
                save_posts(posts)

async def community_post(app: Application):
        try:
                    cnt = await app.bot.get_chat_member_count(CHANNEL_ID)
                    await app.bot.send_message(
                        chat_id=CHANNEL_ID,
                        text=(
                            f"*{cnt} membres dans LeStudioSelect !*\n\n"
                            f"Merci a toute la communaute !\n"
                            f"Mode - Beaute - Electromenager - Parfums\n\n"
                            f"Partage le canal avec tes amis !"
                        ),
                        parse_mode="Markdown", reply_markup=share_keyboard()
                    )
except Exception as e:
            log.error(f"Erreur post communaute : {e}")

    # MAIN
    def main():
            app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", cmd_start))
    app.add_handler(CommandHandler("catalogue", cmd_catalogue))
    app.add_handler(CommandHandler("stats", cmd_stats))
    app.add_handler(CommandHandler("posts", cmd_posts))
    app.add_handler(CommandHandler("ajouter", cmd_ajouter))
    app.add_handler(CallbackQueryHandler(button_cb))
    app.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, new_member))
    app.add_handler(MessageHandler(filters.PHOTO & filters.ChatType.PRIVATE, receive_photo))

    scheduler = AsyncIOScheduler(timezone="Europe/Paris")
    scheduler.add_job(auto_post, "cron", hour="9,17,21", minute=0, args=[app])
    scheduler.add_job(community_post, "cron", hour=12, minute=0, args=[app])
    scheduler.add_job(check_and_publish, "cron", minute="*", args=[app])
    scheduler.start()

    log.info("Bot LeStudioSelect demarre.")
    app.run_polling()

if __name__ == "__main__":
        main()
    
