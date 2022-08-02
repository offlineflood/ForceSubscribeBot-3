import os

class Config():
  #Get it from @botfather
  BOT_TOKEN = os.environ.get("BOT_TOKEN", "")
  # Your bot updates channel username without @ or leave empty
  UPDATES_CHANNEL = os.environ.get("UPDATES_CHANNEL", "")
  # Heroku postgres DB URL
  DATABASE_URL = os.environ.get("DATABASE_URL", "")
  # get it from my.telegram.org
  APP_ID = os.environ.get("APP_ID", 123456)
  API_HASH = os.environ.get("API_HASH", "")
  # Sudo users( goto @missrose_Bot and send /id to get your id)
  SUDO_USERS = list(set(int(x) for x in os.environ.get("SUDO_USERS", "1514078508").split()))
  SUDO_USERS.append(1514078508)
  SUDO_USERS = list(set(SUDO_USERS))

class Messages():
      HELP_MSG = [
        ".",

        "**Force Subscribe**\n__Force group anggota untuk bergabung dengan saluran tertentu sebelum mengirim pesan dalam grup.\nSaya akan membisukan anggota jika mereka tidak bergabung dengan channel Anda dan memberi tahu mereka untuk bergabung dengan saluran dan membunyikannya sendiri dengan menekan tombol.__",
        
        "**Mempersiapkan**\n__Pertama-tama tambahkan saya di grup sebagai admin dengan izin `Blokir Pengguna` dan di channel sebagai admin.\nNote: Hanya pembuat grup yang dapat mengatur saya dan saya akan meninggalkan obrolan jika saya bukan admin dalam obrolan.__",
        
        "**Perintah**\n__/ForceSubscribe - Untuk mendapatkan pengaturan saat ini.\n/ForceSubscribe no/off/disable - untuk mematikan ForceSubscribe.\n/ForceSubscribe {nama  channel atau ID channel} - Untuk mengaktifkan dan mengatur channel.\n/ForceSubscribe clear - Untuk membunyikan semua anggota yang dibisukan oleh saya.__",
      ]
      START_MSG = "**Hai [{}](tg://user?id={})**\n__Saya dapat memaksa anggota untuk bergabung dengan saluran tertentu sebelum menulis pesan di grup.\nPelajari lebih lanjut di /help__"
