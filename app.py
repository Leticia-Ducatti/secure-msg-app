import streamlit as st
st.set_page_config(page_title="🔐 Crypto Message App", layout="centered")

from crypto_utils import (
    generate_aes_key, encrypt_aes, decrypt_aes,
    generate_rsa_keys, encrypt_rsa, decrypt_rsa
)

st.title("🔐 Crypto Message App")
st.write("Welcome to the Crypto Message App! Encrypt and decrypt your messages securely using AES (symmetric) or RSA (asymmetric) encryption methods.")

encryption_method = st.selectbox("Choose encryption method:", ["AES", "RSA"])

if encryption_method == "AES":
    st.subheader("🔐 AES Encryption")

    if 'aes_key' not in st.session_state:
        st.session_state.aes_key = generate_aes_key()

    with st.form("aes_form"):
        message = st.text_area("Enter your message:")
        encrypt_button = st.form_submit_button("Encrypt")

        if encrypt_button and message:
            encrypted_data = encrypt_aes(message, st.session_state.aes_key)
            st.session_state.encrypted_data = encrypted_data
            st.success("Message encrypted successfully!")
            st.code(encrypted_data['cipher_text'], language='text')

    if 'encrypted_data' in st.session_state:
        if st.button("Decrypt"):
            decrypted = decrypt_aes(st.session_state.encrypted_data, st.session_state.aes_key)
            st.success("Decrypted message:")
            st.code(decrypted, language='text')

elif encryption_method == "RSA":
    st.subheader("🔐 RSA Encryption")

    if 'private_key' not in st.session_state or 'public_key' not in st.session_state:
        private_key, public_key = generate_rsa_keys()
        st.session_state.private_key = private_key
        st.session_state.public_key = public_key

    with st.form("rsa_form"):
        message = st.text_area("Enter your message:")
        encrypt_button = st.form_submit_button("Encrypt")

        if encrypt_button and message:
            encrypted = encrypt_rsa(message, st.session_state.public_key)
            st.session_state.encrypted_rsa = encrypted
            st.success("Message encrypted successfully!")
            st.code(encrypted, language='text')

    if 'encrypted_rsa' in st.session_state:
        if st.button("Decrypt"):
            try:
                decrypted = decrypt_rsa(st.session_state.encrypted_rsa, st.session_state.private_key)
                st.success("Decrypted message:")
                st.code(decrypted, language='text')
            except ValueError:
                st.error("❌ Failed to decrypt. Please ensure keys match and encryption was correct.")
