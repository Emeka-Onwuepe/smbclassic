from xhtml2pdf import pisa
import win32api
import os 

data = {'branch_address':'Okeke Str',
        'branch phone':'08132180216',
        'purchase_id': '#3235254636454',
        'c_name':'Emeka Onwuepe',
        'c_phone':"08068263707",
        'c_email':'pascalemy2019@gmail.com',
        'c_address': 'Onwuepe compound',
        'c_payment': 'Cash',
        'items':[
                {'name':["First Turkish Suit","pdpdp - sksks - sskks - sjsjssj - sjsjs - ssjj - ksksk"],
                 'price':10000,'qty':1,'total':10000
                  },
                 {'name':["First Turkish Suit","pdpdp - sksks - sskks - sjsjssj - sjsjs - ssjj - ksksk"],
                 'price':10000,'qty':1,'total':10000
                  }, 
                 {'name':["First Turkish Suit","pdpdp - sksks - sskks - sjsjssj - sjsjs - ssjj - ksksk"],
                 'price':10000,'qty':1,'total':10000
                  },
                   {'name':["First Turkish Suit","pdpdp - sksks - sskks - sjsjssj - sjsjs - ssjj - ksksk"],
                 'price':10000,'qty':1,'total':10000
                  },
                 ]
        }

def create_receipt(data = data):
    store_details = f'''
    <div class="store_detail">
                 <table>
                 <tr>
                 <td>
                  <img src="./logo.png" alt=""
            srcset=""width='100px' height="auto">
                 </td>
                  <tr>
                 <td>
                 SMBCLASSIC BOUTIQUE
                 </td>
                 </tr>
                  <tr>
                 <td>
                 {data["branch_address"]}
                 </td>
                 </tr>
                  <tr>
                 <td>
                 {data["branch phone"]}</
                 </td>
                 </tr>
                
                 </table>  
        </div>
            '''
    items = ''
    index = 1
    for item in data['items']:
        proto = f'''<tr>
                        <td>{index}</td>
                        <td>{item['name'][0]}<br/>
                        <span class='info'>{item['name'][1]}<span>
                        </td>
                        <td>{item['price']}</td>
                        <td>{item['qty']}</td>
                        <td>{item['total']}</td>
                    </tr>
                '''
        items += proto
        index+=1
        
    page = f'''
            <!DOCTYPE html>
    <html lang="en">
    <head>
    <meta charset="UTF-8">
    <title>Invoice</title>
    <style>
        
        .center{{margin-bottom: 5px;}}
        .remove_margin{{margin-bottom: 0px;}}

        *{{padding: 0;
          margin: 0;
          font-size: 13px;
          font-family: 'PT Sans', sans-serif;
            }}
        .items td{{
            
            text-align: center;
            padding:2px
        }}
        .store_detail td{{text-align:center;width:280px}}
        
        .info{{font-size:10px}}
      .thanks{{
            font-size: 11px;
            
        }}
        .wrapper{{width: 300px;
                 padding: 10px;
                margin: auto;
                box-sizing: border-box;}}
       
        .top{{margin-top: 10px;}}
        .key{{width:105px}}
        .value{{width:170px}}
        

    </style>
    </head>
    <body>
    <div class="wrapper">
        <!-- <h1 class="center ">Sales Receipt</h1> -->
        {store_details}
        <p class="top">Purchase ID: <strong>{data["purchase_id"]}</strong></p>

        <div class="top">
            <table>
                <tr>
                    <td class='key'>Name:</td>
                    <td class='value'>{data["c_name"]}</td>
                </tr>
                <tr>
                    <td class='key'>Phone:</td>
                    <td class='value'>{data['c_phone']}</td>
                </tr>
                <tr>
                    <td class='key'>Email:</td>
                    <td class='value'>{data["c_email"]}</td>
                </tr>
                <tr>
                    <td class='key'>Address:</td>
                    <td class='value'>{data["c_address"]}</td>
                </tr>
                <tr>
                    <td class='key'>Payment Method:</td>
                    <td class='value'>{data["c_payment"]}</td>
                </tr>
            </table>
        </div>
        <div class="top items">
            <table class="top">
                <thead>
                    <tr>
                        <th style="width: 10px;">SN</th>
                        <th style="width: 130px;">Item</th>
                        <th style="width: 60px;">Price</th>
                        <th style="width: 20px;">Qty</th>
                        <th style="width: 60px;">Total</th>
                    </tr>
                </thead>
                <tbody>
                    {items}
                </tbody>
                <tfoot class='tfoot'>
                 <tr>
                 <td colspan=2 ><strong>Grand Total</strong></td>
                 <td colspan=3><strong>2000000</strong></td>
                 </tr>
                </tfoot>
            </table>
            </div>
            <p class='top thanks'>Thanks for your patronage, We hope to seen again soon.</p>
        </div>
    </body>
    </html>
        '''
    page = page.replace('\n','')
    page = page.strip()
    
    name = f"{data['purchase_id']}.pdf"
    path = os.path.abspath(f'./receipts/pdfs/{name}')
    
    with open(path,'w+b') as outfile:
        pisa.CreatePDF(page,dest=outfile) 
    
    # win32api.ShellExecute(0,'print',path,None,'.',0)
    
    # return page
# with open('reciept.html','w') as outfile:
#     outfile.write(page)