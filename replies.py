# Data storage class, basically
class Replies:
    def __init__(self):
        pekora_noises = {
            "naww": "https://www.youtube.com/watch?v=JNgCFHbPARg",
            "motherfucker": "https://www.youtube.com/watch?v=1OjQVMiyUMg",
            "oh no jesus": "https://www.youtube.com/watch?v=MwCNEySMNWg",
            "yolo": "https://www.youtube.com/watch?v=MSUckSO-Dsw",
            "ogey rrat": "https://www.youtube.com/watch?v=JacN1MzyeKo",
            "rrat simulator rrrra": "https://www.youtube.com/watch?v=Xr_pKdyeIJo"
        }
        self.nothing_changed_reply_list = ["Sorry, I couldn't pekofy the comment for some reason peko. "
                                           f"So here's a video of Pekora saying [{title}]({link}) instead peko."
                                           for title, link in pekora_noises.items()]
        self.no_recursion_reply = "[no](https://www.youtube.com/watch?v=3FOe-KNUwb4)"
        self.pain_peko_reply = "[pain-peko.](https://preview.redd.it/dvk3bft2a9l51.jpg?auto=webp&s=d5e53605dc0e99ed55884fc00c9b965c7dd38e7c)"
        self.hey_moona_reply = "#Hey Moona!"
        self.limit_reached_reply = "Sorry peko, but I can't pekofy it any further to prevent spam peko. Thank you for your understanding peko."
        self.bot_score_abuse_reply = "Sorry peko, can't pekofy that due to potential bot score abuse peko."
        self.confused_reply = "eh?"

        # some of them are repeated to increase chance
        self.thanks = ["Thank you peko", "Thank you peko!", "Thank you peko~", "Arigatou peko!", "Thank you peko!",
                  "Thank you peko~", "Arigatou peko!", "Arigatou peko~", "ありがとうぺこ～", "ありがとうぺこ！",
                  "Thank you peko!", "Thank you peko~", "Ehehe", "Ehehe", "Ehehe",
                  "Arigatou peko da ne! [peko~](https://www.youtube.com/watch?v=zOUPxaA6mBM)",
                  "[Arigatou peko.](https://www.youtube.com/watch?v=swGNEJ56EFI)"]
        self.sorrys = ["Sorry peko ; ;", "Sorry peko...", "G-Gomen peko.", "ごめんぺこ・・・"]
        self.insults = ["Bakatare ga!", "Bakatare ga!", "Bakatare ga!", "Bakatare ga!", "Anta wa baka nano?", "バカたれが！",
                   "ばかたれが！", "あんたはバカなの？", "ぺっ", "Go peko yourself!",
                   "[Disgusting.](https://streamable.com/6ntf2g)"]
        self.loves = ["Thank you guys. Don't cheat on me, okay? [Peko~](https://streamable.com/8gagri)",
                 "[Love you](https://streamable.com/dbzfxj) too peko!", "I love you too peko!", "Love you too peko~"]
        self.cutes = ["You're cute too peko!", "You're also cute peko!", "You're cute too peko~", "You're also cute peko~",
                 "Ehehe", "あなたもかわいいぺこ！"]