import config
from modules.gui.service.gui import Gui

def main():
    gui = Gui(config.HEIGHT, 
              config.WIDTH,
                config.RESIZEABLE, 
                config.TITLE, 
                config.INFO)
    
    gui.mainloop()

def experiments():
    from experiment_executor import ExperimentExecutor
    
    # Change the path to the experiment file you want to execute
    executor = ExperimentExecutor(config.READ_COMMITTED_PATH)
    executor.execute()
    # wait for the executor to finish
    # be patient, it may take a while


if __name__ == '__main__':
    # main()
    experiments()