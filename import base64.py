import base64
import re


def is_base64(sb):
    try:
        if isinstance(sb, str):
            # Verifica se é uma string válida Base64 (evitando erros comuns)
            sb_bytes = sb.encode("ascii")
        elif isinstance(sb, bytes):
            sb_bytes = sb
        else:
            return False
        return base64.b64encode(base64.b64decode(sb_bytes)) == sb_bytes
    except Exception:
        return False


# O QR code retornado na resposta
qr_code_data = "2@fugKiGoltk7ZiKEzAI1jubmsFw74K6rj3ay1szpdRwVVC7ZdjyKDzJL7b3eYSPBn1FoiwMUtmXEt4k2NFG2WQ7nCqwaH7Bh/ICs=,x+JGcRI9Q0gwUjRVD+cXHoq3yu6lqyj7+ila4EB8djI=,nGnbH41tPjX5twos4rcqKjhXom3+hoTAYUI/Ot6HBgg=,NL1xU/XLtE+PgPzcmKWfuU/9tpVZZFYz20Ov4Idj9ms=,1"

# Remova os caracteres não Base64, se existirem (como separadores de colunas)
qr_code_data = re.sub(r"[^A-Za-z0-9+/=]", "", qr_code_data)

# Verifica se o dado é Base64
if is_base64(qr_code_data):
    # Decodifica o valor
    qr_code_bytes = base64.b64decode(qr_code_data)

    # Salva como uma imagem
    with open("qr_code.png", "wb") as f:
        f.write(qr_code_bytes)

    print("QR code salvo como 'qr_code.png'.")
else:
    print("O dado não está em formato Base64.")
