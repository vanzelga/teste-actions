# auto_acompanhamento.py
# Justifica automaticamente (Acompanhamento) SEM e-mail para a whitelist enviada.

import os
import requests
from datetime import datetime
import pandas as pd
import openpyxl

# ======= PREENCHER AQUI =======
COOKIE   = "INGRESSCOOKIE=94f1f16c869794d4051756aaea145e45|9641fa8c7ed9fdd96cdde0cc91a2453f; _ga=GA1.1.868357845.1752840641; _clck=ife97g%7C2%7Cfxp%7C0%7C2025; _ga_L7E6E0NQD3=GS2.1.s1752844597$o2$g0$t1752844597$j60$l0$h0; _ga_R2B565MMDW=GS2.1.s1752844597$o27$g0$t1752844597$j60$l0$h0; _clsk=g73aev%7C1752844609517%7C2%7C1%7Cl.clarity.ms%2Fcollect; smtUserSession=5B%2FFbTETCmCbbq9GVN308Ubl2BSe7rJ%2BCcgkPSdEcYWmhzo94knVwi5sUZW0oBeyl52Lxf%2BZzpil%2BBLZd5aODQqT9GKYxX8BrZ00yQ%2BB015uLM6TZ6E51WgfcFGD0PLYIdMyJAXxLjrskKr9FPGf2%2BtegU2x9BfaZAnJ239kgClhqS175Luy2Po037dtTrwIKYyf38EoISfkX%2F05JFxlJoNvdiuvj5RCwNv2IgaNOX7wlU6aJNQScvCMpt0HMdVSLx2yphBBZTf7p1sD2DtR7HzVyJTL81qn1dtyKE6Qu3GJ6qrmjFS%2BAeuyaMDX3YIg%2FiVwBP81GpAW1FnPkuFzUNP1h6n7%2Fr88DIFjmYbjdghBJuKjNPXte%2Frux1OczB6QlooKuNjU7OO%2B%2F3VV2kSgHyTxzschdIbCqMUDvIfU0kLIdPSN0wTQfS7crGNPZIp6A4zY6mNBQluQrZk99dIP9PInXc%2FvJk1DnwgSadLdgVq35h1yGQjsv3GZLFUyxDGJnvQE0GD%2BV1okVTV793Xj6DMrMJZL7aPZacGbPtlxOWTwiOwRS4Abcza4dOAnywjBRa5xrUkJerEM5NE%2F67JAxl3rl5ZWCx%2F6IhOkaHKG9DairIDNshIWwTUxJwq9Bj0KyxmKwqbfQWTGNuZIUeRyNussGTbfxncqLvSXoj1CFt8JsZhlkMt1UeDSmy6jCKpBuKXPfYbi5SUF4Ffdoco%2B2%2FeaQU5MSQRvBmt57MWifC%2FsozaJDCHdY%2FAghDeofbwbZPrMSHJSwJq9A1YGHqvpsjxtBVqKKIczJhFudpjhQ9qP0VfLSfsH7%2FT3eWWSib%2BZ5NSuAYJSylWJGPqdFTM3U1Y5yCoGveq4%2FzcC1sehzEjIdPSN0wTQfS7crGNPZIp6EFc0paPken66YyuyuzMvYrFsbd89xEeT%2FBJsZZkY1uz2Tr1p3QqWDw2i6BYHM8hjgYIC4FdmbosVtwzRCgaScamQA5%2BaAyi2fyu2QRDDaiixLXykt%2FAWpaAi9u%2Bq%2Ff6YhW5AcrluueIhjNc%2BZrDrKriFLa78BydTYrSOyB4S%2B48UIJbQ2iQXULFifOkEMYwI0%2FPzHIOKaZcMNLOqFWN15ZaKCrjY1Ozjvv91VdpEoB9bZX0ywreNP0pIzj5lbQVfZWoVEro0etX%2Bf7d3Yo1%2F%2BDx2gqfyD4nljUEsjxS3qxhDOkhpvhX3dVrMTgMKAdZQErRmKvMD1GNjHyL64f2ojiBuQGLJRAwZkn7U%2FBg6qZ63DLDqQJK2s6k%2FZ9UxlLXdh6%2F1NHGSPxkhwZEt2syJ0Z13zXS0X9L2ty4QNcxJzwRQCHZ9l5MRukOSnJ86j%2BvejKp6qdSzfPdNOAAhFt61L2tW8sKAU1gqgeUQgBUUyvStYrHNIAq2E%2B%2BiPHpGKkeB0sZ7wZVHNjQBmezWX4O4Yg%3D%3D; _dd_s=rum=2&id=e33c2ff6-5a26-47d8-83e2-1bd7b17c418c&created=1752843884724&expire=1752846056267; _ga_TNFNTP8NSE=GS2.1.s1752843884$o124$g1$t1752845156$j12$l0$h1678161541"
XCRYPTO  = "5B/FbTETCmCbbq9GVN308ZkusgOQDsZdLXMAiaxRVczd2+wwHfIeHiOU8vnf7HAk7OdeSF7Xbz5MosDZZjN07dDUEYT9RTGX8Dp6PJbq/jYl15eUTi9nE1b9W+J10mheEFxYHQrF+r81qbYSC/FWCbw9ZUKe7597+5yda8haY/xuY0HGHqor8jAj+xTzmWv06wAgzg/BbVS8hsM33LR3DJ2Rpmjbp/z23wn9NU8wAaMqFYpF0smHl3C/gf6bbljV/buR52ZfDX25clF+8mqLqlK0IJCLlUEQH9mTVaIGuNipttxlzZgQThUx82Q/yGcgowwTOj+onrDGDJ9fZYAskeVP8ERm2ZZubcu3S+DVM34RgNywjpbf5sj8AAoSijHswZJ0AGebhnpG9BFLXTiKpq4/H15V4i/mhvfZSTJIGZ+qmavKzi6U387qb3mo/Dqj4kPaVWPTm8AEtHHsX6busaMarsShh/5WiPlzZw1gJstsNYKdZBh5+A/D+MtiW6HFj9FXy0n7B+/093llkom/mdhjByHD0fjZPzJUUhe07h0x9ShhKRU7f0x5ujTngCAjKtE/p9Lk/Jxzrq5KQ+xrc2zARf8TWRL1hVsbXGR2bzGzHi2H9GSIP51nPre3/adSFCCW0NokF1CxYnzpBDGMCJKo02LMBksMqBVZGr9cD3XILPMqT0UhEP/MLSDApq4B7cdLJqcRnBQCUg8PRN2twvT4w7z81aTuoopdWQsZRu5IlN0ico8OXSGxF2hy0e6VWkxqsSGocSq8QmRZJv0hvVKuOBUrIkix3bmrhZEO03cHWLa7pOOaTG+Xolbs7dVR+ao6aRSCeY3Q/pbZG2GkD2tERlcjBX5KjXvV8EGuj6xiWxeRyipLthwUKWjKuw+DKPpSbns+z1O+00CBiEyZyGpFRiotbtx3G0EljOCZO11FGkC1+NuYuA/XReMFJKmh"
USUARIO  = "gabriel.vanzela@btgpactual.com"
# ==============================

