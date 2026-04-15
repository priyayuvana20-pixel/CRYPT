from flask import Flask, render_template, request
import hashlib
import hmac

app = Flask(__name__)

stored_message = ""
stored_key = ""
stored_mac = ""
stored_hash = ""

@app.route("/", methods=["GET","POST"])
def sender():

    global stored_message, stored_key, stored_mac, stored_hash

    if request.method == "POST":

        stored_message = request.form["message"]
        stored_key = request.form["key"]

        message_bytes = stored_message.encode()
        key_bytes = stored_key.encode()

        stored_hash = hashlib.sha256(message_bytes).hexdigest()
        stored_mac = hmac.new(key_bytes, message_bytes, hashlib.sha256).hexdigest()

        print("Sender Message:", stored_message)
        print("Key:", stored_key)
        print("SHA256:", stored_hash)
        print("HMAC:", stored_mac)

        return render_template(
            "sender.html",
            hash_value=stored_hash,
            mac=stored_mac
        )

    return render_template("sender.html")


@app.route("/receiver")
def receiver():
    return render_template("receiver.html")


@app.route("/verify", methods=["POST"])
def verify():

    received = request.form["received"]

    key_bytes = stored_key.encode()
    received_bytes = received.encode()

    received_mac = hmac.new(key_bytes, received_bytes, hashlib.sha256).hexdigest()

    if received_mac == stored_mac:
        result = "Message is Authentic"
        color = "green"
    else:
        result = "Message has been Tampered"
        color = "red"

    return render_template(
        "receiver.html",
        hash_value=stored_hash,
        mac=stored_mac,
        result=result,
        color=color
    )


if __name__ == "__main__":
    app.run(debug=True)