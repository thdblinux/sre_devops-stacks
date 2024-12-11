# %%
import mysql.connector
import pandas as pd

def carga_categories(df_categories):
    cnx = mysql.connector.connect(user='root',password='12345',host='localhost',database='python' )  
    cursor = cnx.cursor() 
    #interage no df e realiza Carga dos dados para Banco 
    for i,df_categories_coluna in df_categories.iterrows():
        cursor.execute('''select category_id FROM python.categories 
                       where category_id = %s''',( df_categories_coluna['category_id'],))
        result=cursor.fetchone()   
        
        if not result :    
            #inserir dados 
            cursor.execute(
                '''
                insert into python.categories(
                category_id,
                category_name
                ) 
                values (%s,%s)  
                ''',(
                    df_categories_coluna['category_id'],
                    df_categories_coluna['category_name']
                )            
            ) 
    cnx.commit()
    cursor.close() 
    cnx.close() 

def carga_products(df_products):
    cnx = mysql.connector.connect(user='root',password='12345',host='localhost',database='python' )  
    cursor = cnx.cursor() 
    #interage no df e realiza Carga dos dados para Banco 
    for i,df_products_coluna in df_products.iterrows():
        cursor.execute('''SELECT product_id FROM python.products 
                       where product_id =  %s''',( df_products_coluna['product_id'],))
        result=cursor.fetchone()           
        if not result :    
            #inserir dados 
            cursor.execute(
                '''
                insert into python.products(
                product_id,
                product_name,
                brand_id,
                model_year,
                list_price,
                category_id
                ) 
                values (%s,%s,%s,%s,%s,%s)  
                ''',(
                    df_products_coluna['product_id'],
                    df_products_coluna['product_name'],
                    df_products_coluna['brand_id'],
                    df_products_coluna['model_year'],
                    df_products_coluna['list_price'],
                    df_products_coluna['category_id']
 

                    
                )            
            ) 
    cnx.commit()
    cursor.close() 
    cnx.close() 

def carga_stores(df_stores):
    cnx = mysql.connector.connect(user='root',password='12345',host='localhost',database='python' )  
    cursor = cnx.cursor() 
    #interage no df e realiza Carga dos dados para Banco 
    for i,df_stores_coluna in df_stores.iterrows():
        cursor.execute('''SELECT store_id  FROM python.stores 
                                where store_id = %s''',( df_stores_coluna['store_id'],))
        result=cursor.fetchone()           
        if not result :    
            #inserir dados 
            cursor.execute(
                '''
                insert into python.stores(
                store_id,
                store_name,
                phone,
                email,
                street,
                city,
                state,
                zip_code
                ) 
                values (%s,%s,%s,%s,%s,%s,%s,%s)  
                ''',(
                    df_stores_coluna['store_id'],
                    df_stores_coluna['store_name'],
                    df_stores_coluna['phone'],
                    df_stores_coluna['email'],
                    df_stores_coluna['street'],
                    df_stores_coluna['city'],
                    df_stores_coluna['state'],
                    df_stores_coluna['zip_code']
                    
                )            
            ) 
    cnx.commit()
    cursor.close() 
    cnx.close() 

def carga_customer(df_customers):
    cnx = mysql.connector.connect(user='root',password='12345',host='localhost',database='python' )  
    cursor = cnx.cursor() 
    #interage no df e realiza Carga dos dados para Banco 
    for i,df_customer_coluna in df_customers.iterrows():
        cursor.execute('''SELECT customer_id FROM python.customers 
                       where customer_id =  %s''',( df_customer_coluna['customer_id'],))
        result=cursor.fetchone()           
        if not result :    
            #inserir dados 
            cursor.execute(
                '''
                insert into python.customers(
                customer_id,
                first_name,
                last_name,
                phone,
                email,
                street,
                city,
                state,
                zip_code
                ) 
                values (%s,%s,%s,%s,%s,%s,%s,%s,%s)  
                ''',(
                    df_customer_coluna['customer_id'],
                    df_customer_coluna['first_name'],
                    df_customer_coluna['last_name'],
                    df_customer_coluna['phone'],
                    df_customer_coluna['email'],
                    df_customer_coluna['street'],
                    df_customer_coluna['city'],
                    df_customer_coluna['state'],
                    df_customer_coluna['zip_code']

                    
                )            
            ) 
    cnx.commit()
    cursor.close() 
    cnx.close() 

