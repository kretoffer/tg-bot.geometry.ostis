from aiogram import Bot
from aiogram.types import ReplyMarkupUnion, InputMediaPhoto, InputMediaVideo


async def send_message_with_content(chat_id, content: str, bot: Bot, markup: ReplyMarkupUnion):
    content = content.split(" && ")
    if len(content) == 1:
        [content] = content
        if content.startswith("http"):
            if content.endswith((".jpg", ".jpeg", ".png")):
                await bot.send_photo(chat_id, InputMediaPhoto(media=content), reply_markup=markup)
            elif content.endswith((".mp4", ".mov", ".avi")):
                await bot.send_video(chat_id, InputMediaVideo(media=content), reply_markup=markup)
            else:
                await bot.send_message(chat_id, content, parse_mode="markdown", reply_markup=markup)
    else:
        media = []
        caption = None
        for el in content:
            if el.endswith((".jpg", ".jpeg", ".png")):
                media.append(InputMediaPhoto(media=el, parse_mode="markdown"))
            elif el.endswith((".mp4", ".mov", ".avi")):
                media.append(InputMediaVideo(media=el, parse_mode="markdown"))
            else:
                caption = el
        media[-1].caption = caption

        await bot.send_media_group(chat_id, media, reply_markup=markup)