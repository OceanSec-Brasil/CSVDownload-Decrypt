# decrypt.py

# Importando bibliotecas necessárias
import os
import requests
from Crypto.Cipher import AES
from Crypto.Hash import SHA256
from Crypto.Util.Padding import unpad
import pandas as pd

# COLOQUE A SENHA AQUI NO LUGAR DE ##################
KEY = SHA256.new(b"##################").digest()
IV = b"0123456789ABCDEF"  # IV (Vetor de inicialização) de tamanho de bloco AES
MODE = AES.MODE_CBC
CIPHER = AES.new(KEY, MODE, IV)

def download_file(url, dest_filename):
    """
    Função para baixar arquivos da web.

    Parâmetros:
    - url: Link do arquivo que deve ser baixado.
    - dest_filename: Nome do arquivo de destino onde o conteúdo será salvo.
    """
    try:
        r = requests.get(url, stream=True)
        r.raise_for_status()  # Se houver um erro (por exemplo: 404), isso gerará uma exceção.

        # Escrevendo o arquivo baixado em chunks para lidar com arquivos grandes
        with open(dest_filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)
                
    except requests.RequestException as e:
        print(f"Erro ao baixar o arquivo: {e}")
        return False

    return True

def decrypt_data(encrypted_data):
    """
    Função para descriptografar dados.

    Parâmetro:
    - encrypted_data: Dados encriptados como string hex.
    """
    try:
        decrypted = unpad(CIPHER.decrypt(bytes.fromhex(encrypted_data)), AES.block_size)
        return decrypted.decode('utf-8')
    except (ValueError, UnicodeDecodeError):
        # Captura possíveis erros durante descriptografia ou conversão de bytes para string
        print("Erro ao descriptografar. A chave fornecida pode estar errada.")
        return None

def decrypt_csv(input_filename, output_filename):
    """
    Função para descriptografar um arquivo CSV.

    Parâmetros:
    - input_filename: Nome do arquivo CSV encriptado.
    - output_filename: Nome do arquivo CSV onde os dados descriptografados serão salvos.
    """
    try:
        df = pd.read_csv(input_filename, delimiter=';')
        for column in df.columns:
            df[column] = df[column].apply(lambda x: decrypt_data(str(x)))

            # Verifica se houve algum erro durante a descriptografia
            if df[column].isnull().any():
                print("Falha ao descriptografar o CSV.")
                return

        df.to_csv(output_filename, sep=';', index=False)
        print("Descriptografia concluída com sucesso!")
        
    except pd.errors.EmptyDataError:
        print("Erro: Arquivo CSV está vazio ou não foi possível lê-lo.")

# COLOQUE A URL COM O ARQUIVO ENCRIPTADO NO LUGAR DE ##################
if download_file('##################', 'downloaded_encrypted.csv'):
    decrypt_csv('downloaded_encrypted.csv', 'decrypted.csv')

    # Apaga o arquivo encriptado após descriptografia
    try:
        os.remove('downloaded_encrypted.csv')
        print("Arquivo encriptado apagado com sucesso!")
    except OSError:
        print("Erro ao tentar apagar o arquivo encriptado.")
