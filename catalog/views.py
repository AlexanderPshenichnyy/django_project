from django.contrib.auth.decorators import permission_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms import inlineformset_factory
from django.http import Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import PermissionRequiredMixin
from catalog.models import Category, Product, Version
from catalog.forms import ProductForm, VersionForm


class CategoryListView(ListView):
    model = Category
    template_name = 'catalog/homepage.html'


class ProductCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    permission_required = 'catalog.add_product'
    success_url = reverse_lazy('catalog:products')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Создание товара'
        VersionFormset = inlineformset_factory(Product, Version, form=VersionForm, extra=1)
        if self.request.method == 'POST':
            context['formset'] = VersionFormset(self.request.POST)
        else:
            context['formset'] = VersionFormset()
        return context

    def form_valid(self, form):

        formset = self.get_context_data()['formset']
        self.object = form.save()
        self.object.owner = self.request.user
        form.save()
        if formset.is_valid():
            formset.instance = self.object
            formset.save()
        return super().form_valid(form)


class ProductUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Product
    form_class = ProductForm
    permission_required = 'catalog.change_product'

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.object.owner != self.request.user:
            raise Http404
        return self.object


def get_success_url(self):
    return reverse('catalog:product', kwargs={'pk': self.object.pk})


def get_context_data(self, **kwargs):
    context_data = super().get_context_data(**kwargs)
    VersionFormset = inlineformset_factory(Product, Version, form=VersionForm, extra=1)
    if self.request.method == 'POST':
        context_data['formset'] = VersionFormset(self.request.POST, instance=self.object)
    else:
        context_data['formset'] = VersionFormset(instance=self.object)
    return context_data


def form_valid(self, form):
    formset = self.get_context_data()['formset']
    self.object = form.save()
    if formset.is_valid():
        formset.instance = self.object
        formset.save()
    return super().form_valid(form)


class ProductDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Product
    success_url = reverse_lazy('catalog:products')
    permission_required = 'catalog.delete_product'


class ProductListView(ListView):
    model = Product
    template_name = 'catalog/products.html'


class ProductDetailView(DetailView):
    model = Product
    template_name = 'catalog/product.html'

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['version'] = Version.objects.filter(product=self.kwargs['pk'], sign_is_active=True)
        print(context_data)
        return context_data


def contacts(request):
    return render(request, 'catalog/contacts.html', {'title': 'Контакты'})
