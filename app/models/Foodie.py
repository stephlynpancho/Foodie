from system.core.model import Model
import re

class Foodie(Model):
    def __init__(self):
        super(Foodie, self).__init__()

    def add_users(self, users):
        EMAIL_REGEX = re.compile(r'^[a-za-z0-9\.\+_-]+@[a-za-z0-9\._-]+\.[a-za-z]*$')
        errors =[]
        password= users['password']
        

        if not users['first_name']:
            errors.append('Name cannot be blank')   
        elif len(users['first_name'])<2:
            errors.append("Name must be atleast 2 characters")
        if not users['last_name']:
            errors.append('Name cannot be blank')
        elif len(users['last_name'])<2:
            errors.append("Name must be atleast 2 characters")
        if not users['email']:
            errors.append("Email cannot be blank")
        elif not EMAIL_REGEX.match(users['email']):
            errors.append("Email type is invalid")
        if users['password']<5:
            errors.append("Password must be atleast 5 characters long")
        if not users['password']:
            errors.append("Password cannot be blank")
        if users['password'] != users['cpw']:
            errors.append("Passwords do no match")
        if len(self.db.query_db("SELECT email from users WHERE email = '{}'".format(re.escape(users['email'])))) > 0:
            errors.append("User already exists.")


        if errors:
            return {"status":False, "errors":errors}
            print errors
        else:
            hashed_pw = self.bcrypt.generate_password_hash(password)
            query = "INSERT INTO users (first_name, last_name, email, password, created_at) VALUES(%s, %s, %s, %s, NOW())"
            data = [users['first_name'], users['last_name'], users['email'], hashed_pw]
                
            self.db.query_db(query, data)

            get_user_query = "SELECT * FROM users ORDER BY created_at DESC LIMIT 1"
            users=self.db.query_db(get_user_query)
            query = "INSERT INTO shopping_lists (created_at, user_id) VALUES (NOW(),%s)"
            data = [users[0]['id']]
            self.db.query_db(query, data)
            query = "SELECT users.id, users.first_name, shopping_lists.id as shopping_list_id FROM users LEFT JOIN shopping_lists ON users.id = shopping_lists.user_id WHERE users.id=%s"
            users = self.db.query_db(query, data)
            return {"status" : True, "user":users[0]}


    def log_in(self, login_data):
        errors = []
        password= login_data['password']
        query= "SELECT * FROM users WHERE email=%s"
        data=[login_data['email']]
        emailvalid = self.db.query_db(query, data)


        if emailvalid:
            if self.bcrypt.check_password_hash(emailvalid[0]['password'], password):
                query = "SELECT users.id, users.first_name, shopping_lists.id as shopping_list_id FROM users LEFT JOIN shopping_lists ON users.id = shopping_lists.user_id WHERE users.id=%s"
                user = self.db.query_db(query, [emailvalid[0]['id']])
                return {"status": True, 'user_info': user[0] }

        errors.append('Your username and/or password do not match our records')
        return {"status" : False, 'errors' : errors}


    def add_grocery(self, item, shopping_id):
        query = "INSERT INTO list_items (item, shopping_list_id) VALUES (%s, %s)"
        data = [item, shopping_id]
        self.db.query_db(query, data)

    def get_groceries(self, shopping_id):
        query = "SELECT * from list_items WHERE shopping_list_id = %s"
        data = [shopping_id]
        return self.db.query_db(query, data)

    def remove_grocery(self, item, shopping_id):
        query = "DELETE FROM list_items WHERE id =%s and shopping_list_id=%s"
        data = [item, shopping_id]
        self.db.query_db(query, data)







