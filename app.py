from flask import Flask, render_template, request, redirect, url_for

# Fungsi enkripsi dan deskripsi Vigenère
def encrypt_vigenere(message, password):
    encrypted_message = []
    password = password.lower()  # Password selalu dalam huruf kecil
    password_length = len(password)

    for i, char in enumerate(message):
        if char.isalpha():  # Hanya mengenkripsi huruf
            shift = ord(password[i % password_length]) - ord('a')
            if char.islower():
                encrypted_message.append(chr((ord(char) - ord('a') + shift) % 26 + ord('a')))
            else:
                encrypted_message.append(chr((ord(char) - ord('A') + shift) % 26 + ord('A')))
        else:
            encrypted_message.append(char)  # Karakter non-alfabet tetap
    return ''.join(encrypted_message)

def decrypt_vigenere(encrypted_message, password):
    decrypted_message = []
    password = password.lower()  # Password selalu dalam huruf kecil
    password_length = len(password)

    for i, char in enumerate(encrypted_message):
        if char.isalpha():  # Hanya mendekripsi huruf
            shift = ord(password[i % password_length]) - ord('a')
            if char.islower():
                decrypted_message.append(chr((ord(char) - ord('a') - shift) % 26 + ord('a')))
            else:
                decrypted_message.append(chr((ord(char) - ord('A') - shift) % 26 + ord('A')))
        else:
            decrypted_message.append(char)  # Karakter non-alfabet tetap
    return ''.join(decrypted_message)

# Fungsi enkripsi dan deskripsi Math Formula
def encrypt_math_formula(message):
    encrypted_message = []
    for i, char in enumerate(message):
        if char.isalpha():
            numeric_value = ord(char)
            encrypted_value = (numeric_value * 2 + 5)  # Formula menghasilkan angka
            encrypted_message.append(str(encrypted_value))  # Simpan angka sebagai string
        else:
            encrypted_message.append(char)  # Karakter non-alfabet tetap
    return ' '.join(encrypted_message)  # Gabungkan angka dengan spasi

def decrypt_math_formula(encrypted_message):
    decrypted_message = []
    for part in encrypted_message.split():  # Pisahkan angka berdasarkan spasi
        if part.isdigit():
            encrypted_value = int(part)
            numeric_value = (encrypted_value - 5) // 2  # Formula invers dari enkripsi
            decrypted_message.append(chr(numeric_value))  # Ubah kembali ke karakter
        else:
            decrypted_message.append(part)  # Karakter non-angka tetap
    return ''.join(decrypted_message)

# Fungsi enkripsi dan deskripsi Morse Code
def encrypt_morse_code(message):
    morse_mapping = {
        'a': '.-', 'b': '-...', 'c': '-.-.', 'd': '-..', 'e': '.', 
        'f': '..-.', 'g': '--.', 'h': '....', 'i': '..', 'j': '.---', 
        'k': '-.-', 'l': '.-..', 'm': '--', 'n': '-.', 'o': '---', 
        'p': '.--.', 'q': '--.-', 'r': '.-.', 's': '...', 't': '-', 
        'u': '..-', 'v': '...-', 'w': '.--', 'x': '-..-', 'y': '-.--', 
        'z': '--..', '0': '-----', '1': '.----', '2': '..---', 
        '3': '...--', '4': '....-', '5': '.....', '6': '-....', 
        '7': '--...', '8': '---..', '9': '----.', ' ': '/'
    }
    encrypted_message = ' '.join(morse_mapping.get(char, '') for char in message.lower())
    return encrypted_message

def decrypt_morse_code(morse_code):
    reverse_morse_mapping = {
        '.-': 'a', '-...': 'b', '-.-.': 'c', '-..': 'd', '.': 'e',
        '..-.': 'f', '--.': 'g', '....': 'h', '..': 'i', '.---': 'j',
        '-.-': 'k', '.-..': 'l', '--': 'm', '-.': 'n', '---': 'o',
        '.--.': 'p', '--.-': 'q', '.-.': 'r', '...': 's', '-': 't',
        '..-': 'u', '...-': 'v', '.--': 'w', '-..-': 'x', '-.--': 'y',
        '--..': 'z', '-----': '0', '.----': '1', '..---': '2',
        '...--': '3', '....-': '4', '.....': '5', '-....': '6',
        '--...': '7', '---..': '8', '----.': '9', '/': ' '  # '/' adalah pemisah kata
    }
    words = morse_code.split(' ')  # Pisahkan berdasarkan spasi antar simbol
    decrypted_message = []

    for code in words:
        if code in reverse_morse_mapping:
            decrypted_message.append(reverse_morse_mapping[code])
        else:
            decrypted_message.append('?')  # Tanda untuk simbol Morse tidak dikenal

    return ''.join(decrypted_message)

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key_here'

