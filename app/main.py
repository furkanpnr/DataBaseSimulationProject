import config
from modules.gui.service.gui import Gui

def main():
    gui = Gui(config.HEIGHT, 
              config.WIDTH,
                config.RESIZEABLE, 
                config.TITLE, 
                config.INFO)
    
    gui.mainloop()


if __name__ == '__main__':
    main()