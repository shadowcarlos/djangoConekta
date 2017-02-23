from django.shortcuts import render, redirect, render_to_response, get_object_or_404
import conekta
from django.http import HttpResponse
from .models import PreciosCertificados, Iva, VentaCertificados, conektaComision
from django.contrib import messages
from django.core.mail import send_mail
from zeep import Client
import xmltodict
from decimal import *
import json

def cobrar2(request):
    conekta.api_key = 'key_HzXsr9oQQpqXd6z7AsrYsA'
    conekta.locale = 'es'
    try:
        order = conekta.Order.create({
      "line_items": [
          {
              "name": "Box of Cohiba S1s",
              "description": "Imported From Mex.",
              "unit_price": 20000,
              "quantity": 1,
              "sku": "cohb_s1",
              "category": "food",
              "type" : "physical",
              "tags" : ["food", "mexican food"]
          }
      ],
      "shipping_lines":[
        {
          "amount": 0,
          "tracking_number": "TRACK123",
          "carrier": "USPS",
          "method": "Train",
          "metadata": {
             "random_key": "random_value"
          }
        }],
      "customer_info":{   
          "name": "John Constantine",
          "phone": "+525533445566",
          "email": "john@meh.com",
          "corporate": False,
          "vertical_info": {}
        },
      "shipping_contact":{
          "phone" : "5544332211",
          "receiver": "Marvin Fuller",
          "between_streets": "Ackerman Crescent",
          "address": {
              "street1": "250 Alexis St",
              "state": "Alberta",
              "country": "MX",
              "postal_code": "23455",
              "metadata":{ "soft_validations": True}
          }
      },
      "fiscal_entity":{
        "tax_id": "AMGH851205MN1",
        "name": "Nike SA de CV",
        "address": {
            "street1": "250 Alexis St",
            "internal_number": "19",
            "external_number": "91",
            "city": "Red Deer",
            "state": "Alberta",
            "country": "CA",
            "postal_code": "33242"
        }
      },
      "charges": [{
        "payment_method":{
          "type": "card",
          "token_id": "tok_test_visa_4242"
        },
        "amount": 20000
      }],
      "currency" : "mxn",
      "metadata" : {"test" : "extra info"}
    })

        pass
    except conekta.ConektaError as e:
        print (e.message) 
  #El pago no pudo ser procesado

#You can also get the attributes from the conekta response class:
    print (order.id)
    return render(request, 'index.html')

    
def venta(request):
    objprecios = PreciosCertificados.objects.latest('id')
    
    objiva = Iva.objects.latest('id')
    instance = VentaCertificados()
    print(objiva.precioiva)
    objComision = conektaComision.objects.latest('id')


    server = Client("http://www.banxico.org.mx/DgieWSWeb/DgieWS?WSDL")
    results = server.service.tiposDeCambioBanxico()
    results = xmltodict.parse(results)
    tipo_cambio = 0
    for serie in results['CompactData']['bm:DataSet']['bm:Series']:
        if serie['@BANXICO_UNIT_TYPE'] == 'PesoxDoll':
            tipo_cambio = serie['bm:Obs']['@OBS_VALUE']
            break
    tipo_cambio = float(tipo_cambio)
    print(tipo_cambio)
    #En Pesos
    n_precio =  round(float(objprecios.preciocertificado) * tipo_cambio, 2)
    print(float(objprecios.preciocertificado))
    print(n_precio)
    return render(request, 'venta.html', {"instances": instance, "preciocert": n_precio, "iva": objiva.precioiva, "tipocambio": tipo_cambio, "objComision": objComision})

def cobrar(request):
    if request.method == 'POST':
        #Cachar valores
        token_id = request.POST.get('conektaTokenId', "")
        
        cantidad = int(request.POST.get('cantidad', 0))
        print(cantidad)
        objprecios = PreciosCertificados.objects.latest('id')
        objiva = Iva.objects.latest('id')
        objComision = conektaComision.objects.latest('id')
        server = Client("http://www.banxico.org.mx/DgieWSWeb/DgieWS?WSDL")
        results = server.service.tiposDeCambioBanxico()
        results = xmltodict.parse(results)
        tipo_cambio = 0
        for serie in results['CompactData']['bm:DataSet']['bm:Series']:
            if serie['@BANXICO_UNIT_TYPE'] == 'PesoxDoll':
                tipo_cambio = serie['bm:Obs']['@OBS_VALUE']
                break
        tipo_cambio = float(tipo_cambio)
        #En Pesos
        n_precio =  round(float(objprecios.preciocertificado) * tipo_cambio, 2)

        #OPERACIONES
        monto = n_precio * cantidad
        print(monto)
        get_iva = round(monto * (float(objiva.precioiva) / 100),2)
        print(get_iva)
        get_sub = round(monto + get_iva,2)
        print(get_sub)
        get_comi = get_sub + ((get_sub / (100 - float(objComision.comision))) * float(objComision.comision)) + 2.5
        comi = round(get_comi - get_sub,2)
        print(comi)
        get_total = round(get_sub + comi,2)
        print(get_total)

        #DAtos
        nombre = request.POST.get('asociacion', "")
        print(nombre)
        print(int(get_total * 100))
        #P_Unit = 140.84951999999998
        conekta.api_key = 'key_HzXsr9oQQpqXd6z7AsrYsA'
        conekta.locale = 'es'
        try:
            order = conekta.Order.create({
      "line_items": [
          {
              "name": "Certificados",
              "unit_price": int(get_total * 100),
              "quantity": 1
          }
      ],
      "customer_info":{   
          "name": nombre,
          "phone": "+525533445566",
          "email": "john@meh.com",
          "corporate": False,
          "vertical_info": {}
        },
      "charges": [{
        "payment_method":{
          "type": "card",
          "token_id": token_id
        },
        "amount": int(get_total * 100),
      }],
      "currency" : "mxn",
      "metadata" : {"test" : "extra info"}
    })
    
        except conekta.ConektaError as e:
            error = True 
            return render(request, 'venta.html', {"preciocert": n_precio, "iva": objiva.precioiva, "tipocambio": tipo_cambio, "objComision": objComision, "error": error}) 

    #Crear objeto

    objVenta = VentaCertificados.objects.create()
    objVenta.asociacion = nombre
    objVenta.preciocertificado = objiva.precioiva
    objVenta.cantidad = cantidad
    objVenta.tipocambio = tipo_cambio
    objVenta.ivaporcentaje = float(objiva.precioiva)
    objVenta.monto = monto
    objVenta.montoiva = get_iva
    objVenta.total = get_total
    objVenta.save()
    return render(request, 'index.html') 



def tarjeta(request):
    if request.method == 'POST':
       print("Holi") 
    return render(request, 'tarejeta.html')