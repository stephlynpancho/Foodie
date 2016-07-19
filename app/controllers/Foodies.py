
from system.core.controller import *
access = "d40b90968cc0a0052dd0155deb54550f"

class Foodies(Controller):
    def __init__(self, action):
        super(Foodies, self).__init__(action)
        self.load_model('Foodie')
        self.load_model('Preference')

    def index(self):
        return self.load_view('index.html')

    def add_user(self):
    	user_info = {
        'first_name': request.form['first_name'], 
        'last_name': request.form['last_name'], 
        'email': request.form['email'], 
        'password': request.form['password'],
        'cpw': request.form['cpw']
    	}
    	add_status = self.models['Foodie'].add_users(user_info)
    	if add_status['status']== True:
    	   session['first_name'] = add_status['user']['first_name']
           session['id'] = add_status['user']['id']
           session['shopping_id'] = add_status['user']['shopping_list_id']
    	   return redirect('/preferences')
    	else:
    		for message in add_status['errors']:
    			flash(message)
    		return redirect('/')

    def log(self):
        return self.load_view("login.html")
        
    def login(self):
        login_data = { 
        'email': request.form['email'], 
        'password': request.form['password']
        }
        login= self.models['Foodie'].log_in(login_data)

        if login['status'] == True:
            session['first_name']= login['user_info']['first_name']
            session['id']= login['user_info']['id']
            session['shopping_id'] = login['user_info']['shopping_list_id']
            return redirect('/Foodies/content')
        else:
            for message in login['errors']:
                flash(message)
            return redirect('/Foodies/log') 

    def logout(self):
        session.pop("first_name")
        session.pop("id")
        flash("You have successfully logged out")
        return redirect('/Foodies/log')

    def content(self):
        prefs = self.models['Preference'].get_user_prefs(session['id'])
        print prefs
        if not prefs[0]['preference_id']:
            return redirect('/preferences')
        groceries = self.models['Foodie'].get_groceries(session['shopping_id'])
    
        return self.load_view('content.html', prefs=prefs, groceries=groceries)

    def get_recipes(self, key):
        key = key.replace(' ','%20')
        url = "http://food2fork.com/api/search?key="+access+"&q="+key
        recipes = requests.get(url).content
        return recipes

    def get_twtr(self, key):
        key = key.replace(' ','')
        twtr_string = ""
        twtr_dict = {
        'American' : "<a class=\"twitter-timeline\" href=\"https://twitter.com/hashtag/americanfood\" data-widget-id=\"715247134249848832\" width=\"300\" data-chrome=\"nofooter noborders\" data-tweet-limit=\"20\">#americanfood Tweets</a>",
        'Asian' : "<a class=\"twitter-timeline\" href=\"https://twitter.com/hashtag/asianfood\" data-widget-id=\"715242264616763392\" width=\"300\" data-chrome=\"nofooter noborders\" data-tweet-limit=\"20\">#asianfood Tweets</a>",
        'Brunch' : "<a class=\"twitter-timeline\" href=\"https://twitter.com/hashtag/sundaybrunch\" data-widget-id=\"715218114317651968\" width=\"300\" data-chrome=\"nofooter noborders\" data-tweet-limit=\"20\">#sundaybrunch Tweets</a>",
        'Coffee' : "<a class=\"twitter-timeline\" href=\"https://twitter.com/hashtag/coffee\" data-widget-id=\"715256715298516993\" width=\"300\" data-chrome=\"nofooter noborders\" data-tweet-limit=\"20\">#coffee Tweets</a>",
        'Dessert' : "<a class=\"twitter-timeline\" href=\"https://twitter.com/hashtag/dessert\" data-widget-id=\"715243048255369216\" width=\"300\" data-chrome=\"nofooter noborders\" data-tweet-limit=\"20\">#dessert Tweets</a>",
        'Healthy' : "<a class=\"twitter-timeline\" href=\"https://twitter.com/hashtag/healthyfood\" data-widget-id=\"715257155197100032\" width=\"300\" data-chrome=\"nofooter noborders\" data-tweet-limit=\"20\">#healthyfood Tweets</a>",
        'Italian' : "<a class=\"twitter-timeline\" href=\"https://twitter.com/hashtag/Italianfood\" data-widget-id=\"715257476849860608\" width=\"300\" data-chrome=\"nofooter noborders\" data-tweet-limit=\"20\">#Italianfood Tweets</a>",
        'Smoothies' : "<a class=\"twitter-timeline\" href=\"https://twitter.com/hashtag/smoothies\" data-widget-id=\"715246140023701504\" width=\"300\" data-chrome=\"nofooter noborders\" data-tweet-limit=\"20\">#juices Tweets</a>",
        'Mexican' : "<a class=\"twitter-timeline\" href=\"https://twitter.com/hashtag/latinfood\" data-widget-id=\"715246675619545088\" width=\"300\" data-chrome=\"nofooter noborders\" data-tweet-limit=\"20\">#latinfood Tweets</a>"

        }

        if key in twtr_dict.keys():
            twtr_string += twtr_dict[key]
        return twtr_string

    def show_recipe(self, key):
        url = "http://food2fork.com/api/get?key="+access+"&rId="+key
        recipe = requests.get(url).content
        return recipe

    def add_grocery(self):
        item = request.form['item']
        grocery_list = self.models['Foodie'].add_grocery(item, session['shopping_id'])
        return redirect('/Foodies/content')

    def remove_grocery(self):
        item = request.form['item']
        self.models['Foodie'].remove_grocery(item, session['shopping_id'])
        return redirect('/Foodies/content')

    def get_groceries(self):
        groceries = self.models['Foodie'].get_groceries(session['shopping_id'])
        return self.load_view('partials/grocery_list.html', groceries=groceries)



