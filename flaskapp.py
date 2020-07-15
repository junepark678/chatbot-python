from flask import Flask, render_template, redirect, url_for, request
import main, math
app = Flask(__name__)
app.config['SECRET_KEY'] = r"""MIIEvwIBADANBgkqhkiG9w0BAQEFAASCBKkwggSlAgEAAoIBAQDhc2qMPuuiVxEd\nAjE1PMcjAJOfxOPbftfJrMnuEqNFQinVzPbErsEeFVV2uXGuHf14U3Fw1Lo7PZiX\nxb2CJ2m0Yw7Srp8V6thFHig+4lKXv/WWrsTUyqpRgNgm9xrsnc/zcuRmpKU+My7V\nHjHEgtPoppP4WIubm3w02DC3ohA4uSEfmQS3+wM46TFNS9Fn0c2+oM3HJEyGEPdC\nyExN5xrw5l601SwlECdSok/rkIj1uDQcFC6Mkyx0uzvRJEeSlM+fPFQGvHkrIZfh\nFgYm52vhz5k8TRmbkoOwyk+ZYTUpzpZ9AGKyf2/sSkYLfjVWmVOj1+IiYwlsOT0N\n/IqvD7K5AgMBAAECggEBAJCesOJ2GkFxCJFLLrWv3y4c2JXMfz32CAZeyMnnOsTa\nxGtZp5JTZ54coU4fd0TyB/5/yG1QiIYn5RK2zfIHxk7onEGZsoMkusbbqYVtOP4P\nLUMTqT+3IbpWpFGagbL3KMZKFSmixD06J/id/d7I7ZZ4BMNySVvwSaS8acPiOfWn\n1392VrKGxIpg1bp4bzdhZakhswgh9ROCQFBVWFhZRYJBd4QubT+oQ/KqVJ3vFW51\nHlleOYTVUzZOxwhLi3wQaw+Mbs0UToyoXRVDxCCZk/A9JDGXipPa0uSmXG4QzhaH\nNwqzqd4dBfAN7JkkU5okKflEoR69mcyP59zv4iDBX+ECgYEA+9/moGiMLAeyaOSb\n8zuEh26mJMizM7lFEn703wbAhje9mH98Mc+mKDFxQ8qQuKiEuTG8Jxc1vyJq/OjZ\neNKH6OT/Aql6Ujpd9RChEDLTfhl0hGoqatQ3OaXvM34w9qDkWCxxINQ8QawLCwcM\n5+wyUaipKow8mDBlKrN6z3361xMCgYEA5SS4vG5udOCbFmHgxJk52u2T5M4u3FwG\nLsv5wwgBbI9qk/88ttNb2N7BDgb2cJcvNm481AuDYErZDhmgFeCRjxan6tuPDUL0\nMduCl7YHPDQboHJ78+8f0LH9vWzNw9MTkae+b08YI+Rxhnu9wcHyEMHzRQks3pY7\n5/2CqZn+TIMCgYEA1PY3FaHQAtpvKulAQqQsJiaUK73WZwFbOYxGltwqpFE06V/B\nLoyXvJwxXFRFkRxLPBqlL5gcRYNgWn62gcXgTDZyt1l8p1HaZ36r7/pJf/Ed52es\nfa75ErEOUsd7tsvKxhKthEhuukgw/h3z95Rp50ln3yW7hiJFJ5mhWRb3pCkCgYEA\nrmPNKLNO4yqRPW6OVnFa47BODyOP7Gso1XKtie3Mz6cycKIevfGLhDi7aoaIBdY5\nu04YgzSj7qPoH2AHQr8faGvQreAdNfWPzWYHNJj3Vq09nVWj2llRuE3OE9z7mJ5K\n1V55g1MJxz8z2yrPlueY54IEN7Us7dYej4eTaqplLCsCgYB/7Z5zn2PE3diTBHBR\nxH+KdATn/qMqrmREh5pgb4W5NyIpKIUezIWAvzdzth1h1CWc4rMthp4FzAZK28AL\ni3dBN2YEcfNCA/suXo4FINeS0wPWf2AHXcpQmZS9Ri0oFrFiaPHZiJS961vnDRWB\nIt7ZHP7mDqAQI5yxujpboDBoVg=="""

messages = []

@app.route("/")
def sessions():
    return render_template("chat.html", messages=messages)

@app.route("/send", methods=["POST", "GET"])
def send():
    message = request.form["chat"]
    messages.append(message)
    results = main.model.predict([main.bag_of_words(message, main.words)])
    results_index = main.numpy.argmax(results)
    tag = main.labels[results_index]
    for tg in main.data["intents"]:
        if tg['tag'] == tag:
            responses = tg['responses']
    if tag == "math":
        return render_template("math.html")

    messages.append(main.random.choice(responses))
    return redirect(url_for("sessions"))

@app.route("/math", methods=["POST", "GET"])
def math1():
    eq = request.form["eq"]
    try:
        a = eval(eq)
    except:
        a = "enter a vailid equation"
    messages.append(a)
    return redirect(url_for("sessions"))    


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80)