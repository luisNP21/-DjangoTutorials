from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView, ListView
from django.views import View
from django.http import HttpResponseRedirect
from django import forms
from django.shortcuts import render, redirect
from django.urls import reverse
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
        viewData = {}
        viewData["title"] = "Products - Online Store"
        viewData["subtitle"] = "List of products"
        viewData["products"] = Product.objects.all()

        return render(request, self.template_name, viewData)


class ProductShowView(View):
    template_name = 'products/show.html'

    def get(self, request, id):
        try:
            product_id = int(id)
            if product_id < 1:
                raise ValueError("Product id must be 1 or greater")

            product = get_object_or_404(Product, pk=product_id)

        except (ValueError, Product.DoesNotExist):
            return HttpResponseRedirect(reverse('home'))

        viewData = {}
        viewData["title"] = f"{product.name} - Online Store"
        viewData["subtitle"] = f"{product.name} - Product information"
        viewData["product"] = product

        return render(request, self.template_name, viewData)



class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'price', 'description']
    
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
            form.save()

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



class ProductListView(ListView):
    model = Product
    template_name = 'products/product_list.html'
    context_object_name = 'products'  # Usarás "products" en la plantilla

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Products - Online Store'
        context['subtitle'] = 'List of products'
        return context


