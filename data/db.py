import psycopg2
from .jsonDataPostgre import data_base

class DB:
    def __init__(self):
        try:
            self.connect = psycopg2.connect(user=data_base['postgreSQL']['user'],
                                            password=data_base['postgreSQL']['password'],
                                            host=data_base['postgreSQL']['host'],
                                            port=data_base['postgreSQL']['port'],
                                            database=data_base['postgreSQL']['database'])
            self.cursor = self.connect.cursor()
            self.create_table()
        except (Exception, psycopg2.Error) as ep:
            print(f'Ощибка при работе с базой: {ep}')


    def __enter__(self):
        return self
    

    def __exit__(self, type, value, traceback):
        self.cursor.close()
        self.connect.close()


    def with_append(self, cursor):
        try:
            with self.connect:
                cursor
        except psycopg2.InterfaceError:
            self.new_cursor_connect()
            print('Ощибка выполнения задач')


    def create_table(self):
        self.new_cursor_connect()
        tasks = [self.cursor.execute("""CREATE TABLE IF NOT EXISTS users(
            id SERIAL PRIMARY KEY NOT NULL,
            id_user bigint NOT NULL,
            balance_rub double precision NOT NULL,
            procent double precision,
            name TEXT,
            lastname TEXT,
            username TEXT,
            langcode TEXT,
            all_money_deposit bigint            
        )"""),

        self.cursor.execute("""CREATE TABLE IF NOT EXISTS catalogs(
            id SERIAL PRIMARY KEY NOT NULL,
            name_catalogs text NOT NULL
        )"""),

        self.cursor.execute("""CREATE TABLE IF NOT EXISTS products(
            id SERIAL PRIMARY KEY NOT NULL,
            id_catalog bigint NOT NULL,
            name_product VARCHAR(100) NOT NULL,
            description_product VARCHAR(601),
            price bigint,
            count_products bigint,
            link_products TEXT
        )"""),

        self.cursor.execute("""CREATE TABLE IF NOT EXISTS ban_list (
            id SERIAL PRIMARY KEY NOT NULL,
            id_user bigint,
            info_ban TEXT
        )"""),
        
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS basket (
            id_user bigint NOT NULL,
            id_products bigint NOT NULL,
            id_catalogs bigint NOT NULL,
            count_buy_product bigint default 1
        )"""),
        
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS manager_bot (
            message_is_buy_product TEXT,
            message_is_start TEXT,
            message_is_new_user TEXT,
            status_bot bool,
            max_summ_top_up bigint,
            min_summ_top_up bigint,
            message_is_faq TEXT,
            service_bot_message TEXT,
            captcha_users bigint,
            ref_summ double precision,
            ref_procent_top_up double precision,
            karma bigint
        )"""),

        self.cursor.execute("""CREATE TABLE IF NOT EXISTS admins (
            id SERIAL PRIMARY KEY NOT NULL,
            id_admin bigint,
            full_name TEXT,
            karma bigint
        )"""),
        
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS statistic_finance(
            my_money bigint
        )"""),
        
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS ref_system (
            id SERIAL PRIMARY KEY NOT NULL,
            id_user bigint,
            id_ref bigint
        )""")]

        self.with_append(tasks)


    def new_cursor_connect(self):
        self.connect = psycopg2.connect(user=data_base['postgreSQL']['user'],
                                        password=data_base['postgreSQL']['password'],
                                        host=data_base['postgreSQL']['host'],
                                        port=data_base['postgreSQL']['port'],
                                        database=data_base['postgreSQL']['database'])
        self.cursor = self.connect.cursor()
        return self.cursor
        

    def give_id_user(self, id_user):
        try:
            self.new_cursor_connect()
            self.cursor.execute(f'SELECT id_user FROM users WHERE id_user = {id_user}')
            set_fetch = self.cursor.fetchone()
            return set_fetch
        
        except Exception as ep:
            print(f"Ощибка при получении id пользователя: {ep}")
            return False
        

    def add_new_user(self, _id_user, _balance_rub, _procent, _name, _lastname, _username, _langcode, _all_money_deposit):
        self.new_cursor_connect()
        task = self.cursor.execute(f"""INSERT INTO users (id_user,
                                   balance_rub,
                                   procent,
                                   name,
                                   lastname,
                                   username,
                                   langcode,
                                   all_money_deposit) VALUES ({_id_user}, {_balance_rub}, {_procent}, '{_name}', '{_lastname}', '{_username}', '{_langcode}', {_all_money_deposit})""")
        
        self.with_append(task)


    def give_all_catalogs(self):
        try:
            self.new_cursor_connect()
            self.cursor.execute("SELECT * FROM catalogs")
            get_catalogs = self.cursor.fetchall()
            return get_catalogs
        except Exception as ep:
            print(f'Ощибка при выдачи каталогов: {ep}')
            return False
        

    def add_catalog(self, name):
        self.new_cursor_connect()
        task = self.cursor.execute(f"INSERT INTO catalogs (name_catalogs) VALUES ('{name}')")
        self.with_append(task)


    def add_product_in_catalogs(self, id_catalog, name_product, description_product, price, count_products, link):
        self.new_cursor_connect()
        task = self.cursor.execute(f"INSERT INTO products (id_catalog, name_product, description_product, price, count_products, link_products) VALUES ({id_catalog}, '{name_product}', '{description_product}', {price}, {count_products}, '{link}')")
        self.with_append(task)


    def give_all_product_in_catalogs(self, id_catalog):
        self.new_cursor_connect()
        self.cursor.execute(f"SELECT * FROM products WHERE id_catalog = '{id_catalog}'")
        fetch_all = self.cursor.fetchall()
        return fetch_all
            
        
    def give_info_product(self, id_product):
        self.new_cursor_connect()
        self.cursor.execute(f"SELECT * FROM products WHERE id = {id_product}")
        fetch_all = self.cursor.fetchall()
        return fetch_all


    def give_info_buy_products(self, id_products):
        self.new_cursor_connect()
        self.cursor.execute(f"SELECT name_product FROM products WHERE id = '{id_products}'")
        fetch_one = self.cursor.fetchone()
        return fetch_one
    
    
    def add_products_in_basket(self, id_user, id_products, id_catalogs, count_products):
        self.new_cursor_connect()
        task = self.cursor.execute(f"INSERT INTO basket (id_user, id_products, id_catalogs, count_buy_product) VALUES ({id_user}, {id_products}, {id_catalogs}, {count_products})")
        self.with_append(task)


    def give_basket_products_all(self, id_user):
        self.new_cursor_connect()
        self.cursor.execute(f"SELECT * FROM basket WHERE id_user = '{id_user}'")
        fetch_all = self.cursor.fetchall()
        return fetch_all
    

    def give_basket_product(self, id_user, id_product):
        self.new_cursor_connect()
        self.cursor.execute(f"SELECT * FROM basket WHERE id_user = '{id_user}' AND id_products = {id_product}")
        fetch_all = self.cursor.fetchall()
        return fetch_all
    

    def edit_count_products_in_basket(self, id_user, id_products, count_products):
        self.new_cursor_connect()
        task = self.cursor.execute(f"UPDATE basket SET count_buy_product = {count_products} WHERE id_user = {id_user} AND id_products = {id_products}")
        self.with_append(task)


    def select_method_products(self, method, id_products):
        self.new_cursor_connect()
        self.cursor.execute(f"SELECT {method} FROM products WHERE id = '{id_products}'")
        fetch_method = self.cursor.fetchone()
        return fetch_method
    

    def check_basket_product(self, id_user, id_product):
        self.new_cursor_connect()
        self.cursor.execute(f"SELECT id_products FROM basket WHERE id_user={id_user} AND id_products={id_product}")
        fetch_one = self.cursor.fetchone()
        if fetch_one != None:
            return True
        else:
            return False
        

    def delete_product_in_basket(self, id_user, id_product):
        self.new_cursor_connect()
        task = self.cursor.execute(f"DELETE FROM basket WHERE id_user = {id_user} AND id_products={id_product}")
        self.with_append(task)
        

    def give_info_user(self, method, id_user):
        self.new_cursor_connect()
        self.cursor.execute(f"SELECT {method} FROM users WHERE id_user = {id_user}")
        fetch_one = self.cursor.fetchone()
        return fetch_one
    

    def basket_isBuyProduct(self, id_user, id_products, max_count_product, count_products, _add_summ):
        self.new_cursor_connect()
        tasks = [self.cursor.execute(f"DELETE FROM basket WHERE id_user = {int(id_user)} AND id_products = {int(id_products)}"),
                self.cursor.execute(f"UPDATE users SET balance_rub = {int(_add_summ)} WHERE id_user = {id_user}"),
                self.cursor.execute(f"UPDATE products SET count_products = {int(max_count_product) - int(count_products)} WHERE id = {id_products}")]
        self.with_append(tasks)

         
    def update_products(self, type_value, value_method, set_method, id_product):
        self.new_cursor_connect()
        task = self.cursor.execute(f"UPDATE products SET {value_method} = '{set_method}' WHERE id = {id_product}")
        if type_value == 'int':
            task = self.cursor.execute(f"UPDATE products SET {value_method} = {set_method} WHERE id = {id_product}")
        self.with_append(task)


    def give_name_catalogs(self, id_catalog):
        self.new_cursor_connect()
        self.cursor.execute(f"SELECT name_catalogs FROM catalogs WHERE id = {id_catalog}")
        fetch_one = self.cursor.fetchone()
        return fetch_one
    

    def delete_from_products(self, id_products):
        self.new_cursor_connect()
        tasks = [self.cursor.execute(f"DELETE FROM products WHERE id = {id_products}"),
                self.cursor.execute(f"DELETE FROM basket WHERE id_products = {id_products}")]
        self.with_append(tasks)


    def delete_from_catalogs(self, id_catalog):
        self.new_cursor_connect()
        tasks = [self.cursor.execute(f"DELETE FROM products WHERE id_catalog = {id_catalog}"),
                 self.cursor.execute(f"DELETE FROM catalogs WHERE id = {id_catalog}"),
                 self.cursor.execute(f"DELETE FROM basket WHERE id_catalogs = {id_catalog}")]
        self.with_append(tasks)


    def delete_all_products_from_catalog(self, id_catalog):
        self.new_cursor_connect()
        task = self.cursor.execute(f"DELETE FROM products WHERE id_catalog = {id_catalog}")
        self.with_append(task)

    
    def delete_all_catalogs_one_clicked(self):
        self.new_cursor_connect()
        task = self.cursor.execute("DELETE FROM catalogs")
        self.with_append(task)
        

    def get_count_users_in_spam(self):
        self.new_cursor_connect()
        self.cursor.execute("SELECT id_user FROM users")
        fetch_all = self.cursor.fetchall()
        return fetch_all
    

    def give_all_msg_in_data(self):
        self.new_cursor_connect()
        self.cursor.execute("SELECT message_is_buy_product, message_is_start FROM manager_bot")
        fetch_one = self.cursor.fetchone()
        return fetch_one
    

    def give_top_up_balance_rub(self, id_user, _summ):
        self.new_cursor_connect()
        self.cursor.execute(f"SELECT balance_rub FROM users WHERE id_user = {id_user}")
        balance_user = self.cursor.fetchone()[0]
        task = self.cursor.execute(f"UPDATE users SET balance_rub = {int(_summ) + int(balance_user)} WHERE id_user = {id_user}")
        self.with_append(task)


    def give_max_and_min_summ(self):
        self.new_cursor_connect()
        self.cursor.execute("SELECT max_summ_top_up, min_summ_top_up FROM manager_bot")
        fetch_one = self.cursor.fetchone()
        return fetch_one
    

    def give_message_is_start_and_message_is_buy_and_status_bot_and_captcha(self):
        self.new_cursor_connect()
        self.cursor.execute("SELECT message_is_start, message_is_buy_product, message_is_new_user, status_bot, service_bot_message, captcha_users FROM manager_bot")
        fetch_one = self.cursor.fetchone()
        return fetch_one


    def сharacteristic_bot(self):
        self.new_cursor_connect()
        self.cursor.execute("SELECT * FROM manager_bot")
        fetch_all = self.cursor.fetchall()
        return fetch_all
    

    def update_сharacteristic_bot(self, type_value, value_method, set_method):
        self.new_cursor_connect()
        task = self.cursor.execute(f"UPDATE manager_bot SET {value_method} = '{set_method}'")
        if type_value == 'int':
            task = self.cursor.execute(f"UPDATE manager_bot SET {value_method} = {set_method}")

        if type_value == 'float':
            task = self.cursor.execute(f"UPDATE manager_bot SET {value_method} = {set_method}")

        self.with_append(task)


    def add_is_not_add_basic_value_in_db(self):
        self.new_cursor_connect()
        tasks = [self.cursor.execute(f"""INSERT INTO manager_bot (
                                    message_is_buy_product,
                                    message_is_start,
                                    message_is_new_user,
                                    status_bot, max_summ_top_up,
                                    min_summ_top_up,
                                    message_is_faq,
                                    service_bot_message,
                                    captcha_users,
                                    ref_summ,
                                    ref_procent_top_up,
                                    karma) VALUES ('-', '-', '-', True, 0, 0, 'FAQ: тут Пусто', '-', 0, 0, 0, 0)"""),
                
                self.cursor.execute(f"INSERT INTO statistic_finance (my_money) VALUES (0)")]
        
        self.with_append(tasks)


    def give_faq_shop(self):
        self.new_cursor_connect()
        self.cursor.execute("SELECT message_is_faq FROM manager_bot")
        fetch_one = self.cursor.fetchone()
        return fetch_one
    

    def give_count_users(self):
        self.new_cursor_connect()
        self.cursor.execute("SELECT count(*) FROM users")
        fetch_all = self.cursor.fetchall()
        return fetch_all
    
    
    def give_count_ban_users(self):
        self.new_cursor_connect()
        self.cursor.execute("SELECT count(*) FROM ban_list")
        fetch_all = self.cursor.fetchall()
        return fetch_all
    

    def give_count_admins(self):
        self.new_cursor_connect()
        self.cursor.execute("SELECT count(*) FROM admins")
        fetch_all = self.cursor.fetchall()
        return fetch_all
    

    def give_money_admin(self):
        self.new_cursor_connect()
        self.cursor.execute("SELECT my_money FROM statistic_finance")
        fetch_one = self.cursor.fetchone()
        return fetch_one
    

    def add_top_up_money_in_finance(self, _summ):
        self.new_cursor_connect()
        self.cursor.execute("SELECT my_money FROM statistic_finance")
        fetch_one = self.cursor.fetchone()
        task = self.cursor.execute(f"UPDATE statistic_finance SET my_money = {fetch_one[0]+int(_summ)}")
        self.with_append(task)


    def update_procent_users(self, _procent, id_user):
        self.new_cursor_connect()
        task = self.cursor.execute(f"UPDATE users SET procent = {_procent} WHERE id_user = {id_user}")
        self.with_append(task)


    def update_multi_balance_user(self, _summ, id_user):
        self.new_cursor_connect()
        task = self.cursor.execute(f"UPDATE users SET balance_rub = {_summ} WHERE id_user = {id_user}")
        self.with_append(task)


    def give_is_ban_users(self, id_user):
        self.new_cursor_connect()
        self.cursor.execute(f"SELECT id_user FROM ban_list WHERE id_user = {id_user}")
        fetch_one = self.cursor.fetchone()
        if fetch_one is None:
            return False
        return bool(fetch_one)


    def update_ban_list(self, _method, _id_user, _info_ban):
        self.new_cursor_connect()
        task = []

        if _method == 'unban':
            task.append(self.cursor.execute(f"DELETE FROM ban_list WHERE id_user = {_id_user}"))

        if _method == 'ban':
            task.append(self.cursor.execute(f"INSERT INTO ban_list (id_user, info_ban) VALUES ({_id_user}, '{_info_ban}')"))

        self.with_append(task)


    def give_ban_info_user(self, id_user):
        self.new_cursor_connect()
        self.cursor.execute(f"SELECT id_user, info_ban FROM ban_list WHERE id_user = {id_user}")
        fetch_one = self.cursor.fetchone()
        return fetch_one
    

    def give_all_from_table_method(self, method):
        self.new_cursor_connect()
        self.cursor.execute(f'SELECT * FROM {method}')
        fetch_all = self.cursor.fetchall()
        return fetch_all

    
    def edit_all_procent(self, _procent):
        self.new_cursor_connect()
        task = self.cursor.execute(f'UPDATE users SET procent = {_procent}')
        self.with_append(task)


    def give_all_admin_list(self):
        self.new_cursor_connect()
        self.cursor.execute("SELECT * FROM admins")
        fetch_all = self.cursor.fetchall()
        return fetch_all
    

    def delete_admins(self, _id_admin):
        self.new_cursor_connect()
        task = self.cursor.execute(f"DELETE FROM admins WHERE id_admin = {_id_admin}")
        self.with_append(task)
    

    def add_new_admin(self, _id_admin, _full_name_admin, _karma):
        self.new_cursor_connect()
        task = self.cursor.execute(f"INSERT INTO admins (id_admin, full_name, karma) VALUES ({_id_admin}, '{_full_name_admin}', {_karma})")
        self.with_append(task)


    def update_captcha_in_manager_bot(self, capthca_id):
        self.new_cursor_connect()
        task = self.cursor.execute(f"UPDATE manager_bot SET captcha_users = {capthca_id}")
        self.with_append(task)


    def give_id_ref_users(self, _id_user):
        self.new_cursor_connect()
        get_is_ref_user = self.cursor.execute(f"SELECT id_user FROM ref_system WHERE id_user = {_id_user}")

        if get_is_ref_user is None:
            return True
        
        return False
    

    def add_ref_system(self, id_user, id_ref):
        self.new_cursor_connect()
        task = self.cursor.execute(f"INSERT INTO ref_system (id_user, id_ref) VALUES ({id_user}, {id_ref})")
        self.with_append(task)


    def add_bonus_ref(self, id_ref, _old_balance_rub, _old_procent, _new_balance_rub, _new_procent):
        self.new_cursor_connect()
        task = []

        if _new_balance_rub != 0.0:
            task.append(self.cursor.execute(f"UPDATE users SET balance_rub = {_old_balance_rub + int(_new_balance_rub)} WHERE id_user = {id_ref}"))
        
        if _new_procent != 0.0:
            task.append(self.cursor.execute(f"UPDATE users SET procent = {_old_procent + _new_procent} WHERE id_user = {id_ref}"))

        self.with_append(task)

    
    def give_count_all_not_ref_users(self):
        self.new_cursor_connect()
        self.cursor.execute("SELECT count(id_user) FROM ref_system WHERE id_ref = 0")
        fetch_all = self.cursor.fetchall()
        return fetch_all
    
    def give_count_all_ref_users(self):
        self.new_cursor_connect()
        self.cursor.execute("SELECT count(id_user) FROM ref_system WHERE id_ref != 0")
        fetch_all = self.cursor.fetchall()
        return fetch_all
    
    def give_count_ref_users_profile(self, id_user):
        self.new_cursor_connect()
        self.cursor.execute(f"SELECT count(id_user) FROM ref_system WHERE id_ref = {id_user}")
        fetch_all = self.cursor.fetchall()
        return fetch_all

    def give_user_ref_id(self, id_user):
        self.new_cursor_connect()
        self.cursor.execute(f"SELECT id_ref FROM ref_system WHERE id_user = {id_user}")
        fetch_one = self.cursor.fetchone()
        return fetch_one

    def unlock_all_users(self):
        self.new_cursor_connect()
        task = self.cursor.execute("DELETE FROM ban_list")
        self.with_append(task)

    def give_is_not_None_ban_list(self):
        self.new_cursor_connect()
        self.cursor.execute("SELECT * FROM ban_list")
        fech_all = self.cursor.fetchall()
        return fech_all
    
    def select_users_not_admins(self, id_admin):
        self.new_cursor_connect()

        self.cursor.execute(f"SELECT id_user FROM users WHERE id_user != {id_admin}")
        fetch_all = self.cursor.fetchall()
        return fetch_all
    

    def give_karma_admin(self, _id_admin):
        self.new_cursor_connect()
        self.cursor.execute(f"SELECT karma FROM admins WHERE id_admin = {_id_admin}")
        fetch_one = self.cursor.fetchone()
        return fetch_one
    
    def update_karma_admin(self, _id_admin, count_karma, old_count_karma):
        self.new_cursor_connect()
        task = self.cursor.execute(f"UPDATE admins SET karma = {old_count_karma + count_karma} WHERE id_admin = {_id_admin}")
        self.with_append(task)
    