from models import *
from database import init_db, db_session
from datetime import datetime

class Twitter:
    def __init__(self):
        self.active_user = None
    
    """
    The menu to print once a user has logged in
    """
    def print_menu(self):
        print("\nPlease select a menu option:")
        print("1. View Feed")
        print("2. View My Tweets")
        print("3. Search by Tag")
        print("4. Search by User")
        print("5. Tweet")
        print("6. Follow")
        print("7. Unfollow")
        print("0. Logout")
    
    """
    Prints the provided list of tweets.
    """
    def print_tweets(self, tweets):
        for tweet in tweets:
            print("==============================")
            print(tweet)
        print("==============================")

    """
    Should be run at the end of the program
    """
    def end(self):
        print("Thanks for visiting!")
        db_session.remove()
    
    """
    Registers a new user. The user
    is guaranteed to be logged in after this function.
    """
    def register_user(self):
        registered = False

        while not registered:
            username = input("\nWhat will your Twitter handle be?\n")

            password = input("Enter a password:\n")
            confirm_password = input("Re-enter your password:\n")

            existing_user = db_session.query(User).filter(User.username == username).first()

            if existing_user:
                print("That username is already taken. Try again. ")
            elif password != confirm_password:
                print("Those passwords don't match. Try again. \n")
            else:
                registered = True

        new_user = User(username=username, password=password)
        db_session.add(new_user)
        db_session.commit()

        print(f"Welcome {username}!")

    """
    Logs the user in. The user
    is guaranteed to be logged in after this function.
    """
    def login(self):
        logged_in = False

        while not logged_in:
            username = input("Username: ")
            password = input("Password: ")

            user = db_session.query(User).filter(User.username == username).first()

            if user and user.password == password:
                logged_in = True
            else:
                print("Invalid username or password")

        print(f"Welcome {username}!")

        self.active_user = user

    def logout(self):
        self.active_user = None

    """
    Allows the user to login,  
    register, or exit.
    """
    def startup(self):
        print("Please select a Menu Option")
        choice = input("1. Login\n2. Register User\n3. Exit\n")

        if choice == "1":
            self.login()
        elif choice == "2":
            self.register_user()
        elif choice == "3":
            self.logout()
            self.end()
        else:
            print("Please input a valid option\n")
            self.startup()

    def follow(self):
        account_to_follow_username = input("Who would you like to follow?\n")
        account_to_follow = db_session.query(User).filter(User.username == account_to_follow_username).first()

        if account_to_follow in self.active_user.following:
            print(f"You already follow {account_to_follow_username}")
        elif not account_to_follow:
            print(f"User {account_to_follow_username} does not exist")
        else:
            print(f"You are now following {account_to_follow_username}")
            self.active_user.following.append(account_to_follow)

            db_session.commit()


    def unfollow(self):
        account_to_unfollow_username = input("Who would you like to unfollow?\n")
        account_to_unfollow = db_session.query(User).filter(User.username == account_to_unfollow_username).first()

        if account_to_unfollow not in self.active_user.following:
            print(f"You don't follow {account_to_unfollow_username}")
        elif not account_to_unfollow:
            print(f"User {account_to_unfollow} does not exist. ")
        else:
            print(f"You no longer follow {account_to_unfollow}")
            self.active_user.following.remove(account_to_unfollow)

    def tweet(self):
        content = input("Create Tweet: ")
        tags = input("Enter your tags separated by spaces: ").split()
        tags = [Tag(content=tag) for tag in tags]

        tweet = Tweet(content=content, timestamp=datetime.now(), tags=tags)

        self.active_user.tweets.append(tweet)

        db_session.commit()

    
    def view_my_tweets(self):
        self.print_tweets(self.active_user.tweets)
    
    """
    Prints the 5 most recent tweets of the 
    people the user follows
    """
    def view_feed(self):
        following_usernames = [user.username for user in self.active_user.following]

        tweets = db_session.query(Tweet).where(Tweet.username.in_(following_usernames)).order_by(Tweet.timestamp).limit(5).all()

        self.print_tweets(tweets)

    def search_by_user(self):
        username = input("Username: ")

        user = db_session.query(User).filter(User.username == username).first()
        if not user:
            print("There is no user by that name. ")
        else:
            tweets = db_session.query(Tweet).filter(Tweet.username == username).all()
            self.print_tweets(tweets)

    def search_by_tag(self):
        tag = input("Enter a tag: ")

        tweets = db_session.query(Tweet).filter(Tweet.tags.any(content=tag))
        self.print_tweets(tweets)

    """
    Allows the user to select from the 
    ATCS Twitter Menu
    """
    def run(self):
        init_db()

        print("Welcome to ATCS Twitter!")
        self.startup()
        done = False

        while not done:
            self.print_menu()
            option = int(input(""))

            if option == 1:
                self.view_feed()
            elif option == 2:
                self.view_my_tweets()
            elif option == 3:
                self.search_by_tag()
            elif option == 4:
                self.search_by_user()
            elif option == 5:
                self.tweet()
            elif option == 6:
                self.follow()
            elif option == 7:
                self.unfollow()
            else:
                self.logout()
                done = True
        
        self.end()
