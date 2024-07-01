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
    'queue_menu': {
        'next_post': '⏩ получить следующий пост',
        'start_stop_queue': '⏯ вкл/выкл автопубликацию очереди',
        
    }
     
}

LEXICON_COMMANDS = {
    '/get_post': 'запросить рецепт',
    '/queue_menu': 'настройки очереди постов',
    '/switch_autoposting': 'вкл/выкл автоматическую отправку постов',
}

# ✅❌🔄✏️📆🗑🔼🔽⬅️✉️⏩⏯