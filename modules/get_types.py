import modules.Google as g
import smtplib, ssl
import pandas as pd

def fetch_type_resource_from_excel():#fetch fom s3
    spreadsheetId = "1w4r0KSdQKI9zXlink5CmJoiWArCIJPTdbZ8Bsp-XIGs"
    df_chain= g.fetch_excel(spreadsheetId, "description list", "A1:T")
    
    return df_chain

def email_alert(description):
    port = 465  # For SSL
    smtp_server = "smtp.gmail.com"
    sender_email = "donotreply.growth@gmail.com"  # Enter your address
    receiver_email = "jean.mellot@choco.com"  # Enter receiver address
    password = "Growth2021!"
    message = """Subject: New Google Description without Category!

    The following Google description : {} is not referenced, Please update the description ressource. Thank you !""".format(description)

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message)
        server.quit()
        print('message sent')
 
def get_type_and_category(description):
    ressource = fetch_type_resource_from_excel()
    new_buyer_type = ''
    new_buyer_type_category = ''
    
    for line in ressource.iterrows():
        if line[1]["Buyer Type Google"].strip() == description.strip():
            new_buyer_type = line[1]["New Buyer Type"]
            new_buyer_type_category = line[1]["New Buyer Type Category"]
    
    if new_buyer_type == '':
        email_alert(description)
        
    df = pd.DataFrame([(description,new_buyer_type,new_buyer_type_category)])
    df.columns = ['description','new_buyer_type','new_buyer_type_category']
    return(df)


if __name__ == "__main__":
    ressource = fetch_type_resource_from_excel()
    description = 'Dessert fp'
    a = get_type_and_category(description)