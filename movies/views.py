from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import Movie, MovieRating, Genres, TempPrefer
from .forms import SignupForm, MyCustomLoginForm
import json

# 첫 페이지
def index(request):
    if request.user.is_authenticated is True:
        return redirect('prefer-test')
    return render(request, 'movies/index.html')


# 가입시 선호 영화 선택 창
def preferenceTest(request):
    # 선호영화를 고른사람은 바로 영화 화면으로 리디렉션
    if request.user.prefer != None:
        return redirect('movies')
    
    # 안고른사람은 고를 수 있도록 선호체크 화면으로 랜더링
    return redirect('prefer')


# 첫 회원가입 혹은 로그인 시 선호 작품 선택하게 해주는 뷰
def preference(request):
    if request.method == 'GET':
        movies = TempPrefer.objects.all()
        context = {'movies':movies}
        return render(request, 'movies/preference.html', context)
    elif request.method == 'POST':
        post_data = json.loads(request.body.decode("utf-8"))
        data = post_data.get('text')
        myuser = request.user
        myuser.prefer = data
        myuser.save()
        return redirect('movies')

def recommendList(request):
    if request.user.is_authenticated:

        if request.method == "GET":
            img_ls = [
                "https://an2-img.amz.wtchn.net/image/v2/T7qP_idp-A7AdHCV6-wZBA.jpg?jwt=ZXlKaGJHY2lPaUpJVXpJMU5pSjkuZXlKdmNIUnpJanBiSW1SZk5Ea3dlRGN3TUhFNE1DSmRMQ0p3SWpvaUwzWXlMM04wYjNKbEwybHRZV2RsTHpFMk56VTJOVE16TlRNNE9EVTVNVEEyTURVaWZRLmZxSThtNU1jQl9HSDFxQ0plZGlUYUxPa1R4WTVwSC1kZGhNWVhISy16anM",
                "https://an2-img.amz.wtchn.net/image/v2/KdZZFDjbAnzNfrYsEH6csQ.jpg?jwt=ZXlKaGJHY2lPaUpJVXpJMU5pSjkuZXlKdmNIUnpJanBiSW1SZk5Ea3dlRGN3TUhFNE1DSmRMQ0p3SWpvaUwzWXlMM04wYjNKbEwybHRZV2RsTHpFMk56RTNOalk0TlRjMU1EVTFNamMzTWpVaWZRLkFjc1FZVGZkSHdueEVBX2dpQ20xcnQ3WUhuTDdfLTllQzlYa0l3NWVvVUk",
                "https://an2-img.amz.wtchn.net/image/v2/aYGHhHRw6fLVcy5Z9pW8-Q.jpg?jwt=ZXlKaGJHY2lPaUpJVXpJMU5pSjkuZXlKdmNIUnpJanBiSW1SZk5Ea3dlRGN3TUhFNE1DSmRMQ0p3SWpvaUwzWXlMM04wYjNKbEwybHRZV2RsTHpFMk56WTFPVGszTXpJMk56UTNNekkyTURVaWZRLmZVZEdGOEl1cVpFeGJvOWhmMDJzdTFDaHBjQ0pJeHpORElld29Jc2p0RDg",
                "https://an2-img.amz.wtchn.net/image/v2/zMCmf_akyzZCKoQuF309hQ.jpg?jwt=ZXlKaGJHY2lPaUpJVXpJMU5pSjkuZXlKdmNIUnpJanBiSW1SZk5Ea3dlRGN3TUhFNE1DSmRMQ0p3SWpvaUwzWXlMM04wYjNKbEwybHRZV2RsTHpFMk56WTRNemt5TkRZNU1qTXpPREE1T1RZaWZRLk55UURqMlJxUTR1WXIwZWppU1hlTVNGVHNzR1hoYk94MzdTZkRtMTBXQ28",
                "https://an2-img.amz.wtchn.net/image/v2/b3vUj5RxXNSMEuv8StYk0w.jpg?jwt=ZXlKaGJHY2lPaUpJVXpJMU5pSjkuZXlKdmNIUnpJanBiSW1SZk5Ea3dlRGN3TUhFNE1DSmRMQ0p3SWpvaUwzWXlMM04wYjNKbEwybHRZV2RsTHpFMk56YzFNemd4T0RZek1qSTFORE00TVRnaWZRLk92Z2Z6ZzNrTkFEYXBmOWNHdVQ1YVduZENiMTFUTlpJM0RJZmVvSldZZGc",
                "https://an2-img.amz.wtchn.net/image/v2/CaEoPXXKc7vSOKCFtKa4Yw.jpg?jwt=ZXlKaGJHY2lPaUpJVXpJMU5pSjkuZXlKdmNIUnpJanBiSW1SZk5Ea3dlRGN3TUhFNE1DSmRMQ0p3SWpvaUwzWXlMM04wYjNKbEwybHRZV2RsTHpFMk56VTRNelUwTVRreU1ESTRORGczTURFaWZRLkg0aGlKX2Q3Q21POTYwT3BZMnlxS1RMS194QzFRbVZ2bXdaNTlfMXdHNU0",
                "https://an2-img.amz.wtchn.net/image/v2/lS7z4u46NJ6QXKaWQwApfw.jpg?jwt=ZXlKaGJHY2lPaUpJVXpJMU5pSjkuZXlKdmNIUnpJanBiSW1SZk5Ea3dlRGN3TUhFNE1DSmRMQ0p3SWpvaUwzWXlMM04wYjNKbEwybHRZV2RsTHpFMk56WTFPVGt3TVRVek1EYzVNREl5TXpFaWZRLlFrM09TUlpmMC1TQ2NSdkl4ajI3YnQ4V2xGUmU0blNHdlIxNmlScGdqWnM",
                "https://an2-img.amz.wtchn.net/image/v2/YUwgLWf5GjrzQYMDL6wfug.jpg?jwt=ZXlKaGJHY2lPaUpJVXpJMU5pSjkuZXlKdmNIUnpJanBiSW1SZk5Ea3dlRGN3TUhFNE1DSmRMQ0p3SWpvaUwzWXlMM04wYjNKbEwybHRZV2RsTHpFMk5USTJPREUzTXpNeE56SXlNVEE1TmpjaWZRLi1YMnQ4bmxvaTI3U0RDMXZBaVJqSEdXWTFsdEREZjVIbTg1NWhYVHh5M1U",
                "https://an2-img.amz.wtchn.net/image/v2/biVpbQFuhi0l3I7YpLDFYw.jpg?jwt=ZXlKaGJHY2lPaUpJVXpJMU5pSjkuZXlKdmNIUnpJanBiSW1SZk5Ea3dlRGN3TUhFNE1DSmRMQ0p3SWpvaUwzWXlMM04wYjNKbEwybHRZV2RsTHpFMk56VTVPVGM0TnpFMk9USTFNREExTkRZaWZRLjZ5bmxINVNpVk85R240aWNEeUNpWDhqTkNFdElyUjJwdFhjUXFWb2s1WjA",
                "https://an2-img.amz.wtchn.net/image/v2/BDpXAImcYxsTO7JLcCtfkA.jpg?jwt=ZXlKaGJHY2lPaUpJVXpJMU5pSjkuZXlKdmNIUnpJanBiSW1SZk5Ea3dlRGN3TUhFNE1DSmRMQ0p3SWpvaUwzWXlMM04wYjNKbEwybHRZV2RsTHpFMk56Z3dPRFUyTXpjM01UWXlOakF5TXpJaWZRLkM4MF9IcVF6b3dobnlhNVg2dklnV1VFbWpTRVFia2sydFYxYjlUNGpSWXM",
            ]
            img_ls2 = [
                "https://an2-img.amz.wtchn.net/image/v2/Z6JMMvgh70CwzIIVRGj8Wg.jpg?jwt=ZXlKaGJHY2lPaUpJVXpJMU5pSjkuZXlKdmNIUnpJanBiSW1SZk5Ea3dlRGN3TUhFNE1DSmRMQ0p3SWpvaUwzWXlMM04wYjNKbEwybHRZV2RsTHpFMk5EUXlNREUwTVRReU56QXlNakU1TVRJaWZRLm9wUnV4R0R5emYzWXBIZndtVGxqbU94SlVCYXkwdk9GT0lBVVpZN3hlaHc",
                "https://an2-img.amz.wtchn.net/image/v2/tkmsakQ3xtdo7JXj6Gogqw.jpg?jwt=ZXlKaGJHY2lPaUpJVXpJMU5pSjkuZXlKdmNIUnpJanBiSW1SZk5Ea3dlRGN3TUhFNE1DSmRMQ0p3SWpvaUwzWXlMM04wYjNKbEwybHRZV2RsTHpFMk5UZzRPREF6TXpjeU5qY3dNREkxTXpraWZRLjU3cGhtemxyblpFdW5jU1BfZy1ycUhNU1VjV19WTDlLSjJITmh3anJPVWM",
                "https://an2-img.amz.wtchn.net/image/v2/981xSWRzzosPOjw7Zeiq-A.jpg?jwt=ZXlKaGJHY2lPaUpJVXpJMU5pSjkuZXlKdmNIUnpJanBiSW1SZk5Ea3dlRGN3TUhFNE1DSmRMQ0p3SWpvaUwzWXhMMjVrY0hwak4zZHBaR2gyYVdsMVpXdDRaWE55SW4wLkZfNFk4ek9wMWFTVnQ5TzNsd2loTjZmeTNoWDhqMV9YS0o5NkJ0V25ld0E",
                "https://an2-img.amz.wtchn.net/image/v2/93ikI9PjazpuYaM1HUjj5Q.jpg?jwt=ZXlKaGJHY2lPaUpJVXpJMU5pSjkuZXlKdmNIUnpJanBiSW1SZk5Ea3dlRGN3TUhFNE1DSmRMQ0p3SWpvaUwzWXlMM04wYjNKbEwybHRZV2RsTHpFMk16a3pNakF6TnpVeU1URXpPRFUzTVRZaWZRLmY4OUM3dnc4Q09UNElFMllYN00yU2UyaVhNQnYxbzRmWmxOeXdpbmR0WnM",
                "https://an2-img.amz.wtchn.net/image/v2/QqtmKstt8JHnc5QwA98kEQ.jpg?jwt=ZXlKaGJHY2lPaUpJVXpJMU5pSjkuZXlKdmNIUnpJanBiSW1SZk5Ea3dlRGN3TUhFNE1DSmRMQ0p3SWpvaUwzWXlMM04wYjNKbEwybHRZV2RsTHpFMk56STVNalE1TWpjek9UUTRNakUxTmpnaWZRLlBIcmNGOWR2YWNQdGpXNjgzZm91WFJnQlpudjdxU1lnU0NZLTJxSzNaWkk",
                "https://an2-img.amz.wtchn.net/image/v2/4vhjmPctbs9uHInWh3pKqw.jpg?jwt=ZXlKaGJHY2lPaUpJVXpJMU5pSjkuZXlKdmNIUnpJanBiSW1SZk5Ea3dlRGN3TUhFNE1DSmRMQ0p3SWpvaUwzWXhMMnQ1Wm5jd2FITnZhbXh5TVhObVkydHlibVprSW4wLlZuZE5XZXFLUzN3SnhURllYZVdjZXl1emU0WUx2WjBGaFJxN2Z2RzVfekU",
                "https://an2-img.amz.wtchn.net/image/v2/9TrYTXkmKQX3dvgcgi4sIg.jpg?jwt=ZXlKaGJHY2lPaUpJVXpJMU5pSjkuZXlKdmNIUnpJanBiSW1SZk5Ea3dlRGN3TUhFNE1DSmRMQ0p3SWpvaUwzWXlMM04wYjNKbEwybHRZV2RsTHpFMk5EZzBORE14T0RJeE1qTTNNRFl3TURBaWZRLjVHa1R1Zk12c0I5RnlsWEZDSG5pMUZWdnVvQmNSSU10VVJDMFlocmRlN2s",
                "https://an2-img.amz.wtchn.net/image/v2/HkA9Wh_YWE_YmstdBdptsg.jpg?jwt=ZXlKaGJHY2lPaUpJVXpJMU5pSjkuZXlKdmNIUnpJanBiSW1SZk5Ea3dlRGN3TUhFNE1DSmRMQ0p3SWpvaUwzWXhMM1Z5YkdKbFpERmpkRzgyWjJoamRYQnBiMjV4SW4wLjBHUzZiZXZaRGdDVlBrMzZyZmpyUDFfM25jRUtDTDJXT2hhRUxOaXR0RFk",
                "https://an2-img.amz.wtchn.net/image/v2/VsbOBHKO4HntnkPqwyKoGA.jpg?jwt=ZXlKaGJHY2lPaUpJVXpJMU5pSjkuZXlKdmNIUnpJanBiSW1SZk5Ea3dlRGN3TUhFNE1DSmRMQ0p3SWpvaUwzWXlMM04wYjNKbEwybHRZV2RsTHpFMk5UZzBOVGM0TkRBMk16TTFPRGcwTVRJaWZRLjV2NVB4VGVkWDZXLUJaUGNoS0NRbkk5anBaMFRMN3hxMDNBb1ZFUFdDZms",
                "https://an2-img.amz.wtchn.net/image/v2/1E9ZN6C7ATEGolUAh_0k_w.jpg?jwt=ZXlKaGJHY2lPaUpJVXpJMU5pSjkuZXlKdmNIUnpJanBiSW1SZk5Ea3dlRGN3TUhFNE1DSmRMQ0p3SWpvaUwzWXlMM04wYjNKbEwybHRZV2RsTHpFMk1UVXhPRGc1TmpZeU9UazFOemd4TmpnaWZRLmJ3OUJObXpHbGRBY1pZMU92aVNqdFVPMmtWakhFZkdCU0UxOUJWQkJ0ZTg",
            ]
            context = {
                'imgs': img_ls,
                'imgs2': img_ls2,
            }
            return render(request, 'movies/recommendation.html', context)

    else:
        return redirect('account_login')



def movieList(request):
    movies = Movie.objects.all()
    context = {
        'movies':movies,
    }
    return render(request, 'movies/movie-list.html', context=context)

