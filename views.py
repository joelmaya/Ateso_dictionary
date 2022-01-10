from django.shortcuts import render,redirect
from django.views.generic import TemplateView, DetailView, ListView
from.models import item
from django.core.paginator import Paginator
import requests


# Create your views here.


def home(request):
	context={}
	return render(request, "dict/home.html", context)



class WordListView(ListView):
	model = item
	template_name = 'dict/home.html'
	context_object_name = "words"
	paginate_by = 4


class SearchView(TemplateView):
	template_name = 'dict/search.html'
	paginate_by = 10

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		kw = self.request.GET.get('keyword')

		if kw != "":
			results = item.objects.filter(word__icontains=kw)
			p = Paginator(results, 6)
			page_num = self.request.GET.get('page', 1)

			try:
				page = p.page(page_num)
			except EmptyPage:
				page = p.page(1) 
			context ={
			 'results': page
			} 

		else:
			print('please')
			
		
		return context


def detail(request, pk):
	Item = item.objects.get(pk=pk)
	recently_viewed_word = None

	if 'recently_viewed' in request.session:
		if pk in request.session['recently_viewed']:
			request.session['recently_viewed'].remove(pk)

		products = item.objects.filter(pk__in=request.session['recently_viewed'])
		recently_viewed_word = sorted(products,
			key=lambda x: request.session['recently_viewed'].index(x.id)
			)
		request.session['recently_viewed'].insert(0, pk)
		if len(request.session['recently_viewed']) > 5:
			request.session['recently_viewed'].pop()
	else:
		request.session['recently_viewed'] = [pk]
	request.session.modified = True

	context = {
		'Item':Item,
		'recently_viewed_word':recently_viewed_word
	}

	return render(request, 'dict/item_detail.html', context)

