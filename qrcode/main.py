import qrcode

url = "https://www.tbank.ru/cf/4PfMeqXD1Ar"
img = qrcode.make(url)
img.save("tbank.png")
