from my_python import lib


class Kubectl:
    def __init__(self, kubefile_path, command_path=lib.path_for_command('kubectl')):
        self.__kubefile_path = kubefile_path
        self.__command_path = command_path

    def get_pods(self):
        return lib.invoke_subprocess([self.__command_path, 'get', 'pods'])
