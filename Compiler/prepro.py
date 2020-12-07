import re

class PrePro:
    @staticmethod
    def filter(string):
        return re.sub("(#=)(.|\n)*?(=#)", "", string)