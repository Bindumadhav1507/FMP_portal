from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import HttpResponse,JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db import connection

# Create your views here.
def home(request):
    return render(request,'home.html')

def about(request):
    return render(request,'about.html')

def support_us(request):
    return render(request,'support_us.html')

def contact_us(request):
    return render(request,'contact_us.html')

@csrf_exempt
def getdata(request):
    if request.method == 'POST':
        asset_value = request.POST['Asset']
        option_value = request.POST['option']
        data = {
            'FI' : {
                    'Capula' : ['Repo','IRS','OIS','ILS','Bonds'],
                    'Pimco' : ['Repo','IRS','OIS','ILS','Bonds'],
                    'Invesco' : ['IRS', 'OIS', 'Bonds'],
                   },

            'EQ' :{
                    'Wellington' : ['Equities',"CFD'S"],
                    'Henderson' : ['Equities',"CFD'S"],
                  }
        }
          # Convert the list to a hashable type, such as a tuple or a string
        result = {'message': 'Success!', 'data': data.get(asset_value, {}).get(option_value, [])}

        return JsonResponse(result)
    return JsonResponse({'error': 'Invalid request method'})

def content(request, category, option_name):
    assets = category.upper()
    company_name = option_name.capitalize()

    page_content = {
        "FI" : {
                'Capula' : '''Capula Investment Management LLP is a British hedge fund, the fourth largest in Europe, with assets under management (AUM) of about  
$23 billion as of H2 2020. The firm manages absolute return, enhanced fixed income, macro and crisis alpha strategies.''',

                'Pimco' : '''PIMCO (officially Pacific Investment Management Company LLC) is an American investment management firm focusing on active fixed incomm
e management worldwide. PIMCO manages investments in many asset classes such as fixed income, equities, commodities, asset allocation, ETFs, hedge funds, and privv
ate equity. PIMCO is one of the largest investment managers, actively managing more than $2 trillion in assets for central banks, sovereign wealth funds, pension  
funds, corporations, foundations and endowments, and individual investors around the world. PIMCO’s headquarters are in Newport Beach, California; the firm has ovv
er 3,100 employees working in 22 offices throughout the Americas, Europe, and Asia.PIMCO and Allianz Global Investors manage around €2.5 trillion of third-party aa
ssets.''',

                
                'Invesco' : '''Invesco Ltd. is an American independent investment management company that is headquartered in Atlanta, Georgia, with additional brr
anch offices in 20 countries. Its common stock is a constituent of the S&P 500 and trades on the New York stock exchange.Invesco operates under the Invesco, Trimaa
rk, Invesco Perpetual, WL Ross & Co and Powershares brand names.''',

              },

        "EQ" : {
                'Wellington' : '''Wellington Management Company is a private, independent investment management firm with client assets under management totaling  
over US$1 trillion based in Boston, Massachusetts, United States.

                                  The firm serves as an investment advisor to over 2,200 institutions in over 60 countries, as of 30 June 2020. Its clients includd
e central banks and sovereign institutions, pension funds, endowments and foundations, family offices, fund sponsors, insurance companies, financial intermediariee
s, and wealth managers.''',

                'Henderson' : '''Henderson Group plc was a global investment management company with its principal place of business in the City of London. It merr
ged with Janus Capital Group in May 2017 to create Janus Henderson.
                                 The Company was established in 1934 to administer the estates of Alexander Henderson, 1st Baron Faringdon.In 1975, it started mann
aging pension funds. It was first listed on the London Stock Exchange in 1983.''',
              },
        }
    # Construct the SQL query
    query = f"SELECT fund_manager, funding, domicile, initial_trade, swaps_included, cleared, bilateral FROM FundManagersData WHERE fund_manager = '{company_name}' AND asset_class = '{assets}';"

    # Execute the query
    with connection.cursor() as cursor:
        cursor.execute(query)
        data = cursor.fetchall()

    # Check if any results were found
    data = data if data else {'result': None}

    # Retrieve distinct product types
    query = f"SELECT DISTINCT(product_type) FROM FundManagersData WHERE fund_manager = '{company_name}' AND asset_class = '{assets}';"
    with connection.cursor() as cursor:
        cursor.execute(query)
        products = cursor.fetchall() or "no products"

    context = {
        'data': data,
        'products': products,
        'img_path': f'images/{company_name}.png',
        'page_content' : page_content[assets][company_name],
    }

    return render(request, 'content.html', {'context': context})
