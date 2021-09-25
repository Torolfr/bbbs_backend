import pytest


class Test01APIEndpoints:

    @pytest.mark.django_db(transaction=True)
    def test_01_account_endpoints_not_auth(self, client):
        response = client.get('/api/v1/token/')
        assert response.status_code != 404, (
            'Страница `/api/v1/token/` не найдена, проверьте этот адрес в *urls.py*'
        )
        response = client.get('/api/v1/token/refresh/')
        assert response.status_code != 404, (
            'Страница `/api/v1/token/refresh/` не найдена, проверьте этот адрес в *urls.py*'
        )

    @pytest.mark.django_db(transaction=True)
    def test_02_api_endpoints_not_auth(self, client):
        response = client.get('/api/v1/articles/')
        assert response.status_code != 404, (
            'Страница `/api/v1/articles/` не найдена, проверьте этот адрес в *urls.py*'
        )
        response = client.get('/api/v1/books/')
        assert response.status_code != 404, (
            'Страница `/api/v1/books/` не найдена, проверьте этот адрес в *urls.py*'
        )
        response = client.get('/api/v1/catalog/')
        assert response.status_code != 404, (
            'Страница `/api/v1/catalog/` не найдена, проверьте этот адрес в *urls.py*'
        )
        response = client.get('/api/v1/history/')
        assert response.status_code != 404, (
            'Страница `/api/v1/history/` не найдена, проверьте этот адрес в *urls.py*'
        )
        response = client.get('/api/v1/places/activity-types/')
        assert response.status_code != 404, (
            'Страница `/api/v1/places/activity-types/` не найдена, проверьте этот адрес в *urls.py*'
        )
        response = client.get('/api/v1/places/')
        assert response.status_code != 404, (
            'Страница `/api/v1/places/` не найдена, проверьте этот адрес в *urls.py*'
        )
        response = client.get('/api/v1/tags/')
        assert response.status_code != 404, (
            'Страница `/api/v1/tags/` не найдена, проверьте этот адрес в *urls.py*'
        )
        response = client.get('/api/v1/rights/')
        assert response.status_code != 404, (
            'Страница `/api/v1/rights/` не найдена, проверьте этот адрес в *urls.py*'
        )
        response = client.get('/api/v1/movies/')
        assert response.status_code != 404, (
            'Страница `/api/v1/movies/` не найдена, проверьте этот адрес в *urls.py*'
        )
        response = client.get('/api/v1/videos/')
        assert response.status_code != 404, (
            'Страница `/api/v1/videos/` не найдена, проверьте этот адрес в *urls.py*'
        )
        response = client.get('/api/v1/questions/')
        assert response.status_code != 404, (
            'Страница `/api/v1/questions/` не найдена, проверьте этот адрес в *urls.py*'
        )
        response = client.get('/api/v1/cities/')
        assert response.status_code != 404, (
            'Страница `/api/v1/cities/` не найдена, проверьте этот адрес в *urls.py*'
        )
        response = client.get('/api/v1/profile/diaries/')
        assert response.status_code != 404, (
            'Страница `/api/v1/profile/diaries/` не найдена, проверьте этот адрес в *urls.py*'
        )
        response = client.get('/api/v1/afisha/events/')
        assert response.status_code != 404, (
            'Страница `/api/v1/afisha/events/` не найдена, проверьте этот адрес в *urls.py*'
        )
        response = client.get('/api/v1/afisha/event-participants/archive/')
        assert response.status_code != 404, (
            'Страница `/api/v1/afisha/event-participants/archive/` не найдена, проверьте этот адрес в *urls.py*'
        )
        response = client.get('/api/v1/afisha/event-participants/')
        assert response.status_code != 404, (
            'Страница `/api/v1/afisha/event-participants/` не найдена, проверьте этот адрес в *urls.py*'
        )
        response = client.get('/api/v1/main/')
        assert response.status_code != 404, (
            'Страница `/api/v1/main/` не найдена, проверьте этот адрес в *urls.py*'
        )
        response = client.get('/api/v1/profile/send_password/')
        assert response.status_code != 404, (
            'Страница `/api/v1/profile/send_password/` не найдена, проверьте этот адрес в *urls.py*'
        )
        response = client.get('/api/v1/profile/')
        assert response.status_code != 404, (
            'Страница `/api/v1/profile/` не найдена, проверьте этот адрес в *urls.py*'
        )
