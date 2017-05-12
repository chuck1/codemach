import django.views
import django.urls
import django.shortcuts

import sheets_app.models

class IndexView(django.views.View):
    def get(self, request, *args, **kwargs):
        print('reverse index =', django.urls.reverse('index'))
        
        context = {
                'user': request.user,
                'url_login_redirect': django.urls.reverse('index'),
                'url_logout_redirect': django.urls.reverse('index'),
                'url_select_account_redirect': django.urls.reverse('index'),
                }

        return django.shortcuts.render(request, "index.html", context)

