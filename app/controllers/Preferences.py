from system.core.controller import *

class Preferences(Controller):
    def __init__(self, action):
        super(Preferences, self).__init__(action)
        self.load_model('Preference')
        # self.load_model('Foodie')

    def preferences(self):
        return self.load_view('preferences.html')

    def add_prefs(self):
        preferences = {
        'Asian': request.form['Asian'],
        'Dessert': request.form['Dessert'],
        'Juices': request.form['Juices'],
        'Mexican': request.form['Mexican'],
        'New American': request.form['New American'],
        'Sunday Brunch': request.form['Sunday Brunch'],
        'Coffee': request.form['Coffee'],
        'Italian': request.form['Italian'],
        'Healthy': request.form['Healthy'],
        }
        count = 0
        for x in preferences.keys():
            if not preferences[x]:
                count += 1
        if count == len(preferences.keys()):
            flash("Please choose at least one preference")
            return redirect('/preferences')
        else:
            prefs = {}
            for keys in preferences.keys():
                if preferences[keys]:
                    prefs[keys] = preferences[keys]
            self.models['Preference'].add_preferences(prefs, session["id"])
            return redirect ('/Foodies/content')

        
