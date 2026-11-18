def gerar_mensagem_whatsapp(itens_criticos):
    if not itens_criticos:
        return "Estoque regularizado! Nenhum item em falta no momento."
    linhas = ["*Lista de Necessidades Urgentes - EloSolidario:*"]
    for item in itens_criticos:
        linhas.append(f"- {item.nome_item} (Saldo atual: {item.quantidade_atual})")
    return "\n".join(linhas)
