def render_login_page(self, message=""):
    self.send_response(200)
    self.send_header("Content-type", "text/html")
    self.end_headers()
    self.wfile.write(f"""
    <html>
        <body>
            <h2>Login</h2>
            <p>{message}</p>
            <form method="post" action="/login">
                <input type="text" name="username" placeholder="Username">
                <input type="password" name="password" placeholder="Password">
                <input type="submit" value="Login">
            </form>
        </body>
    </html>
    """.encode("utf-8"))
