from config_data.config import load_config

config = load_config()

LEXICON_RU = {
    '/start': 'приветик'
}

CALLBACK_RU: dict[str, dict] = {
    'main_actions': {
        'publish_post': '✅ опубликовать пост',
        'reject_post': '❌ отклонить пост',
        'edit_menu': '✏️ редактировать пост',
        'add_to_queue': '📆 добавить в очередь',
        'swap_post': '🔄 другой пост',
    },
    'edit_menu': {
        'delete_first_string': '🔼🗑 удалить первый абзац',
        'delete_last_string': '🔽🗑 удалить последний абзац',
        'add_link': '✉️ добавить ссылку на себя',
        'main_actions': '⬅️ назад'
    },
    'main_menu': {
        'start_stop_queue': '⏯ вкл/выкл автопубликацию очереди',
        'next_post': '⏩ получить следующий пост',
        'last_post': '⏪ получить последний пост',
        'bot_mode': '🔁 переключение каналов',
        'swap_post': '➡️ получить пост'
    },
    'bot_mode': {
        link: link for link in config.tg_channel.channel_names
    },
    
    
    'on_buttons_click': {
        'main_actions_add_to_queue':
            {
                'publish_post': '✅ опубликовать пост',
                'reject_post': '❌ отклонить пост',
                'edit_menu': '✏️ редактировать пост',
                'none': '📝 добавлено в очередь',
                'swap_post': '🔄 другой пост',
            },
        
    }
}

LEXICON_COMMANDS = {
    '/get_post': 'запросить рецепт',
    '/bot_menu': 'меню бота',
    '/switch_autoposting': 'вкл/выкл автоматическую отправку постов',
}


# ✅❌🔄✏️📆🗑🔼🔽⬅️✉️⏪⏩⏯🔁➡️📝