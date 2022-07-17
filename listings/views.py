from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Q

from .models import Listing
from listings.choices import (price_choices,
                              bedroom_choices,
                              state_choices)



def index(request):
    listings = Listing.objects.order_by('-list_date').filter(is_published=True)
    pagination = Paginator(listings, 9)
    page = request.GET.get('page')
    paged_listings = pagination.get_page(page)
    context = {
        'listings': paged_listings
    }
    return render(request, 'listings/listings.html', context)


def listing(request, listing_id):
    listing = get_object_or_404(Listing, pk=listing_id)
    context = { 'listing': listing}
    return render(request, 'listings/listing.html', context)


def search(request):
    good = True
    
    listings_qs = Listing.objects.none()
    # getting cities where at-least one listing presents.
    active_cities = Listing.objects.order_by().values_list('city').distinct()
    active_cities = [x[0] for x in active_cities]
    # # getting search result from 'keywords'
    # if 'keywords' in request.GET:
    #     keywords = request.GET.get('keywords')
    #     listings_qs = Listing.objects.filter(description__icontains=keywords)
    # # getting search result from 'city'
    # if 'city' in request.GET:
    #     print(request.GET.get("city") == "")
    #     city = request.GET.get('city')
    #     listings_qs = Listing.objects.filter(city__iexact=city)
    # # getting search result from 'state'
    # if 'state' in request.GET:
    #     state = request.GET.get('state')
    #     listings_qs = Listing.objects.filter(state__iexact=state)
    # # getting search result from 'bedrooms'
    # if 'bedrooms' in request.GET:
    #     bedrooms = request.GET.get('bedrooms')
    #     listings_qs = Listing.objects.filter(bedrooms__lte=bedrooms)
    # # getting search result from 'price'
    # if 'price' in request.GET:
    #     price = request.GET.get('price')
    #     listings_qs = Listing.objects.filter(price__lte=price)
        
    if good:
        keywords = request.GET.get('keywords') or str('')
        city = request.GET.get('city') or str('')
        state = request.GET.get('state') or str('')
        bedrooms = request.GET.get('bedrooms') or int(1)
        price = request.GET.get('price') or int(1000000)
        
        print(keywords)
        print(city)
        print(bedrooms)
        print(price)
        
        listings_qs = Listing.objects.filter(Q(description__icontains=keywords) | Q(city__iexact=city) | Q(state__iexact=state) | Q(bedrooms__lte=bedrooms), Q(price__lte=price))
        print(listings_qs)
        

        
        # mylist = dict(keywords=keywords, city=city, bedrooms=bedrooms, price=price)
        # new_list = {}
        # print(mylist)
        
        # for key, value in mylist.items():
        #     if value == "" or value is None:
        #         print("None")
        #     else:
        #         print(value)
        #         new_list[key] = value
                
        # print(new_list)
        
        # for k, v in new_list.items():
        #     query = 
        #     listings_qs = Listing.objects.filter()
        good = False
    
    context = {
        'price_choices': price_choices,
        'bedroom_choices': bedroom_choices,
        'state_choices': state_choices,
        'listings': listings_qs, 
        'active_cities': active_cities,
        'values': request.GET
    }
    return render(request, 'listings/search.html', context)
