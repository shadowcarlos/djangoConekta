from django.shortcuts import render, redirect, render_to_response
import conekta

def main(request):
    print("holi")
    return render(request, 'index.html')