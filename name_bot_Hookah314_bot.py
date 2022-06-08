
def balans (user_id,namebot,сurrency):
    import iz_func
    itog = 0
    db,cursor = iz_func.connect ()
    sql = "select id,summ from money_log where namebot = '"+str(namebot)+"' and user_id = '"+str(user_id)+"' and currency = '"+str(сurrency)+"' "
    cursor.execute(sql)
    results = cursor.fetchall()    
    itog = 0        
    for row in results:
        id,summ = row.values()
        itog = itog + summ
        print ('    [+]itog:',id,summ,itog)
    return itog     


def add_menu (markup,user_id,namebot):
    import iz_telegram
    from telebot import types
    setting = iz_telegram.get_namekey (user_id,namebot,'Избранный список')        
    mn01 = types.InlineKeyboardButton(text=setting,callback_data = "Избранный список")
    markup.add(mn01)
    return markup


def message_tovar (user_id,namebot,message_id,kod_produkta,regim):    
    name = ''
    price = 0
    about = ''
    import iz_func    
    db,cursor = iz_func.connect ()
    sql = "select id,name,price,kod_1c,about from bot_product where kod_1c = "+str(kod_produkta)+"" 
    cursor.execute(sql)
    data = cursor.fetchall()
    id = 0
    for rec in data: 
        id,name,price,kod_1c,about  = rec.values()    
    if id != 0:
        from telebot import types    
        import iz_telegram
        import telebot
        markup = types.InlineKeyboardMarkup(row_width=4)
        sql = "select id,id_tovar,koll from bot_select_tovar where namebot = '"+str(namebot)+"' and user_id = '"+str(user_id)+"' and id_tovar = '"+str(kod_produkta)+"'" 
        cursor.execute(sql)
        data = cursor.fetchall()
        id = 0
        koll = 1
        for rec in data: 
            id,id_tovar,koll = rec.values() 

        if id == 0:
            sql = "INSERT INTO bot_select_tovar (id_tovar,koll,name_tovar,namebot,user_id) VALUES ('{}',{},'{}','{}','{}')".format (kod_produkta,koll,name,namebot,user_id)
            cursor.execute(sql)
            db.commit()
        mn011 = types.InlineKeyboardButton(text=  iz_telegram.get_namekey (user_id,namebot,"-1"),callback_data = "add1_"+str(kod_produkta))
        mn012 = types.InlineKeyboardButton(text=  iz_telegram.get_namekey (user_id,namebot,str(int(koll))+" шт."),callback_data = "back_"+str(kod_produkta))
        mn013 = types.InlineKeyboardButton(text=  iz_telegram.get_namekey (user_id,namebot,"+1"),callback_data = "add2_"+str(kod_produkta))
        markup.add(mn011,mn012,mn013)
        sql = "select id,`like` from bot_favorites where namebot = '{}' and user_id = {} and id_tovar = '{}' limit 1;".format(namebot,user_id,kod_produkta)
        cursor.execute(sql)
        data = cursor.fetchall()
        like = 0
        for rec in data: 
            id,like = rec.values()    
        mn021 = types.InlineKeyboardButton(text=  iz_telegram.get_namekey (user_id,namebot,"❤ ("+str(like)+")"),callback_data = "like_"+str(kod_produkta))
        mn022 = types.InlineKeyboardButton(text=  iz_telegram.get_namekey (user_id,namebot,"Корзина "+str(price)+" грв."),callback_data = "Корзина_"+str(kod_produkta))
        markup.add(mn021,mn022)
        mn031 = types.InlineKeyboardButton(text=  iz_telegram.get_namekey (user_id,namebot,"Назад"),callback_data = "back_"+str(kod_produkta))
        markup.add(mn031)
        if regim == 'new':
            message_out,menu = iz_telegram.get_message (user_id,'Шапка товара',namebot)
            message_out = message_out.replace('%%name%%',name)
            message_out = message_out.replace('%%about%%',about)
            message_out = message_out.replace('%%price%%',str(price))    
            answer = iz_telegram.bot_send (user_id,namebot,message_out,'',message_id) 
            namefile = ''
            try:        
                namefile = '/var/www/html/picture/hookah314_bot/'+str(kod_1c)+'.jpeg'    
                print ('[+] Имя файла для скачивания:',namefile)
                photo = open(namefile, 'rb')
                token = iz_telegram.get_token (namebot)
                bot   = telebot.TeleBot(token)
                bot.send_photo(user_id, photo)        
            except Exception as e:
                print ('[+]',namefile,e)
                namefile = iz_telegram.bot_setting(namebot,'Файл отсутствие картинки')
                if namefile == '':
                    namefile = '/home/izofen/Studiya/FL/picture/no_foto-800x800.jpg'
                photo = open(namefile, 'rb')
                token = iz_telegram.get_token (namebot)
                try:
                    bot   = telebot.TeleBot(token)
                    bot.send_photo(user_id, photo)        
                except:
                    pass         
            message_out,menu = iz_telegram.get_message (user_id,"Описание товара",namebot)
            message_out = message_out.replace('%%name%%',name)
            message_out = message_out.replace('%%about%%',about)
            message_out = message_out.replace('%%price%%',str(price))    
            answer = iz_telegram.bot_send (user_id,namebot,message_out,markup,0) 
        if regim == 'reg':
            message_out,menu = iz_telegram.get_message (user_id,"Описание товара",namebot)
            message_out = message_out.replace('%%name%%',name)
            message_out = message_out.replace('%%about%%',about)
            message_out = message_out.replace('%%price%%',str(price))    
            answer = iz_telegram.bot_send (user_id,namebot,message_out,markup,message_id) 
    else:
        print ('[+] Товар не обнаружен')    


