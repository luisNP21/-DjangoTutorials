from django.shortcuts import render
from django.views.generic import TemplateView
from django.views import View
from django.http import HttpResponseRedirect
from django import forms
from django.shortcuts import render, redirect
from .models import Product





class HomePageView(TemplateView):
    template_name = 'pages/home.html'
    def get(self, request):
        viewData = {
            "title": "Home - Online Store",
            "subtitle": "Welcome to the store"
        }
        return render(request, self.template_name, viewData)


class AboutPageView(TemplateView):
    template_name = 'pages/about.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            "title": "About us - Online Store",
            "subtitle": "About us",
            "description": "This is an about page ...",
            "author": "Developed by: Your Name",
        })
        return context


class ContactPageView(TemplateView):
    template_name = 'pages/contact.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            "title": "Contact - Online Store",
            "subtitle": "Contact Us",
        })
        return context

class StaticProduct:
    products = [
        {"id": "1", "name": "TV", "description": "Best TV", "price": 999.99},
        {"id": "2", "name": "iPhone", "description": "Best iPhone", "price": 1299.50},
        {"id": "3", "name": "Chromecast", "description": "Best Chromecast", "price": 49.90},
        {"id": "4", "name": "Glasses", "description": "Best Glasses", "price": 120.00},
    ]


class ProductIndexView(View):
    template_name = 'products/index.html'

    def get(self, request):
        viewData = {
            "title": "Products - Online Store",
            "subtitle": "List of products",
            "products": Product.objects.all()
        }
        return render(request, self.template_name, viewData)

class ProductShowView(View):
    template_name = 'products/show.html'

    def get(self, request, id):
        try:
            product = Product.objects.get(id=id)
        except Product.DoesNotExist:
            return HttpResponseRedirect("/")  # redirige a home si el id es inválido

        viewData = {
            "title": f"{product.name} - Online Store",
            "subtitle": f"{product.name} - Product information",
            "product": product
        }
        return render(request, self.template_name, viewData)


class ProductForm(forms.Form):
    name = forms.CharField(required=True)
    price = forms.FloatField(required=True)
    
    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price is not None and price <= 0:
            raise forms.ValidationError("El precio debe ser mayor que cero.")
        return price

class ProductCreateView(View):
    template_name = 'products/create.html'

    def get(self, request):
        form = ProductForm()
        viewData = {
            "title": "Create product",
            "form": form
        }
        return render(request, self.template_name, viewData)

    def post(self, request):
        form = ProductForm(request.POST)
        if form.is_valid():
            # Crear y guardar el producto en la base de datos
            product = Product(
                name=form.cleaned_data['name'],
                price=form.cleaned_data['price']
            )
            product.save()
            return redirect("product_created")  # Redirige a la página de confirmación
        else:
            viewData = {
                "title": "Create product",
                "form": form
            }
            return render(request, self.template_name, viewData)


class ProductCreatedView(TemplateView):
    template_name = 'products/created.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            "title": "Producto Creado - Online Store",
            "subtitle": "Producto Creado Exitosamente",
        })
        return context


