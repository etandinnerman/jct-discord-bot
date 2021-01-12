def parse(msg : str):
    # dictionary has: title, desc, author, options{emoji: meaning} 
    tokens = msg.split("|")
    tokens = [token.strip() for token in tokens]
    return tokens