messages = []

@app.route('/')
def index():
    return redirect(url_for('submit'))

@app.route('/home')
def home():
    return render_template('home.html', nav_links=get_nav_links())

@app.route('/guide')
def guide():
    return render_template('guide.html', nav_links=get_nav_links())

@app.route('/submit', methods=['GET', 'POST'])
def submit():
    if request.method == 'POST':
        recipient = request.form.get('recipient')
        message = request.form.get('message')
        password = request.form.get('password')
        hint = request.form.get('hint')
        encryption_type = request.form.get('encryption')

        if len(password) < 8 or len(set(password)) < 2:
            error = "Password must be at least 8 characters long with at least 2 unique characters."
            return render_template('submit.html', nav_links=get_nav_links(), error=error)

        # Proses enkripsi berdasarkan jenis yang dipilih
        if encryption_type == 'text':
            encrypted_message = encrypt_vigenere(message, password)
        elif encryption_type == 'math':
            encrypted_message = encrypt_math_formula(message)
        elif encryption_type == 'morse':
            encrypted_message = encrypt_morse_code(message)
        else:
            error = "Invalid encryption type selected."
            return render_template('submit.html', nav_links=get_nav_links(), error=error)

        messages.append({'recipient': recipient, 'message': encrypted_message, 'hint': hint, 'password': password})
        return redirect(url_for('history'))
    return render_template('submit.html', nav_links=get_nav_links())

@app.route('/history')
def history():
    return render_template('history.html', messages=messages, nav_links=get_nav_links())

@app.route('/message/<int:index>')
def message(index):
    if 0 <= index < len(messages):
        selected_message = messages[index]
        return render_template(
            'message.html',
            index=index,
            message=selected_message,
            nav_links=get_nav_links()
        )
    else:
        return "Message not found", 404

@app.route('/decrypt/<int:index>', methods=['POST'])
def decrypt(index):
    selected_message = messages[index]
    password = request.form.get('password')
    encryption_type = request.form.get('encryption_type')  # Pastikan nilai ini dikirim

    if not encryption_type:
        error = "Encryption type is missing. Please try again."
        return render_template(
            'message.html',
            index=index,
            message=selected_message,
            error=error,
            nav_links=get_nav_links()
        )

    # Check if password matches
    if password != selected_message['password']:
        error = "Incorrect password. Please try again."
        return render_template(
            'message.html',
            index=index,
            message=selected_message,
            error=error,
            nav_links=get_nav_links()
        )

    # Decrypt message based on encryption type
    encrypted_message = selected_message['message']
    decrypted_message = None

    try:
        if encryption_type == 'text':  # Vigenère Cipher
            decrypted_message = decrypt_vigenere(encrypted_message, password)
        
        elif encryption_type == 'morse':  # Morse Code
            # Validasi format Morse Code: hanya mengandung '.', '-', '/', dan spasi
            if not all(char in ".-/ " for char in encrypted_message):
                error = "Invalid Morse Code format. Ensure it only contains '.', '-', '/', and spaces."
                return render_template(
                    'message.html',
                    index=index,
                    message=selected_message,
                    error=error,
                    nav_links=get_nav_links()
                )
            decrypted_message = decrypt_morse_code(encrypted_message)

        elif encryption_type == 'math':  # Math Formula
            decrypted_message = decrypt_math_formula(encrypted_message)
        else:
            error = "Unknown encryption type. Unable to decrypt."
            return render_template(
                'message.html',
                index=index,
                message=selected_message,
                error=error,
                nav_links=get_nav_links()
            )
    except Exception as e:
        error = f"An error occurred during decryption: {str(e)}"
        return render_template(
            'message.html',
            index=index,
            message=selected_message,
            error=error,
            nav_links=get_nav_links()
        )

    return render_template(
        'message.html',
        index=index,
        message=selected_message,
        decrypted_message=decrypted_message,
        nav_links=get_nav_links()
    )

# Fungsi enkripsi dan deskripsi Vigenère
# Tetap menggunakan karakter unik pada password


def get_nav_links():
    return {
        'Home': url_for('home'),
        'Guide': url_for('guide'),
        'Submit': url_for('submit'),
        'History': url_for('history')
    }

if __name__ == '__main__':
    app.run(debug=True)
