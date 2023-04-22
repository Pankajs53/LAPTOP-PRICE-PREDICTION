import mysql.connector
import pandas as pd

class DB:
    def __init__(self):
        # connect with database
        try:
            self.conn=mysql.connector.connect(
                host='127.0.0.1',
                user='root',
                password='1234',
                database='LP'
            )
            self.mycursor=self.conn.cursor()
            print("Connection Established")
        except:
            print("connection error/DB Down")


    def pricevar_withcompany(self):
        company=[]
        avg_price=[]
        self.mycursor.execute("""
        select Company,round(avg(Price),0) as "avg_price" from laptop group by Company order by avg_price desc
        """)

        data=self.mycursor.fetchall()
        for item in data:
            company.append(item[0])
            avg_price.append(item[1])

        return company,avg_price

    def avg_price_with_combo(self):
        Company1 = []
        TypeName1 = []

        self.mycursor.execute("""
                select distinct(TypeName) from laptop
                """)

        data = self.mycursor.fetchall()
        for item in data:
            TypeName1.append(item[0])

        self.mycursor.execute("""
                        select distinct(Company) from laptop
                        """)

        data1 = self.mycursor.fetchall()
        for item in data1:
            Company1.append(item[0])

        return (Company1, TypeName1)

    def fetch_avg_price(self,Company1,TypeName1):
        self.mycursor.execute("""
        select round(avg(Price),0) from laptop where Company='{}' and TypeName='{}'
        """.format(Company1,TypeName1))

        data2=self.mycursor.fetchone()

        return data2

    def scatter_plot(self):
        ram=[]
        price=[]
        self.mycursor.execute("""
                        select ram, Price from laptop
                        """)

        data=self.mycursor.fetchall()
        for item in data:
            ram.append(item[0])
            price.append(item[1])

        return (ram,price)


    def touch_screen(self):
        TouchScreen = []
        price = []
        self.mycursor.execute("""
                                select TouchScreen,round(avg(Price),2) from laptop group by TouchScreen
                                """)

        data = self.mycursor.fetchall()
        for item in data:
            TouchScreen.append(item[0])
            price.append(item[1])

        return (TouchScreen,price)

    #;
    def operating_system(self):
        os = []
        price = []
        self.mycursor.execute("""
                                select os,round(avg(Price),2) from laptop group by os
                                """)

        data = self.mycursor.fetchall()
        for item in data:
            os.append(item[0])
            price.append(item[1])

        return (os,price)

    def line_plot(self):
          # fetch the data from the database
          ppi=[]
          HDD=[]
          SSD=[]
          price=[]
          Weight=[]
          self.mycursor.execute("""
                                    select ppi,HDD,SSD,Price,Weight from laptop 
                                    """)
          data = self.mycursor.fetchall()
          for item in data:
              ppi.append(item[0])
              HDD.append(item[1])
              SSD.append(item[2])
              price.append(item[3])
              Weight.append(item[4])

          return (ppi,HDD,SSD,price,Weight)

    def correlation(self):
        self.mycursor.execute("""
                                            select Ram,Weight,Price,Touchscreen,Ips,ppi,HDD,SSD from laptop 
                                            """)
        data = self.mycursor.fetchall()
        df = pd.DataFrame(data,
                          columns=['Ram', 'Weight', 'Price', 'Touchscreen', 'Ips', 'ppi', 'HDD', 'SSD'])


        return df

    # select ,Price from laptop;