BASE = "http://fundsplatform/enq-monitor/api/Historico/justificativa"

HEADERS = {
    "Content-Type": "application/json",
    "accept": "*/*",
    "Cookie": COOKIE,
    "x-crypto-token": XCRYPTO,
    "User-Agent": "Python/requests"
}

cges = None
data_fim = "2025-11-14"
data_inicio = "2025-11-01"
tipo_fundo = 2  # 2 PARA FUNDOS LÍQUIDOS
tipo_posicao = "E"
USUARIO = None

def post_json(url, body):
    r = requests.post(url, headers=HEADERS, json=body, timeout=30)
    r.raise_for_status()
    return r.json() if r.text.strip() else {}


# Obtém a lista de fundos executados no monitor
def get_historico():
    body = {
        "cges": None,
        "tipoFundo": 2, # 2 PARA FUNDOS LÍQUIDOS
        "dtJustificativaFim": data_fim,
        "dtJustificativaInicio": data_inicio,
        "tipoFundo": tipo_fundo,
        "tipoPosicao": tipo_posicao,
        "usuario": USUARIO
    }
    return post_json(BASE, body)

historico = get_historico()

df = pd.DataFrame(historico)

len(df)

df.dtypes

import pandas as pd

# --- Datas ---
for c in ['dataPosicao','dhJustificativa','dataPrazoPlano']:
    df[c] = pd.to_datetime(df[c], errors='coerce')

# --- Números inteiros ---
int_cols = [
    'id','identificador','idRegra','idTipoJustificativa',
    'idTipoDesenquadramento','diasDesenquadramento','nrClasseCvm',
    'grupoGestor','opcaoResultado','cgePortfolio','tipoPortfolioScp'
]
for c in int_cols:
    df[c] = pd.to_numeric(df[c], errors='coerce').astype('Int64')

# --- Decimais ---
dec_cols = ['resultado','limite','min','max']
for c in dec_cols:
    df[c] = pd.to_numeric(df[c], errors='coerce')

# --- Booleanos ---
df['explodida'] = df['explodida'].astype(bool)
df['onShore']   = df['onShore'].astype(bool)

# --- Strings ---
str_cols = [
    'guidMensagem','nmFundo','nmRegra','tpPosicao','dsTipoJustificativa',
    'dsJustificativa','usuarioJustificativa','dsTipoDesenquadramento',
    'planoAcao','operacao','ativos'
]
for c in str_cols:
    df[c] = df[c].astype(str)


df.columns


df_filtered = df[['cgePortfolio', 'nmFundo', 'dataPosicao', 
                  'idRegra', 'nmRegra', 'explodida', 'tpPosicao', 
                  'dsTipoJustificativa', 'dsJustificativa', 'dhJustificativa', 
                  'usuarioJustificativa', 'dsTipoDesenquadramento', 'diasDesenquadramento']
                ]


# Dropar linhas duplicadas
len(df_filtered)
df_filtered = df_filtered.drop_duplicates()
len(df_filtered)

# Salva o DataFrame em CSV
caminho = "historico_justificativa_teste.xlsx"

# with pd.ExcelWriter(caminho, engine='openpyxl', mode='a' if os.path.exists(caminho) else 'w') as writer:
#     df_filtered.to_excel(writer, sheet_name='historico', index=False)

# Se já existir → carrega histórico completo
if os.path.exists(caminho):
    df_old = pd.read_excel(caminho, sheet_name='historico', dtype=str)
    df_append = pd.concat([df_old, df_filtered], ignore_index=True)

    # Remove duplicados novamente
    df_append = df_append.drop_duplicates()

else:
    df_append = df_filtered.copy()

# Salva tudo novamente (recria o arquivo limpo)
df_append.to_excel(caminho, sheet_name='historico', index=False)




