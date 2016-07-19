from system.core.model import Model

class Preference(Model):
    def __init__(self):
        super(Preference, self).__init__()

    def add_preferences(self, prefs, user_id):
        #select user id of current user
        #select preference ids that correspond with the input preferences
        for value in prefs.keys():
            query = "SELECT id from preferences WHERE preference = %s"
            data = value
            user_preferences = self.db.query_db(query, [data])
            #Insert new preferences for user
            query = "INSERT INTO user_prefs (user_id, preference_id) VALUES (%s, %s)"
            data = [user_id, user_preferences[0]['id']]
            self.db.query_db(query, data)

    def get_user_prefs(self, user_id):
        query = "SELECT users.id, user_prefs.preference_id, preferences.preference from users LEFT JOIN user_prefs ON users.id = user_prefs.user_id LEFT JOIN preferences ON preferences.id = user_prefs.preference_id WHERE users.id = %s ORDER BY preferences.preference"
        data = [user_id]
        return self.db.query_db(query, data)
