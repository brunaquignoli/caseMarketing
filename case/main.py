from flask import Flask, render_template, request, jsonify, redirect, url_for
import pandas as pd
import csv

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

# todas as rotas que vão levar pras páginas:

@app.route('/')
def home():
    return render_template('login.html')

@app.route('/cadastroClientes')
def novoCadastro():
    return render_template("cadastroClientes.html")

@app.route("/deletarClientes") 
def deletar_clientes():
    return render_template("deletarClientes.html")

@app.route('/homeAdmin')
def voltar():
    return render_template("homeAdmin.html")

@app.route('/login', methods=['POST'])
def login():
    email = request.form.get('email')
    senha = request.form.get('senha')
    funcao = request.form.get('role')

    if email!= None and senha != None and funcao == "admin":
        return redirect(url_for("home_admin"))
    
    elif email!= None and senha != None and funcao == "user":
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

@app.route("/cadastroCliente", methods=["POST"])
def adicionar_cliente():
    global df

    name = request.form.get("name")
    company = request.form.get("company")
    occupation = request.form.get("occupation")
    email = request.form.get("email")
    age = request.form.get("age")
    country = request.form.get("country")
    telephone = request.form.get("telephone")

    novo_id = df["id"].max() + 1 if not df.empty else 1

    novo_cliente = {
        "id": int(novo_id),
        "name": name,
        "age": age,
        "telephone": telephone,
        "email": email,
        "country": country,
        "occupation": occupation,
        "company": company
    }

    if (name, age, telephone, email, country, occupation, company) == "" or None:
        return "<h1> Por favor, preencha todos os campos do formulário. </h1>"

    df = pd.concat([df, pd.DataFrame([novo_cliente])], ignore_index=True)
    df.to_csv(caminho_csv, index=False)


    return '''<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link rel="stylesheet" href="https://cdn.datatables.net/1.13.1/css/dataTables.bootstrap5.min.css">
    <link rel="stylesheet" href="/static/css/home.css" />
    <title>Cadastrar novo cliente</title>
</head>

<body class="bg-light">
    <div class="p-4">
        <a class="btn btn-secondary" href="/homeAdmin" role="button">Voltar</a>
        <h1> Cliente cadastrado com sucesso!</h1>
    </div>
</body>
    '''



@app.route("/deletarCliente", methods=["GET", "POST"])
def deletar_cliente():
    global df
    id = request.form.get('id')

    if not id:
        return "<h1>Por favor, informe um ID válido.</h1>"

    try:
        id = int(id)
    except ValueError:
        return "<h1>ID inválido. Digite um número inteiro.</h1>"

    if id not in df['id'].values:
        return "<h1>Não existe nenhum cliente com esse ID dentro do sistema.</h1>"

    df = df[df['id'] != id]
        
    return '''<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link rel="stylesheet" href="https://cdn.datatables.net/1.13.1/css/dataTables.bootstrap5.min.css">
    <link rel="stylesheet" href="/static/css/home.css" />
    <title>Cadastrar novo cliente</title>
</head>

<body class="bg-light">
    <div class="p-4">
        <a class="btn btn-secondary" href="/homeAdmin" role="button">Voltar</a>
        <h1> Cliente deletado com sucesso!</h1>
    </div>
</body>
'''
    

    # preciso definir que vai ser a linha que começa com a númeração id, e apagar ela
    
    





if __name__ == "__main__":
    app.run(debug=True)
