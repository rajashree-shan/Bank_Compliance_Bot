def mpc_secure_query(query, context_docs):
    return f"[MPC-Secure] Query: {query}\nTop Context:\n{context_docs[0][:300]}"
