from .models import Article, Movie, Question


class BBBSGeneralError(Exception):
    pass


class BBBSInvalidCountError(BBBSGeneralError):
    def __init__(self, model):
        self.model = model
        if model == Movie:
            super().__init__(400, 'InvalidMovieCount')
            self.message = 'Invalid number of movies'
        if model == Article:
            super().__init__(400, 'InvalidArticleCount')
            self.message = 'Invalid number of articles'
        if model == Question:
            super().__init__(400, 'InvalidQuestionCount')
            self.message = 'Invalid number of questions'

    def __str__(self) -> str:
        return f'{self.message}'
