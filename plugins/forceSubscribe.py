import time
import logging
from Config import Config
from pyrogram import Client, filters
from sql_helpers import forceSubscribe_sql as sql
from pyrogram.types import ChatPermissions, InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors.exceptions.bad_request_400 import UserNotParticipant, UsernameNotOccupied, ChatAdminRequired, PeerIdInvalid

logging.basicConfig(level=logging.INFO)

static_data_filter = filters.create(lambda _, __, query: query.data == "onUnMuteRequest")
@Client.on_callback_query(static_data_filter)
def _onUnMuteRequest(client, cb):
  user_id = cb.from_user.id
  chat_id = cb.message.chat.id
  chat_db = sql.fs_settings(chat_id)
  if chat_db:
    channel = chat_db.channel
    chat_member = client.get_chat_member(chat_id, user_id)
    if chat_member.restricted_by:
      if chat_member.restricted_by.id == (client.get_me()).id:
          try:
            client.get_chat_member(channel, user_id)
            client.unban_chat_member(chat_id, user_id)
            if cb.message.reply_to_message.from_user.id == user_id:
              cb.message.delete()
          except UserNotParticipant:
            client.answer_callback_query(cb.id, text="❗ Bergabunglah dengan 'channel' yang disebutkan dan tekan tombol 'Bunyikan Saya' lagi.", show_alert=True)
      else:
        client.answer_callback_query(cb.id, text="❗ Anda dibisukan oleh admin karena alasan lain.", show_alert=True)
    else:
      if not client.get_chat_member(chat_id, (client.get_me()).id).status == 'administrator':
        client.send_message(chat_id, f"❗ **{cb.from_user.mention} sedang mencoba untuk mengaktifkan suara sendiri tetapi saya tidak dapat mengaktifkannya karena saya bukan admin dalam obrolan ini, tambahkan saya sebagai admin lagi.**\n__`Leaving this chat...`__")
        client.leave_chat(chat_id)
      else:
        client.answer_callback_query(cb.id, text="❗ Peringatan: Jangan klik tombol jika Anda dapat berbicara dengan bebas.", show_alert=True)



@Client.on_message(filters.text & ~filters.private & ~filters.edited, group=1)
def _check_member(client, message):
  chat_id = message.chat.id
  chat_db = sql.fs_settings(chat_id)
  if chat_db:
    user_id = message.from_user.id
    if not client.get_chat_member(chat_id, user_id).status in ("administrator", "creator") and not user_id in Config.SUDO_USERS:
      channel = chat_db.channel
      if channel.startswith("-"):
          channel_url = client.export_chat_invite_link(int(channel))
      else:
          channel_url = f"https://t.me/{channel}"
      try:
        client.get_chat_member(channel, user_id)
      except UserNotParticipant:
        try:
          sent_message = message.reply_text(
              " {} , Anda belum berlangganan saluran saya. Silakan bergabung menggunakan tombol di bawah ini dan tekan **Bunyikan Saya** untuk mengaktifkan suara Anda sendiri.".format(message.from_user.mention, channel, channel),
              disable_web_page_preview=True,
             reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("Subscribe My Channel", url=channel_url)
                ],
                [
                    InlineKeyboardButton("Bunyikan Saya", callback_data="onUnMuteRequest")
                ]
            ]
        )
          )
          client.restrict_chat_member(chat_id, user_id, ChatPermissions(can_send_messages=False))
        except ChatAdminRequired:
          sent_message.edit("❗ **saya bukan admin disini.**\n__Jadikan saya admin dengan izin Blokir Pengguna dan tambahkan saya lagi.\n`Leaving this chat...`__")
          client.leave_chat(chat_id)
      except ChatAdminRequired:
        client.send_message(chat_id, text=f"❗ **Saya bukan admin di channel tersebut**\n__Jadikan saya admin di saluran dan tambahkan saya lagi.\n`Leaving this chat...`__")
        client.leave_chat(chat_id)


@Client.on_message(filters.command(["forcesubscribe", "fsub"]) & ~filters.private)
def config(client, message):
  user = client.get_chat_member(message.chat.id, message.from_user.id)
  if user.status is "creator" or user.user.id in Config.SUDO_USERS:
    chat_id = message.chat.id
    if len(message.command) > 1:
      input_str = message.command[1]
      input_str = input_str.replace("@", "")
      if input_str.lower() in ("off", "no", "disable"):
        sql.disapprove(chat_id)
        message.reply_text("❌ **Force Subscribe Berhasil Dinonaktifkan.**")
      elif input_str.lower() in ('clear'):
        sent_message = message.reply_text('**Unmuting all members who are muted by me...**')
        try:
          for chat_member in client.get_chat_members(message.chat.id, filter="restricted"):
            if chat_member.restricted_by.id == (client.get_me()).id:
                client.unban_chat_member(chat_id, chat_member.user.id)
                time.sleep(1)
          sent_message.edit('✅ **Suarakan semua anggota yang dibisukan oleh saya.**')
        except ChatAdminRequired:
          sent_message.edit('❗ **Saya bukan admin di chat ini.**\n__saya bisa\ suarakan anggota karena saya bukan admin dalam obrolan ini, jadikan saya admin dengan izin Blokir Pengguna.__')
      else:
        try:
          client.get_chat_member(input_str, "me")
          sql.add_channel(chat_id, input_str)
          if input_str.startswith("-"):
              channel_url = client.export_chat_invite_link(int(input_str))
          else:
              channel_url = f"https://t.me/{input_str}"
          message.reply_text(f"✅ **Paksa Berlangganan Diaktifkan**\n__Force Subscribe diaktifkan, semua anggota grup harus berlangganan di channel tersebut untuk mengirim pesan di grup ini.__", disable_web_page_preview=True)
        except UserNotParticipant:
          message.reply_text(f"❗ **Bukan Admin di Channel**\n__Saya bukan admin di channel tersebut. Tambahkan saya sebagai admin untuk mengaktifkan ForceSubscribe.__", disable_web_page_preview=True)
        except (UsernameNotOccupied, PeerIdInvalid):
          message.reply_text(f"❗ **Channel Username/ID Tidak valid.**")
        except Exception as err:
          message.reply_text(f"❗ **ERROR:** ```{err}```")
    else:
      if sql.fs_settings(chat_id):
        my_channel = sql.fs_settings(chat_id).channel
        if my_channel.startswith("-"):
            channel_url = client.export_chat_invite_link(int(input_str))
        else:
            channel_url = f"https://t.me/{my_channel}"
        message.reply_text(f"✅ **Paksa Berlangganan diaktifkan di obrolan ini.**\n__Untuk [Channel]({channel_url}) ini__", disable_web_page_preview=True)
      else:
        message.reply_text("❌ **Force subscribe dinonaktifkan dalam obrolan ini.**")
  else:
      message.reply_text("❗ **Diperlukan Pembuat Grup**\n__Anda harus menjadi pembuat grup untuk melakukan itu.__")
