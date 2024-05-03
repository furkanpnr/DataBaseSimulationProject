import datetime

class AUser():
    def update(self):
        print("database updated."+ str(datetime.datetime.now()))
    
    def start(self):
        self.update()


class BUser():
    def read_data(self):
        print('database read.'+ str(datetime.datetime.now()))

    def start(self):
        self.read_data()

