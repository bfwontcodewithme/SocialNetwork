import matplotlib.pyplot as plt
from PIL import Image
'''
    pass tests in windows.
    fail in ubuntu - the differences between output and student output are by \r\n
    even after adding manually \r\n, there are still specific spots that won't change resulting in fail
    the files considered different.
    this explanation is also in mail sent to oopariel@gmail.com with screenshots 
'''

class SocialNetwork:  # Singleton design pattern
    __instance = None

    def __init__(self, name):
        if SocialNetwork.__instance is not None:
            raise Exception("SocialNetwork is already instantiated")
        else:
            self.Name = name
            self.Users = []
            SocialNetwork.__instance = self
            print(f"The social network {self.Name} was created!")

    def __str__(self):
        nl = '\n'
        return f"{self.Name} social network:\n"+"\n".join(str(user) for user in self.Users) + nl

    @staticmethod
    def get_instance():
        if SocialNetwork.__instance is None:
            SocialNetwork.__instance = SocialNetwork("SocialNetwork")
        return SocialNetwork.__instance

    def sign_up(self, username, password):
        for user in self.Users:
            if user.username == username:
                raise Exception("username taken")
        if not (4 <= len(password) <= 8):
            raise Exception("password needs to be between 4-8 characters")
        user = User(username, password)
        self.Users.append(user)
        return user

    def log_in(self, username, password):
        for user in self.Users:
            if user.username == username and user.password == password:
                if user.online:
                    print("user already logged in")
                    return
                user.online = True
                print(f"{username} connected")
                return
        print("wrong username or password")

    def log_out(self, username):
        for user in self.Users:
            if user.username == username:
                if not user.online:
                    print("user already logged out")
                    return
                user.online = False
                print(f"{username} disconnected")
                return
        print("user not found")


class User:  # Observer design pattern

    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.following = []
        self.followers = []
        self.posts = []
        self.notifications = []
        self.online = True

    def __str__(self):
        return f"User name: {self.username}, Number of posts: {len(self.posts)}, Number of followers: {len(self.followers)}"

    def notify(self, data):
        self.notifications.append(data)

    def follow(self, user):
        if self.online:
            self.following.append(user)
            user.followers.append(self)
            print(f"{self.username} started following {user.username}")
        else:
            raise Exception("you are not logged in")

    def unfollow(self, user):
        if self.online:
            user.followers.remove(self)
            self.following.remove(user)
            print(f"{self.username} unfollowed {user.username}")
        else:
            raise Exception("you are not logged in")

    def publish_post(self, type, *args):
        if not self.online:
            raise Exception("user not logged in")
        else:
            postFactory = PostFactory()
            if type == "Image":
                return postFactory.createImagePost(self, *args)

            elif type == "Text":
                return postFactory.createTextPost(self, *args)

            elif type == "Sale":
                return postFactory.createSalesPost(self, *args)

    def print_notifications(self):
        print(f"{self.username}'s notifications:")
        for notif in self.notifications:
            print(notif)


class Post:  # Factory design pattern
    Sold: bool = None

    def __init__(self, tag: int, poster: User, data: str, price: int = None, location: str = None):
        self.poster = poster
        self.Likes = 0
        self.comments = []
        self.postTag = tag

        if tag == 1 or tag == 2:
            self.data = data

        if tag == 3:
            self.carName = data
            self.price = price
            self.location = location
            self.Sold = False

        self.poster.posts.append(self)
        for follower in self.poster.followers:
            follower.notify(f"{self.poster.username} has a new post")
        print(self)

    def __str__(self):
        if self.postTag == 1:
            return f'{self.poster.username} published a post:\n'+f'"{self.data}"\n'

        if self.postTag == 2:
            return f"{self.poster.username} posted a picture\n"

        if self.postTag == 3:
            first_part = f"{self.poster.username} posted a product for sale:\n"
            if not self.Sold:
                return first_part + f"For sale! {self.carName}, price: {self.price}, pickup from: {self.location}\n"
            else:
                return first_part + f"Sold! {self.carName}, price: {self.price}, pickup from: {self.location}\n"

    def like(self, user):
        if self.poster is not user:
            self.Likes += 1
            notification = f"{user.username} liked your post"
            print(f"notification to {self.poster.username}: "+notification)
            self.poster.notify(notification)
        #  else:
        #    raise Exception("You can't like yourself")


    def comment(self, user, text):
        comment = Comment(user.username, text)
        self.comments.append(comment)
        notification = f"{user.username} commented on your post"
        print(f"notification to {self.poster.username}: "+notification+f": {comment.text}")
        self.poster.notify(notification)

    def display(self):
        if self.postTag == 2:
            print("Shows picture")

            imagePath = self.data
            image = Image.open(imagePath)

            plt.imshow(image)
            plt.axis('off')  # Turn off axis numbers
            plt.show()

        else:
            raise Exception("Not an image post")

    def discount(self, amount, password):
        if self.postTag == 3 and password == self.poster.password:  # and amount >= 0:
            self.price = self.price - (self.price / 100) * amount
            print(f"Discount on {self.poster.username} product! the new price is: {self.price}")

    def sold(self, password):
        if self.postTag == 3 and self.poster.password == password:
            self.Sold = True
            print(f"{self.poster.username}'s product is sold")


class Comment:
    def __init__(self, username, text):
        self.username = username
        self.text = text

    def __str__(self):
        return f"{self.username}: {self.text}"


class PostFactory:

    def createTextPost(self, poster, textData):
        return Post(1, poster, textData)

    def createImagePost(self, poster, imagePath):
        return Post(2, poster, imagePath)

    def createSalesPost(self, poster, carName, price, location):
        return Post(3, poster, carName, price, location)
