# -*- coding: utf-8 -*-
"""
Created on Mon Jul 25 15:43:12 2022

@author: i.adamovich
"""
import emoji, random

def random_text():
    text = [
            emoji.emojize('Доброе утро! Твоя посылочка :package:, распишись куда-нибудь.')
            ,emoji.emojize('Оп, очередной подгон адресочков :office_building: для бизнесвумэн дня :woman_office_worker_light_skin_tone:')
            ,emoji.emojize('День будет отличным :black_heart:')
            ,emoji.emojize('Ну-ка быстро искать красивый и удобный дом для детей :detective:! Вот вариантики:')
            ,emoji.emojize('Сегодня не много (может и много, я всего-лишь заранне написанный текст, не ебу :man_shrugging:), но это честная работа.')
            ,emoji.emojize('Это тебе :backhand_index_pointing_right::backhand_index_pointing_left:...')
            ,emoji.emojize('Придумывать фразы довольно сложно :face_with_steam_from_nose:, поэтому держи просто файл. Но ты умница!')
            ,'Иногда я жалею, что просто не забил сюда сборник цитат волков...'
            ,emoji.emojize(':smiling_face_with_horns::eggplant:')
            ,emoji.emojize('Мне всё ещё приходится вручную запускать этот скрипт каждый день за исключением выходных :slightly_frowning_face:')
            ,emoji.emojize('Как думаешь, сколько нужно вариантов, чтобы один и тот же не попадался чаще двух раз в неделю?\n\n\n\nМного.')
            ,emoji.emojize('Купил мужик :top_hat:, а она ему :thumbs_up_medium_skin_tone:.')
            ,'Вопрос:\n— С луком и с яйцами, но не пирожок?\nОтвет:\n— Робин Гуд.'
            ,'Ö'
            ,'Нейросети справляются с написанием смешных текстов гораздо лучше('
            ,emoji.emojize(':turtle:')
            ,emoji.emojize(':hedgehog:')
            ,emoji.emojize(':helicopter: — :helicopter:...')
            ,'Честное слово, это не спам...'
            ,'Обычных мгновений не бывает.'
            ,emoji.emojize('Да, непросто. А что поделать? Просто ничего не бывает, старайся :sparkling_heart:')
            ,'А это, ох, как бы тебе лучше объяснить... Понимаешь, это такое животное, но в то же время, это всё тот же не заслуживающий уважения мужчина, у которго проблемы с задним проходом...'
            ,'- Знаешь, сэр Макс, если честно, мне никогда не нравился лозунг "Победа или смерть", - усмехнулся Джуффин.\n- "Победа или какая-нибудь другая победа" - звучит куда привлекательнее!'
            ,'Скептический ум - страшное оружие в борьбе с собственным счастьем.\n«Большая телега»'
            ,'Всякое существо рождается для того, чтобы познавать мир. А не для того, чтобы всем в этом мире понравиться.\n«Мастер ветров и закатов»'
            ,'Себя надо любить и хвалить. Не поручать же такое ответственное дело чужим людям!\n«Простые волшебные вещи»'
            ,'Была бы задница, а приключения на неё всегда найдутся.\n«Гнезда Химер. Хроники Хугайды»'
            ,'Любить следует путь, а не грядущий конечный пункт, чем бы он ни был.\n«Книга Одиночеств»'
            ,'... время уходит, лето заканчивается, жизнь твоя тратится на ерунду, и другой жизни у тебя, между прочим, нет, ты в курсе?\n«Сказки старого Вильнюса»'
            ,'''Говорит:
    «Однажды свинью резали. Меня тогда со двора прогнали, чтобы не смотрел».
    Пауза.
    Добавляет:
    «Лучше бы они меня прогнали, когда жизнь свою жили. На такое детям действительно смотреть нельзя».
    '''
            ,'''— Я — «свой». Хороший, пушистый и совершенно безопасный. Честно.
    — Пушистый и безопасный? Это уже какой-то хомяк в презервативе получается.
    '''
            ,'Если ты это читаешь, значит, я заебался копировать и вставлять цитаты Макса Фрая.'
    ]
    
    return random.choice(text)
