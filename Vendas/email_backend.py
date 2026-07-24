from django.core.mail.backends.console import EmailBackend as ConsoleEmailBackend


class PlainTextEmailBackend(ConsoleEmailBackend):
    """
    Backend de e-mail que exibe no terminal sem quoted-printable,
    evitando quebra de linhas em links longos como tokens de reset de senha.
    """

    def write_message(self, message):
        """
        Escreve a mensagem formatada manualmente no stream como string,
        sem usar quoted-printable, mantendo URLs intactas.
        """
        self.stream.write(f"Subject: {message.subject}\n")
        self.stream.write(f"From: {message.from_email}\n")
        self.stream.write(f"To: {', '.join(message.to)}\n")
        self.stream.write(f"Date: {message.message()['Date']}\n")
        self.stream.write("\n")

        # Pega o corpo como string pura sem encoding quoted-printable
        body = message.body
        self.stream.write(body)
        self.stream.write("\n")
        self.stream.write("-" * 79)
        self.stream.write("\n")