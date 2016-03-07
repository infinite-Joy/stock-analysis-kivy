import json
import time
import multiprocessing

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.listview import ListItemButton
from kivy.properties import ObjectProperty
from kivy.network.urlrequest import UrlRequest
from kivy.factory import Factory

from get_stock_data import Populate
from get_stock_data import companies_to_investigate

class LocationButton(ListItemButton):
    pass

class WeatherRoot(BoxLayout):
    def show_current_weather(self, location):
        from kivy.uix.label import Label
        self.clear_widgets()
        current_weather = Factory.CurrentWeather()
        current_weather.location = location
        self.add_widget(current_weather)

    def show_add_location_form(self):
        self.clear_widgets()
        self.add_widget(AddLocationForm())

"""def companies_to_investigate():
    return ["NTPC", "Amtek-Auto"]"""
    
class AddLocationForm(BoxLayout):
    search_input = ObjectProperty()

    def search_location(self):
        stock_companies_to_investigate = companies_to_investigate()
        jobs = []
        pool = multiprocessing.Pool(processes=5)
        p = Populate()
        for stock_company in stock_companies_to_investigate:
            #pool.apply_async(company_page_analysis, args=(stock_company,))
            #pool.apply_async(p.company_page_analysis, args=(stock_company,))
            p.company_page_analysis(stock_company)
            """
        self.search_results.item_strings = p.companies_investigated_n_found_good
        #self.search_results.adapter.data.clear() # only in python 3
        del self.search_results.adapter.data[:] # for python 2
        self.search_results.adapter.data.extend(p.companies_investigated_n_found_good)
        self.search_results._trigger_reset_populate()"""
        pool.close()
        pool.join()
        #cities = companies_to_investigate()
        
        self.search_results.item_strings = p.companies_investigated_n_found_good
        del self.search_results.adapter.data[:] # for python 2
        self.search_results.adapter.data.extend(p.companies_investigated_n_found_good)
        self.search_results._trigger_reset_populate()
        
        
    def found_location(self, request, data):
        self.search_results.item_strings = cities
        #self.search_results.adapter.data.clear() # only in python 3
        del self.search_results.adapter.data[:] # for python 2
        self.search_results.adapter.data.extend(cities)
        self.search_results._trigger_reset_populate()

class WeatherApp(App):
    pass
    
if __name__ == '__main__':
    WeatherApp().run()