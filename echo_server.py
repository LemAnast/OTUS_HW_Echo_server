import socket
from urllib.parse import urlparse, parse_qs
from http import HTTPStatus


def create_server(host='127.0.0.1', port=5000):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((host, port))
        s.listen()
        print(f"Сервер запущен на http://{host}:{port}/")

        while True:
            conn, addr = s.accept()
            with conn:
                request = conn.recv(1024).decode("utf-8")
                print(f"Полученный запрос:\n{request}\n")

                if not request:
                    continue

                request_lines = request.splitlines()
                request_line = request_lines[0].split()
                method = request_line[0]
                path = request_line[1]

                parsed_url = urlparse(path)
                query_params = parse_qs(parsed_url.query)
                status_code = query_params.get('status', ['200'])[0]

                if not status_code.isdigit() or int(status_code) not in [s.value for s in HTTPStatus]:
                    status_code = '200'

                status_message = HTTPStatus(int(status_code)).phrase

                headers = "\r\n".join(
                    f"{line.split(':')[0]}: {line.split(':')[1].strip()}"
                    for line in request_lines[1:] if ':' in line
                )

                response_text = (
                    f"Request Method: {method}\r\n"
                    f"Request Source: {addr}\r\n"
                    f"Response Status: {status_code} {status_message}\r\n"
                    f"{headers}\r\n\r\n"
                )

                response = (f"HTTP/1.1 {status_code} {status_message}\r\n"
                            f"\r\n"
                            f"{response_text}")

                print("Отправляемый ответ:\n")
                print(response)
                print("**************************************")

                conn.sendall(response.encode("utf-8"))


if __name__ == "__main__":
    create_server()
