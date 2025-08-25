from flask import Flask, render_template, request, jsonify, redirect, url_for
import pandas as pd

app = Flask(__name__)
app.config['SECRET_KEY'] = 'br'

# --- Carrega CSV (uma vez) ---
caminho_csv = "metrics.csv"
# garante que 'date' vire datetime
df = pd.read_csv(caminho_csv, parse_dates=["date"], dtype={
    "account_id": str, "campaign_id": str
})
df['date'] = pd.to_datetime(df['date'], errors='coerce')  # coerção segura

# helper: aplica filtro por data, busca global e ordenação
def apply_filters(df_in, search_value=None, start_date=None, end_date=None,
                  order_col=None, order_dir="asc"):
    df_local = df_in

    # filtro por data (se fornecido)
    if start_date:
        try:
            sd = pd.to_datetime(start_date, errors='coerce')
            if pd.notnull(sd):
                df_local = df_local[df_local['date'] >= sd]
        except Exception:
            pass

    if end_date:
        try:
            ed = pd.to_datetime(end_date, errors='coerce')
            if pd.notnull(ed):
                df_local = df_local[df_local['date'] <= ed]
        except Exception:
            pass

    # busca global (procura em todas as colunas visíveis)
    if search_value:
        sv = str(search_value)
        # cria máscara inicial False
        mask = pd.Series(False, index=df_local.index)
        for col in df_local.columns:
            # evita procurar em colunas não string convertendo pra str (rápido suficiente)
            mask |= df_local[col].astype(str).str.contains(sv, case=False, na=False)
        df_local = df_local[mask]

    # ordenação (se coluna válida)
    if order_col and order_col in df_local.columns:
        ascending = (order_dir == "asc")
        try:
            df_local = df_local.sort_values(by=order_col, ascending=ascending)
        except Exception:
            # fallback: tentar ordenar por string
            df_local = df_local.assign(_sort_key=df_local[order_col].astype(str))
            df_local = df_local.sort_values(by="_sort_key", ascending=ascending).drop(columns=["_sort_key"])

    return df_local


# --- Rotas do app (login + páginas) ---
@app.route('/')
def home():
    return render_template('login.html')


@app.route('/login', methods=['POST'])
def login():
    email = request.form.get('email')
    senha = request.form.get('senha')
    funcao = request.form.get('role')

    if email == "user1" and senha == "oeiruhn56146" and funcao == "admin":
        return redirect(url_for("home_admin"))
    elif email == "user2" and senha == "908ijofff" and funcao == "user":
        return redirect(url_for("home_user"))
    else:
        return "<h1>Não foi possível fazer o login. Usuário inválido.</h1>"


@app.route("/admin")
def home_admin():
    return render_template("homeAdmin.html")


@app.route("/user")
def home_user():
    return render_template("homeUser.html")


# --- API Admin (server-side DataTables) ---
@app.route("/api/admin_data")
def admin_data():
    # parâmetros do DataTables
    draw = int(request.args.get("draw", 0))
    start = int(request.args.get("start", 0))
    length = int(request.args.get("length", 10))

    # DataTables envia order como índice de coluna; pegamos o nome real
    order_idx = request.args.get("order[0][column]")
    order_col = None
    if order_idx is not None:
        order_col = request.args.get(f"columns[{order_idx}][data]")

    order_dir = request.args.get("order[0][dir]", "asc")
    search_value = request.args.get("search[value]", "")

    # filtros custom (data)
    start_date = request.args.get("start_date", None)
    end_date = request.args.get("end_date", None)

    # total antes do filtro
    records_total = len(df)

    # aplica filtros/search/ordering
    df_filtered = apply_filters(df, search_value=search_value,
                                start_date=start_date, end_date=end_date,
                                order_col=order_col, order_dir=order_dir)

    records_filtered = len(df_filtered)

    # paginação
    page = df_filtered.iloc[start:start+length].copy()

    # formata date para JSON (string ISO)
    if 'date' in page.columns:
        page['date'] = page['date'].apply(lambda x: x.isoformat() if pd.notnull(x) else "")

    data = page.to_dict(orient="records")

    return jsonify({
        "draw": draw,
        "recordsTotal": records_total,
        "recordsFiltered": records_filtered,
        "data": data
    })


# --- API User (sem cost_micros) ---
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

    start_date = request.args.get("start_date", None)
    end_date = request.args.get("end_date", None)

    # base para o usuário (sem cost_micros)
    df_user_base = df.drop(columns=["cost_micros"])

    records_total = len(df_user_base)

    df_filtered = apply_filters(df_user_base, search_value=search_value,
                                start_date=start_date, end_date=end_date,
                                order_col=order_col, order_dir=order_dir)

    records_filtered = len(df_filtered)

    page = df_filtered.iloc[start:start+length].copy()
    if 'date' in page.columns:
        page['date'] = page['date'].apply(lambda x: x.isoformat() if pd.notnull(x) else "")

    data = page.to_dict(orient="records")

    return jsonify({
        "draw": draw,
        "recordsTotal": records_total,
        "recordsFiltered": records_filtered,
        "data": data
    })


if __name__ == "__main__":
    app.run(debug=True)
