# -*- coding: utf-8 -*-

import requests
from requests.cookies import RequestsCookieJar

cookies = "_octo=GH1.1.1819589382.1584486488; _device_id=099cf2a13524a2c20ad62f0e91191d4d; _ga=GA1.2.813069593.1584486504; tz=Asia%2FShanghai; user_session=ReKP5u5LLH61NGCHZ7Dj4YlpvLt26tHIqIPIK-k9kLWgwp0B; __Host-user_session_same_site=ReKP5u5LLH61NGCHZ7Dj4YlpvLt26tHIqIPIK-k9kLWgwp0B; logged_in=yes; dotcom_user=Gedanke; _gh_sess=bBnIWA4C5jutpcfzayOqVqOHZZvOoX2I9EikNoCNSpNelUcxCvsKTOyKL9n8gjW6cSl08wHzYuEPtDa2NS%2BziQmaxyydldvS22jLFMrOj59jr68j8nDY2IxnTPZsN4rN7vC99Z9ktKubl01LwB%2FroOC3roPhnAabaXbmU1z%2BfF0viOxPDXhw8Su0MdRtVlu8WIEiLwfUdbRABefUVjMxN0OdhRXLOBKyFLLH23Y50wriV47UEy0UuZi0fbcrtW22sFUVk6XCw9tbJ4vCtxD8mScPZCTRyhZE7nGuYLYGsPs8xsZrIkBmEUk1gUXfUlDf%2B1SM5%2BHKhzIDKQkn6%2BSHEfXyMq%2FTJgrUBkFHKy7au%2FYn5zbdeC4aIBQ%2Bdj1U%2FlgaR8pMLiYZGaMPiefoeNdcE1og9jAVOjGG0HF9%2FjGirYVmbgKWReGrbu3Ypm6EXRGrCuCnuLzcjcVDMTl7n5ubq%2F3Le0Io6Wvk4xyIcxeK1OwcGnRtGNfjtGf66C4TTDv3ZLdPJdAxFJxcH2119FRFdXVVN843A%2Fw%2BcsgV6NFbinoXPXtj1ZVznLPD3lj79VwvD1zdgMbqPuuneyTAKWKMPOrZ5w%2B4BHoE0vl%2BHViGVlh07AkdZhfEmSDOPB945z2Z8nOawRjdmybxw%2FDlGGW2y9qHBcLK2BXlgnve0vFCr2bKyj7xPVlHkOFVV032OiiV0eIDsgN5QIsVIgiQwA2R05jO6%2Fu%2F27jerdRSPY72e49sC3ILPo07X%2FogPFnUiD7SNT63CUZHz3V%2FAU0b61esLCMgJjdmNFCTwhLqXGbjdL9tbZpQVr0VmIxOkadO76qK8Wjwl7BYtzctAInrnCS8Z6GTbzvdmO%2FOcmhRjapFANsuw6ma4PtYiScFeJb2NmUwTRJpFIVcOstsrzn2nbvAGp8IsXwn2PTff6XA9E3oca2b%2F71%2Fs3x9ub8EKCzs75%2F2zYnCS1sewoWp9O0ttxo0s0YWdjfSSrMrBhSw4UHgYY43pBFsFpVJetJbfvBCzSo6%2Bmzc8zqE2TqaREdtH73NXTlI%2BAo13VhYVY0%2BaLurI5cKoaGK2iuJrED5xMhtjGhMVbEl9%2BkQMBvca%2FMOVqBUivXcFB9xju7zOauUqQeDMmiXEhyHfMnRnp7LQsi8RuTfi4mXWpGJ6zyiUQS7Bm592jdV77O4oS5gLKdNHcW%2FHv0QAfP81oWPtHMGkB7YzEAaMN06IB%2BXnGYTv2%2Fljuc4Idj3c7A3ALAF5X3HDTIXZZtqM5R%2FvW2tvGNI%2Fr%2FKxKs4%2FmeK6qOoEWS6rDuw0lu9NlyCWGRJxly0QKUUIuhpICSOzg%2FNyurfwZMRdbydfXKo9rh25LbqPxncwxZ1LB81ZBkiclsu%2FwtnjmLmOTpElm4zfB2fPSY2xbsXVyTr07ibNuqCnXJJ5rkJVT773Q5RhOl2LzG7N6oKXEF42UeZUBdJugY31oISUdx8T13nwCtD36QX%2FuEREXzGMQrK%2B8Yt64u%2F6TWJFb9YcYP%2Bdo6eDTcEwgnRBgBgwdDc%2Bg69R2pT2dDn%2B9wi%2BFDIBIuf00yUwzO7WE8skh1b%2FR4ElaEcicPNfmvUX5P9Be4G32WlGCfS0V%2FoQp4QDMt1my47syqBFvrM5RwHfdo9ITwXolR9%2BSsU0r6VTrZWKjvdsaM19AnJ6iCAu7td43YzOf%2BV35hZA2mCi7OePKqRbg%2BWaElXDMJm%2F4R0Fwoie%2B7R1PEPIFpxPcJO%2FpWpbFTziYmgDuOJy%2BWP7L2mIptMe0TZB%2B90TLJejOY4zVWx1FVjZ5qtULq99Ls7%2B%2B0dYQqaTzcCua4FGmXyajMOaOi6T%2FqoIqLFehIDTbNGGvryP4QSC6woVSihpCf7XNC1ALVIfvTu--5lqrnPABlumLAeh2--FIRpm6tm1fHIQ%2FqiVWwqVg%3D%3D"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/80.0.3987.132 Safari/537.36"
}
url = "https://github.com/"
jar = RequestsCookieJar()
for cookie in cookies.split(";"):
    key, value = cookie.split("=", 1)
    jar.set(key, value)

r = requests.get(url=url, cookies=jar, headers=headers)
print(r.text)