def carga_orders(df_orders):
    cnx = None
    cursor = None
    cnx = mysql.connector.connect(user='root',password='12345',host='localhost',database='python' )  
    cursor = cnx.cursor() 
    #interage no df e realiza Carga dos dados para Banco 
    for i,df_orders_coluna in df_orders.iterrows():
        cursor.execute('''SELECT order_id FROM python.orders 
                       where order_id =  %s''',( df_orders_coluna['order_id'],))
        result=cursor.fetchone()           
        if not result :    
            #inserir dados 
            cursor.execute(
                '''
                insert into python.orders(
                order_id,
                customer_id,
                store_id,
                order_status,
                order_date,
                required_date,
                shipped_date,
                staff_id
                ) 
                values (%s,%s,%s,%s,%s,%s,%s,%s)  
                ''',(
                    df_orders_coluna['order_id'],
                    df_orders_coluna['customer_id'],
                    df_orders_coluna['store_id'],
                    df_orders_coluna['order_status'],
                    df_orders_coluna['order_date'],
                    df_orders_coluna['required_date'],
                    df_orders_coluna['shipped_date'],
                    df_orders_coluna['staff_id']

                    
                )            
            ) 
    cnx.commit()
    cursor.close() 
    cnx.close() 

def carga_order_items(df_order_items):
    cnx = mysql.connector.connect(user='root',password='12345',host='localhost',database='python' )  
    cursor = cnx.cursor() 
    #interage no df e realiza Carga dos dados para Banco 
    for i,df_order_items_coluna in df_order_items.iterrows():
        cursor.execute('''select distinct order_id from python.order_items 
                       where order_id=  %s''',( df_order_items_coluna['order_id'],))
        result=cursor.fetchone()           
        if not result :    
            #inserir dados 
            cursor.execute(
                '''
                insert into python.order_items(
                item_id,
                product_id,
                order_id,
                quantity,
                list_price,
                discount
                ) 
                values (%s,%s,%s,%s,%s,%s)  
                ''',(
                    df_order_items_coluna['item_id'],
                    df_order_items_coluna['product_id'],
                    df_order_items_coluna['order_id'],
                    df_order_items_coluna['quantity'],
                    df_order_items_coluna['list_price'],
                    df_order_items_coluna['discount']
 

                    
                ) 
                           
            ) 
            
    cnx.commit()
    cursor.close() 
    cnx.close()
    

df_categories = pd.read_csv(r'C:\Users\edmil\OneDrive\Documentos\Cursos\Python - SGBDS - Arquivos\Origem de dados\Bikes\categories.csv',sep=',').fillna('')
df_products = pd.read_csv(r"C:\Users\edmil\OneDrive\Documentos\Cursos\Python - SGBDS - Arquivos\Origem de dados\Bikes\products.csv",sep=',').fillna('')
df_stores = pd.read_csv(r'C:\Users\edmil\OneDrive\Documentos\Cursos\Python - SGBDS - Arquivos\Origem de dados\Bikes\stores.csv',sep=',').fillna('')
df_customers= pd.read_csv(r"C:\Users\edmil\OneDrive\Documentos\Cursos\Python - SGBDS - Arquivos\Origem de dados\Bikes\customers.csv",sep=',').fillna('')
#df_customers=df_customers.fillna('') # Transformação de dados (eliminando Nulos)
df_order_items = pd.read_csv(r"C:\Users\edmil\OneDrive\Documentos\Cursos\Python - SGBDS - Arquivos\Origem de dados\Bikes\order_items.csv",sep=',').fillna('')

df_orders = pd.read_csv(r"C:\Users\edmil\OneDrive\Documentos\Cursos\Python - SGBDS - Arquivos\Origem de dados\Bikes\orders.csv",sep=',').fillna('')
df_orders['order_date'] = pd.to_datetime(df_orders['order_date'])
df_orders['required_date'] = pd.to_datetime(df_orders['required_date'])
df_orders['shipped_date'] = pd.to_datetime(df_orders['shipped_date'])



#Executa carga de Dados
carga_categories(df_categories)
carga_products(df_products)
carga_stores(df_stores)
carga_customer(df_customers)
carga_orders(df_orders)
carga_order_items(df_order_items)


