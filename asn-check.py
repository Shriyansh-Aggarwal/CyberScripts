import argparse
import socket

parser = argparse.ArgumentParser(
    prog="asn-check",
    description="Checks a domain's registered ASN by querying whois.cymru.com over sockets",
    epilog="Example usage: python3 asn-check.py -d example.com"
)
parser.add_argument("-d", "--domain", required=True, help="The domain to lookup ASN for")
args = parser.parse_args()
domain = args.domain
ip = socket.gethostbyname(domain)

def query_cymru(ip):
    server = "whois.cymru.com"
    port = 43
    query = f"-v {ip}\n"
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((server, port))
            s.sendall(query.encode())
            response = b""
            while True:
                data = s.recv(4096)
                if not data:
                    break
                response += data
        print(response.decode())
    except:
        print("Couldn't retrieve information for provided host.")

if __name__ == "__main__":
    query_cymru(ip)