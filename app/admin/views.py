from flask_login import current_user
from flask_admin.contrib import sqla

# Create customized model view class
class MyUserView(sqla.ModelView):

    def is_accessible(self):
        return current_user.is_authenticated