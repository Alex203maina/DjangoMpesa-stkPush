from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
import requests
from .credentials import MpesaAccessToken, MpesaPassword
# Create your views here.
def index(request):
    return render(request, 'index.html')

def pay(request):
    return render(request, 'pay.html')

def stk(request):
    if request.method == 'POST':
        phone = request.POST.get('phone')
        amount = request.POST.get('amount')
        access_token = MpesaAccessToken.mpesa_access_token
        api_url = 'https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest'
        headers = {'Authorization': "Bearer %s" % access_token}
        request = {   
            "BusinessShortCode": MpesaPassword.business_short_code,    
            "Password": MpesaPassword.decode_password,    
            "Timestamp":MpesaPassword.lipa_time,    
            "TransactionType": "CustomerPayBillOnline",    
            "Amount": amount,    
            "PartyA":phone,    
            "PartyB":MpesaPassword.business_short_code,    
            "PhoneNumber":phone,    
            "CallBackURL": "https://sandbox.safaricom.co.ke/mpesa",    
            "AccountReference":"Test",    
            "TransactionDesc":"Test"
            }
        try:
            # Send request to Mpesa API
            response = requests.post(api_url, json=request, headers=headers)
            response_data = response.json()

            # Check if the response is successful
            if response.status_code == 200:
                return JsonResponse({'status': 'success', 'message': 'Payment request sent successfully', 'data': response_data})
            else:
                return JsonResponse({'status': 'error', 'message': 'Failed to initiate payment', 'data': response_data}, status=400)
        except requests.exceptions.RequestException as e:
            return JsonResponse({'status': 'error', 'message': f'Request failed: {str(e)}'}, status=500)

    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=405)