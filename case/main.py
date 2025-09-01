<<<<<<< HEAD
from flask import Flask, render_template, request, jsonify, redirect, url_for
import pandas as pd

app = Flask(__name__)

app.config['SECRET_KEY'] = 'bru'

caminho_csv = "case/dados.csv"

df = pd.read_csv(caminho_csv)

def apply_filters(df_in, search_value=None, order_col=None, order_dir="asc"):
    df_local = df_in

    if search_value:
        sv = str(search_value)
        mask = pd.Series(False, index=df_local.index)

        for col in df_local.columns:
            mask |= df_local[col].astype(str).str.contains(sv, case=False, na=False)
        df_local = df_local[mask]

    if order_col and order_col in df_local.columns:
        ascending = (order_dir == "asc")

        try:
            df_local = df_local.sort_values(by=order_col, ascending=ascending)

        except Exception:
            df_local = df_local.assign(_sort_key=df_local[order_col].astype(str))
            df_local = df_local.sort_values(by="_sort_key", ascending=ascending).drop(columns=["_sort_key"])

    return df_local

@app.route('/')
def home():
    return render_template('login.html')


@app.route('/login', methods=['POST'])
def login():
    funcao = request.form.get('role')

    if funcao == "admin":
        return redirect(url_for("home_admin"))
    
    elif funcao == "user":
        return redirect(url_for("home_user"))
    
    else:
        return "<h1>Não foi possível fazer o login. Usuário inválido.</h1>"


@app.route("/admin")
def home_admin():
    return render_template("homeAdmin.html")


@app.route("/user")
def home_user():
    return render_template("homeUser.html")

@app.route("/api/admin_data")
def admin_data():
    draw = int(request.args.get("draw", 0))
    start = int(request.args.get("start", 0))
    length = int(request.args.get("length", 10))

    order_idx = request.args.get("order[0][column]")
    order_col = None

    if order_idx is not None:
        order_col = request.args.get(f"columns[{order_idx}][data]")

    order_dir = request.args.get("order[0][dir]", "asc")

    search_value = request.args.get("search[value]", "")

    records_total = len(df)

    df_filtered = apply_filters(df, search_value=search_value,
                                order_col=order_col, order_dir=order_dir)

    records_filtered = len(df_filtered)

    page = df_filtered.iloc[start:start+length].copy()

    data = page.to_dict(orient="records")

    return jsonify({
        "draw": draw,
        "recordsTotal": records_total,
        "recordsFiltered": records_filtered,
        "data": data
    })

@app.route("/api/user_data")
def user_data():
    draw = int(request.args.get("draw", 0))
    start = int(request.args.get("start", 0))
    length = int(request.args.get("length", 10))

    order_idx = request.args.get("order[0][column]")
    order_col = None

    if order_idx is not None:
        order_col = request.args.get(f"columns[{order_idx}][data]")

    order_dir = request.args.get("order[0][dir]", "asc")
    search_value = request.args.get("search[value]", "")


    df_user_base = df.drop(columns=["id"])

    records_total = len(df_user_base)

    df_filtered = apply_filters(df_user_base, search_value=search_value,
                                order_col=order_col, order_dir=order_dir)

    records_filtered = len(df_filtered)

    page = df_filtered.iloc[start:start+length].copy()

    data = page.to_dict(orient="records")

    return jsonify({
        "draw": draw,
        "recordsTotal": records_total,
        "recordsFiltered": records_filtered,
        "data": data
    })


if __name__ == "__main__":
    app.run(debug=True)
=======
from flask import Flask, render_template, request, jsonify, redirect, url_for
import pandas as pd

app = Flask(__name__)

app.config['SECRET_KEY'] = 'bru'

caminho_csv = "case/dados.csv"

df = pd.read_csv(caminho_csv)

def apply_filters(df_in, search_value=None, order_col=None, order_dir="asc"):
    df_local = df_in

    if search_value:
        sv = str(search_value)
        mask = pd.Series(False, index=df_local.index)

        for col in df_local.columns:
            mask |= df_local[col].astype(str).str.contains(sv, case=False, na=False)
        df_local = df_local[mask]

    if order_col and order_col in df_local.columns:
        ascending = (order_dir == "asc")

        try:
            df_local = df_local.sort_values(by=order_col, ascending=ascending)

        except Exception:
            df_local = df_local.assign(_sort_key=df_local[order_col].astype(str))
            df_local = df_local.sort_values(by="_sort_key", ascending=ascending).drop(columns=["_sort_key"])

    return df_local

@app.route('/')
def home():
    return render_template('login.html')


@app.route('/login', methods=['POST'])
def login():
    funcao = request.form.get('role')

    if funcao == "admin":
        return redirect(url_for("home_admin"))
    
    elif funcao == "user":
        return redirect(url_for("home_user"))
    
    else:
        return "<h1>Não foi possível fazer o login. Usuário inválido.</h1>"


@app.route("/admin")
def home_admin():
    return render_template("homeAdmin.html")


@app.route("/user")
def home_user():
    return render_template("homeUser.html")

@app.route("/api/admin_data")
def admin_data():
    draw = int(request.args.get("draw", 0))
    start = int(request.args.get("start", 0))
    length = int(request.args.get("length", 10))

    order_idx = request.args.get("order[0][column]")
    order_col = None

    if order_idx is not None:
        order_col = request.args.get(f"columns[{order_idx}][data]")

    order_dir = request.args.get("order[0][dir]", "asc")

    search_value = request.args.get("search[value]", "")

    records_total = len(df)

    df_filtered = apply_filters(df, search_value=search_value,
                                order_col=order_col, order_dir=order_dir)

    records_filtered = len(df_filtered)

    page = df_filtered.iloc[start:start+length].copy()

    data = page.to_dict(orient="records")

    return jsonify({
        "draw": draw,
        "recordsTotal": records_total,
        "recordsFiltered": records_filtered,
        "data": data
    })

@app.route("/api/user_data")
def user_data():
    draw = int(request.args.get("draw", 0))
    start = int(request.args.get("start", 0))
    length = int(request.args.get("length", 10))

    order_idx = request.args.get("order[0][column]")
    order_col = None

    if order_idx is not None:
        order_col = request.args.get(f"columns[{order_idx}][data]")

    order_dir = request.args.get("order[0][dir]", "asc")
    search_value = request.args.get("search[value]", "")


    df_user_base = df.drop(columns=["id"])

    records_total = len(df_user_base)

    df_filtered = apply_filters(df_user_base, search_value=search_value,
                                order_col=order_col, order_dir=order_dir)

    records_filtered = len(df_filtered)

    page = df_filtered.iloc[start:start+length].copy()

    data = page.to_dict(orient="records")

    return jsonify({
        "draw": draw,
        "recordsTotal": records_total,
        "recordsFiltered": records_filtered,
        "data": data
    })


if __name__ == "__main__":
    app.run(debug=True)
>>>>>>> 3f921b58e7e20227f446aaa50f236fa97e943bcf
