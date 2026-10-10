from flask import Flask,request,jsonify
from flask_cors import CORS
import re
app=Flask(__name__)
CORS(app)
def check_strength(password):
    score=0
    if(len(password)>=8):
        score+=1
    if re.search(r"[0-9]",password):
        score+=1
    if re.search(r"[A-Z]",password):
        score+=1
    if re.search(r"[!@#$%^&*()<?|\>,.;{}]",password):
        score+=1
    if score<=1:
        return "Weak"
    elif score<=3:
        return "Medium"
    else:
        return "Strong"
def estimate_crack_time(password):
    pool=0
    if re.search(r"[a-z]",password):
        pool+=26
    if re.search(r"[A-Z]",password):
        pool+=26
    if re.search(r"[0-9]",password):
        pool+=10
    if re.search(r"[!@#$%^&*()<?|\>,.;{}]",password):
        pool+=32
    if pool==0:
        return "Can't estimate empty Password"
    combi=pool**len(password)
    gps=10000000000
    seconds=combi/gps
    if seconds<60:
        return f"{seconds:.2f} seconds"
    elif seconds<3600:
        return f"{seconds/60:.2f} minutes"
    elif seconds<86400:
        return f"{seconds/3600:.2f} hours"
    elif seconds<31536000:
         return f"{seconds/86400:.2f} hours"
    elif seconds<31536000:
         return f"{seconds/86400:.2f} days"
    else:
        return f"{seconds/31536000:.2f} years"
@app.route("/check",methods=["POST"])
def check():
    data=request.get_json()
    password=data["password"]
    return jsonify({
        "strength":check_strength(password),"crack_time":estimate_crack_time(password)
    })
if __name__=="__main__":
    app.run(port=5000)