def katalog (user_id,namebot,message_id,parents):
    import iz_func
    import iz_telegram

def start_prog (user_id,namebot,message_in,status,message_id,name_file_picture,telefon_nome):
    import iz_func
    import iz_game
    import iz_main
    import time
    import iz_telegram
    message_old = message_in
    label = 'send'
    db,cursor = iz_func.connect ()

    if message_in == 'зарегистрироваться':
        label = 'no send'
        iz_telegram.save_variable (user_id,namebot,"status",'Укажите Ваш номер телефона')
        message_out,menu,answer = iz_telegram.send_message (user_id,namebot,'Укажите Ваш номер телефона','S',0)

        iz_telegram.save_variable (user_id,namebot,"Номер телефона регистрация",'')
        iz_telegram.save_variable (user_id,namebot,"ФИО регистрация ",'')

    if status == 'Укажите Ваш номер телефона':
        label = 'no send'
        iz_telegram.save_variable (user_id,namebot,"Номер телефона регистрация",message_in)
        iz_telegram.save_variable (user_id,namebot,"status",'Ваше имя и фамилия')
        message_out,menu,answer = iz_telegram.send_message (user_id,namebot,'Ваше имя и фамилия','S',0)

    if status == 'Ваше имя и фамилия':
        label = 'no send'
        iz_telegram.save_variable (user_id,namebot,"ФИО регистрация ",message_in)
        label = 'no send'
        iz_telegram.save_variable (user_id,namebot,"status",'')
        message_out,menu,answer = iz_telegram.send_message (user_id,namebot,'Спасибо за регистрацию','S',0)

        telefon = iz_telegram.load_variable (user_id,namebot,"Номер телефона регистрация")
        kontragent_name = iz_telegram.load_variable (user_id,namebot,"ФИО регистрация ") 

        sql = "INSERT INTO 1С_information_maps (kod_1C,kontragent_kod,kontragent_name,name_1C,namebot,telefon) VALUES ('{}','{}','{}','{}','{}','{}')".format ('','',kontragent_name,'',namebot,telefon)
        cursor.execute(sql)
        db.commit()






    if message_in.find ('Избранный список') != -1:
        label = 'no send'
        from telebot import types
        markup = types.InlineKeyboardMarkup(row_width=4)
        message_out = ''
        import iz_func
        db,cursor = iz_func.connect ()
        sql = "select id,id_tovar,name_tovar from bot_favorites where namebot = '"+str(namebot)+"' and user_id = "+str(user_id)+" and `like` = 1"
        cursor.execute(sql)
        data = cursor.fetchall()
        id = 0
        for rec in data: 
            id,id_tovar,name_tovar = rec.values()
            sql = "select id,name from bot_product where kod_1c = "+str(id_tovar)+" limit 1"
            cursor.execute(sql)
            data_t = cursor.fetchall()
            name_t = 'Нет названия товара'
            for rec_t in data_t: 
                id_t,name_t = rec_t.values()
            mn01 = types.InlineKeyboardButton(text=name_t,callback_data = "katalog_"+str(id_tovar))
            markup.add(mn01)
        if id == 0:
            message_out,menu = iz_telegram.get_message (user_id,'Спиcок избранный пустой',namebot)
            markup = 0
            answer = iz_telegram.bot_send (user_id,namebot,message_out,markup,message_id)
        else:    
            message_out,menu = iz_telegram.get_message (user_id,'Избранный список вывести',namebot)
            answer = iz_telegram.bot_send (user_id,namebot,message_out,markup,message_id)
           
  
    if message_in.find ('like_') != -1: 
        label = 'no send'
        word  = message_in.replace('like_','')
        sql = "select id,`like` from bot_favorites where namebot = '{}' and user_id = {} and id_tovar = '{}' limit 1;".format(namebot,user_id,word)
        cursor.execute(sql)
        data = cursor.fetchall()
        id = 0
        like = 0
        for rec in data: 
            id,like = rec.values()         
        if id == 0:
            sql = "INSERT INTO bot_favorites (id_tovar,`like`,name_tovar,namebot,user_id) VALUES ('{}',{},'{}','{}','{}')".format (word,1,'',namebot,user_id)
            cursor.execute(sql)
            db.commit()            
        
        if like == 0:
            sql = "UPDATE bot_favorites SET `like` = 1 WHERE id = "+str(id)+""
            cursor.execute(sql)
            db.commit()             

        if like == 1:
            sql = "UPDATE bot_favorites SET `like` = 0 WHERE id = "+str(id)+""
            cursor.execute(sql)
            db.commit()             



        message_tovar (user_id,namebot,message_id,word,'reg') 
     
    if message_in.find ('add2_') != -1: 
        label = 'no send'
        word  = message_in.replace('add2_','')
        sql = "UPDATE bot_select_tovar SET koll = koll + 1 WHERE `id_tovar` = '"+str(word)+"'"
        cursor.execute(sql)
        db.commit()   
        message_tovar (user_id,namebot,message_id,word,'reg') 

    if message_in.find ('add1_') != -1: 
        label = 'no send'
        word  = message_in.replace('add1_','')
        sql = "UPDATE bot_select_tovar SET koll = koll - 1 WHERE `id_tovar` = '"+str(word)+"'"
        cursor.execute(sql)
        db.commit()   
        message_tovar (user_id,namebot,message_id,word,'reg') 

    if message_in.find ('Отмена') != -1:
        iz_func.save_variable (user_id,"status","",namebot)
        status = ''
        message_out,menu,answer  = iz_telegram.send_message (user_id,namebot,'ОтменаЗапуск  ','S',message_id)
        label = 'no send'
        
    if message_in.find ('buy_tovar') != -1: 
        label = 'no send'
        message_out,menu,answer  = iz_telegram.send_message (user_id,namebot,'Укажите Ваш телефон','S',message_id)
        iz_func.save_variable (user_id,"status","Укажите Ваш телефон",namebot)
                
    if status == 'Укажите Ваш телефон':
        label = 'no send'
        iz_func.save_variable (user_id,"status","Укажите адрес доставки",namebot)
        iz_func.save_variable (user_id,"Телефон доставки",message_in,namebot)
        message_out,menu,answer  = iz_telegram.send_message (user_id,namebot,'Укажите адрес доставки','S',0)

    if status == 'Укажите адрес доставки':
        import iz_func
        import iz_telegram
        label = 'no send'
        iz_func.save_variable (user_id,"Адрес доставки",message_in,namebot)
        iz_func.save_variable (user_id,"status","",namebot)
        message_out,menu,answer  = iz_telegram.send_message (user_id,namebot,'Информация передана продавцу','S',0)
        #iz_telegram.send_message_all_admin (namebot,'Новый заказ. Пользователь: '+str(user_id))        
        db,cursor = iz_func.connect ()
        login     = ''  
        project   = ''  
        summ      = ''  
        system    = ''  
        wallet    = ''  
        komment   = ''  
        adress    = iz_telegram.load_variable (user_id,namebot,"Телефон доставки")
        telefon   = iz_telegram.load_variable (user_id,namebot,"Адрес доставки")
        sql = "INSERT INTO bot_active_user (language,namebot,user_id,login,project,summ,`system`,wallet,komment,adress,telefon) VALUES ('{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}')".format ('ru',namebot,user_id,login,project,summ,system,wallet,komment,adress,telefon)
        cursor.execute(sql)
        db.commit()

    if message_in.find ('Корзина_') != -1: 
        label = 'no send'
        word  = message_in.replace('Корзина_','')
        markup = ''                
        message_out,menu = iz_telegram.get_message (user_id,"Товар в корзине",namebot)
        answer = iz_telegram.bot_send (user_id,namebot,message_out,markup,0) 
        import time 
        unixtime = int(time.time())
        sql = "INSERT INTO bot_basket (`namebot`,`user_id`,product,price,сurrency,status,unixtime) VALUES ('{}','{}','{}',0,'','',{})".format (namebot,user_id,word,unixtime)
        cursor.execute(sql)
        db.commit()
    
    if message_in == 'No moving_':
        label = 'no send'  
        word  = message_in.replace('No moving_','')   
        message_out,menu = iz_telegram.get_message (user_id,"Товар убран из корзины",namebot)
        markup = ''
        answer = iz_telegram.bot_send (user_id,namebot,message_out,markup,message_id)
        
    if message_in == 'clear_tovar':
        label = 'no send'
        db,cursor = iz_func.connect ()
        sql = "DELETE FROM  bot_basket WHERE user_id = '"+str(user_id)+"'"
        cursor.execute(sql)
        db.commit()
        #message_out = "Корзина пустая"
        message_out,menu = iz_telegram.get_message (user_id,"Корзина пустая",namebot)
        markup = ''
        message_out,menu,answer  = iz_telegram.send_message (user_id,namebot,"Корзина пустая",'S',message_id) 

    if message_in == 'Корзина':
        import time
        unixtime = int(time.time ()) - 60*60*24*3
        label = 'no send'
        db,cursor = iz_func.connect ()
        sql = "select id,product,price,сurrency from bot_basket where user_id = '"+str(user_id)+"' and unixtime > "+str(unixtime)+" "
        cursor.execute(sql)
        results = cursor.fetchall()    
        from telebot import types
        markup = types.InlineKeyboardMarkup(row_width=4)
        message_out,menu = iz_telegram.get_message (user_id,"Список товаров в корзине",namebot)        
        for row in results:
            id,product,price,сurrency = row.values()  
            sql = "select id,name,price,grup,kod_1c,about from bot_product where kod_1c = "+str(product)+" "
            cursor.execute(sql)
            results1 = cursor.fetchall()                
            name_l = "Товар удален или отсутствует"
            about  = ""
            price  = 0            
            for row1 in results1:
                id_l,name_l,price,grup_l,kod_1c_l,about = row1.values()  
            sitting,menu = iz_telegram.get_message (user_id,"Вывод кнопка товар в корзине",namebot) 
            sitting = sitting.replace('%%name%%',name_l)
            sitting = sitting.replace('%%about%%',about)
            sitting = sitting.replace('%%price%%',str(price))                        
            ## name_l + "  "+str(price)+" грн."            
            mn01 = types.InlineKeyboardButton(text = sitting,callback_data = "No moving_")            
            markup.add(mn01)

        mn01 = types.InlineKeyboardButton(text = iz_telegram.get_namekey (user_id,namebot,"Редактировать"),callback_data = "edit_tovar")
        mn02 = types.InlineKeyboardButton(text = iz_telegram.get_namekey (user_id,namebot,"Очистить корзину"),callback_data = "clear_tovar")
        markup.add(mn01,mn02)            
        mn01 = types.InlineKeyboardButton(text = iz_telegram.get_namekey (user_id,namebot,"Оформить заказ"),callback_data = "buy_tovar")
        markup.add(mn01)            
        answer = iz_telegram.bot_send (user_id,namebot,message_out,markup,0)     

    if message_in.find ('Отмена') != -1:
        label = 'no send'

    if message_in.find ('edit_tovar') != -1:
        label = 'no send'

    if message_in.find ('Баланс') != -1:
        summ_fiat_griv = balans (user_id,namebot,'гривны')
        label = 'no send'
        message_out = "Ваш баланс: "+str(summ_fiat_griv)+'  гривны'
        from telebot import types
        markup = types.InlineKeyboardMarkup(row_width=4)
        mn01 = types.InlineKeyboardButton(text='Корзина',callback_data = "Корзина")
        markup.add(mn01)
        answer = iz_telegram.bot_send (user_id,namebot,message_out,markup,message_id) 

    if message_in.find ('Задать вопрос') != -1:
        label = 'no send'
        message_out = "Ваш баланс: "
        from telebot import types
        markup = types.InlineKeyboardMarkup(row_width=4)
        mn01 = types.InlineKeyboardButton(text='Корзина',callback_data = "Корзина")
        markup.add(mn01)

    if message_in.find ('back_') != -1:
        label = 'no send'
        word  = message_in.replace('back_','')
        sql = "select id,name,grup,price,namebot,parents,kod_1c from bot_product where namebot = '"+str(namebot)+"' and kod_1c = '"+str(word)+"' limit 1"
        cursor.execute(sql) 
        results = cursor.fetchall()    
        for row in results:
            id_m,name_m,grup_m,price_m,namebot_m,parents_m,kod_1c_m = row.values()
            sql_id = iz_telegram.start_list (user_id,namebot,10,0,'не равно 0','не равно 0',0)
            markup = iz_telegram.get_menu_tovar (user_id,namebot,message_id,parents_m,sql_id,2)
            markup = add_menu (markup,user_id,namebot)
            message_out,menu = iz_telegram.get_message (user_id,'Каталог товаров',namebot)
            answer = iz_telegram.bot_send (user_id,namebot,message_out,markup,message_id)
            
    if message_in.find ('katalog_') != -1:
        word  = message_in.replace('katalog_','')
        label = 'no send'
    
    if message_in.find ('Поиск') != -1:
        message_out,menu,answer  = iz_telegram.send_message (user_id,namebot,'Укажите примерное название товара.\nНапример -Уголь-','S',0)
        label = 'no send'

    if message_in == 'Каталог':
        label = 'no send'
        parents = "Родитель Продукта в 1С не указан"
        #sql_id = iz_telegram.start_list (user_id,namebot,10,0,'не равно 0','не равно 0')
        sql_id = iz_telegram.start_list (user_id,namebot,10,0,0,'',parents,'id') ## Записываю новый порядок показа списка, По 10 штук, начиная с первого, с показателем родителя

        #markup = iz_telegram.get_menu_tovar (user_id,namebot,message_id,parents,sql_id,2)


        markup = iz_telegram.get_menu_tovar (user_id,namebot,sql_id,1,'','')
        #markup = iz_telegram.get_menu_tovar (user_id,namebot,sql_id,1,markup,'')   #### Получаю список товаров. Согласно SQL



        markup = add_menu (markup,user_id,namebot)  
        message_out,menu = iz_telegram.get_message (user_id,'Каталог товаров',namebot)
        answer = iz_telegram.bot_send (user_id,namebot,message_out,markup,message_id)

    if message_in.find ('katalog_') != -1:
        word  = message_in.replace('katalog_','')
        label = 'no send'
        parents = word
        if_grup = iz_telegram.if_grup (user_id,namebot,word)        
        if if_grup == 'Да':
            #sql_id = iz_telegram.start_list (user_id,namebot,10,0,'не равно 0','не равно 0')
            sql_id = iz_telegram.start_list (user_id,namebot,10,0,0,'',parents,0)
            #markup = iz_telegram.get_menu_tovar (user_id,namebot,message_id,parents,sql_id,2)
            markup = iz_telegram.get_menu_tovar (user_id,namebot,sql_id,1,'','')
            markup = add_menu (markup,user_id,namebot)
            message_out,menu = iz_telegram.get_message (user_id,'Каталог товаров',namebot)
            answer = iz_telegram.bot_send (user_id,namebot,message_out,markup,message_id)

        if if_grup == 'Нет' or if_grup == '':  
            sql = "UPDATE bot_select_tovar SET koll = 1 WHERE `id_tovar` = '"+str(word)+"'"
            cursor.execute(sql)
            db.commit()   
            message_tovar (user_id,namebot,message_id,word,'new')

    if message_in.find('grup') != -1:
        word  = message_in.replace('grup_','')  
        label = 'no send'
        set_whele = 'parents = "'+str(word)+'"'
        #markup = iz_telegram.message_send_sql (user_id,namebot,0,0)
        message_out,menu = iz_telegram.get_message (user_id,'Каталог товаров',namebot)
        answer = iz_telegram.bot_send (user_id,namebot,message_out,markup,message_id)

    if telefon_nome != '' or status == 'Телефон':
        label = 'no send'
        if status == 'Телефон':
            telefon_nome = message_in
        iz_func.save_variable (user_id,"status","",namebot)
        status = ''
        label = 'no send'
        telefon_nome = telefon_nome.replace('+','')
        if len(telefon_nome) == 11:
            telefon_nome = telefon_nome+'0'
        #message_out = 'Поиск информации в базе данных по номеру: '+str(telefon_nome)
        message_out,menu = iz_telegram.get_message (user_id,"Поиск информации в базе данных по номеру",namebot)
        message_out = message_out.replace('%%telefon_nome%%',str(telefon_nome))
        markup      = ''
        #answer = iz_func.bot_send (user_id,message_out,markup,namebot)  
        name_u = ''
        telefon_nome_kod = telefon_nome.replace('+','<9>')
        db,cursor = iz_func.connect () 
        sql = "select id,kontragent_name,kod_1C from 1С_information_maps where telefon like '%"+str(telefon_nome)+"%' " 
        kod_1C = 0
        cursor.execute(sql)
        results = cursor.fetchall()    
        kontragent_name = ''
        for row in results:
            id_u,kontragent_name,kod_1C = row.values()
        if kontragent_name == '':            
            markup      = ''
            message_out = 'В базе данных не обнаружен'
            #message_out,menu,answer  = iz_telegram.send_message (user_id,namebot,message_out,'S',0)

            message_out = 'Зарегистрируй в что бы получить скидку на купленный товар'
            message_out,menu,answer  = iz_telegram.send_message (user_id,namebot,message_out,'S',0)

        else:
            markup      = ''
            message_out,menu = iz_telegram.get_message (user_id,"Пользователь обнаружен",namebot)
            message_out      = message_out.replace('%%kontragent_name%%',str(kontragent_name))            
            markup = iz_telegram.get_menu (user_id,'Главное меню',namebot)            
            #answer = iz_telegram.bot_send (user_id,namebot,message_out,markup,0)                                     
            message_out,menu = iz_telegram.get_message (user_id,"Вывести список документов",namebot)
            from telebot import types
            markup = types.InlineKeyboardMarkup(row_width=4)            
            string_key = iz_telegram.get_namekey (user_id,namebot,'Вывести документы')             
            mn01 = types.InlineKeyboardButton(text=string_key,callback_data = "send_document_"+str(kod_1C))
            markup.add(mn01)       
            answer = iz_telegram.bot_send (user_id,namebot,message_out,markup,0)            
        
    if message_in.find ('send_document_') != -1:
        label = 'no send'
        word  = message_in.replace('send_document_','')        
        sql = "select id,name_file from 1С_document where kod_karta = '"+str(word)+"' " 
        cursor.execute(sql)
        results = cursor.fetchall()    
        markup      = ''
        import telebot    
        token = iz_func.get_token (namebot)
        bot   = telebot.TeleBot(token)  
        for row in results:
            id,name_file = row.values()
            try:
                doc = open('/var/www/html/picture/hookah314_bot/'+name_file, 'rb')
                bot.send_document(user_id, doc)
            except:
                pass  
        message_out = 'Поиск завершен'          
        message_out,menu,answer  = iz_telegram.send_message (user_id,namebot,'Поиск завершен','S',0)
        
    if message_in.find ('/chet') != -1:
        from freekassa import FreeKassaApi
        client = FreeKassaApi(first_secret='nvusr6ye',second_secret='nvusr6ye',merchant_id='122379', wallet_id='F103217044')
        payment_link = client.generate_payment_link(1, 200, 'kupinov@mail.ru', "Оплата по счету за услуги")
        label = 'no send'
        message_out = ''
        message_out = message_out + '<b>Счет на оплату № 1</b>' + '\n'
        message_out = message_out + '' + '\n'
        message_out = message_out + 'Оплата услуг - 100 руб.' + '\n'
        message_out = message_out + 'Товар        - 100 руб.' + '\n'
        message_out = message_out + 'Товар        - 100 руб.' + '\n'
        message_out = message_out + '' + '\n'
        message_out = message_out + '<b>Итого 300 рублей.</b>' + '\n'
        message_out = message_out + '' + '\n'
        message_out = message_out + 'Для оплаты услуги перейдите по ссылке:' + '\n'
        markup      = ''
        answer      = iz_func.bot_send (user_id,message_out,markup,namebot)
        message_out = payment_link
        answer      = iz_func.bot_send (user_id,message_out,markup,namebot)
        
    if message_in.find ('/start') != -1:
        label = 'no send'

    if message_in.find ('Скидка') != -1:
        label = 'no send'
        iz_telegram.save_variable (user_id,namebot,"status","Телефон")        
        import telebot 
        from telebot import types 
        token   = iz_telegram.get_token (namebot)
        bot     = telebot.TeleBot(token)            
        keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
        button_abort = types.KeyboardButton(text="Отмена")
        button_phone = types.KeyboardButton(text="Отправить номер телефона", request_contact=True)
        button_geo = types.KeyboardButton(text="Отправить местоположение", request_location=True)
        keyboard.add(button_abort,button_phone, button_geo)        
        bot.send_message(user_id, "Для проверки скидки отправь мне свой номер", reply_markup=keyboard)
              
    if message_in.find ('Next_') != -1:
        label = 'no send'
        word = message_in.replace('Next_','')
        db,cursor = iz_func.connect ()
        sql = "select id,`lost`,`see`,`strong`,`name`,`while` from sql_name where id = '"+str(word)+"' limit 1;"
        cursor.execute(sql)
        data = cursor.fetchall()
        for rec in data: 
            id_L,lost_L,see_L,strong_L,name_L,while_L = rec.values()
        n_all    = 0                      
        n_lost   = 0
        n_see    = 0
        n_next   = 0
        p_lost   = lost_L+1
        p_see    = see_L-1
        p_strong = 'DESC'
        print ('name_L:',name_L)
        if name_L == 'Поиск товара по названию': 
            sql = "select id,name  from bot_product where name like '%"+str(while_L)+"%' ORDER BY id DESC;"
        data = cursor.fetchall()
        for rec in data: 
            n_all = n_all + 1
            id,name = rec.values()
            if n_all < p_lost: 
                n_lost  = n_lost  + 1

            if n_all >= p_lost and n_all <= p_lost+p_see:     
                n_see = n_see + 1
                iz_game.Hookah314_bot (id,user_id,namebot)

            if n_all > p_lost+p_see:  
                n_next = n_next + 1

        if n_next != 0:
            #message_out = ''
            #message_out = message_out + 'Продолжить поиск' + '\n'
            #message_out = message_out + 'Всего найдено: ' + str(n_all)   + '\n'
            #message_out = message_out + 'Пропушено   : '  + str(n_lost)  + '\n'
            #message_out = message_out + 'Показано    : '  + str(n_see)   + '\n'
            #message_out = message_out + 'Не показано : '  + str(n_next)  + '\n'
            #message_out = message_out + 'Направление : '  + str(p_strong)+ '\n'
            #from telebot import types
            #markup = types.InlineKeyboardMarkup(row_width=4)
            #menu01 = "Вперед"
            #mn01 = types.InlineKeyboardButton(text=menu01,callback_data = "Next_"+str(word))
            #markup.add(mn01)
            #answer = iz_func.bot_send (user_id,message_out,markup,namebot)    
            sql = "UPDATE sql_name SET `lost` = "+str(n_lost+n_see)+" WHERE `id` = '"+str(word)+"'"
            cursor.execute(sql)
            db.commit()

    if label == 'send':
        message_out,menu = iz_telegram.get_message (user_id,'Поиск в названии товара',namebot)
        message_out = message_out.replace('%%Товар%%',str(message_in))
        markup = ''
        answer = iz_telegram.bot_send (user_id,namebot,message_out,markup,0) 
        n_all     = 0                      
        n_lost    = 0
        n_see     = 0
        n_next    = 0
        p_lost    = 0
        p_see     = 3
        p_strong  = 'DESC'
        db,cursor = iz_func.connect ()
        sql = "select id,name,price,kod_1c,about from bot_product where name like '%"+str(message_in)+"%' ORDER BY id DESC limit 5; "
        cursor.execute(sql)
        data = cursor.fetchall()
        for rec in data: 
            id,name,price,kod_1c,about = rec.values()
            print ('[+] Найден продукт в поиске:',kod_1c,name,) 
            message_tovar (user_id,namebot,0,kod_1c,'new') 


        #    n_all = n_all + 1
        #    if n_all < p_lost: 
        #        n_lost  = n_lost  + 1
        #    if n_all >= p_lost and n_all <= p_lost+p_see:     
        #        n_see = n_see + 1
        #    if n_all > p_lost+p_see:  
        #        n_next = n_next + 1
        #sql = "INSERT INTO sql_name (`lost`,`see`,`strong`,`name`,`while`,`good`,`bad`,`komment`) VALUES ({},{},'{}','{}','{}',0,0,'')".format (p_see,p_see,p_strong,'Поиск товара по названию',message_in)
        #cursor.execute(sql)
        #db.commit()
        #lastid = cursor.lastrowid

